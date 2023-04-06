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
from django.core.paginator import (
    Paginator,
    EmptyPage,
    Page,
    PageNotAnInteger
)

from core.models import (
    Category,
    Product,
    Order,
    OrderItem,
    Customer,
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
    OrderItemSerializerTest,
)


class CategoryList(APIView):
    """Listing our all Categories."""

    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.filter().order_by('-id')
        serializer = self.serializer_class(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductList(APIView):
    """Listing all products."""

    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all().order_by('-id')

        """Adding Pagination."""
        page = request.query_params.get('page')
        paginator = Paginator(products, 5)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page is None:
            page = 1
        page = int(page)

        serializer = self.serializer_class(products, many=True)

        return Response({
            'products': serializer.data,
            'page': page,
            'pages': paginator.num_pages
        }, status=status.HTTP_200_OK)


class ProductListByCategory(APIView):
    """Listing products by category."""

    serializer_class = ProductSerializer

    def get(self, request, category_id):

        products = Product.objects.filter(category__id=category_id)

        serializer = self.serializer_class(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    """Product Retrieve Update destroy."""

    serializer_class = ProductSerializer

    def get(self, request, product_id, format=None):
        product = Product.objects.get(id=product_id)
        serializer = self.serializer_class(product, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


# permission_classes[IsAdminUser]


class CustomerOrder(APIView):
    """Customer Order."""
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get(self, request, format=None):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        order.get_cart_total()

        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCart(APIView):
    """Add or remove item from the cart."""

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, action, format=None):
        product = Product.objects.get(pk=pk)
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        order_item, created = OrderItem.objects.get_or_create(
            order_id=order.id, product_id=product.id)

        if action == 'add':
            order_item.quantity = (order_item.quantity+1)
        elif action == 'remove':
            order_item.quantity = (order_item.quantity-1)

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()
        return Response({'msg': 'Add to cart Success'}, status=status.HTTP_201_CREATED)


class CartItem(APIView):
    """Sample CartItem View."""

    serializer_class = OrderItemSerializerTest

    def get(self, request, format=None):
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = order.get_cart_total()
        # total = 0
        order_items = OrderItem.objects.filter(order=order)
        serializer = self.serializer_class(order_items, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'cart_items': serializer.data,
            'total': total,
        }, status=status.HTTP_200_OK)
