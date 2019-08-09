from datetime import datetime, timedelta, time

from django.core.mail import send_mail
from jinja2 import Template


def send_plain_email(subject, message, to, from_email='hello@breakwire.me'):
    send_mail(subject, message, from_email, [to])


def send_html_email(subject,
                    message,
                    html_message,
                    to,
                    from_email='hello@breakwire.me'):
    send_mail(subject, message, from_email, [to], html_message=html_message)


def read_email_template(path):
    with open(path, 'r') as f:
        template = Template(f.read())
        return template


def get_today_start_end():
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    return today_start, today_end


def get_user_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip
