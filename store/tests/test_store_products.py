"""
Test for Products APIs.
"""
import tempfile
import os
from PIL import Image

from decimal import Decimal
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import (
    Category,
    Product,
)

from store.serializers import (
    CategorySerializer,
    ProductSerializer,
)

PRODUCT_URL = reverse('store:products')
CATEGORY_URL = reverse('store:category')
PRODUCT_CREATE_URL = reverse('admin_user:product-admin')


def detail_url(category_id):
    """Create and return an url for listing item based on category."""
    return reverse('store:product_category', args=[category_id])


def detail_url_for_product(product_id):
    """Create and return an url for get individual product."""
    return reverse('store:product-detail', args=[product_id])


def detail_url_for_product_admin(product_id):
    """Create and return an url for get product admin."""
    return reverse('admin_user:product-admin-detail', args=[product_id])


def create_product(**params):
    """Create and return a product."""
    c1 = Category.objects.create(
        name='Electronics',
    )
    defaults = {
        'name': 'Hp Elitebook 840 G1',
        'price': Decimal('500.50'),
        'category_id': c1.id,
        'description': 'Intel core i5 4th gen, 8gb Ram.'
    }

    defaults.update(params)

    product = Product.objects.create(**defaults)

    return product


class PublicProductAPITest(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_list_of_category(self):
        """Test retrieving list of product categories."""
        c1 = Category.objects.create(
            name='Electronics',
        )
        c2 = Category.objects.create(
            name='IT',
        )

        categories = Category.objects.all().order_by('-id')

        serializer = CategorySerializer(categories, many=True)

        response = self.client.get(CATEGORY_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_of_products(self):
        """Test listing our products."""
        p1 = create_product()
        p2 = create_product(name='SurfaceBook 2', price=500.00)

        response = self.client.get(PRODUCT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data['products'], serializer.data)

    def test_list_product_by_category(self):
        """Test displaying the products based on Category."""
        c1 = Category.objects.create(
            name='Electronics',
        )
        c2 = Category.objects.create(
            name='IT',
        )
        p1 = create_product()
        p2 = create_product(
            name='MackbookPro M1',
            price='2000.50',
            category_id=c2.id,
            description='Powerfull Mackbook Pro with Apple M1 powered chipsets.'
        )

        url = detail_url(c2.id)

        response = self.client.get(url)

        s1 = ProductSerializer(p1)
        s2 = ProductSerializer(p2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(s2.data, response.data)
        self.assertNotIn(s1.data, response.data)

    def test_retrieve_individual_product(self):
        """Test retriving asingle product by id."""
        c1 = Category.objects.create(
            name='Electronics',
        )
        c2 = Category.objects.create(
            name='IT',
        )
        p1 = create_product()
        p2 = create_product(
            name='MackbookPro M1',
            price='2000.50',
            category=c2,
            description='Powerfull Mackbook Pro with Apple M1 powered chipsets.'
        )

        url = detail_url_for_product(p1.id)

        response = self.client.get(url)
        s1 = ProductSerializer(p1)
        s2 = ProductSerializer(p2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(s1.data, response.data)

    def test_post_is_not_allowed_in_product(self):
        """Test You cant't update product only admin can."""
        p1 = create_product()
        url = detail_url_for_product(p1.id)

        response = self.client.post(url, {})

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class PrivateProductAPITests(TestCase):
    """Test Product of private user."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='admin@example.com', password='testpass123')

        # self.token = Token.objects.create(user=self.user)

        self.client.force_authenticate(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    # def test_create_product_successfull(self):
    #     """Test create a product by admin."""
    #     c1 = Category.objects.create(
    #         name='Electronics',
    #     )
    #     with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
    #         img = Image.new('RGB', (10, 10))
    #         img.save(image_file, format='JPEG')
    #         image_file.seek(0)

    #         payload = {
    #             'name': 'Hp Elitebook 840 G1',
    #             'price': Decimal('500.50'),
    #             'category_id': c1.id,
    #             'description': 'Intel core i5 4th gen, 8gb Ram.',
    #             'image': image_file
    #         }

    #         res = self.client.post(
    #             PRODUCT_CREATE_URL, payload, format='multipart')

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_normal_user_create_product_fails(self):
        """Test normal user will not be able to create a product."""
        user = get_user_model().objects.create(
            email='user@example.com', password='testpass123')

        self.client.force_authenticate(user)
        c1 = Category.objects.create(
            name='Electronics',
        )
        payload = {
            'name': 'Hp Elitebook 840 G1',
            'price': Decimal('500.50'),
            'category': c1.id,
            'description': 'Intel core i5 4th gen, 8gb Ram.',
        }

        response = self.client.post(PRODUCT_CREATE_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_by_admin(self):
        """Test updating a product by admin."""
        p1 = create_product()

        url = detail_url_for_product_admin(p1.id)
        payload = {
            'name': 'Product name changed',
            'price': '250.50'
        }
        response = self.client.patch(url, payload, format='json')

        p1.refresh_from_db()
        s1 = ProductSerializer(p1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], payload['price'])

    def test_product_delete_by_admin(self):
        """Test deleting a product."""
        p1 = create_product()

        url = detail_url_for_product_admin(p1.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_product_by_invalid_category_id(self):
        """Test creating a product with invalid category id raise error."""
        c1 = Category.objects.create(
            name='Electronics',
        )
        payload = {
            'name': 'Hp Elitebook 840 G1',
            'price': Decimal('500.50'),
            'category_id': 3,
            'description': 'Intel core i5 4th gen, 8gb Ram.',
        }

        response = self.client.post(
            PRODUCT_CREATE_URL, payload, format='json')
        # print(response.status_code)
        products = Product.objects.all()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(products.count(), 0)
