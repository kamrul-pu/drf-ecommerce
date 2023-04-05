"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
# TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the public features of the User API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successfull."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_users_with_existing_email_error(self):
        """Test error returned if the user email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 characters."""

        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    # def test_create_token_for_user(self):
    #     """Test generates token for valid credentials."""
    #     user_details = {
    #         'email': 'test@example.com',
    #         'password': 'testpass123',
    #         'name': 'Test Name',
    #     }

    #     create_user(**user_details)

    #     payload = {
    #         'email': 'test@example.com',
    #         'password': 'testpass123',
    #     }

    #     res = self.client.post(TOKEN_URL, payload)

    #     self.assertIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_create_token_bad_credentials(self):
    #     """Test returns error if credentials invalid."""
    #     create_user(email='test@example.com', password='goodpass')

    #     payload = {'email': 'test@example.com', 'password': 'badpass'}
    #     res = self.client.post(TOKEN_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertNotIn('token', res.data)

    # def test_create_token_blank_password(self):
    #     """Test posting a blank password returns an error."""
    #     payload = {'email': 'test@example.com', 'password': ''}
    #     res = self.client.post(TOKEN_URL, payload)

    #     self.assertNotIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_authorized(self):
        """Test authentication is required for users."""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requested that requires authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_me_not_allowed(self):
        """Tets POST is not allowed for the me endpoint."""
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated Name', 'password': 'newpassword'}

        response = self.client.patch(ME_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, response.data['name'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
