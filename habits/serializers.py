from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.relations import SlugRelatedField

from habits.models import Habit
from habits.validators import (RelatedAndRewardValidator,
                               PleasantRewardRelatedValidator, DurationValidator,
                               FrequencyValidator, related_and_pleasant)


class HabitSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Habit """
    duration = IntegerField()
    related_habit = SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedAndRewardValidator(field1='related_habit',
                                      field2='reward'),
            PleasantRewardRelatedValidator(field1='is_pleasant',
                                           field2='related_habit',
                                           field3='reward'),
            DurationValidator(field='duration'),
            FrequencyValidator(field='frequency'),
            related_and_pleasant
        ]


class HabitCreateSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Habit """
    duration = IntegerField()

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedAndRewardValidator(field1='related_habit',
                                      field2='reward'),
            PleasantRewardRelatedValidator(field1='is_pleasant',
                                           field2='related_habit',
                                           field3='reward'),
            DurationValidator(field='duration'),
            FrequencyValidator(field='frequency'),
            related_and_pleasant
        ]
