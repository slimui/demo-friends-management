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

    def to_dict(self):
        return {
            'user_id': self.user_id,
        }

    def befriend(self, other_user):
        """Befriends `other_user`, returns `self`.

        Note that friendships are bidirectional, i.e.
        when self (befriender) -- befriends --> other_user
        does not equate to other_user -- befriends --> self.

        To create bidirectional friendships, you must establish connections
        at both sides, example

        ```
        user1.befriend(user2.befriend(user1))
        ```
        """
        if not self.is_friend_of(other_user):
            if other_user.is_blocking(self):
                raise UserBlockedException()
            self._add_connection_with(other_user, CONNECTION_FRIEND)
        return self

    def unfriend(self, other_user):
        """Unfriends `other_user`, returns `self`"""
        if self.is_friend_of(other_user):
            self._remove_connection_with(other_user, CONNECTION_FRIEND)
        return self

    def is_friend_of(self, other_user):
        """Returns True if `self` has befriended `other_user`."""
        return self._has_connection_with(other_user, CONNECTION_FRIEND)

    def follow(self, other_user):
        """Follow `other_user`, returns `self`.

        Note that following is bidirectional, i.e.
        when self (follower) -- follows --> other_user
        does not equate to other_user -- follows --> self.

        To create bidirectional following, you must establish connections
        at both sides, example

        ```
        user1.follow(user2.follow(user1))
        ```
        """
        if not self.is_following(other_user):
            if other_user.is_blocking(self):
                raise UserBlockedException()
            self._add_connection_with(other_user, CONNECTION_FOLLOW)
        return self

    def unfollow(self, other_user):
        """Unfollow `other_user`, returns `self`"""
        if self.is_following(other_user):
            self._remove_connection_with(other_user, CONNECTION_FOLLOW)
        return self

    def is_following(self, other_user):
        """Returns True if `self` has followed `other_user`."""
        return self._has_connection_with(other_user, CONNECTION_FOLLOW)

    def block(self, other_user):
        """Blocks `other_user`, returns `self`.

        Note that blocking is bidirectional, i.e.
        when self (blocker) -- blocks --> other_user
        does not equate to other_user -- blocks --> self.

        To create bidirectional blocking, you must establish connections
        at both sides, example

        ```
        user1.block(user2.block(user1))
        ```
        """
        if not self.is_blocking(other_user):
            self._add_connection_with(other_user, CONNECTION_BLOCK)
        return self

    def unblock(self, other_user):
        """Unblocks `other_user`, returns `self`"""
        if self.is_blocking(other_user):
            self._remove_connection_with(other_user, CONNECTION_BLOCK)
        return self

    def is_blocking(self, other_user):
        """Returns True if `self` has blocked `other_user`."""
        return self._has_connection_with(other_user, CONNECTION_BLOCK)

    # Note: @mention is ambigious in the question.
    # When does @mention establish connection:
    #  - a @mention b?
    #  - b @mention a?
    #  - both?
    # Leaving this feature out until clarification
    # def mention(self, other_user):
    #     """Mentioned `other_user`, returns `self`"""
    #     if not self.has_mentioned(other_user):
    #         self._add_connection_with(other_user, CONNECTION_MENTION)
    #     return self
    #
    # def unmention(self, other_user):
    #     """Unmention `other_user`, returns `self`"""
    #     if self.has_mentioned(other_user):
    #         self._remove_connection_with(other_user, CONNECTION_MENTION)
    #     return self
    #
    # def has_mentioned(self, other_user):
    #     """Returns True if `self` has mentioned `other_user`."""
    #     return self._has_connection_with(other_user, CONNECTION_MENTION)

    def is_subscribing(self, other_user):
        """Returns True if `self` is subscribing to `other_user`.

        Subscription is establised when:
        - self has not blocked other_user
        - at least one of the following:
          - self is a friend of other_user
          - self is a follower of other_user
        """
        connection = self._connection_with(other_user)
        if connection & ~CONNECTION_BLOCK:
            return connection & CONNECTION_SUBSCRIBED and True or False
        return False

    def _connection_with(self, other_user):
        """Returns an bitwise flag containing connection information
        with `other`. See `ConnectionTypes`.
        """
        _assert_is_user(other_user)
        if self.__connections is None:
            self.__connections = {}
        if other_user.user_id not in self.__connections:
            q = db.session.query(connections.c.connection).\
                filter(connections.c.source_id == self.user_id).\
                filter(connections.c.target_id == other_user.user_id)
            self.__connections[other_user.user_id] = \
                q.scalar() or CONNECTION_NONE
        return self.__connections.get(other_user.user_id, CONNECTION_NONE)

    def _add_connection_with(self, other_user, connection):
        current = self._connection_with(other_user)
        return self._update_connection_with(other_user, current | connection)

    def _remove_connection_with(self, other_user, connection):
        current = self._connection_with(other_user)
        return self._update_connection_with(other_user, current & ~connection)

    def _has_connection_with(self, other_user, connection):
        return self._connection_with(other_user) & connection == connection

    def _update_connection_with(self, other_user, connection):
        upsert = insert(connections).values(
            source_id=self.user_id,
            target_id=other_user.user_id,
            connection=connection
        ).on_conflict_do_update(
            index_elements=('source_id', 'target_id'),
            set_=dict(connection=connection)
        )
        db.session.execute(upsert)
        self.__connections[other_user.user_id] = connection


def _assert_is_user(userMaybe):
    assert isinstance(userMaybe, User), 'Expects user but got %s' % userMaybe
