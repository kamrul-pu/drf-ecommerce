"""
Tests for model
"""
from unittest.mock import patch

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and returns a new user."""
    return get_user_model().objects.create_user(email, password)


def create_category():
    """Create and returns a category."""
    return models.Category.objects.create(
        name='Electronic',
    )


class ModelTests(TestCase):
    """Test models."""

    def test_craete_user_successfull(self):
        """Test creating a user with email is successfull."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email(self):
        """Test email is normalized for new users."""
        smaple_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in smaple_emails:
            user = get_user_model().objects.create_user(email, 'samplepass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass')

    def test_create_super_user(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_category_success(self):
        """Test Crating a category."""
        category = models.Category.objects.create(
            name='Electronic',
        )

        self.assertTrue(str(category), category.name)

    def test_create_product_success(self):
        """Test creating Product is successfull."""
        category = create_category()
        product = models.Product.objects.create(
            name='Hp Elitebook 840 G1',
            price=Decimal('500.50'),
            category=category,
            description='Intel core i5 4th gen, 8gb Ram.'
        )

        self.assertEqual(str(product), product.name)
        self.assertEqual(category.id, product.category.id)

    def test_create_customer_success(self):
        """Test Creating Customer Success."""
        user = create_user()
        customer = models.Customer.objects.create(
            user=user, name='Kamrul', phone_number='123456789')

        self.assertEqual(str(customer), customer.name)
        self.assertEqual(customer.user_id, user.id)

    def test_customer_one_to_one(self):
        """Test an user can have only one customer object."""
        user = create_user()
        c1 = models.Customer.objects.create(
            user=user, name='Kamrul', phone_number='123456789')

        self.assertEqual(str(c1), c1.name)

        with self.assertRaises(IntegrityError):
            models.Customer.objects.create(
                user=user, name='Test', phone_number='123451234')

    def test_create_order_success(self):
        """Test creating an order successfull."""
        user = create_user()
        customer = models.Customer.objects.create(
            user=user, name='Kamrul', phone_number='123456789')

        order = models.Order.objects.create(customer=customer, cart_total=500)

        self.assertEqual(str(order), str(order.id))

    def test_add_order_item_success(self):
        """Test adding a product to order."""
        category = models.Category.objects.create(
            name='Electronic',
        )
        product = models.Product.objects.create(
            name='Hp Elitebook 840 G1',
            price=Decimal('500.50'),
            category=category,
            description='Intel core i5 4th gen, 8gb Ram.'
        )
        user = create_user()
        c1 = models.Customer.objects.create(
            user=user, name='Kamrul', phone_number='123456789')
        order, created = models.Order.objects.get_or_create(
            customer=c1, complete=False)
        item = models.OrderItem.objects.create(order=order, product=product)

        self.assertEqual(str(item), str(product.id))

    def test_create_discount_object(self):
        """Test creating discount Object."""
        category = create_category()
        discount = models.Discount.objects.create(
            category=category, name='Eid Discount', percentage=20)
        self.assertEqual(str(discount), discount.name)

    def test_create_tag_success(self):
        """Test Creating tag successfull."""
        tag = models.Tag.objects.create(
            title='Tag1',
            description="Test Tag",
        )

        self.assertEqual(str(tag), tag.title)

    def test_create_tag_product_connector_success(self):
        """Test Creating Tag and Product Connector Success."""
        tag = models.Tag.objects.create(
            title='Tag1',
            description="Test Tag",
        )
        category = models.Category.objects.create(
            name='Electronic',
        )
        product = models.Product.objects.create(
            name='Hp Elitebook 840 G1',
            price=Decimal('500.50'),
            category=category,
            description='Intel core i5 4th gen, 8gb Ram.'
        )

        product_tag_connector = models.ProductTagConnector(
            tag=tag,
            product=product
        )

        self.assertEqual(product_tag_connector.tag_id, tag.id)
        self.assertEqual(product_tag_connector.product_id, product.id)
