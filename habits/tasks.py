from celery import shared_task
from datetime import datetime, timedelta

from habits.models import Habit
from habits.services import MyBot


@shared_task
def send_habit_reminders():
    """
        Отправляет напоминания о привычках пользователям через Telegram.
    """
    good_habit = Habit.objects.filter(is_pleasant=False)
    now_time = datetime.now().time()
    now_date = datetime.now().today()

    for habit in good_habit:
        if habit.date == now_date or not habit.date:
            if habit.time >= now_time:
                telegram_id, message = MyBot.create_message(habit)
                MyBot.send_message(telegram_id, message)
                habit.date = now_date + timedelta(days=habit.frequency)
                habit.save()
