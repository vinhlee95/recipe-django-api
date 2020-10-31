from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

	def test_create_user_with_email_successful(self):
		"""Test creating a new user with an email is successful"""
		email = 'vinh@test.com'
		password = 'password'
		user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))

	def test_normalized_email(self):
		"""Test creating a new user with normalized email"""
		email = 'vinh@TEST.COM'
		password = 'password'
		user = get_user_model().objects.create_user(
			email=email,
			password=password
		)
		self.assertEqual(user.email, email.lower())

	def test_create_user_invalid_email(self):
		"""Test creating user with invalid email should throw ValueError"""
		password = 'password'
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(email=None, password=password)

	def test_create_superuser(self):
		"""Test creating super user with valid superuser and staff role"""
		email = 'vinh@TEST.COM'
		password = 'password'
		user = get_user_model().objects.create_superuser(email=email, password=password)
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)