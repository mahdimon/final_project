from django.test import TestCase
from django.contrib.auth import get_user_model
from orders.models import Coupon, Order, OrderProduct
from products.models import Product
from datetime import datetime, timedelta
from django.utils.timezone import now

User = get_user_model()


class SafeDeleteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number = "09367776666",username="testuser", password="password123")
        self.product = Product.objects.create(name="Laptop", price=1000.00)
        self.coupon = Coupon.objects.create(
            discount_type=Coupon.PERCENTAGE,
            code="DISCOUNT10",
            value=10.00,
            valid_from=now(),
            valid_to=now() + timedelta(days=10),
            max_discount=50.00
        )
        self.order = Order.objects.create(user=self.user, total_price=1000.00, coupon=self.coupon)
        self.order_product = OrderProduct.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=950.00,
            discount_type=OrderProduct.PERCENTAGE,
            discount_value=50.00,
            prediscount_price=1000.00
        )

    def test_soft_delete_coupon(self):
        self.coupon.delete()
        
        self.assertFalse(Coupon.objects.filter(id=self.coupon.id).exists())
       
        self.assertTrue(Coupon.all_objects.filter(id=self.coupon.id).exists())

    def test_soft_delete_order(self):
        self.order.delete()
   
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())
   
        self.assertTrue(Order.all_objects.filter(id=self.order.id).exists())

    def test_soft_delete_cascade_order(self):
        self.order.delete()
   
        self.assertFalse(OrderProduct.objects.filter(order=self.order).exists())
        self.assertTrue(OrderProduct.all_objects.filter(order=self.order).exists())

    def test_restore_soft_deleted_coupon(self):
        self.coupon.delete()
  
        self.coupon.undelete()

        self.assertTrue(Coupon.objects.filter(id=self.coupon.id).exists())


    def test_soft_delete_order_product(self):
        self.order_product.delete()

        self.assertFalse(OrderProduct.objects.filter(id=self.order_product.id).exists())

        self.assertTrue(OrderProduct.all_objects.filter(id=self.order_product.id).exists())

    def test_restore_soft_deleted_order_product(self):
        self.order_product.delete()

        self.order_product.undelete()

        self.assertTrue(OrderProduct.objects.filter(id=self.order_product.id).exists())
