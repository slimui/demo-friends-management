import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .users import User
from ..requests import current_user


class Query(graphene.ObjectType):

    node = relay.Node.Field()
    me = graphene.Field(User)

    all_users = SQLAlchemyConnectionField(lambda: User)

    def resolve_me(*args):
        return current_user()


types = [User]

schema = graphene.Schema(query=Query, types=types)
