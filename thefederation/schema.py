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
    nodes = graphene.List(
        NodeType,
        host=graphene.String(),
        platform=graphene.String(),
    )
    platforms = graphene.List(
        PlatformType,
        name=graphene.String(),
    )
    protocols = graphene.List(
        ProtocolType,
        name=graphene.String(),
    )
    stats = graphene.List(StatType)
    stats_counts_nodes = graphene.List(
        DateCountType,
        value=graphene.String(),
        itemType=graphene.String(),
    )
    stats_global_today = graphene.Field(
        StatType,
        platform=graphene.String(),
    )
    stats_nodes = graphene.List(
        StatType,
        host=graphene.String(),
        platform=graphene.String(),
    )
    stats_platform_today = graphene.Field(
        StatType,
        name=graphene.String(),
    )
    stats_protocol_today = graphene.Field(
        StatType,
        name=graphene.String(),
    )
    stats_users_total = graphene.List(
        DateCountType,
        itemType=graphene.String(),
        value=graphene.String(),
    )
    stats_users_half_year = graphene.List(
        DateCountType,
        itemType=graphene.String(),
        value=graphene.String(),
    )
    stats_users_monthly = graphene.List(
        DateCountType,
        itemType=graphene.String(),
        value=graphene.String(),
    )
    stats_users_weekly = graphene.List(
        DateCountType,
        itemType=graphene.String(),
        value=graphene.String(),
    )
    stats_local_posts = graphene.List(
        DateCountType,
        itemType=graphene.String(),
        value=graphene.String(),
    )
    stats_local_comments = graphene.List(
        DateCountType,
        itemType=graphene.String(),
        value=graphene.String(),
    )

    def resolve_nodes(self, info, **kwargs):
        if kwargs.get('platform'):
            qs = Node.objects.filter(platform__name=kwargs.get('platform'))
        else:
            qs = Node.objects.all()

        if kwargs.get('host'):
            qs = qs.filter(host=kwargs.get('host'))

        stat = Stat.objects.filter(
            node=OuterRef('pk'), date=now().date()
        ).values('users_monthly').annotate(users=Max('users_monthly')).values('users')

        return qs.active().annotate(
            users=Subquery(stat, output_field=IntegerField())
        ).order_by(
            F('users').desc(nulls_last=True)
        ).select_related('platform')

    def resolve_platforms(self, info, **kwargs):
        if kwargs.get('name'):
            qs = Platform.objects.filter(name=kwargs.get('name').lower())
        else:
            qs = Platform.objects.all()

        nodes = Node.objects.active().filter(
            platform=OuterRef('pk')).values('platform').annotate(c=Count('*')).values('c')
        return qs.prefetch_related('nodes').annotate(
            active_nodes=Subquery(nodes, output_field=IntegerField())
        ).filter(active_nodes__gt=0).order_by('-active_nodes')

    def resolve_protocols(self, info, **kwargs):
        nodes = Node.objects.active().filter(
            protocols=OuterRef('pk')).values('protocols').annotate(c=Count('*')).values('c')
        return Protocol.objects.prefetch_related('nodes').annotate(
            active_nodes=Subquery(nodes, output_field=IntegerField())
        ).filter(active_nodes__gt=0).order_by('-active_nodes')

    def resolve_stats(self, info, **kwargs):
        return Stat.objects.all()

    def resolve_stats_counts_nodes(self, info, **kwargs):
        if kwargs.get('value') and kwargs.get('itemType'):
            if kwargs.get('itemType') == 'platform':
                qs = Stat.objects.filter(node__platform__name=kwargs.get('value'))
            elif kwargs.get('itemType') == 'node':
                qs = Stat.objects.filter(node__host=kwargs.get('value'))
            else:
                raise ValueError('itemType should be "platform" or "node"')
        else:
            qs = Stat.objects.filter(node__isnull=False)
        return qs.values('date').annotate(
            count=Count('id')
        ).values('date', 'count').order_by('date')

    def resolve_stats_global_today(self, info, **kwargs):
        if kwargs.get('platform'):
            qs = Stat.objects.filter(platform__name=kwargs.get('platform'))
        else:
            qs = Stat.objects.filter(platform__isnull=True)

        return qs.filter(
            node__isnull=True, protocol__isnull=True, date=now().date(),
        ).first()

    def resolve_stats_nodes(self, info, **kwargs):
        if kwargs.get('platform'):
            qs = Stat.objects.filter(node__platform__name=kwargs.get('platform'))
        else:
            qs = Stat.objects.all()

        if kwargs.get('host'):
            qs = qs.filter(node__host=kwargs.get('host'))

        return qs.filter(date=now().date(), node__isnull=False, protocol__isnull=True, platform__isnull=True)

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

    @staticmethod
    def _get_stat_date_counts(stat, value=None, item_type=None):
        if value and item_type:
            if item_type == 'platform':
                qs = Stat.objects.filter(node__platform__name=value)
            elif item_type == 'node':
                qs = Stat.objects.filter(node__host=value)
            else:
                raise ValueError('itemType should be "platform" or "node"')
        else:
            qs = Stat.objects.filter(node__isnull=False)

        return qs.values('date').annotate(
            count=Sum(stat)
        ).values('date', 'count').order_by('date')

    def resolve_stats_users_total(self, info, **kwargs):
        return Query._get_stat_date_counts('users_total', value=kwargs.get('value'), item_type=kwargs.get('itemType'))

    def resolve_stats_users_half_year(self, info, **kwargs):
        return Query._get_stat_date_counts('users_half_year', value=kwargs.get('value'), item_type=kwargs.get('itemType'))

    def resolve_stats_users_monthly(self, info, **kwargs):
        return Query._get_stat_date_counts('users_monthly', value=kwargs.get('value'), item_type=kwargs.get('itemType'))

    def resolve_stats_users_weekly(self, info, **kwargs):
        return Query._get_stat_date_counts('users_weekly', value=kwargs.get('value'), item_type=kwargs.get('itemType'))

    def resolve_stats_local_posts(self, info, **kwargs):
        return Query._get_stat_date_counts('local_posts', value=kwargs.get('value'), item_type=kwargs.get('itemType'))

    def resolve_stats_local_comments(self, info, **kwargs):
        return Query._get_stat_date_counts('local_comments', value=kwargs.get('value'), item_type=kwargs.get('itemType'))
