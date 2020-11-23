from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth import get_user_model

def mock_user(email='test@example.com', password='helloworld'):
	"""Mock an user"""
	return get_user_model().objects.create_user(email=email, password=password)

class AuthenticatedTestCase(TestCase):
	"""Setup authenticated test case"""
	def setUp(self):
		"""
		Setup authenticated test case
		- Setup mock user
		- Setup API client for making API request
		- Authenticate user
		"""
		self.user = mock_user()
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)