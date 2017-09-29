from ..logging import logger  # noqa
from ..utils import g_get
from ..models import (
    db, current_user, common_friends_between, current_user_id,
    User as UserModel, connections, ConnectionType
)
from graphene import relay, types
from graphene_sqlalchemy import SQLAlchemyObjectType
from promise import Promise
from promise.dataloader import DataLoader


class UserLoader(DataLoader):

    @classmethod
    def loader(cls):
        return g_get('user_loader', lambda: cls(cache=True))

    def batch_load_fn(self, keys):
        user_ids = set(keys)
        logger.debug('Batch loading users for {}'.format(user_ids))
        q = UserModel.query.filter(UserModel.user_id.in_(user_ids))
        users = dict([(user.user_id, user) for user in q.all()])
        # Important, must return in same order as `keys`
        return Promise.resolve([users.get(user_id, None) for user_id in keys])


class CurrentUserCommonFriendIdsLoader(DataLoader):

    @classmethod
    def loader(cls):
        return g_get(
            'current_user_common_friend_ids_loader', lambda: cls(cache=True))

    def batch_load_fn(self, keys):
        target_ids = set(keys)
        logger.debug('Batch loading common friend for {}'.format(target_ids))
        friends = dict(common_friends_between(current_user_id(), target_ids))
        # Use UserLoader to batch fetch friends
        return Promise.resolve([
            Promise.resolve([
                friend_id
                for friend_id in friends.get(target_id, [])
            ])
            for target_id in keys
        ])


class CurrentUserConnectionLoader(DataLoader):

    @classmethod
    def loader(cls):
        return g_get(
            'current_user_connection_loader', lambda: cls(cache=True))

    def batch_load_fn(self, keys):
        target_ids = set(keys)
        logger.debug('Batch loading connections with {}'.format(target_ids))
        q = db.session.query(
                connections.c.target_id,
                connections.c.connection,
            ).\
            filter(connections.c.source_id == current_user_id()).\
            filter(connections.c.target_id.in_(target_ids))
        connects = dict(q.all())
        return Promise.resolve([
            connects.get(target_id, 0) for target_id in keys
        ])


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
            'is_followed_by_me': types.Field(types.Boolean),
            'is_blocked_by_me': types.Field(types.Boolean),
            'is_subscribed_by_me': types.Field(types.Boolean),
            'common_friends_with_me': types.Field(types.List(lambda: User)),
        }

    def resolve_full_name(self, args, context, info):
        return '{} {}'.format(self.first_name, self.last_name)

    def resolve_is_friend_of_me(self, args, context, info):
        return CurrentUserConnectionLoader.loader().load(self.user_id).\
            then(ConnectionType.is_friend)

    def resolve_is_followed_by_me(self, args, context, info):
        return CurrentUserConnectionLoader.loader().load(self.user_id).\
            then(ConnectionType.is_follow)

    def resolve_is_blocked_by_me(self, args, context, info):
        return CurrentUserConnectionLoader.loader().load(self.user_id).\
            then(ConnectionType.is_block)

    def resolve_is_subscribed_by_me(self, args, context, info):
        return CurrentUserConnectionLoader.loader().load(self.user_id).\
            then(ConnectionType.is_subscribed)

    def resolve_common_friends_with_me(self, args, context, info):
        if self.user_id == current_user_id():
            return []
        user_loader = UserLoader.loader()
        return CurrentUserCommonFriendIdsLoader.loader().load(self.user_id).\
            then(lambda friend_ids: Promise.resolve(
                [user_loader.load(friend_id) for friend_id in friend_ids]))


ALLOWED_CONNECTION_MUTATIONS = (
    'block', 'unblock', 'follow', 'unfollow', 'befriend', 'unfriend'
)


class UserConnectionMutation(relay.ClientIDMutation):

    class Input:
        user_id = types.List(types.Int, required=True)

    users = types.List(User)
    related_users = types.List(User)

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
            if mutation in ('befriend', 'unfriend'):
                # befriending/unfriending needs special handling
                # as we need to provide means to access the changes
                # to common friends, especially in unfriending.
                # We cache the common friend here
                common = common_friends_between(current_user_id(), user_ids)
                related_user_ids = sum(  # flatten array
                    [friend_ids for _, friend_ids in common], [])
            else:
                related_user_ids = []
            mutate = getattr(me, mutation)
            for user_id in user_ids:
                mutate(user_id)
            db.session.commit()
            user_loader = UserLoader.loader()
            return cls(
                users=[user_loader.load(user_id) for user_id in user_ids],
                related_users=[
                    user_loader.load(user_id) for user_id in related_user_ids]
            )
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            raise e
