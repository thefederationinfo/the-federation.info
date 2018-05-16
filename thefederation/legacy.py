import datetime

import MySQLdb
from MySQLdb.cursors import DictCursor
from django.conf import settings
from django.utils.timezone import now

from thefederation.models import Platform, Node, Stat


def sync_legacy_data():
    db = MySQLdb.connect(
        host=settings.THEFEDERATION_LEGACY_HOST,
        user=settings.THEFEDERATION_LEGACY_USER,
        passwd=settings.THEFEDERATION_LEGACY_PASSWORD,
        db=settings.THEFEDERATION_LEGACY_DB,
        cursorclass=DictCursor,
    )
    cursor = db.cursor()

    # Pods
    cursor.execute("""select * from pods""")
    row = cursor.fetchone()
    while row:
        if Node.objects.filter(host=row['host']).exists():
            row = cursor.fetchone()
            continue

        platform, _created = Platform.objects.get_or_create(name=row['network'].lower())
        data = {
            'name': row['name'],
            'host': row['host'],
            'version': row['version'],
            'open_signups': row['registrations_open'],
            'last_success': now() - datetime.timedelta(days=row['failures']),
            'ip': row['ip4'],
            'country': row['country'] or '',
            'platform': platform,
        }
        node, _created = Node.objects.get_or_create(host=row['host'], defaults=data)
        print('Synced!:', node)
        row = cursor.fetchone()

    cursor.close()
    db.close()


def sync_legacy_stats():
    db = MySQLdb.connect(
        host=settings.THEFEDERATION_LEGACY_HOST,
        user=settings.THEFEDERATION_LEGACY_USER,
        passwd=settings.THEFEDERATION_LEGACY_PASSWORD,
        db=settings.THEFEDERATION_LEGACY_DB,
        cursorclass=DictCursor,
    )
    cursor = db.cursor()
    cursor2 = db.cursor()

    cursor.execute("""select * from stats""")
    row = cursor.fetchone()
    while row:
        cursor2.execute("""select host from pods where id = %s""", (row['pod_id'],))
        old_node = cursor2.fetchone()

        if not old_node or Stat.objects.filter(node__host=old_node['host'], date=row['date']).exists():
            row = cursor.fetchone()
            continue

        try:
            node = Node.objects.get(host=old_node['host'])
        except Node.DoesNotExist:
            row = cursor.fetchone()
            continue

        data = {
            'node': node,
            'date': row['date'],
            'users_total': row['total_users'] if row['total_users'] and row['total_users'] > 0 else None,
            'users_half_year': row['active_users_halfyear'] if row['active_users_halfyear'] and
                                                               row['active_users_halfyear'] > 0 else None,
            'users_monthly': row['active_users_monthly'] if row['active_users_monthly'] and
                                                            row['active_users_monthly'] > 0 else None,
            'local_posts': row['local_posts'] if row['local_posts'] and row['local_posts'] > 0 else None,
            'local_comments': row['local_comments'] if row['local_comments'] and row['local_comments'] > 0 else None,
        }
        stat = Stat.objects.create(**data)
        print('Synced!:', stat)
        row = cursor.fetchone()

    cursor.close()
    cursor2.close()
    db.close()
