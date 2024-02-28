from django.core.mail import EmailMultiAlternatives


class BaseEmailSender:

    def __init__(self, subject, body, email):
        self._subject = subject
        self._body = body
        self._email = email

    def send_mail(self):
        mail = EmailMultiAlternatives(
            subject=self._subject,
            body=self._body,
            to=[self._email]
        )
        mail.send()
