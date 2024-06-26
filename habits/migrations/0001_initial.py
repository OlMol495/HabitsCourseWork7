# Generated by Django 5.0 on 2024-04-15 22:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField(verbose_name="описание привычки")),
                ("place", models.CharField(max_length=155, verbose_name="место")),
                ("time", models.TimeField(blank=True, null=True, verbose_name="время")),
                ("is_pleasant", models.BooleanField(verbose_name="приятная")),
                (
                    "frequency",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="периодичность в днях"
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="награда"
                    ),
                ),
                (
                    "duration",
                    models.PositiveIntegerField(
                        verbose_name="продолжительность выполнения привычки в секундах"
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(default=False, verbose_name="публичная"),
                ),
                (
                    "related_habit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="habits.habit",
                        verbose_name="связанная привычка",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "привычка",
                "verbose_name_plural": "привычки",
            },
        ),
    ]
