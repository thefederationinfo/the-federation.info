import datetime

import MySQLdb
from MySQLdb.cursors import DictCursor
from django.conf import settings
from django.utils.timezone import now

from thefederation.models import Platform, Node


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
