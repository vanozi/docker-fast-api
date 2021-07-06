from email.message import EmailMessage
from smtplib import SMTP

from app.core import config


class Mailer:
    @staticmethod
    def send_message(content: str, subject: str, mail_to: str):
        message = EmailMessage()
        message.set_content(content)
        message['Subject'] = subject
        message['From'] = config.MAIL_SENDER
        message['To'] = mail_to
        mailer = SMTP(host=config.SMTP_HOST, port=config.SMTP_PORT)
        mailer.send_message(message)

    @staticmethod
    def send_confirmation_message(token: str, mail_to: str):
        confirmation_url = f'{config.BASE_URL_FRONTEND}{config.API_PREFIX}/auth/activate_email/{token}'
        message = '''Hi!
    Please confirm your registration: {}.'''.format(confirmation_url)
        Mailer.send_message(
            message,
            'Please confirm your registration',
            mail_to
        )

    @staticmethod
    def send_password_reset_message(token: str, mail_to: str):
        reset_password_url = f'{config.BASE_URL_FRONTEND}{config.API_PREFIX}/auth/reset_password/{token}'
        message = '''Hi!
    Click on the link to reset your password: {}.'''.format(reset_password_url)
        Mailer.send_message(
            message,
            'Please reset your password',
            mail_to
        )
