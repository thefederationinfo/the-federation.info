import graphene
from django.utils.timezone import now
from graphene_django import DjangoObjectType

from thefederation.models import Node, Platform, Protocol, Stat


class NodeType(DjangoObjectType):
    class Meta:
        model = Node


class PlatformType(DjangoObjectType):
    class Meta:
        model = Platform


class ProtocolType(DjangoObjectType):
    class Meta:
        model = Protocol


class StatType(DjangoObjectType):
    class Meta:
        model = Stat


class Query:
    nodes = graphene.List(NodeType)
    platforms = graphene.List(PlatformType)
    protocols = graphene.List(ProtocolType)
    stats = graphene.List(StatType)
    stats_global_today = graphene.Field(StatType)
    stats_platform_today = graphene.Field(
        StatType,
        name=graphene.String(),
    )

    def resolve_nodes(self, info, **kwargs):
        return Node.objects.select_related('platform').active()

    def resolve_platforms(self, info, **kwargs):
        return Platform.objects.prefetch_related('nodes').all()

    def resolve_protocols(self, info, **kwargs):
        return Protocol.objects.prefetch_related('nodes').all()

    def resolve_stats(self, info, **kwargs):
        return Stat.objects.all()

    def resolve_stats_global_today(self, info, **kwargs):
        return Stat.objects.filter(node__isnull=True, platform__isnull=True, date=now().date()).first()

    def resolve_stats_platform_today(self, info, **kwargs):
        name = kwargs.get('name')
        if not name:
            return Stat.objects.none()

        return Stat.objects.filter(node__isnull=True, platform__name=name, date=now().date()).first()
