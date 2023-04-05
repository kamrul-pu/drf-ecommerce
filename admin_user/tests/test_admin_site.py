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
    TagSerialiser,
    CategorySerializer,
)

DISCOUNT_URL = reverse('admin_user:discount')
TAG_URL = reverse('admin_user:tags')
CATEGORY_URL = reverse('admin_user:category')


def get_tag_url(tag_id):
    """Create and return a tag url."""
    return reverse('admin_user:tag-detail', args=[tag_id])


def get_category_url(category_id):
    """Create and return category url"""
    return reverse('admin_user:category-detail', args=[category_id])


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
            'category_id': category.id,
            'name': 'Eid Ul Fitre Discount',
            'percentage': 30,
        }

        url = get_detail_url(discount['id'])
        response = self.client.patch(url, payload)

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

    def test_create_tag_success(self):
        """Create a tag by admin user success."""
        payload = {
            'title': 'Sample Tag',
            'description': 'Sample Tag Create'
        }

        response = self.client.post(TAG_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # tag = TagSerialiser(response)

        self.assertEqual(response.data['title'], payload['title'])

    def test_update_tag_success(self):
        """Test Updating tag is successfull."""
        payload = {
            'title': 'Sample Tag',
            'description': 'Sample Tag Created'
        }

        response = self.client.post(TAG_URL, payload)
        # print('response ', response.data)
        payload = {
            'title': 'Sample Tag Updated',
            'description': 'Updated Description'
        }

        url = get_tag_url(response.data['id'])
        response1 = self.client.put(url, payload)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data['title'], payload['title'])

    def test_delete_tag_success(self):
        """Test Deleting tag successfull."""
        payload = {
            'title': 'Sample Tag',
            'description': 'Sample Tag Created'
        }

        response = self.client.post(TAG_URL, payload)

        url = get_tag_url(response.data['id'])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_category_success(self):
        """Test Creating category successfull."""
        payload = {
            'name': 'Sample Category'
        }

        response = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['name'], payload['name'])

    def test_update_category_success(self):
        """Test Updating Category Success."""
        payload = {
            'name': 'Sample Category'
        }

        category = self.client.post(CATEGORY_URL, payload)
        payload = {
            'name': 'Sample Category Updated'
        }

        url = get_category_url(category.data['id'])
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], payload['name'])

    def test_delete_category_success(self):
        """Test Deleting category success."""
        payload = {
            'name': 'Sample Category'
        }
        category = self.client.post(CATEGORY_URL, payload)
        url = get_category_url(category.data['id'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
