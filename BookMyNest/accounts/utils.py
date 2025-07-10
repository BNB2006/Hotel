import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Hotel
from django.urls import reverse

def generateRandomToken():
    return str(uuid.uuid4())




def sendEmailToken(request, email, token, user):
    subject = "Verify Your Email Address"
    if user == "user":
        relative_link = reverse('verify_email_token', args=[token]) 
    else:
        relative_link = reverse('verify_email_token_vendor', args=[token]) 

    absolute_link = request.build_absolute_uri(relative_link)
    message = f"Hi,Welcome to BookMyNest please verify your email account by clicking this link:\n\n{absolute_link}\n"
    send_mail(
       subject,
       message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def sendOTPtoEmail(email , otp):
    subject = "OTP for Account Login BookMyNest"
    message = f"""Hi use this otp for login \n\n{otp}\n\n\n\nThank you."""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def generateSlug(hotel_name):
    slug = f"{slugify(hotel_name)}-"+str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug = slug).exists():
        return generateSlug(hotel_name)
    return slug