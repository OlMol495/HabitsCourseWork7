from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    title = models.TextField(verbose_name="описание привычки")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.CharField(max_length=155, verbose_name="место")
    time = models.TimeField(verbose_name="время", **NULLABLE)
    is_pleasant = models.BooleanField(verbose_name="приятная")
    related_habit = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name="связанная привычка", **NULLABLE)
    frequency = models.PositiveSmallIntegerField(verbose_name="периодичность в днях", default=1)
    reward = models.CharField(max_length=255, verbose_name="награда", **NULLABLE)
    duration = models.PositiveIntegerField(
        verbose_name="продолжительность выполнения привычки в секундах", default=1)
    is_public = models.BooleanField(verbose_name="публичная", default=False)

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return f"{self.title}"
