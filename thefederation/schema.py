import graphene
from graphene_django import DjangoObjectType

from thefederation.models import Node, Platform


class NodeType(DjangoObjectType):
    class Meta:
        model = Node


class PlatformType(DjangoObjectType):
    class Meta:
        model = Platform


class Query:
    all_nodes = graphene.List(NodeType)
    all_platforms = graphene.List(PlatformType)

    def resolve_all_nodes(self, info, **kwargs):
        return Node.objects.select_related('platform').all()

    def resolve_all_platforms(self, info, **kwargs):
        return Platform.objects.prefetch_related('nodes').all()
