import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thefederation', '0020_remove_port_from_node_hostnames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='features',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='node',
            name='server_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
