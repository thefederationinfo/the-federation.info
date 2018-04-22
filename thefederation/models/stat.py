from django.db import models

__all__ = ('Stat',)


class Stat(models.Model):
    date = models.DateField(auto_now=True)

    # NOTE! only one or the other node or platform can be filled
    # If neither filled -> global stats
    node = models.ForeignKey('thefederation.Node', on_delete=models.CASCADE, null=True, blank=True)
    platform = models.ForeignKey('thefederation.Platform', on_delete=models.CASCADE, null=True, blank=True)

    users_total = models.PositiveIntegerField(null=True)
    users_half_year = models.PositiveIntegerField(null=True)
    users_monthly = models.PositiveIntegerField(null=True)
    users_weekly = models.PositiveIntegerField(null=True)
    local_posts = models.PositiveIntegerField(null=True)
    local_comments = models.PositiveIntegerField(null=True)

    def __str__(self):
        if self.node:
            return f"Node ID {self.node_id} <{self.date}>"
        elif self.platform:
            return f"Platform ID {self.platform_id} <{self.date}>"
        return f"Global <{self.date}>"

    def save(self, *args, **kwargs):
        if self.node and self.platform:
            raise ValueError("Cannot fill both node and platform!")
        super().save(*args, **kwargs)
