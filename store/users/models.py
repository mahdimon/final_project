from core.models import BaseModel
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from .managers import CustomUserManager
from safedelete.models import SOFT_DELETE_CASCADE, SOFT_DELETE, SafeDeleteModel


class CustomUser(SafeDeleteModel, AbstractUser):
    _safedelete_policy = SOFT_DELETE_CASCADE

    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)

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

    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
    )

    objects = CustomUserManager()

    

    def __str__(self):
        return self.email


class Address(BaseModel):
    _safedelete_policy = SOFT_DELETE

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Customer'
    )
    city = models.CharField(max_length=100, verbose_name='City')
    province = models.CharField(max_length=100, verbose_name='Province')
    detailed_address = models.TextField(verbose_name='Detailed Address')
    postal_code = models.CharField(max_length=20, verbose_name='Postal Code')

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['province', 'city']

    def __str__(self):
        return f"{self.city}, {self.province} - {self.customer}"

# Create your models here.
