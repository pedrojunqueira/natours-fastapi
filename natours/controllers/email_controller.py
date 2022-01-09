import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from natours.config import settings
from natours.controllers.email_template import render_email_html


EMAIL_USER_NAME = settings.MAIL_USERNAME
EMAIL_SENDER = settings.MAIL_FROM
EMAIL_PASSWORD = settings.MAIL_PASSWORD
EMAIL_SERVER = settings.MAIL_SERVER
EMAIL_PORT = settings.MAIL_PORT

if settings.FASTAPI_ENV == "production":
    EMAIL_USER_NAME = settings.GMAIL_USERNAME
    EMAIL_SENDER = settings.GMAIL_USERNAME
    EMAIL_PASSWORD = settings.GMAIL_PASSWORD
    EMAIL_SERVER = settings.GMAIL_SERVER
    EMAIL_PORT = settings.GMAIL_PORT


def render_email_message(reset_url):

    html = f"""
    <p> reset your password visiting this url: {reset_url} </p> 
    """

    return html


def render_email_message_reset_password(*args, **kwargs):

    body_template = f"""
                                <p> Hi {kwargs.get("email") or kwargs.get("name")} ,</p>
                                <p>
                                    reset your password visiting this url: { kwargs.get("reset_url") }
                                </p>
                                <p>
                                    If you need any help with booking your next
                                    tour, please don't hesitate to contact me!
                                </p>
                                <p>- Pedro Junqueira, CEO</p>
    """

    return body_template


def render_email_message_confirm_password_reset(*args, **kwargs):

    body_template = f"""
                    <p> password for email: {kwargs.get("email")} was successfully changed </p> 
    """

    return body_template


def prepare_email_message(subject, email_to, body_template):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = email_to

    body = body_template

    # Create the plain-text and HTML version of your message
    text = f"""
    {body}
    """
    html = render_email_html(body_template=body)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    return message


def send_email_sync(email, message):
    username = EMAIL_USER_NAME
    sender_email = EMAIL_SENDER
    receiver_email = email
    password = EMAIL_PASSWORD

    if settings.FASTAPI_ENV == "production":
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return

    with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
