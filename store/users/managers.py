from safedelete.managers import SafeDeleteManager
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from safedelete.managers import SafeDeleteManager
from django.contrib.auth.models import BaseUserManager
from .models import CustomUser as CU


CustomUser:CU = get_user_model()

class CustomUserManager(SafeDeleteManager, BaseUserManager):
    def create_user(self, email, phone_number, password=None, role=None, **extra_fields):
        if role and role not in (x[0] for x in CustomUser.ROLE_CHOICES):
            raise ValueError("role must be valid or None")
        
        if not email and role != CustomUser.CUSTOMER:
            raise ValueError("The Email field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        if role != CustomUser.CUSTOMER:
            extra_fields.setdefault("is_staff", True)

            if extra_fields.get("is_staff") is not True:
                raise ValueError(" must have is_staff=True.")


        user = super().create_user(email=email, password=password, **extra_fields)
        user.phone_number = phone_number
        user.role = role
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, phone_number=phone_number, password=password, role=CustomUser.SUPERVISOR, **extra_fields)
