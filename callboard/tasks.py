import smtplib
from email.message import EmailMessage

from celery import shared_task
from django.conf import settings


@shared_task
def send_user_email(receiver_email):
    email_message = get_simple_formatted_email(
        subject='Feedback',
        receiver_email=receiver_email,
        text=(f'Регистрация прошла успешно!<br><br>'
              f'Данные для авторизации<br>'
              f'Логин: <strong>{receiver_email}</strong><br>'
              f'Ссылка на сервис <a href="</a>')
    )
    send_email(email_message)


def get_simple_formatted_email(subject: str, text: str, receiver_email: str):
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = settings.EMAIL_HOST_USER
    email["To"] = receiver_email

    email.set_content(text, subtype="html")
    return email


def send_email(email: EmailMessage):
    with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=20) as server:
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(email)

