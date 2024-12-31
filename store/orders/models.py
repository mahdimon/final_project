from django.db import models
from core.models import BaseModel
from safedelete.models import SOFT_DELETE, HARD_DELETE, SOFT_DELETE_CASCADE
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Coupon(BaseModel):
    _safedelete_policy = SOFT_DELETE
    PERCENTAGE = 'p'
    FIXED = 'f'

    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed'),
    ]

    discount_type = models.CharField( max_length=1, choices=DISCOUNT_TYPE_CHOICES, blank=False, null=False, verbose_name="Discount Type" )
    code = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    max_discount = models.DecimalField( max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Maximum Discount" )
    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ['valid_from']

    def __str__(self):
        return self.code


class Order(BaseModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    STATUS_CHOICES = [
        ('P', 'Processing'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders' )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    products = models.ManyToManyField(Product,through='OrderProduct',related_name='orders')

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderProduct(BaseModel):
    _safedelete_policy = SOFT_DELETE
    PERCENTAGE = 'p'
    FIXED = 'f'

    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='order_products')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=1,choices=DISCOUNT_TYPE_CHOICES,blank=True,null=True,verbose_name="Discount Type" )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    prediscount_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"
        unique_together = ('order', 'product')  

    def __str__(self):
        return f"{self.product.name} in Order #{self.order.id}"

