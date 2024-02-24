from rest_framework import serializers
from django.utils import timezone

from accounts.models import User
from events.models import Events, Category


class CategoryField(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

    def to_representation(self, value):
        """Что бы категория выводилась без ключа 'title'"""
        return value.title


class UsersField(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, value):
        """Что бы категория выводилась без ключа 'title'"""
        return value.username


class EventsListSerializer(serializers.ModelSerializer):
    category = CategoryField()
    users = UsersField(many=True, read_only=True)

    class Meta:
        model = Events
        fields = ['id', 'title', 'description', 'meeting_time', 'category', 'users']
        read_only_fields = ['id', 'title', 'description', 'meeting_time', 'category', 'users']


class SubscribeEventSerializer(serializers.ModelSerializer):
    users = UsersField(many=True, read_only=True)

    class Meta:
        model = Events
        fields = ['id', 'title', 'description', 'meeting_time', 'category', 'users']
        read_only_fields = ['id', 'title', 'description', 'meeting_time', 'category', 'users']

    def validate(self, data):
        if self.instance.meeting_time < timezone.now():
            raise serializers.ValidationError("Мероприятие уже прошло.")
        return data
