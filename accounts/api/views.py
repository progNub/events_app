from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser, Http404
from rest_framework.permissions import SAFE_METHODS

from accounts.api.serializers import UserListSerializer, UserCreateSerializer
from accounts.models import User


class ListUserApiView(ListCreateAPIView):
    queryset = User.objects.all()  # как и где брать объекты
    lookup_field = 'id'

    # permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        elif self.request.user.is_superuser:
            return UserListSerializer
        else:
            raise PermissionDenied("У вас нет доступа")

    def perform_create(self, serializer):
        data = serializer.validated_data
        password = make_password(data.get('password'))
        serializer.save(password=password)
