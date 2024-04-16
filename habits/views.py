from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.paginators import ListPaginator
from habits.permissions import IsModerator, IsOwner

from habits.models import Habit
from habits.serializers import HabitSerializer, HabitCreateSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Вьюшка на созданиеание привычки"""
    serializer_class = HabitCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]  # доступ имеют авторизованные пользователи, но не модер

    def perform_create(self, serializer):
        """Привязывает юзера к создаваемой им привычке"""
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class HabitsOwnListAPIView(generics.ListAPIView):
    """вьюшка на просмотр списка привычек конкретного юзера"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]  # Доступ имеет владелец
    pagination_class = ListPaginator


class HabitsPublicListAPIView(generics.ListAPIView):
    """Вьюшка на просмотр списка публичных привычек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_pleasant=False, is_public=True)
    permission_classes = [IsAuthenticated]  # Доступ имеют авторизованные юзеры
    pagination_class = ListPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Вьюшка на просмотр конкретной привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]  # Доступ имеют владельцы и модератор


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Вьюшка на редактирование урока"""
    serializer_class = HabitCreateSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]  # Доступ имеют владельцы и модератор


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Вьюшка на удаление привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]  # Доступ имеют владельцы и модератор