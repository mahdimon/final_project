from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@shared_task
def send_otp_email(email,otp):

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp}.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
    
