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

    def test_list_habit_own(self):
        """ Тесты на список собственных привычек """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('habits:habits-own-list'))

        # Проверка на статус ответа
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на верность структуры и полей в списке
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                    "count": 2,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 4,
                            "duration": 25,
                            "related_habit": None,
                            "title": "Test-pleasant",
                            "place": "test-place",
                            "time": "07:20:00",
                            "is_pleasant": True,
                            "frequency": 1,
                            "reward": None,
                            "is_public": False,
                            "user": 3
                        },
                        {
                            "id": 5,
                            "duration": 25,
                            "related_habit": None,
                            "title": "Test-good",
                            "place": "test-place",
                            "time": "07:20:00",
                            "is_pleasant": False,
                            "frequency": 1,
                            "reward": "test-reward",
                            "is_public": False,
                            "user": 3,
                        }
                    ]
            }
        )

    def test_list_habit_public(self):
        """ Тесты на список публичных привычек """
        self.client.force_authenticate(user=self.user2)
        Habit.objects.create(
            title='Test1',
            user=self.user1,
            place="test-place",
            time="07:20:00",
            is_pleasant=True,
            frequency=1,
            reward="test-reward",
            duration=25,
            is_public=True,
        )

        response = self.client.get(reverse('habits:habits-public-list'))

        # Проверка на статус ответа
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на верность структуры и полей в списке
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 3,
                            "duration": 25,
                            "related_habit": None,
                            "title": "Test1",
                            "place": "test-place",
                            "time": "07:20:00",
                            "is_pleasant": True,
                            "frequency": 1,
                            "reward": "test-reward",
                            "is_public": True,
                            "user": 1
                        }
                    ]
            }
        )
    def test_detail_habit(self):
        """ Тест на отображение деталей конкретной привычки """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse("habits:habit-detail", args=[1])
        )
        # Проверка на код ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка на содержимое поля title
        self.assertEqual(response.data["title"], "Test-pleasant")

    def test_detail_habit_alien(self):
        """ Тест на отображение деталей конкретной привычки
        посторонним пользователем"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(
            reverse("habits:habit-detail", args=[1])
        )
        # Проверка на код ответа
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_habit(self):
        """ Тесты на обновление данных привычки """
        #self.client.force_authenticate(user=self.user1)

        #response = self.client.post(reverse('habits:habit-update', args=[1]))
        #habit_id = response.data['id']

        # Проверка, что владелец может вносить изменения
        self.client.force_authenticate(user=self.user1)
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[1]),
            data={"title": "Test1"}
        )
        # Проверка на статус ответа
        self.assertEqual(update_habit.status_code, status.HTTP_200_OK)
        # Проверка на верность изменямых полей
        self.assertEqual(
            update_habit.data["title"],
            "Test1"
        )

        # Проверка на невозможность внесения изменений в урок, созданный другим пользователем
        self.client.force_authenticate(user=self.user2)
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[1]),
            data={"title": "Updated title"},
        )
        self.assertEqual(
            update_habit.status_code, status.HTTP_403_FORBIDDEN
        )
