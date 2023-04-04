"""Serializer for admin users."""
from rest_framework import serializers
from django.http import Http404

from core.models import (
    Category, Discount, OrderItem
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
    order_id = serializers.IntegerField()
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

    # orderitem = OrderItemSerializerAdmin(many=True)
