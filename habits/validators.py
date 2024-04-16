from rest_framework.serializers import ValidationError


class RelatedAndRewardValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)
        reward = dict(value).get(self.field2)

        if related_habit and reward:
            raise ValidationError(
                'Нельзя использовать одновременно '
                'связанную привычку и вознаграждение')


# class RelatedHabitPleasantValidator:
#
#     def __init__(self, field1):
#         self.field1 = field1
#
#     def __call__(self, value):
#         related_habit = dict(value).get(self.field1)
#
#         if related_habit and not related_habit.is_pleasant:
#             raise ValidationError('Связанная привычка должна иметь признак приятной')


class PleasantRewardRelatedValidator:

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        is_pleasant = dict(value).get(self.field1)
        related_habit = dict(value).get(self.field2)
        reward = dict(value).get(self.field3)

        if is_pleasant:
            if reward or related_habit:
                raise ValidationError(
                    'Приятная привычка не должна сочетаться с вознаграждением'
                    'и иметь связанную привычку')


class DurationValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = dict(value).get(self.field)

        if duration > 120:
            raise ValidationError(
                'Выполнение привычки не может превышать 120 секунд'
            )


class FrequencyValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        frequency = dict(value).get(self.field)

        if frequency > 7:
            raise ValidationError(
                'Привычку надо повторять минимум один раз в семь дней'
            )


# def related_and_pleasant(value):
#     related_habit = value["related_habit"]
#     if related_habit and not related_habit.is_pleasant:
#         raise ValidationError(
#             "Связанная привычка должна иметь признак приятной"
#         )
