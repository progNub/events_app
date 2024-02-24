import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from events.api import serializers as ser
from events.models import Events


class ListEventsApiView(ListAPIView):
    serializer_class = ser.EventsListSerializer
    permission_classes = [AllowAny]
    queryset = Events.objects.filter(meeting_time__gt=timezone.now()).select_related('category')


class UpdateEventApiView(UpdateAPIView):
    serializer_class = ser.SubscribeEventSerializer
    queryset = Events.objects.all()
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        instance: Events = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        subscriber = instance.users.filter(id=request.user.id)
        if serializer.is_valid():
            if subscriber:
                instance.users.remove(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                instance.users.add(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
