from django.core.mail import EmailMultiAlternatives


class BaseEmailSender:

    def __init__(self, subject, body, email):
        self._subject = subject
        self._body = body
        self._email = email

    def send_mail(self):
        try:
            mail = EmailMultiAlternatives(
                subject=self._subject,
                body=self._body,
                to=[self._email]
            )
            # Отправка письма
            mail.send()
            return True  # Успешно отправлено
        except Exception as e:
            # Обработка ошибок при отправке письма
            print(f"Failed to send email: {e}")
            return False  # Ошибка при отправке

