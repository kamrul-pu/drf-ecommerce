"""Serializer for admin users."""
from rest_framework import serializers


class DiscountSerializer(serializers.Serializer):
    """Serializer for discount."""
    category_id = serializers.IntegerField()
    name = serializers.CharField()
    percentage = serializers.IntegerField()
