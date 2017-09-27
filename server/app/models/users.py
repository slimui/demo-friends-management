from .core import Model, now, metadata, relationship
from sqlalchemy import (
    Column, Integer, String, DateTime, Table, ForeignKey
)
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


class User(Model):
    """Represents a user entity."""

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)

    email = Column(String, nullable=False)

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

    def __repr__(self):
        return '<User({})>'.format(self.user_id)

    def to_dict(self):
        return {
            'user_id': self.user_id,
        }
