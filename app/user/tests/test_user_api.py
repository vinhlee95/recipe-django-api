from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, force_authenticate
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
MANAGE_USER_URL = reverse('user:me')

USER_PAYLOAD = {
	'email': 'test@testi.com',
	'password': 'helloworld',
	'name': 'Test user'
}

def create_user(**params):
	return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
	"""Test the public users API"""
	def setUp(self):
		self.client = APIClient()

	def test_create_valid_user_success(self):
		"""Test creating user with valid payload"""
		# Make API request
		res = self.client.post(CREATE_USER_URL, USER_PAYLOAD)
		self.assertEquals(res.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(**res.data)
		self.assertTrue(user.check_password(USER_PAYLOAD['password']))
		self.assertNotIn('password', res.data)

	def test_user_exists(self):
		"""Test if creating an already existed user fails"""
		# Create an user
		create_user(**USER_PAYLOAD)
		res = self.client.post(CREATE_USER_URL, USER_PAYLOAD)
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_user_valid_password(self):
		"""Test if creating a new user with less than 5 chars password fails"""
		res = self.client.post(CREATE_USER_URL, {
			'email': USER_PAYLOAD['email'],
			'password': '123'
		})
		user_exists = get_user_model().objects.filter(email = USER_PAYLOAD['email'])
		self.assertFalse(user_exists)

	def test_create_token(self):
		"""Test that a valid token could be created for an user"""
		# First, create a new user
		create_user(**USER_PAYLOAD)
		# Use data of the new user to request for the token
		res = self.client.post(TOKEN_URL, USER_PAYLOAD)
		# Assertions
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		# Make sure token field exists in res.data
		self.assertIn('token', res.data)

	def test_create_token_invalid_credentials(self):
		"""Test if create token fails if invalid credentials are provided"""
		create_user(**USER_PAYLOAD)
		invalid_credential = USER_PAYLOAD.copy()
		invalid_credential['email'] = 'invalid_email@test.com'
		res = self.client.post(TOKEN_URL, invalid_credential)
		# Assertions
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotIn('token', res.data)

	def test_create_token_missing_user_fields(self):
		"""Test if create token fails if user fields are missing"""
		create_user(**USER_PAYLOAD)
		missing_fields_credential = USER_PAYLOAD.copy()
		missing_fields_credential['password'] = ''
		res = self.client.post(TOKEN_URL, missing_fields_credential)
		# Assertions
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotIn('token', res.data)

	def test_private_manage_user_endpoint(self):
		"""Test if manage user endpoint is a private one."""
		res = self.client.get(MANAGE_USER_URL)
		# Assertions
		self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
	def setUp(self):
		self.user = create_user(**USER_PAYLOAD)
		self.client = APIClient()
		# Force authenticate the user
		self.client.force_authenticate(user=self.user)

	def test_get_user_success(self):
		"""Test if authenticated user can get own user data"""
		res = self.client.get(MANAGE_USER_URL)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, {
			'email': self.user.email,
			'name': self.user.name
		})

	def test_update_user_success(self):
		"""Test if user can update own data."""
		params = {'email': 'update_user@test.com', 'name': 'update_user'}
		res = self.client.patch(MANAGE_USER_URL, params)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, {
			'email': params['email'],
			'name': params['name']
		})

