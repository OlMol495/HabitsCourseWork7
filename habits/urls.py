from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView,
                          HabitDestroyAPIView, HabitsOwnListAPIView, HabitsPublicListAPIView)

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits_own/', HabitsOwnListAPIView.as_view(), name='habits-own-list'),
    path('habits/', HabitsPublicListAPIView.as_view(), name='habits-public-list'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-detail'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habit/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit-delete'),
]
