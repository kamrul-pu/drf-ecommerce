"""
Views for our Ecommerce Store.
"""
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import authentication
from rest_framework import status

from core.models import (
    Category,
    Product,
    Order,
    OrderItem,
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


class CategoryList(APIView):
    """Listing our all Categories."""

    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductList(APIView):
    """Listing all products."""

    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


class ProductListByCategory(APIView):
    """Listing products by category."""

    serializer_class = ProductSerializer

    def get(self, request, category_id):

        products = Product.objects.filter(category__id=category_id)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    """Product Retrieve Update destroy."""

    serializer_class = ProductSerializer

    def get(self, request, product_id, format=None):
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


# permission_classes[IsAdminUser]


class CustomerOrder(APIView):
    """Customer Order."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get(self, request, format=None):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCart(APIView):
    """Add or remove item from the cart."""

    serializer_class = OrderItemSerializer

    def post(self, request, pk, action, format=None):
        product = Product.objects.get(pk=pk)
        customer = self.request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        # print("Order", order, "Created", created)

        order_item, created = OrderItem.objects.get_or_create(
            order_id=order.id, product_id=product.id)

        if action == 'add':
            order_item.quantity = (order_item.quantity+1)
        elif action == 'remove':
            order_item.quantity = (order_item.quantity-1)

        order_item.save()
        serializer = OrderItemSerializer(order_item)

        if order_item.quantity <= 0:
            order_item.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
