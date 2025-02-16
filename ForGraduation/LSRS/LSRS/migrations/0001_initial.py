# Generated by Django 5.1.5 on 2025-01-21 12:54

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Reservations",
            fields=[
                ("reservation_id", models.AutoField(primary_key=True, serialize=False)),
                ("reservation_time", models.DateTimeField(blank=True, null=True)),
                ("start_time", models.DateTimeField(blank=True, null=True)),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(blank=True, max_length=9, null=True)),
                ("checked_in", models.IntegerField(blank=True, null=True)),
                ("check_in_time", models.DateTimeField(blank=True, null=True)),
            ],
            options={"db_table": "reservations", "managed": False,},
        ),
        migrations.CreateModel(
            name="Seats",
            fields=[
                ("seat_id", models.IntegerField(primary_key=True, serialize=False)),
                ("status", models.CharField(blank=True, max_length=9, null=True)),
                ("seat_type", models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={"db_table": "seats", "managed": False,},
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=15)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("password", models.CharField(max_length=50)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
            ],
            options={"db_table": "users", "managed": False,},
            managers=[("object", django.db.models.manager.Manager()),],
        ),
    ]
