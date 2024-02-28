from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from accounts.models import User
from events.email import BaseEmailSender
from events.models import Events


@shared_task(ignore_result=True)
def send_email(subject, body, email) -> None:
    """Отправка сообщения на почту"""
    BaseEmailSender(subject=subject, body=body, email=email).send_mail()


@shared_task(ignore_result=True)
def send_reminder_email() -> None:
    six_hours_later = timezone.now() + timedelta(hours=6)
    one_day_later = timezone.now() + timedelta(hours=24)

    events_to_remind = (Events.objects.filter(meeting_time__in=[six_hours_later, one_day_later])
                        .prefetch_related('users__email'))

    for event in events_to_remind:
        users_emails = event.users.values_list('email', flat=True)
        subject = f'Уведомляем вас, что вы согласились посетить {event.title}'
        body = f'Мероприятие будет в {str(event.meeting_time)}\n{event.description}'

        for email in users_emails:
            send_email.delay(subject=subject, body=body, email=email)
