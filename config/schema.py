import graphene

import thefederation.schema


class Query(thefederation.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
