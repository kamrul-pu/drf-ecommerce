"""
Views for the user API.
"""
from django.http import Http404
from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from drf_spectacular.utils import extend_schema

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    CustomerSerializer,
)

from core.models import Customer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for users."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated users."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class CustomerProfile(APIView):
    """View For Customer."""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = CustomerSerializer

    def _get_object(self):
        try:
            return Customer.objects.get(customer_id=self.request.user.id)
        except Customer.DoesNotExist:
            raise Http404

    # @extend_schema(
    #     parameters=[
    #         {
    #             'name': 'Name',
    #             'required': False,
    #             'type': 'string',
    #         }
    #     ]
    # )
    def get(self, request, format=None):
        customer = self._get_object()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request, format=None):
    #     serializer = CustomerSerializer(
    #         data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        customer = self._get_object()
        serialier = CustomerSerializer(
            customer, data=request.data, partial=True)

        if serialier.is_valid():
            serialier.save()
            return Response(serialier.data, status=status.HTTP_200_OK)
        return Response(serialier.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        customer = self._get_object()
        serialier = CustomerSerializer(
            customer, data=request.data)

        if serialier.is_valid():
            serialier.save()
            return Response(serialier.data, status=status.HTTP_200_OK)
        return Response(serialier.errors, status=status.HTTP_400_BAD_REQUEST)
