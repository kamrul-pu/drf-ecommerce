"""
Views for our Ecommerce Store.
"""
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.decorators import permission_classes
from rest_framework import authentication
from rest_framework import status

from core.models import (
    Category,
    Product,
    Order,
    OrderItem,
    Discount,
    ProductTagConnector,
    Tag,
)

from store.serializers import (
    # CategorySerializer,
    ProductSerializer,
    # OrderSerializer,
    # OrderItemSerializer,

)
from admin_user.serializers import (
    OrderSerializerAdmin,
    OrderItemSerializerAdmin,
    TagProductConnectorSerializer,
    TagSerialiser,
    CategorySerializer,
)
from admin_user.serializers import (
    DiscountSerializer,
)

# permission_classes[IsAdminUser]


class TagList(APIView):
    """API View For create and listing Tags."""
    permission_classes = [IsAdminUser]
    serializer_class = TagSerialiser

    def get(self, request, format=None):
        tags = Tag.objects.filter()
        serilizer = TagSerialiser(tags, many=True)

        return Response(serilizer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TagSerialiser(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = TagSerialiser

    def _get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tag = self._get_object(pk)
        serializer = TagSerialiser(tag)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        tag = self._get_object(pk)
        serializer = TagSerialiser(tag, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        tag = self._get_object(pk)
        serializer = TagSerialiser(tag, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tag = self._get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CatgoryList(APIView):
    """Category List Create using API View."""
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        category = Category.objects.filter()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CatgoryDetail(APIView):
    """Category List Create using API View."""
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def _get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self._get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        category = self._get_object(pk)
        serializer = CategorySerializer(category, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        category = self._get_object(pk)
        serializer = CategorySerializer(category, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self._get_object(pk)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAdminList(APIView):
    """Create and return a product."""
    # authentication_classes = [authentication.]
    permission_classes = [IsAdminUser]

    serializer_class = ProductSerializer

    def get(self, request, format=None):
        products = Product.objects.filter()
        serialzer = ProductSerializer(products, many=True)
        return Response(serialzer.data, status=status.HTTP_200_OK)

    # @permission_classes([IsAdminUser, IsAuthenticated])
    def post(self, request, format=None):
        serializer = ProductSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductAdminDetail(APIView):
    """Admin Product Functionality."""
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = ProductSerializer

    def _get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self._get_object(pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        product = self._get_object(pk)
        serializer = ProductSerializer(
            product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        product = self._get_object(pk)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self._get_object(pk=pk)
        product.delete()
        return Response({'msg': 'Data Deleted Successfull'}, status=status.HTTP_204_NO_CONTENT)


class DiscountList(APIView):
    """Apply discount to category."""
    serializer_class = DiscountSerializer

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        discounts = Discount.objects.filter()
        serialzer = DiscountSerializer(discounts, many=True)
        return Response(serialzer.data, status=status.HTTP_200_OK)

    # @permission_classes([IsAdminUser, IsAuthenticated])

    def post(self, request, format=None):
        serializer = DiscountSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountDetail(APIView):
    """Discount Retrieve Update Destroy."""
    serializer_class = DiscountSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def _get_object(self, pk):
        try:
            return Discount.objects.get(id=pk)
        except Discount.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        discount = self._get_object(pk)
        serializer = DiscountSerializer(discount)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        discount = self._get_object(pk)
        serializer = DiscountSerializer(discount,
                                        data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        discount = self._get_object(pk)
        serializer = DiscountSerializer(discount,
                                        data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        discount = self._get_object(pk)
        discount.delete()
        return Response({'msg': 'Delelte Successfull'}, status=status.HTTP_204_NO_CONTENT)


class AdminOrderList(APIView):
    """View for listing all order."""

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = OrderSerializerAdmin

    def get(self, request, format=None):
        # orders = Order.objects.filter().prefetch_related("orderitem_set")
        orders = Order.objects.filter()
        # print("Orders", orders.orderitem)
        serializer = OrderSerializerAdmin(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminOrderDetail(APIView):
    """View for listing all order."""

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = OrderSerializerAdmin

    def _get_object(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = Order.objects.get(pk=pk)
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializerAdmin(order_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        order = self._get_object(pk)
        serializer = OrderSerializerAdmin(order,
                                          data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        order = self._get_object(pk)
        serializer = OrderSerializerAdmin(order,
                                          data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self._get_object(pk)
        order.delete()
        return Response({'msg': 'Delelte Successfull'}, status=status.HTTP_204_NO_CONTENT)


class TagProductList(APIView):
    """View for Tag Product Connector."""

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = TagProductConnectorSerializer

    def get(self, request, format=None):
        product_tags = ProductTagConnector.objects.filter()
        serializer = TagProductConnectorSerializer(product_tags, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TagProductConnectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
