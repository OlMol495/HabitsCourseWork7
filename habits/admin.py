from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class AdminHabit(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "place",
        "time",
        "is_pleasant",
        "related_habit",
        "frequency",
        "reward",
        "duration",
        "is_public",
    )
