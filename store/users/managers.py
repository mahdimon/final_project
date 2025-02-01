from safedelete.managers import SafeDeleteManager
from django.contrib.auth.models import BaseUserManager

from safedelete.managers import SafeDeleteManager
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group


SUPERVISOR = 's'
PRODUCT_MANAGER = 'p'
OPERATOR = 'o'
CUSTOMER = 'c'
ROLE_CHOICES = [
    (SUPERVISOR, 'Supervisor'),
    (PRODUCT_MANAGER, 'Product Manager'),
    (OPERATOR, 'Operator'),
    (CUSTOMER, 'Customer'),
]


class CustomUserManager(SafeDeleteManager, BaseUserManager):
    def create_user(self, phone_number, email=None,  password=None, role=CUSTOMER, **extra_fields):
        if role not in (x[0] for x in ROLE_CHOICES):
            raise ValueError("role must be valid or None")

        if not email and role != CUSTOMER:
            raise ValueError("The Email field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        if role != CUSTOMER:
            extra_fields.setdefault("is_staff", True)

            if extra_fields.get("is_staff") is not True:
                raise ValueError(" must have is_staff=True.")

        extra_fields.setdefault("is_active", True)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.phone_number = phone_number
        user.role = role
        user.save(using=self._db)
        role_to_group = {
            SUPERVISOR: "supervisor",
            PRODUCT_MANAGER: "manager",
            OPERATOR: "operator",
        }

        group_name = role_to_group.get(role)
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, phone_number=phone_number, password=password, role=SUPERVISOR, **extra_fields)
