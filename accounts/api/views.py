from django.contrib.auth.hashers import make_password

from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework.generics import ListCreateAPIView

from accounts.api.serializers import UserListSerializer, UserCreateSerializer
from accounts.models import User


class ListUserApiView(ListCreateAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        elif self.request.method == 'GET':
            if self.request.user.is_superuser:
                return UserListSerializer
            raise PermissionDenied("Нет доступа")
        else:
            raise MethodNotAllowed(f"Метод {self.request.method} не поддерживается")

    def perform_create(self, serializer):
        data = serializer.validated_data
        password = make_password(data.get('password'))
        serializer.save(password=password)
