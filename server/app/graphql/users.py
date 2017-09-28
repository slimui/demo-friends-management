from ..logging import logger
from ..models import db, current_user, User as UserModel
from graphene import relay, types
from graphene_sqlalchemy import SQLAlchemyObjectType


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
            'is_friend_of_me': types.Field(types.Boolean),
            'is_following_me': types.Field(types.Boolean),
            'is_followed_by_me': types.Field(types.Boolean),
            'is_blocked_by_me': types.Field(types.Boolean),
            'is_subscribed_by_me': types.Field(types.Boolean),
        }

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
            users = [UserModel.query.get(user_id) for user_id in user_ids]
            return cls(users=users)
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            raise e
