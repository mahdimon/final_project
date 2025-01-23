from django.contrib import admin
from .models import Order, OrderProduct, Coupon

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Coupon)

# Register your models here.
