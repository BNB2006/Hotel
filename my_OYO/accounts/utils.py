import uuid
from django.core.mail import send_mail
from django.conf import settings


def generateRandomToken():
    return str(uuid.uuid4())


def sendEmailToken(email , token):
    subject = "Verify Your Email Address"
    message = f''' please click the link below to verify your email address:

    http://127.0.0.1:8000/accounts/register/{token}

    If you did not request this, please ignore this email.
    Thank you!
    '''
    send_mail(
       subject,
       message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )