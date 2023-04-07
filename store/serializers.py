"""Seralizers for our Store Items."""

from rest_framework import serializers
from django.http import Http404

from core.models import (
    Category,
    Product,
    Order,
    OrderItem,
    ProductTagConnector,
    ShippingAddress,
)


class ProductSerializer(serializers.Serializer):
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all())
    category_id = serializers.IntegerField()

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(
        required=False)

    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        """"""
        tags = []
        product_tags = ProductTagConnector.objects.select_related('tag').filter(
            product=obj)
        for product_tag in product_tags:
            tags.append({'id': product_tag.tag.id,
                        'title': product_tag.tag.title})
        return tags

    def validate_category_id(self, value):
        try:
            Category.objects.get(id=value)
        except:
            raise Http404

        return value

    def create(self, validated_data):
        category_id = validated_data['category_id']
        # try:
        #     Category.objects.get(id=category_id)
        # except:
        #     raise Http404
        product = Product.objects.create(
            category_id=validated_data['category_id'],
            name=validated_data['name'],
            price=validated_data['price'],
            description=validated_data.get('description', ''),
            image=validated_data.get('image', None)
        )
        return product

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class CategorySerializer(serializers.Serializer):
    """Serializer for Category."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    # products = ProductSerializer(many=True, read_only=True)

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        # for product_data in products_data:
        #     Product.objects.create(category=category,**product_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


"""
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    description = serializers.CharField()
    image = serializers.ImageField()
    created = serializers.DateTimeField()

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    products = ProductSerializer(many=True)

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        category = Category.objects.create(**validated_data)
        for product_data in products_data:
            Product.objects.create(category=category, **product_data)
        return category

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        for product_data in products_data:
            product_id = product_data.get('id')
            if product_id:
                product = Product.objects.get(id=product_id, category=instance)
                product.name = product_data.get('name', product.name)
                product.price = product_data.get('price', product.price)
                product.description = product_data.get('description', product.description)
                product.image = product_data.get('image', product.image)
                product.save()
            else:
                Product.objects.create(category=instance, **product_data)
        return instance
"""


class OrderItemSerializer(serializers.Serializer):
    """Serializer for Order."""
    order_id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(default=1)
    # item_price = serializers.SerializerMethodField()

    # def get_item_price(self,obj):
    #     """Calculate and return item price by quantity."""
    #     try:

    def create(self, validated_data):
        order_item = OrderItem.objects.create()


class CustomerCartSerializer(serializers.Serializer):
    """Serializer for product item in cart."""
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='product.price')
    discount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='product.discount')
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='product.discounted_price')
    # product_image = serializers.ImageField(source='product.image')
    quantity = serializers.IntegerField()

    cart_price = serializers.SerializerMethodField()

    def get_cart_price(self, obj):
        if obj.product.discounted_price < 1:
            return obj.product.price * obj.quantity
        return obj.product.discounted_price * obj.quantity


class OrderSerializer(serializers.Serializer):
    """Serializer for Order."""
    # customer_id = serializers.IntegerField(read_only=True)
    customer_name = serializers.CharField(source='customer.name')
    id = serializers.IntegerField(read_only=True)
    date_ordered = serializers.DateTimeField()
    order_status = serializers.CharField()
    complete = serializers.BooleanField()
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    order_items = CustomerCartSerializer(many=True)


class ShippingAddressSerializer(serializers.Serializer):
    """Serializer for Shipping Address."""
    customer = serializers.CharField(source='customer.name', read_only=True)
    address = serializers.CharField(style={"base_template": "textarea.html"})
    city = serializers.CharField()
    postal_code = serializers.CharField()

    def create(self, validated_data):
        request = self.context.get('request')
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # shipping_address = ShippingAddress.objects.create(
        #     customer=customer,
        #     order=order,
        #     **validated_data
        # )

        # return shipping_address
        return ShippingAddress(customer=customer, order=order, **validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.postal_code = validated_data.get(
            'postal_code', instance.postal_code)

        instance.save()
        return instance
