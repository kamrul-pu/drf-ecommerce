"""
Tests for model
"""
from unittest.mock import patch

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and returns a new user."""
    return get_user_model().objects.create_user(email, password)


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
        category = models.Category.objects.create(
            name='Electronic',
        )
        product = models.Product.objects.create(
            name='Hp Elitebook 840 G1',
            price=Decimal('500.50'),
            category=category,
            description='Intel core i5 4th gen, 8gb Ram.'
        )

        self.assertEqual(str(product), product.name)
        self.assertEqual(category.id, product.category.id)
