"""Serializer for admin users."""
from rest_framework import serializers
from django.http import Http404

from core.models import (
    Category, Discount,
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
