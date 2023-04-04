"""Serializer for admin users."""
from rest_framework import serializers
from django.http import Http404

from core.models import (
    Category, Discount, OrderItem, Tag, Product, ProductTagConnector
)


class DiscountSerializer(serializers.Serializer):
    """Serializer for discount."""
    id = serializers.IntegerField(read_only=True)
    category_id = serializers.IntegerField()
    name = serializers.CharField()
    percentage = serializers.IntegerField()

    def create(self, validated_data):
        category_id = validated_data['category_id']
        try:
            Category.objects.get(id=category_id)
        except:
            raise Http404
        discount = Discount.objects.create(
            category_id=validated_data['category_id'],
            name=validated_data['name'],
            percentage=validated_data['percentage']
        )
        return discount

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get(
            'category_id', instance.category_id)
        instance.name = validated_data.get('name', instance.name)
        instance.percentage = validated_data.get(
            'percentage', instance.percentage)

        instance.save()
        return instance


class OrderItemSerializerAdmin(serializers.Serializer):
    """Serializer for Order."""
    # order_id = serializers.IntegerField()
    id = serializers.IntegerField()
    product = serializers.CharField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        order_item = OrderItem.objects.create()


class OrderSerializerAdmin(serializers.Serializer):
    """Serializer for Order."""
    customer_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    date_ordered = serializers.DateTimeField()
    complete = serializers.BooleanField()
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    order_items = OrderItemSerializerAdmin(many=True)
    # order_item = OrderItemSerializerAdmin(many=True)

    def update(self, instance, validated_data):
        instance.complete = validated_data.get('complete', instance.complete)
        instance.cart_total = validated_data.get(
            'cart_total', instance.cart_total)
        instance.paid_amount = validated_data.get(
            'paid_amount', instance.paid_amount)
        instance.order_items = validated_data.get(
            'order_items', instance.order_items)

        instance.save()

        return instance


class TagProductConnectorSerializer(serializers.Serializer):
    """Tag product Connector serializer."""
    tag_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

    def create(self, validated_data):
        tag_id = validated_data['tag_id']
        try:
            Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            raise Http404
        product_id = validated_data['product_id']
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404

        product_tag_connect = ProductTagConnector.objects.create(
            tag_id=tag_id,
            product_id=product_id
        )

        return product_tag_connect
