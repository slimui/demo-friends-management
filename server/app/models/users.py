from .core import db, Model, metadata, relationship
from ..errors import UserBlockedException
from ..logging import logger
from flask import request, g
from sqlalchemy import (
    Column, Integer, String, Table, ForeignKey, and_, select, func
)
from sqlalchemy.dialects.postgresql import insert
from enum import Enum


class ConnectionType(Enum):
    NONE = 0
    """Denotes no connections."""

    FRIEND = 1 << 0
    """Denotes source has befriended target."""

    FOLLOW = 1 << 1
    """Denotes source is following target."""

    BLOCK = 1 << 2
    """Denotes source has blocked target."""

    SUBSCRIBED = FRIEND | FOLLOW
    """Denotes source has subscribed to target's updates."""

    @classmethod
    def is_none(cls, value):
        return value == cls.NONE.value

    @classmethod
    def is_friend(cls, value):
        return cls.has_connection(value, cls.FRIEND)

    @classmethod
    def is_follow(cls, value):
        return cls.has_connection(value, cls.FOLLOW)

    @classmethod
    def is_block(cls, value):
        return cls.has_connection(value, cls.BLOCK)

    @classmethod
    def is_subscribed(cls, value):
        if not cls.is_block(value):
            return cls.has_connection(value, cls.SUBSCRIBED)
        return False

    @classmethod
    def has_connection(cls, value, flag):
        return value & flag.value > 0


connections = Table(
    'connections', metadata,
    Column(
        'source_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'target_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'connection', Integer, index=True,
        default=lambda: ConnectionType.ConnectionType.NONE.value.value),
)


def common_friends_between(source, targets):
    """Returns an array of `(target_id, [common_friend_id, ..])` tuple where
    - A single `source` (User or user_id)
    - An array of `targets` (User or user_id)

    This is an highly optimised fetch for a fairly common operation to display
    a list of users who have common friends with `me`.

    Example:
    ```
    results = common_friends_between(1, [2,3,4])
    [
      (2, [4, 3]),
      (3, []),
      (4, [5])
    ]
    ```
    """
    source_id = get_user_id(source, strict=True)
    target_ids = [get_user_id(target_id) for target_id in targets]
    if not target_ids:
        return []
    # We use a WITH query (CTE Common Table Expression) to identify source's
    # friends and use it against targets friends. This way we avoid making
    # multiple round trips to the database. The query expression looks like:
    # ----------------------------------------------------------------------
    # -- Define `friends` subquery, returns source's friends user_id
    # WITH friends AS (
    #   SELECT target_id FROM connections
    #     WHERE source_id = [source]
    #     AND connection & 1 > 0
    # )
    # -- We let postgresql do the heavy lifting by grouping the results
    # -- by target_id and getting the source_ids an array.
    # SELECT source_id, array_agg(target_id)
    # FROM connections
    # WHERE
    #   -- source_id are the befrienders, i.e. `targets`
    #   source_id IN ([targets]) AND
    #   -- target_id are the common friends we target
    #   target_id IN (SELECT target_id FROM friends) AND
    #   connection & 1 > 0
    # GROUP BY source_id
    # ----------------------------------------------------------------------
    c = connections.c
    friends = select([c.target_id]).\
        where(
            and_(
                c.source_id == source_id,
                c.connection.op('&')(ConnectionType.FRIEND.value) > 0
            )
        ).\
        cte('friends')
    stmt = select([
            c.source_id,
            func.array_agg(c.target_id)
        ]).\
        where(
            and_(
                c.source_id.in_(target_ids),
                c.target_id.in_(select([friends.c.target_id])),
                c.connection.op('&')(ConnectionType.FRIEND.value) > 0
            )
        ).\
        group_by(c.source_id)
    # {target_id: [common_friend_id, ..]}
    common = dict(db.session.execute(stmt).fetchall())
    return [
        (target_id, common.get(target_id, []))
        for target_id in target_ids
    ]


def get_user(user_or_id, strict=False):
    """Ensures an User instance, where `user_or_id` can be either:
    - a valid user_id
    - a valid user

    When `strict` is True, raises an error when no valid user is found."""
    if isinstance(user_or_id, User):
        user = user_or_id
    elif isinstance(user_or_id, int):
        user = User.query.get(user_or_id)
    else:
        user = None
    if strict:
        assert user, 'Expects valid `User` but got {}'.format(user_or_id)
    return user


def get_user_id(user_or_id, strict=False):
    """Ensures a valid `user_id`, where `user_or_id` can be either:
    - a valid user_id
    - a valid user

    When `strict` is True, raises an error when no valid user_id is found."""
    if isinstance(user_or_id, int):
        user_id = user_or_id
    elif isinstance(user_or_id, User):
        user_id = user_or_id.user_id
    else:
        user_id = 0
    if strict:
        assert user_id, 'Expects valid `user_id` but got {}'.format(user_or_id)
    return user_id


HEADER_CURRENT_USER_ID_KEY = 'x-app-current-user-id'


def current_user_id():
    """Returns the current user_id that is 'logged in'.
    Typically this information is saved in the session cookie upon successful
    user authentication. For the demo we allow users to 'switch' identity
    by providing a 'x-app-current-user-id' HTTP header information.

    When this information is not available, e.g. during testing, the default
    user_id = 1 is used.

    This method must be used within a flask request context."""
    if not hasattr(g, 'current_user_id'):
        try:
            id = int(request.headers.get(HEADER_CURRENT_USER_ID_KEY))
        except:
            id = 1
        if not id:
            id = 1
        setattr(g, 'current_user_id', id)
    return g.current_user_id


def current_user():
    """Returns the `User` instance of the `current_user_id` identity.

    This method must be used within a flask request context."""
    if not hasattr(g, 'current_user'):
        try:
            user = User.query.get(current_user_id())
        except Exception as e:
            logger.exception(e)
            user = None
        setattr(g, 'current_user', user)
    return g.current_user


class User(Model):
    """Represents a user entity."""

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)

    email = Column(String, nullable=False, unique=True)

    first_name = Column(String, nullable=True)

    last_name = Column(String, nullable=True)

    gender = Column(String, nullable=True)

    education = Column(String, nullable=True)

    address = Column(String, nullable=True)

    job = Column(String, nullable=True)

    introduction = Column(String, nullable=True)

    avatar_url = Column(String, nullable=True)

    friends = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.source_id,
            connections.c.connection.op('&')(ConnectionType.FRIEND.value) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    following = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.source_id,
            connections.c.connection.op('&')(ConnectionType.FOLLOW.value) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    followers = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.target_id,
            connections.c.connection.op('&')(ConnectionType.FOLLOW.value) > 0
        ),
        secondaryjoin=user_id == connections.c.source_id,
    )

    blocked = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.source_id,
            connections.c.connection.op('&')(ConnectionType.BLOCK.value) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    subscribing = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.source_id,
            connections.c.connection.op('&')(ConnectionType.BLOCK.value) == 0,
            connections.c.connection.op('&')
                (ConnectionType.SUBSCRIBED.value) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    subscribers = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.target_id,
            connections.c.connection.op('&')(ConnectionType.BLOCK.value) == 0,
            connections.c.connection.op('&')
                (ConnectionType.SUBSCRIBED.value) > 0
        ),
        secondaryjoin=user_id == connections.c.source_id,
    )

    __connections = None

    def __repr__(self):
        return '<User({})>'.format(self.user_id)

    def befriend(self, user_or_id):
        """Befriends `user_or_id`, returns `self`.

        Note that friendships are bidirectional, i.e.
        when self (befriender) -- befriends --> user_or_id
        does not equate to user_or_id -- befriends --> self.

        To create bidirectional friendships, you must establish connections
        at both sides, example

        ```
        user1.befriend(user2.befriend(user1))
        ```
        """
        if not self.is_friend_of(user_or_id):
            user = get_user(user_or_id, strict=True)
            if user.is_blocking(self):
                raise UserBlockedException()
            self._add_connection_with(user_or_id, ConnectionType.FRIEND)
        return self

    def unfriend(self, user_or_id):
        """Unfriends `user_or_id`, returns `self`"""
        if self.is_friend_of(user_or_id):
            self._remove_connection_with(
                user_or_id, ConnectionType.FRIEND)
        return self

    def is_friend_of(self, user_or_id):
        """Returns True if `self` has befriended `user_or_id`."""
        return self._has_connection_with(user_or_id, ConnectionType.FRIEND)

    def follow(self, user_or_id):
        """Follow `user_or_id`, returns `self`.

        Note that following is bidirectional, i.e.
        when self (follower) -- follows --> user_or_id
        does not equate to user_or_id -- follows --> self.

        To create bidirectional following, you must establish connections
        at both sides, example

        ```
        user1.follow(user2.follow(user1))
        ```
        """
        if not self.is_following(user_or_id):
            user = get_user(user_or_id, strict=True)
            if user.is_blocking(self):
                raise UserBlockedException()
            self._add_connection_with(user_or_id, ConnectionType.FOLLOW)
        return self

    def unfollow(self, user_or_id):
        """Unfollow `user_or_id`, returns `self`"""
        if self.is_following(user_or_id):
            self._remove_connection_with(
                user_or_id, ConnectionType.FOLLOW)
        return self

    def is_following(self, user_or_id):
        """Returns True if `self` has followed `user_or_id`."""
        return self._has_connection_with(user_or_id, ConnectionType.FOLLOW)

    def block(self, user_or_id):
        """Blocks `user_or_id`, returns `self`.

        Note that blocking is bidirectional, i.e.
        when self (blocker) -- blocks --> user_or_id
        does not equate to user_or_id -- blocks --> self.

        """
        if not self.is_blocking(user_or_id):
            self._add_connection_with(user_or_id, ConnectionType.BLOCK)
        return self

    def unblock(self, user_or_id):
        """Unblocks `user_or_id`, returns `self`"""
        if self.is_blocking(user_or_id):
            self._remove_connection_with(
                user_or_id, ConnectionType.BLOCK)
        return self

    def is_blocking(self, user_or_id):
        """Returns True if `self` has blocked `user_or_id`."""
        return self._has_connection_with(user_or_id, ConnectionType.BLOCK)

    # Note: @mention is ambigious in the question.
    # When does @mention establish connection:
    #  - a @mention b?
    #  - b @mention a?
    #  - both?
    # Leaving this feature out until clarification
    # def mention(self, user_or_id):
    #     """Mentioned `user_or_id`, returns `self`"""
    #     if not self.has_mentioned(user_or_id):
    #         self._add_connection_with(
    #           user_or_id, ConnectionType.MENTION)
    #     return self
    #
    # def unmention(self, user_or_id):
    #     """Unmention `user_or_id`, returns `self`"""
    #     if self.has_mentioned(user_or_id):
    #         self._remove_connection_with(
    #           user_or_id, ConnectionType.MENTION)
    #     return self
    #
    # def has_mentioned(self, user_or_id):
    #     """Returns True if `self` has mentioned `user_or_id`."""
    #     return self._has_connection_with(user_or_id, ConnectionType.MENTION)

    def is_subscribing(self, user_or_id):
        """Returns True if `self` is subscribing to `user_or_id`.

        Subscription is establised when:
        - self has not blocked user_or_id
        - at least one of the following:
          - self is a friend of user_or_id
          - self is a follower of user_or_id
        """
        connection = self._connection_with(user_or_id)
        return ConnectionType.is_subscribed(connection)

    def _connection_with(self, user_or_id):
        """Returns an bitwise flag containing connection information
        with `other`. See `ConnectionTypes`.
        """
        user_id = get_user_id(user_or_id, strict=True)
        if user_id == self.user_id:
            return ConnectionType.NONE.value
        if self.__connections is None:
            self.__connections = {}
        if user_id not in self.__connections:
            q = db.session.query(connections.c.connection).\
                filter(connections.c.source_id == self.user_id).\
                filter(connections.c.target_id == user_id)
            self.__connections[user_id] = \
                q.scalar() or ConnectionType.NONE.value
        return self.__connections.get(user_id, ConnectionType.NONE.value)

    def _add_connection_with(self, user_or_id, connection_type):
        current = self._connection_with(user_or_id)
        return self._update_connection_with(
            user_or_id, current | connection_type.value)

    def _remove_connection_with(self, user_or_id, connection_type):
        current = self._connection_with(user_or_id)
        return self._update_connection_with(
            user_or_id, current & ~connection_type.value)

    def _has_connection_with(self, user_or_id, connection_type):
        return ConnectionType.has_connection(
            self._connection_with(user_or_id), connection_type)

    def _update_connection_with(self, user_or_id, value):
        user_id = get_user_id(user_or_id, strict=True)
        assert user_id != self.user_id, \
            'Cannot set connection with oneself'
        upsert = insert(connections).values(
            source_id=self.user_id,
            target_id=user_id,
            connection=value
        ).on_conflict_do_update(
            index_elements=('source_id', 'target_id'),
            set_=dict(connection=value)
        )
        db.session.execute(upsert)
        self.__connections[user_id] = value
