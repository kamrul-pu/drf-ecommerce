"""Test Case for Order."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from decimal import Decimal

from core.models import (
    Order,
    Customer,
    Product,
    Category,
    OrderItem,
)


ORDER_URL = reverse('store:order')
SHIPPING_URL = reverse('store:shipping_address')


def order_update(product_id, action='add'):
    """Create and return url."""
    return reverse('store:add-to-cart', args=[product_id, action])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class OrderCustomerTest(TestCase):
    """Tests for Order Public."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@example.com', password='testpass123')
        self.customer = Customer.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

    # def test_customer_order_show(self):
    #     """Test retrieving customer order."""

    #     res = self.client.get(ORDER_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     order = Order.objects.all()
    #     self.assertEqual(order.count(), 1)
        # print("respone data", res.data)

    # def test_customer_order_show_existing(self):
    #     """Test retrieving customer order."""

    #     res = self.client.get(ORDER_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     order = Order.objects.all()
    #     self.assertEqual(order.count(), 1)
        # print("respone data", res.data)

    def test_add_product_to_cart_success(self):
        """Add Product to cart."""
        category = Category.objects.create(
            name='Electronic',
        )
        product = Product.objects.create(
            name='Hp Elitebook 840 G1',
            price=Decimal('500.50'),
            category=category,
            description='Intel core i5 4th gen, 8gb Ram.'
        )
        order, created = Order.objects.get_or_create(
            customer=self.customer, complete=False)
        # print("Type ",type(order))
        # order_item, created = OrderItem.objects.get_or_create(order=order, product=product,
        #                                                       quantity=1)
        url = order_update(product.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_shipping_address_success(self):
        """Test Creating Shipping address Success."""
        payload = {
            'address': 'Lalmatia Dhaka',
            'city': 'Dhaka',
            'postal_code': '1230'
        }

        response = self.client.post(SHIPPING_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['city'], payload['city'])

    def test_update_shipping_address_success(self):
        """Test Updateing Shipping Address Update."""
        payload = {
            'address': 'Lalmatia Dhaka',
            'city': 'Dhaka',
            'postal_code': '1230'
        }

        shipping_address = self.client.post(
            SHIPPING_URL, payload, format='json')
        payload = {
            'address': 'Tejgaon Industrial Area',
            'postal_code': '1208'
        }
        response = self.client.patch(SHIPPING_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['address'], response.data['address'])

    def test_get_customer_shipping_address(self):
        """Test Retrieve Customer Shipping Address."""
        payload = {
            'address': 'Lalmatia Dhaka',
            'city': 'Dhaka',
            'postal_code': '1230'
        }

        shipping_address = self.client.post(
            SHIPPING_URL, payload, format='json')

        response = self.client.get(SHIPPING_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, shipping_address.data)
