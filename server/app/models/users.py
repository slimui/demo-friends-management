from .core import db, Model, metadata, relationship
from ..errors import UserBlockedException
from sqlalchemy import (
    Column, Integer, String, Table, ForeignKey, and_
)
from sqlalchemy.dialects.postgresql import insert


CONNECTION_NONE = 0
"""Denotes no connections."""

CONNECTION_FRIEND = 1 << 0
"""Denotes source has befriended target."""

CONNECTION_FOLLOW = 1 << 1
"""Denotes source is following target."""

CONNECTION_BLOCK = 1 << 2
"""Denotes source has blocked target."""

CONNECTION_SUBSCRIBED = CONNECTION_FRIEND | CONNECTION_FOLLOW
"""Denotes source has subscribed to target's updates."""


connections = Table(
    'connections', metadata,
    Column(
        'source_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'target_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'connection', Integer, index=True, default=CONNECTION_NONE),
)


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
            connections.c.connection.op('&')(CONNECTION_FRIEND) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    following = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.source_id,
            connections.c.connection.op('&')(CONNECTION_FOLLOW) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    followers = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.target_id,
            connections.c.connection.op('&')(CONNECTION_FOLLOW) > 0
        ),
        secondaryjoin=user_id == connections.c.source_id,
    )

    blocked = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.source_id,
            connections.c.connection.op('&')(CONNECTION_BLOCK) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    subscribing = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.source_id,
            connections.c.connection.op('&')(CONNECTION_BLOCK) == 0,
            connections.c.connection.op('&')(CONNECTION_SUBSCRIBED) > 0
        ),
        secondaryjoin=user_id == connections.c.target_id,
    )

    subscribers = relationship(
        'User', secondary=connections,
        cascade='all', lazy='dynamic', viewonly=True,
        primaryjoin=and_(
            user_id == connections.c.target_id,
            connections.c.connection.op('&')(CONNECTION_BLOCK) == 0,
            connections.c.connection.op('&')(CONNECTION_SUBSCRIBED) > 0
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
            if user_or_id.is_blocking(self):
                raise UserBlockedException()
            self._add_connection_with(user_or_id, CONNECTION_FRIEND)
        return self

    def unfriend(self, user_or_id):
        """Unfriends `user_or_id`, returns `self`"""
        if self.is_friend_of(user_or_id):
            self._remove_connection_with(user_or_id, CONNECTION_FRIEND)
        return self

    def is_friend_of(self, user_or_id):
        """Returns True if `self` has befriended `user_or_id`."""
        return self._has_connection_with(user_or_id, CONNECTION_FRIEND)

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
            if user_or_id.is_blocking(self):
                raise UserBlockedException()
            self._add_connection_with(user_or_id, CONNECTION_FOLLOW)
        return self

    def unfollow(self, user_or_id):
        """Unfollow `user_or_id`, returns `self`"""
        if self.is_following(user_or_id):
            self._remove_connection_with(user_or_id, CONNECTION_FOLLOW)
        return self

    def is_following(self, user_or_id):
        """Returns True if `self` has followed `user_or_id`."""
        return self._has_connection_with(user_or_id, CONNECTION_FOLLOW)

    def block(self, user_or_id):
        """Blocks `user_or_id`, returns `self`.

        Note that blocking is bidirectional, i.e.
        when self (blocker) -- blocks --> user_or_id
        does not equate to user_or_id -- blocks --> self.

        To create bidirectional blocking, you must establish connections
        at both sides, example

        ```
        user1.block(user2.block(user1))
        ```
        """
        if not self.is_blocking(user_or_id):
            self._add_connection_with(user_or_id, CONNECTION_BLOCK)
        return self

    def unblock(self, user_or_id):
        """Unblocks `user_or_id`, returns `self`"""
        if self.is_blocking(user_or_id):
            self._remove_connection_with(user_or_id, CONNECTION_BLOCK)
        return self

    def is_blocking(self, user_or_id):
        """Returns True if `self` has blocked `user_or_id`."""
        return self._has_connection_with(user_or_id, CONNECTION_BLOCK)

    # Note: @mention is ambigious in the question.
    # When does @mention establish connection:
    #  - a @mention b?
    #  - b @mention a?
    #  - both?
    # Leaving this feature out until clarification
    # def mention(self, user_or_id):
    #     """Mentioned `user_or_id`, returns `self`"""
    #     if not self.has_mentioned(user_or_id):
    #         self._add_connection_with(user_or_id, CONNECTION_MENTION)
    #     return self
    #
    # def unmention(self, user_or_id):
    #     """Unmention `user_or_id`, returns `self`"""
    #     if self.has_mentioned(user_or_id):
    #         self._remove_connection_with(user_or_id, CONNECTION_MENTION)
    #     return self
    #
    # def has_mentioned(self, user_or_id):
    #     """Returns True if `self` has mentioned `user_or_id`."""
    #     return self._has_connection_with(user_or_id, CONNECTION_MENTION)

    def is_subscribing(self, user_or_id):
        """Returns True if `self` is subscribing to `user_or_id`.

        Subscription is establised when:
        - self has not blocked user_or_id
        - at least one of the following:
          - self is a friend of user_or_id
          - self is a follower of user_or_id
        """
        connection = self._connection_with(user_or_id)
        if connection & ~CONNECTION_BLOCK:
            return connection & CONNECTION_SUBSCRIBED and True or False
        return False

    def _connection_with(self, user_or_id):
        """Returns an bitwise flag containing connection information
        with `other`. See `ConnectionTypes`.
        """
        user_id = get_user_id(user_or_id, strict=True)
        if self.__connections is None:
            self.__connections = {}
        if user_id not in self.__connections:
            q = db.session.query(connections.c.connection).\
                filter(connections.c.source_id == self.user_id).\
                filter(connections.c.target_id == user_id)
            self.__connections[user_id] = \
                q.scalar() or CONNECTION_NONE
        return self.__connections.get(user_id, CONNECTION_NONE)

    def _add_connection_with(self, user_or_id, connection):
        current = self._connection_with(user_or_id)
        return self._update_connection_with(user_or_id, current | connection)

    def _remove_connection_with(self, user_or_id, connection):
        current = self._connection_with(user_or_id)
        return self._update_connection_with(user_or_id, current & ~connection)

    def _has_connection_with(self, user_or_id, connection):
        return self._connection_with(user_or_id) & connection == connection

    def _update_connection_with(self, user_or_id, connection):
        user_id = get_user_id(user_or_id, strict=True)
        upsert = insert(connections).values(
            source_id=self.user_id,
            target_id=user_id,
            connection=connection
        ).on_conflict_do_update(
            index_elements=('source_id', 'target_id'),
            set_=dict(connection=connection)
        )
        db.session.execute(upsert)
        self.__connections[user_id] = connection
