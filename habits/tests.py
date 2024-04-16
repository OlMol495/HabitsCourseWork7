from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """ Тесты на CRUD привычек """

    def setUp(self):
        self.user1 = User.objects.create(email="test1@admin.pro", password="admin")
        self.user2 = User.objects.create(email="test2@admin.pro", password="admin")
        self.habitpleasnt = Habit.objects.create(
            title='Test-pleasant',
            user=self.user1,
            place="test-place",
            time="07:20:00",
            is_pleasant=True,
            frequency=1,
            reward=None,
            duration=25,
            is_public=False,
        )
        self.habitgood = Habit.objects.create(
            title='Test-good',
            user=self.user1,
            place="test-place",
            time="07:20:00",
            is_pleasant=False,
            frequency=1,
            reward="test-reward",
            duration=25,
            is_public=False,
        )

    def test_create_habit(self):
        """ Тесты на создание привычки """
        self.client.force_authenticate(user=self.user1)
        data = {
            "title": "test-title",
            "user": 1,
            "place": "test-place",
            "time": "20:00:00",
            "is_pleasant": False,
            "frequency": 5,
            "reward": "test-reward",
            "duration": 120,
        }
        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )

        # Проверка на статус ответа
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверка на верность создаваемых полей
        self.assertEqual(
            response.json(),
            {
                "id": 3,
                "title": "test-title",
                "user": 1,
                "place": "test-place",
                "time": "20:00:00",
                "is_pleasant": False,
                "related_habit": None,
                "frequency": 5,
                "reward": "test-reward",
                "duration": 120,
                "is_public": False
            }
        )

        # Проверка на то, что запись создалась в базе
        self.assertTrue(
            Habit.objects.all().exists()
        )


