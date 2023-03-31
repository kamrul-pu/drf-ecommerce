"""
Serializers for User APIs.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import Customer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and returns a user."""
        user = get_user_model().objects.create_user(**validated_data)
        name = validated_data.get('name')
        Customer.objects.create(user=user, name=name)
        return user

    def update(self, instance, validated_data):
        """Update and return a user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class CustomerSerializer(serializers.Serializer):
    """Serializer for Customer."""
    user = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=100, allow_null=True, allow_blank=True)
    phone_number = serializers.CharField(
        max_length=20, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        Customer.objects.create(customer=self.user, **validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)

        instance.save()

        return instance


# class UserSerializer(serializers.Serializer):
#     """Serializer Without Model Serializer."""
#     email = serializers.EmailField()
#     password = serializers.CharField(min_length=6, write_only=True)
#     name = serializers.CharField(
#         max_length=100, allow_blank=True, allow_null=True)

#     def create(self, validated_data):
#         # password = validated_data.pop('password')
#         return get_user_model().objects.create_user(**validated_data)

#     def update(self, instance, validated_data):
#         password = validated_data.pop('password', None)
#         instance.name = validated_data.get('name', instance.name)
#         # user = super().update(instance, validated_data)
#         user = instance
#         if password:
#             user.set_password(password)
#             user.save()
#         return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializers for auth TOken"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
