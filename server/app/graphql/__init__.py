import graphene
from graphene import relay
from .users import User
from ..models import User as UserModel


class Query(graphene.ObjectType):

    node = relay.Node.Field()
    me = graphene.Field(User)

    def resolve_me(self, args, context, info):
        return UserModel.query.get(1)


types = [User]

schema = graphene.Schema(query=Query, types=types)
