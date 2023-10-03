import graphene
from graphql_auth.schema import MeQuery
from graphql_auth import mutations
from graphql_auth.models import UserStatus

class CustomRegister(mutations.Register):
    class Input:
        username = graphene.String(required=True)
        email = graphene.String(required=True)  # Add email field

    @classmethod
    def perform_mutation(cls, root, info, username, email, **kwargs):
        # Ensure that both username and email are unique
        if cls.check_unique(username, email):
            user = cls.create_user(username=username, email=email)
            cls.create_user_status(user)
            return cls(user=user)
        else:
            raise ValueError("Username and/or email already exist")

class CustomTokenAuth(mutations.ObtainJSONWebToken):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def perform_mutation(cls, root, info, username, password, **kwargs):
        return cls.resolve(cls, root, info, username=username, password=password)

class Query(MeQuery, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    register = CustomRegister.Field()
    token_auth = CustomTokenAuth.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
