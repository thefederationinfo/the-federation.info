import graphene
from graphene_django import DjangoObjectType

from thefederation.models import Node, Platform, Protocol


class NodeType(DjangoObjectType):
    class Meta:
        model = Node


class PlatformType(DjangoObjectType):
    class Meta:
        model = Platform


class ProtocolType(DjangoObjectType):
    class Meta:
        model = Protocol


class Query:
    nodes = graphene.List(NodeType)
    platforms = graphene.List(PlatformType)
    protocols = graphene.List(ProtocolType)

    def resolve_nodes(self, info, **kwargs):
        return Node.objects.select_related('platform').all()

    def resolve_platforms(self, info, **kwargs):
        return Platform.objects.prefetch_related('nodes').all()

    def resolve_protocols(self, info, **kwargs):
        return Protocol.objects.prefetch_related('nodes').all()
