# Generated by Django 5.1.6 on 2025-03-08 00:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LSRS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='reservation_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 3, 8, 0, 43, 42, 453710, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
