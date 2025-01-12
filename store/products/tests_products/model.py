from django.test import TestCase
from products.models import Discount, Product, Category
from safedelete.models import HARD_DELETE, SOFT_DELETE, SOFT_DELETE_CASCADE
from django.utils.timezone import now

class ProductModelTestCase(TestCase):
    def setUp(self):
   
        self.parent_category = Category.objects.create(name="Electronics")
        self.sub_category = Category.objects.create(name="Laptops", parent=self.parent_category)

       
        self.discount = Discount.objects.create(
            discount_type=Discount.PERCENTAGE,
            value=10.00,
            max_discount=50.00
        )

       
        self.product = Product.objects.create(
            name="Gaming Laptop",
            brand="BrandX",
            description="A powerful gaming laptop",
            stock=5,
            price=1500.00,
            category=self.sub_category,
            discount=self.discount
        )

    def test_create_discount(self):
        discount = Discount.objects.create(
            discount_type=Discount.FIXED,
            value=100.00,
            max_discount=None
        )
        self.assertEqual(discount.discount_type, Discount.FIXED)
        self.assertEqual(discount.value, 100.00)

    def test_create_category(self):
        category = Category.objects.create(name="Smartphones")
        self.assertEqual(category.name, "Smartphones")
        self.assertIsNone(category.parent)

    def test_create_product(self):
        self.assertEqual(self.product.name, "Gaming Laptop")
        self.assertEqual(self.product.category.name, "Laptops")
        self.assertEqual(self.product.discount.value, 10.00)

    def test_soft_delete_category(self):
        self.sub_category.delete()
        self.assertFalse(Category.objects.filter(id=self.sub_category.id).exists())
        self.assertTrue(Category.all_objects.filter(id=self.sub_category.id).exists())

    def test_soft_delete_product(self):
        self.product.delete()
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
        self.assertTrue(Product.all_objects.filter(id=self.product.id).exists())

    def test_cascade_delete_category(self):
        self.parent_category.delete()
        self.assertFalse(Category.objects.filter(id=self.sub_category.id).exists())
        self.assertTrue(Category.all_objects.filter(id=self.sub_category.id).exists())


    def test_update_product(self):
        self.product.name = "Updated Laptop"
        self.product.save()
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, "Updated Laptop")

    def test_related_products_in_category(self):
        products_in_category = self.sub_category.products.all()
        self.assertIn(self.product, products_in_category)

    def test_discount_display(self):
        self.assertEqual(str(self.discount), "Percentage - 10.0")

    def test_category_str(self):
        self.assertEqual(str(self.parent_category), "Electronics")
        self.assertEqual(str(self.sub_category), "Laptops")
