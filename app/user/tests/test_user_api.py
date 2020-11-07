from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
USER_PAYLOAD = {
	'email': 'test@testi.com',
	'password': 'helloworld'
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
