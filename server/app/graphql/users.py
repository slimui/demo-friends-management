from ..models import User as UserModel
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel
        interfaces = (relay.Node, )
        only_fields = (
            'user_id',
            'first_name',
            'last_name',
        )
        # local_fields = {
        #     'friends': SQLAlchemyConnectionField(lambda: User),
        # }
