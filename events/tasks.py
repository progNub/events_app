from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from accounts.models import User
from events.email import BaseEmailSender
from events.models import Events

import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email(subject, body, email):
    """Отправка сообщения на почту"""
    BaseEmailSender(subject=subject, body=body, email=email).send_mail()
    return f'{subject}\n{body}\n{email}'


@shared_task
def send_reminder_email():
    six_hours_later = timezone.now() + timedelta(hours=6)
    one_day_later = timezone.now() + timedelta(hours=24)

    events_to_remind = (Events.objects.filter(meeting_time__in=[six_hours_later, one_day_later])
                        .prefetch_related('users__email'))
    logger.info(f'количество новостей за день или 6 часов =  {str(events_to_remind.count())}')

    for event in events_to_remind:

        users_emails = event.users.values_list('email', flat=True)
        subject = f'Уведомляем вас, что вы согласились посетить {event.title}'
        body = f'Мероприятие будет в {str(event.meeting_time)}\n{event.description}'
        logger.info(f"Количество пользователей: {len(list(users_emails))}")

        for email in users_emails:
            send_email.delay(subject=subject, body=body, email=email)
    return f'количество пользователей: {len(list(events_to_remind))}'
