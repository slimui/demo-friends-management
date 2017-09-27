from ..models import User as UserModel
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
        return False

    def resolve_is_following_me(self, args, context, info):
        return False

    def resolve_is_followed_by_me(self, args, context, info):
        return False

    def resolve_is_blocked_by_me(self, args, context, info):
        return False

    def resolve_is_subscribed_by_me(self, args, context, info):
        return False
