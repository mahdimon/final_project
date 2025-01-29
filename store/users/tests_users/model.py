from django.test import TestCase
from users.models import CustomUser, Address


class CustomUserModelTests(TestCase):
    def test_create_user_with_valid_data(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            phone_number="1234567890",
            email="user@example.com",
            password="securepassword123",
            role=CustomUser.CUSTOMER,
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.role, CustomUser.CUSTOMER)
        self.assertTrue(user.check_password("securepassword123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_for_non_customer_role(self):
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(
                username="testuser",
                phone_number="1234567890",
                email=None,
                password="securepassword123",
                role=CustomUser.SUPERVISOR,
            )
        self.assertEqual(str(context.exception), "The Email field must be set")

    def test_create_user_without_phone_number(self):
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(
                username="testuser",
                phone_number=None,
                email="user@example.com",
                password="securepassword123",
                role=CustomUser.CUSTOMER,
            )
        self.assertEqual(str(context.exception), "The Phone Number field must be set")

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            phone_number="1234567890",
            password="adminpassword123",
        )
        self.assertEqual(superuser.username, "admin")
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertEqual(superuser.phone_number, "1234567890")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_staff_or_superuser_flag(self):
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                phone_number="1234567890",
                password="adminpassword123",
                is_staff=False,
            )
        self.assertEqual(str(context.exception), "Superuser must have is_staff=True.")

        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                phone_number="1234567890",
                password="adminpassword123",
                is_superuser=False,
            )
        self.assertEqual(str(context.exception), "Superuser must have is_superuser=True.")

    def test_string_representation(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            phone_number="1234567890",
            email="user@example.com",
            password="securepassword123",
            role=CustomUser.CUSTOMER,
        )
        self.assertEqual(str(user), "user@example.com")


class AddressModelTests(TestCase):
    def test_create_address(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            phone_number="1234567890",
            email="user@example.com",
            password="securepassword123",
            role=CustomUser.CUSTOMER,
        )
        address = Address.objects.create(
            customer=user,
            city="Tehran",
            province="Tehran Province",
            detailed_address="123 Example Street",
            postal_code="1234567890",
        )
        self.assertEqual(address.customer, user)
        self.assertEqual(address.city, "Tehran")
        self.assertEqual(address.province, "Tehran Province")
        self.assertEqual(address.detailed_address, "123 Example Street")
        self.assertEqual(address.postal_code, "1234567890")

    def test_string_representation(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            phone_number="1234567890",
            email="user@example.com",
            password="securepassword123",
            role=CustomUser.CUSTOMER,
        )
        address = Address.objects.create(
            customer=user,
            city="Tehran",
            province="Tehran Province",
            detailed_address="123 Example Street",
            postal_code="1234567890",
        )
        self.assertEqual(str(address), "Tehran, Tehran Province")

    def test_address_ordering(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            phone_number="1234567890",
            email="user@example.com",
            password="securepassword123",
            role=CustomUser.CUSTOMER,
        )
        Address.objects.create(
            customer=user,
            city="CityB",
            province="ProvinceA",
            detailed_address="AddressB",
            postal_code="22222",
        )
        Address.objects.create(
            customer=user,
            city="CityA",
            province="ProvinceA",
            detailed_address="AddressA",
            postal_code="11111",
        )
        addresses = Address.objects.all()
        self.assertEqual(list(addresses.values_list("city", flat=True)), ["CityA", "CityB"])
