"""
Views for our Ecommerce Store.
"""
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import (
    Category,
    Product
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
)


class CategoryListView(APIView):
    """Listing our all Categories."""

    def get(self, request):
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


class ProductListView(APIView):
    """Listing all products."""

    def get(self, request):
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


class ProductListByCategory(APIView):
    """Listing products by category."""

    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


class ProductDetailView(APIView):
    """Product Retrieve Update destroy."""

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product, many=False)

        return Response(serializer.data)
