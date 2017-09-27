from .core import db, Model, now, metadata, relationship
from sqlalchemy import (
    Column, Integer, String, DateTime, Table, ForeignKey
)
from ..errors import UserBlockedException
# from sqlalchemy.ext.hybrid import hybrid_property
# from flask_sqlalchemy import SignallingSession

friendships = Table(
    'friendships', metadata,
    Column(
        'befriender_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'other_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'created_at', DateTime(timezone=True), nullable=False, default=now)
)

followers = Table(
    'followers', metadata,
    Column(
        'follower_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'other_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'created_at', DateTime(timezone=True), nullable=False, default=now)
)

blocked_users = Table(
    'blocked_users', metadata,
    Column(
        'blocker_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'other_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'created_at', DateTime(timezone=True), nullable=False, default=now)
)

mentioned_users = Table(
    'mentioned_users', metadata,
    Column(
        'mentioner_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'other_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'created_at', DateTime(timezone=True), nullable=False, default=now)
)

connected_users = Table(
    'connected_users', metadata,
    Column(
        'connecter_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'other_id', Integer, ForeignKey('users.user_id'),
        primary_key=True),
    Column(
        'created_at', DateTime(timezone=True), nullable=False, default=now)
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
        'User', secondary=friendships, cascade='all', lazy='dynamic',
        primaryjoin=user_id == friendships.c.befriender_id,
        secondaryjoin=user_id == friendships.c.other_id)

    following = relationship(
        'User', secondary=followers, cascade='all', lazy='dynamic',
        primaryjoin=user_id == followers.c.follower_id,
        secondaryjoin=user_id == followers.c.other_id)

    # Note: this is view only. To add follower, use `following`
    followers = relationship(
        'User', secondary=followers, cascade='all', lazy='dynamic',
        primaryjoin=user_id == followers.c.other_id,
        secondaryjoin=user_id == followers.c.follower_id, viewonly=True)

    blocked_users = relationship(
        'User', secondary=blocked_users, cascade='all', lazy='dynamic',
        primaryjoin=user_id == blocked_users.c.blocker_id,
        secondaryjoin=user_id == blocked_users.c.other_id)

    mentioned_users = relationship(
        'User', secondary=mentioned_users, cascade='all', lazy='dynamic',
        primaryjoin=user_id == mentioned_users.c.mentioner_id,
        secondaryjoin=user_id == mentioned_users.c.other_id)

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
            self.friends.append(other_user)
        return self

    def unfriend(self, other_user):
        """Unfriends `other_user`, returns `self`"""
        if self.is_friend_of(other_user):
            self.friends.remove(other_user)
        return self

    def is_friend_of(self, other_user):
        """Returns True if `self` has befriended `other_user`."""
        _assert_is_user(other_user)
        q = self.friends.filter(
            friendships.c.other_id == other_user.user_id).exists()
        return db.session.query(q).scalar()

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
            self.following.append(other_user)
        return self

    def unfollow(self, other_user):
        """Unfollow `other_user`, returns `self`"""
        if self.is_following(other_user):
            self.following.remove(other_user)
        return self

    def is_following(self, other_user):
        """Returns True if `self` has followed `other_user`."""
        _assert_is_user(other_user)
        q = self.following.filter(
            followers.c.other_id == other_user.user_id).exists()
        return db.session.query(q).scalar()

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
            self.blocked_users.append(other_user)
        return self

    def unblock(self, other_user):
        """Unblocks `other_user`, returns `self`"""
        if self.is_blocking(other_user):
            self.blocked_users.remove(other_user)
        return self

    def is_blocking(self, other_user):
        """Returns True if `self` has blocked `other_user`."""
        _assert_is_user(other_user)
        q = self.blocked_users.filter(
            blocked_users.c.other_id == other_user.user_id).exists()
        return db.session.query(q).scalar()

    def mention(self, other_user):
        """Mentioned `other_user`, returns `self`"""
        if not self.has_mentioned(other_user):
            self.mentioned_users.append(other_user)
        return self

    def unmention(self, other_user):
        """Unmention `other_user`, returns `self`"""
        if self.has_mentioned(other_user):
            self.mentioned_users.remove(other_user)
        return self

    def has_mentioned(self, other_user):
        """Returns True if `self` has mentioned `other_user`."""
        _assert_is_user(other_user)
        q = self.mentioned_users.filter(
            mentioned_users.c.other_id == other_user.user_id).exists()
        return db.session.query(q).scalar()

    def is_connected(self, other_user):
        """Returns True if `self` is connected to `other_user`.

        Connections are establised when:
        - self has not blocked other_user
        - at least one of the following:
          - self is a friend of other_user
          - self is a follower of other_user
          - other_user has mentioned self
          - self has mentioned other_user
        """
        _assert_is_user(other_user)
        q = self.connected_users.filter(
            connected_users.c.connector_id == other_user.user_id).exists()
        return db.session.query(q).scalar()


def _assert_is_user(userMaybe):
    assert isinstance(userMaybe, User), 'Expects user but got %s' % userMaybe
