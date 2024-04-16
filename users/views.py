from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ Вывод данных по юзерам с кастомизированной вьюшкой на детали юзера """
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Дефолтный сериалайзер
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['email', 'telegram_id']
    ordering_fields = ['role', 'is_active']
