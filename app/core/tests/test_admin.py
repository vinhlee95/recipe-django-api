from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminTest(TestCase):

	def setUp(self):
		"""Setup that run before every test"""
		# Setup client
		self.client = Client()
		# Setup admin user and simulate logging in
		self.admin_user = get_user_model().objects.create_superuser(
			email = 'admin@test.com',
			password = 'password'
		)
		self.client.force_login(self.admin_user)
		# Setup normal user
		self.user = get_user_model().objects.create_user(
			email = 'user@test.com',
			password = 'password'
		)

	def test_user_listing(self):
		"""Test if Admin site list all users"""
		url = reverse('admin:core_user_changelist')
		res = self.client.get(url)
		self.assertContains(res, self.user.name)
		self.assertContains(res, self.user.email)


