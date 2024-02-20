from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from accounts.api.serializers import UserListSerializer
from accounts.models import User


class ListUserApiView(ListAPIView):
    queryset = User.objects.all()  # как и где брать объекты
    serializer_class = UserListSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
