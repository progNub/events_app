from collections import OrderedDict
import random

from django.utils import timezone
from rest_framework.reverse import reverse

from tests.BaseTests import CustomAPITestCase
from .fakeData import TestDataEvents as testEvents
from accounts.models import User
from events.models import Events
from events.api.urls import app_name


class BaseTestEvents(CustomAPITestCase):
    future_event: Events = None
    past_event: Events = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        future_event = {
            'title': 'TestFutureEvent',
            'description': 'DescriptionTestFutureEvent',
            'meeting_time': f'{timezone.now() + timezone.timedelta(hours=10)}',
        }
        past_event = {
            'title': 'TestPastEvent',
            'description': 'DescriptionTestPastEvent',
            'meeting_time': f'{timezone.now() - timezone.timedelta(hours=10)}',
        }
        cls.future_event = Events.objects.create(**future_event)
        cls.past_event = Events.objects.create(**past_event)
        # заполняем тестовыми событиями бд
        Events.objects.bulk_create(testEvents.get_list_events())


class TestUpdateEventApiView(BaseTestEvents):

    def test_user_subscribe_and_unsubscribe_to_future_event(self):
        """Тестирование подписки на событие и отписки"""
        self.client.force_login(self.user)
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.future_event.id}))
        self.assertTrue(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(200, response.status_code)
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.future_event.id}))
        self.assertFalse(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(200, response.status_code)

    def test_user_subscribe_to_past_event(self):
        """Тестирование подписки на прошедшее событие авторизованным пользователем"""
        self.client.force_login(self.user)
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.past_event.id}))
        self.assertFalse(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(404, response.status_code)

    def test_anonym_subscribe_and_unsubscribe_to_event(self):
        """Тестирование подписки на прошедшее событие анонимным пользователем"""
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.future_event.id}))
        self.assertFalse(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(401, response.status_code)

    def test_user_subscribe_and_unsubscribe_to_non_existent_event(self):
        """Тестирование подписки на несуществующее событие авторизованным пользователем"""
        self.client.force_login(self.user)
        count = Events.objects.count()
        id_non_existent_event = count + 1
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': id_non_existent_event}))
        self.assertEqual(404, response.status_code)


class TestListEventsApiView(BaseTestEvents):

    def test_get_list_future_events(self):
        """"Получаем список только тех событий, которым ещё предстоит произойти"""
        response = self.client.get(reverse(f'{app_name}:api-list-events'))
        # получаем первый объект Events, так как стоит сортировка по возрастанию даты мы получим самый "старый" объект
        event: OrderedDict = response.data[0]
        # из строки получаем об]ект datatime для сравнения
        datatime_first_event = timezone.datetime.fromisoformat(event.get('meeting_time'))
        self.assertGreater(datatime_first_event, timezone.now())
        self.assertEqual(200, response.status_code)


class TestMyListEventsApiView(BaseTestEvents):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        list_users = User.objects.all()
        list_events = Events.objects.all()
        for event in list_events:
            num_users_to_add = random.randint(1, 5)
            random_users = random.sample(list(list_users), num_users_to_add)
            event.users.add(*random_users)

    def test_get_my_list_events_user(self):
        """Проверка на то что получены события на которые я был подписан"""
        self.client.force_login(self.user)
        response = self.client.get(reverse(f'{app_name}:api-list-my-events'))
        count_users_events = Events.objects.filter(users__id=self.user.id).count()
        self.assertEqual(count_users_events, len(response.data))
        self.assertEqual(200, response.status_code)

    def test_get_my_list_events_anonym(self):
        """проверка на получение событий анонимным пользователем"""
        response = self.client.get(reverse(f'{app_name}:api-list-my-events'))
        self.assertEqual(401, response.status_code)
