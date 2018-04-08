from django.db import models

__all__ = ('Stat',)


class Stat(models.Model):
    date = models.DateField(auto_now=True)
    # Null node means global aggregated stats
    node = models.ForeignKey('thefederation.Node', on_delete=models.CASCADE, null=True)
    users_total = models.PositiveIntegerField(null=True)
    users_half_year = models.PositiveIntegerField(null=True)
    users_monthly = models.PositiveIntegerField(null=True)
    users_weekly = models.PositiveIntegerField(null=True)
    local_posts = models.PositiveIntegerField(null=True)
    local_comments = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Node ID {self.node_id} <{self.date}>"
