# Generated by Django 5.0 on 2024-04-18 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0002_alter_habit_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="habit",
            name="date",
            field=models.DateField(blank=True, null=True, verbose_name="дата"),
        ),
    ]
