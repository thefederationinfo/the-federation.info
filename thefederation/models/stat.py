import datetime

from django.db import models
from django.db.models import Count
from django.utils.timezone import now

from thefederation.utils import single_true

__all__ = ('Stat',)


class StatQuerySet(models.QuerySet):
    def for_days(self, from_date=None, platform=None, protocol=None, node=None):
        assert not all([platform, protocol, node])
        if not from_date:
            from_date = now().date() - datetime.timedelta(days=1)
        if platform:
            qs = Stat.objects.filter(platform__name=platform)
        elif protocol:
            qs = Stat.objects.filter(protocol__name=protocol)
        elif node:
            qs = Stat.objects.filter(node__host=node)
        else:
            qs = Stat.objects.filter(platform__isnull=True, protocol__isnull=True, node__isnull=True)

        qs = qs.filter(date__gte=from_date)

        return qs.order_by('-date')

    def for_global(self):
        return self.filter(node__isnull=True, protocol__isnull=True, platform__isnull=True)

    def node_counts(self, from_date=None, item_type=None, value=None):
        if not from_date:
            from_date = now().date() - datetime.timedelta(days=1)
        if value and item_type:
            if item_type == 'platform':
                qs = self.filter(node__platform__name=value)
            elif item_type == 'protocol':
                qs = self.filter(node__protocols__name=value)
            elif item_type == 'node':
                qs = self.filter(node__host=value)
            else:
                raise ValueError('item_type should be "platform", "node" or "protocol')
        else:
            qs = self.filter(node__isnull=False)

        qs = qs.filter(date__gte=from_date)

        return qs.values('date').annotate(
            count=Count('id')
        ).values('date', 'count').order_by('date')


class Stat(models.Model):
    date = models.DateField(db_index=True)

    # NOTE! only one or the other node or platform or protocol can be filled
    # If none filled -> global stats
    node = models.ForeignKey(
        'thefederation.Node', on_delete=models.CASCADE, null=True, blank=True,
        related_name='stats',
    )
    platform = models.ForeignKey('thefederation.Platform', on_delete=models.CASCADE, null=True, blank=True)
    protocol = models.ForeignKey('thefederation.Protocol', on_delete=models.CASCADE, null=True, blank=True)

    users_total = models.PositiveIntegerField(null=True)
    users_half_year = models.PositiveIntegerField(null=True)
    users_monthly = models.PositiveIntegerField(null=True)
    users_weekly = models.PositiveIntegerField(null=True)
    local_posts = models.PositiveIntegerField(null=True)
    local_comments = models.PositiveIntegerField(null=True)

    objects = StatQuerySet.as_manager()

    class Meta:
        unique_together = (
            ('date', 'node'),
            ('date', 'platform'),
            ('date', 'protocol'),
        )

    def __str__(self):
        if self.node:
            return f"Node ID {self.node_id} <{self.date}>"
        elif self.platform:
            return f"Platform ID {self.platform_id} <{self.date}>"
        elif self.protocol:
            return f"Protocol ID {self.protocol_id} <{self.date}>"
        return f"Global <{self.date}>"

    def save(self, *args, **kwargs):
        values = [self.node, self.platform, self.protocol]
        if any(values) and not single_true(values):
            raise ValueError("Can only fill one of node, platform or protocol!")
        super().save(*args, **kwargs)
