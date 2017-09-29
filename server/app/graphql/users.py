from ..logging import logger
from ..models import (
    db, current_user, current_user_id, connections, User as UserModel,
    CONNECTION_FRIEND
)
from graphene import relay, types
from graphene_sqlalchemy import SQLAlchemyObjectType
from promise import Promise
from promise.dataloader import DataLoader
from flask import g


class UserLoader(DataLoader):

    def batch_load_fn(self, keys):
        user_ids = set(keys)
        logger.debug('Batch loading users for {}'.format(user_ids))
        q = UserModel.query.filter(UserModel.user_id.in_(user_ids))
        users = dict([(user.user_id, user) for user in q.all()])
        # Important, must return in same order as `keys`
        return Promise.resolve([users.get(user_id, None) for user_id in keys])


def current_user_loader():
    if not hasattr(g, 'user_loader'):
        setattr(g, 'user_loader', UserLoader(cache=True))
    return g.user_loader


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel
        interfaces = (relay.Node, )
        only_fields = (
            'user_id',
            'first_name',
            'last_name',
            'gender',
            'education',
            'address',
            'job',
            'introduction',
            'avatar_url',
            'friends',
            'following',
            'followers',
        )
        local_fields = {
            'full_name': types.Field(types.String),
            'is_friend_of_me': types.Field(types.Boolean),
            'is_following_me': types.Field(types.Boolean),
            'is_followed_by_me': types.Field(types.Boolean),
            'is_blocked_by_me': types.Field(types.Boolean),
            'is_subscribed_by_me': types.Field(types.Boolean),
            'common_friends_with_me': types.Field(types.List(lambda: User)),
        }

    def resolve_full_name(self, args, context, info):
        return '{} {}'.format(self.first_name, self.last_name)

    def resolve_is_friend_of_me(self, args, context, info):
        return current_user().is_friend_of(self)

    def resolve_is_following_me(self, args, context, info):
        return self.is_following(current_user())

    def resolve_is_followed_by_me(self, args, context, info):
        return current_user().is_following(self)

    def resolve_is_blocked_by_me(self, args, context, info):
        return current_user().is_blocking(self)

    def resolve_is_subscribed_by_me(self, args, context, info):
        return current_user().is_subscribing(self)

    def resolve_common_friends_with_me(self, args, context, info):
        return []


ALLOWED_CONNECTION_MUTATIONS = (
    'block', 'unblock', 'follow', 'unfollow', 'befriend', 'unfriend'
)


class UserConnectionMutation(relay.ClientIDMutation):

    class Input:
        user_id = types.List(types.Int, required=True)

    users = types.List(User)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        try:
            mutation = info.field_name
            assert mutation in ALLOWED_CONNECTION_MUTATIONS, \
                'Unsupported mutation type: %s' % mutation
            user_ids = input.get('user_id')
            assert user_ids, 'Expects array of user_id'
            me = current_user()
            assert me, '`current_user` not available'
            mutate = getattr(me, mutation)
            for user_id in user_ids:
                mutate(user_id)
            db.session.commit()
            q = UserModel.query.filter(UserModel.user_id.in_(user_ids))
            users = dict([(u.user_id, u) for u in q.all()])
            return cls(
                users=[users.get(user_id, None) for user_id in user_ids]
            )
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            raise e
