"""Test For Custom User Site."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Category,
    Discount,
)

from admin_user.serializers import (
    DiscountSerializer,
)

DISCOUNT_URL = reverse('admin_user:discount')


def get_detail_url(discount_id):
    """Create and return discount detail urls."""
    return reverse('admin_user:discount-detail', args=[discount_id])


class PublicDiscountAPITest(TestCase):
    """Test Discount for Unauthenticated User."""

    def setUp(self):
        self.client = APIClient()

    def test_add_discount_by_normal_user_fails(self):
        """Test Customer can only show discount ."""
        pass

    def test_list_discount_by_unauthorized_user(self):
        """Test Listing discounts."""
        response = self.client.get(DISCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_discount_by_public_failed(self):
        """Test Adding discount Success."""
        category = Category.objects.create(
            name='Electronics',
        )
        payload = {
            'category_id': category.id,
            'name': 'Eid Discount',
            'percentage': 20,
        }

        response = self.client.post(DISCOUNT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDiscountAPITest(TestCase):
    """Test Discount For admin User."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='admin@example.com', password='testpass123'
        )

        self.client.force_authenticate(self.user)

    def test_add_discount_on_category_success(self):
        """Test Adding discount Success."""
        category = Category.objects.create(
            name='Electronics',
        )
        payload = {
            'category_id': category.id,
            'name': 'Eid Discount',
            'percentage': 20,
        }

        response = self.client.post(DISCOUNT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])

    def test_discount_update(self):
        """Test discount update."""
        category = Category.objects.create(
            name='Electronics',
        )
        payload = {
            'category_id': category.id,
            'name': 'Eid Discount',
            'percentage': 20,
        }
        response = self.client.post(DISCOUNT_URL, payload)
        discount = response.data
        payload = {
            'name': 'Eid Ul Fitre Discount',
            'percentage': 30,
        }

        url = get_detail_url(discount['id'])
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], payload['name'])

    def test_delete_discount_success(self):
        """Test deleting discount success."""
        category = Category.objects.create(
            name='Electronics',
        )
        payload = {
            'category_id': category.id,
            'name': 'Eid Discount',
            'percentage': 20,
        }
        response = self.client.post(DISCOUNT_URL, payload)

        url = get_detail_url(response.data['id'])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
