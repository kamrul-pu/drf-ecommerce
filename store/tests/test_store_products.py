"""
Test for Products APIs.
"""

from decimal import Decimal

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


def detail_url(category_id):
    """Create and return an url for listing item based on category."""
    return reverse('store:product_category', args=[category_id])


def detail_url_for_product(product_id):
    """Create and return an url for get individual product."""
    return reverse('store:product-detail', args=[product_id])


def create_product(**params):
    """Create and return a product."""
    c1 = Category.objects.create(
        name='Electronics',
    )
    defaults = {
        'name': 'Hp Elitebook 840 G1',
        'price': Decimal('500.50'),
        'category': c1,
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

        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_of_products(self):
        """Test listing our products."""
        p1 = create_product()
        p2 = create_product(name='SurfaceBook 2', price=500.00)

        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.data, serializer.data)

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
            category=c2,
            description='Powerfull Mackbook Pro with Apple M1 powered chipsets.'
        )

        url = detail_url(c2.id)

        res = self.client.get(url)

        s1 = ProductSerializer(p1)
        s2 = ProductSerializer(p2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s1.data, res.data)

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

        res = self.client.get(url)
        s1 = ProductSerializer(p1)
        s2 = ProductSerializer(p2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(s1.data, res.data)

    def test_post_is_not_allowed_in_product(self):
        """Test You cant't update product only admin can."""
        p1 = create_product()
        url = detail_url_for_product(p1.id)

        res = self.client.post(url, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
