from collections import OrderedDict

from django.utils import timezone

from rest_framework.reverse import reverse

from tests.BaseTests import CustomAPITestCase
from .testFaker import TestDataEvents as test_data
from accounts.models import User
from events.models import Events
from events.api.urls import app_name


class BaseTestEvents(CustomAPITestCase):
    future_event: Events = None
    past_event: Events = None

    @classmethod
    def setUpTestData(cls):
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
        Events.objects.bulk_create(test_data.get_list_events())
        super().setUpTestData()


class TestUpdateEventApiView(BaseTestEvents):

    def test_user_subscribe_and_unsubscribe_to_future_event(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.future_event.id}))
        self.assertTrue(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(200, response.status_code)
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.future_event.id}))
        self.assertFalse(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(200, response.status_code)

    def test_user_subscribe_and_unsubscribe_to_past_event(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.past_event.id}))
        self.assertFalse(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(404, response.status_code)

    def test_anonym_subscribe_and_unsubscribe_to_event(self):
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': self.future_event.id}))
        self.assertFalse(User.objects.filter(events__users__id=self.user.id).exists())
        self.assertEqual(401, response.status_code)

    def test_user_subscribe_and_unsubscribe_to_non_existent_event(self):
        self.client.force_login(self.user)
        count = Events.objects.count()
        id_non_existent_event = count + 1
        response = self.client.post(reverse(f'{app_name}:api-subscribe-event', kwargs={'id': id_non_existent_event}))
        self.assertEqual(404, response.status_code)


class TestListEventsApiView(BaseTestEvents):

    def test_get_list_future_events(self):
        response = self.client.get(reverse('events:api-list-events'))
        # получаем первый объект Events, так как стоит сортировка по возрастанию даты мы получим самый "старый" объект
        event: OrderedDict = response.data[0]
        # из строки получаем об]ект datatime для сравнения
        datatime_first_event = timezone.datetime.fromisoformat(event.get('meeting_time'))
        self.assertGreater(datatime_first_event, timezone.now())
        self.assertEqual(200, response.status_code)