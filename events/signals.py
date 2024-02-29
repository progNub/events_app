from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from tasks import send_email

from events.models import Events
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Events)
def send_message_after_create_event(sender, instance: Events, **kwargs):
    users = User.objects.filter(notify=True)

    subject = f'Уведомляем вас, о новом мероприятии: {instance.title}'
    body = f'Мероприятие будет в {str(instance.meeting_time)}\n{instance.description}'
    logger.info(f'количество пользователей подписанных на рассылку:  {len(list(users))}')
    for user in users:
        send_email.delay(subject=subject, body=body, email=user.email)
