import graphene
from django.db.models import Subquery, OuterRef, Count, Max, IntegerField, F, Sum
from django.utils.timezone import now
from graphene_django import DjangoObjectType

from thefederation.models import Node, Platform, Protocol, Stat


class DateCountType(graphene.ObjectType):
    date = graphene.Date()
    count = graphene.Int()

    def resolve_count(self, info):
        return self.get('count')

    def resolve_date(self, info):
        return self.get('date')


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
    stats_counts_nodes = graphene.List(DateCountType)
    stats_global_today = graphene.Field(StatType)
    stats_nodes = graphene.List(StatType)
    stats_platform_today = graphene.Field(
        StatType,
        name=graphene.String(),
    )
    stats_protocol_today = graphene.Field(
        StatType,
        name=graphene.String(),
    )
    stats_users_total = graphene.List(DateCountType)

    def resolve_nodes(self, info, **kwargs):
        stat = Stat.objects.filter(
            node=OuterRef('pk'), date=now().date()
        ).values('users_monthly').annotate(users=Max('users_monthly')).values('users')

        return Node.objects.active().annotate(
            users=Subquery(stat, output_field=IntegerField())
        ).order_by(
            F('users').desc(nulls_last=True)
        ).select_related('platform')

    def resolve_platforms(self, info, **kwargs):
        nodes = Node.objects.active().filter(
            platform=OuterRef('pk')).values('platform').annotate(c=Count('*')).values('c')
        return Platform.objects.prefetch_related('nodes').annotate(
            active_nodes=Subquery(nodes)
        ).filter(active_nodes__gt=0).order_by('-active_nodes')

    def resolve_protocols(self, info, **kwargs):
        nodes = Node.objects.active().filter(
            protocols=OuterRef('pk')).values('protocols').annotate(c=Count('*')).values('c')
        return Protocol.objects.prefetch_related('nodes').annotate(
            active_nodes=Subquery(nodes)
        ).filter(active_nodes__gt=0).order_by('-active_nodes')

    def resolve_stats(self, info, **kwargs):
        return Stat.objects.all()

    def resolve_stats_counts_nodes(self, info, **kwargs):
        return Stat.objects.filter(node__isnull=False).values('date').annotate(
            count=Count('id')
        ).values('date', 'count').order_by('date')

    def resolve_stats_global_today(self, info, **kwargs):
        return Stat.objects.filter(
            node__isnull=True, platform__isnull=True, protocol__isnull=True, date=now().date(),
        ).first()

    def resolve_stats_nodes(self, info, **kwargs):
        return Stat.objects.filter(date=now().date(), node__isnull=False, protocol__isnull=True, platform__isnull=True)

    def resolve_stats_platform_today(self, info, **kwargs):
        name = kwargs.get('name')
        if not name:
            return Stat.objects.none()

        return Stat.objects.filter(
            node__isnull=True, protocol__isnull=True, platform__name=name, date=now().date(),
        ).first()

    def resolve_stats_protocol_today(self, info, **kwargs):
        name = kwargs.get('name')
        if not name:
            return Stat.objects.none()

        return Stat.objects.filter(
            node__isnull=True, platform__isnull=True, protocol__name=name, date=now().date(),
        ).first()

    def resolve_stats_users_total(self, info, **kwargs):
        return Stat.objects.filter(node__isnull=False).values('date').annotate(
            count=Sum('users_total')
        ).values('date', 'count').order_by('date')
