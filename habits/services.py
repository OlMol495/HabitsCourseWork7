import requests
from django.conf import settings


class MyBot:
    URL = "https://api.telegram.org/bot"
    TOKEN = settings.TELEGRAM_BOT_TOKEN

    def send_message(self, telegram_id, message):
        """ Отправка сообщения в телеграм чат"""
        requests.post(
            url=f'{self.URL}{self.TOKEN}/sendMessage',
            data={
                'chat_id': telegram_id,
                'text': message
            }
        )

    def create_message(habit):
        """ Создание сообщения для бота"""
        if habit.user.telegram_id:
            telegram_id = habit.user.telegram_id
            message = f"Напоминание: {habit.title} в {habit.place} в {habit.time.strftime('%H:%M')}"

        if habit.reward:
            message += f" Награда за выполнение: {habit.reward}."

        if habit.related_habit:
            related_habit_title = habit.related_habit.title
            message += f" Связанная привычка: {related_habit_title}."

        return telegram_id, message
