from faker import Faker

from events.models import Events

fake = Faker('ru-RU')


class TestDataEvents:
    @staticmethod
    def get_future_events(limit) -> list:
        events = []
        for _ in range(limit):
            dict_event = {
                'title': fake.unique.word(),
                'description': fake.text(),
                'meeting_time': fake.date_time_this_century(after_now=True),
            }
            event = Events(**dict_event)
            events.append(event)
            events.sort(key=lambda elem: elem.meeting_time)

        return events

    @staticmethod
    def get_past_events(limit) -> list:
        events = []
        for _ in range(limit):

            dict_event = {
                'title': fake.unique.word(),
                'description': fake.text(),
                'meeting_time': fake.date_time_this_century(before_now=True),
            }
            event = Events(**dict_event)
            events.append(event)
            events.sort(key=lambda elem: elem.meeting_time)

        return events

    @staticmethod
    def get_list_events(lim_past=3, lim_future=3):
        list_past_events = TestDataEvents.get_past_events(lim_past)
        list_future_events = TestDataEvents.get_future_events(lim_future)
        return list_past_events + list_future_events


