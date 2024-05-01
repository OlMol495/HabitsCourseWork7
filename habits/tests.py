from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitCreateTestCase(APITestCase):
    """ Тесты на Create, Read, Update привычек """

    def setUp(self):
        self.user1 = User.objects.create(email="test1@admin.pro", password="admin")
        self.user2 = User.objects.create(email="test2@admin.pro", password="admin")
        self.habitpleasant = Habit.objects.create(
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
            is_public=True,
        )

        self.data_ch = {
            "title": "test-title",
            "place": "test-place",
            "time": "20:00:00",
            "is_pleasant": False,
            "frequency": 5,
            "reward": "test-reward",
            "duration": 120,
        }

    def test_create_habit(self):
        """ Тесты на создание привычки """
        self.client.force_authenticate(user=self.user1)
        data = self.data_ch
        data["user"] = self.user1.pk
        print('DEBUG', data)
        response = self.client.post(
            reverse('habits:habit-create'),
            data=data
        )
        print(response.data)

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
                "date": None,
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
        self.assertEqual(response.json()["count"], 2)

    def test_list_habit_public(self):
        """ Тесты на список публичных привычек """
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(reverse('habits:habits-public-list'))

        # Проверка на статус ответа
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка что список сформирован с учетом фильтров
        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(response.data["count"], 1)

    def test_detail_habit(self):
        """ Тест на отображение деталей конкретной привычки """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse("habits:habit-detail", args=[self.habitgood.pk])
        )
        # Проверка на код ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка на содержимое поля title
        self.assertEqual(response.data["title"], "Test-good")

    def test_detail_habit_alien(self):
        """ Тест на отображение деталей конкретной привычки
        постороннему пользователю"""
        self.client.force_authenticate(user=self.user2)
        data = self.data_ch
        data["user"] = self.user1

        response = self.client.get(
            reverse("habits:habit-detail", args=[self.habitgood.pk])
        )
        # Проверка на код ответа
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_habit(self):
        """ Тесты на обновление данных привычки """

        # Проверка, что владелец может вносить изменения
        self.client.force_authenticate(user=self.user1)
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[self.habitgood.id]),
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
            reverse("habits:habit-update", args=[self.habitgood.id]),
            data={"title": "Updated title"}, )
        self.assertEqual(
            update_habit.status_code, status.HTTP_403_FORBIDDEN)


class HabitDeleteTestCase(APITestCase):
    """ Тесты на Delete привычек """

    def setUp(self):
        self.user1 = User.objects.create(email="test1@admin.pro", password="admin")
        self.user2 = User.objects.create(email="test2@admin.pro", password="admin")
        self.habitpleasant = Habit.objects.create(
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
            is_public=True,
        )
        self.data_ch = {
            "title": "test-title",
            "place": "test-place",
            "time": "20:00:00",
            "is_pleasant": False,
            "frequency": 5,
            "reward": "test-reward",
            "duration": 120,
        }

    def test_delete_habits(self):
        # Проверка на невозможность удаления привычки сторонним пользователем
        self.client.force_authenticate(user=self.user2)
        delete_habit = self.client.delete(reverse(
            'habits:habit-delete', args=[self.habitgood.id]))
        self.assertEqual(delete_habit.status_code, status.HTTP_403_FORBIDDEN)

        # Проверка на удаление привычки владельцем
        self.client.force_authenticate(user=self.user1)
        delete_habit = self.client.delete(reverse(
            'habits:habit-delete', args=[self.habitgood.id]))

        # Проверка статуса ответа
        self.assertEquals(
            delete_habit.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Проверка отсутствия удаленной привычки в базе
        get_deleted_habit = self.client.get(reverse(
            "habits:habit-detail", args=[self.habitgood.id]))
        self.assertEqual(
            get_deleted_habit.status_code, status.HTTP_404_NOT_FOUND
        )


class HabitWrongTestCase(APITestCase):
    """Тесты на создание привычек с ошибками и валидаторы"""

    def setUp(self):
        self.user1 = User.objects.create(email="test1@admin.pro", password="admin")
        self.user2 = User.objects.create(email="test2@admin.pro", password="admin")
        self.habitpleasant = Habit.objects.create(
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
            is_public=True,
        )
        self.data_ch = {
            "title": "test-title",
            "place": "test-place",
            "time": "20:00:00",
            "is_pleasant": False,
            "frequency": 5,
            "reward": "test-reward",
            "duration": 120,
        }

    def test_create_false_habit(self):
        """ Тесты на создание привычки с ошибками """
        self.client.force_authenticate(user=self.user1)

        # Проверка на валидатор RelatedAndReward
        data = self.data_ch
        data["related_habit"] = self.habitpleasant
        response = self.client.post(
            reverse('habits:habit-create'),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор related_and_pleasant
        data = self.data_ch
        data["is_pleasant"] = True
        response = self.client.post(
            reverse('habits:habit-create'),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор PleasantRewardRelated
        data = self.data_ch
        data["related_habit"] = ""
        response = self.client.post(
            reverse('habits:habit-create'),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор DurationValidator
        data = self.data_ch
        data["is_pleasant"] = False
        data["duration"] = 150
        response = self.client.post(
            reverse('habits:habit-create'),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор FrequencyValidator
        data = self.data_ch
        data["frequency"] = 10
        response = self.client.post(
            reverse('habits:habit-create'),
            data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_false_habit(self):
        """ Тесты на изменение привычки с ошибками """
        self.client.force_authenticate(user=self.user1)

        # Проверка на валидатор RelatedAndReward
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[self.habitgood.id]),
            data={"related_habit": self.habitgood.id}
        )
        self.assertEqual(
            update_habit.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор related_and_pleasant
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[self.habitgood.id]),
            data={
                "related_habit": self.habitgood.id,
                "is_pleasant": True,
                "reward": ""})
        self.assertEqual(
            update_habit.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор PleasantRewardRelated
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[self.habitgood.id]),
            data={"related_habit": self.habitgood.id, "is_pleasant": True})
        self.assertEqual(
            update_habit.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор DurationValidator
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[self.habitgood.id]),
            data={"duration": 150})
        self.assertEqual(
            update_habit.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка на валидатор FrequencyValidator
        update_habit = self.client.patch(
            reverse("habits:habit-update", args=[self.habitgood.id]),
            data={"frequency": 10})
        self.assertEqual(
            update_habit.status_code, status.HTTP_400_BAD_REQUEST)
