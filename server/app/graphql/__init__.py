import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .users import (
    User, UserConnectionMutation, current_user
)


class Query(graphene.ObjectType):

    node = relay.Node.Field()
    me = graphene.Field(User)

    all_users = SQLAlchemyConnectionField(lambda: User)

    def resolve_me(*args):
        return current_user()


class Mutation(graphene.ObjectType):

    befriend = UserConnectionMutation.Field()
    unfriend = UserConnectionMutation.Field()
    follow = UserConnectionMutation.Field()
    unfollow = UserConnectionMutation.Field()
    block = UserConnectionMutation.Field()
    unblock = UserConnectionMutation.Field()


types = [User]

schema = graphene.Schema(query=Query, mutation=Mutation, types=types)
