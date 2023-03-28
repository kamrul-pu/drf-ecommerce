"""Seralizers for our Store Items."""

from rest_framework import serializers

from core.models import (
    Category,
    Product,
)


# class ProductSerializer(serializers.ModelSerializer):
#     """Serializers for Product."""
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'category', 'image']

class CategorySerializer(serializers.Serializer):
    """Serializer for Category."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        # for product_data in products_data:
        #     Product.objects.create(category=category,**product_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class ProductSerializer(serializers.Serializer):
    # category = CategorySerializer(read_only=True)
    id = serializers.IntegerField()
    category_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.ImageField()
    description = serializers.TimeField()

    def create(self, validated_data):
        """Create and return Product."""
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)

        return Product.objects.create(category=category, **validated_data)

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id')
        instance.category = Category.objects.get(id=category_id)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)

        instance.save()

        return instance


# class CategorySerializer(serializers.ModelSerializer):
#     """Serializer for our Category."""

#     class Meta:
#         model = Category
#         fields = ['id', 'name']

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
