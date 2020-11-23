from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.tests.authenticated_test_case import AuthenticatedTestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipe.serializers import TagSerializer

TAG_URL = reverse('recipe:tag-list')

def mock_user(email='test@example.com', password='helloworld'):
	return get_user_model().objects.create_user(email=email, password=password)

class PublicTagApiTests(TestCase):
	"""Test public tag API."""
	def setUp(self):
		self.client = APIClient()

	def test_authentication_required(self):
		res = self.client.get(TAG_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagApiTests(AuthenticatedTestCase):
	"""Test private tag API."""
	def setUp(self):
		super().setUp()

	def test_list_all_tags(self):
		"""Test if authenticated user could list all tag"""
		# Create some tags
		Tag.objects.create(name='Tag1', user=self.user)
		Tag.objects.create(name='Tag2', user=self.user)

		res = self.client.get(TAG_URL)
		tags = Tag.objects.all().order_by('name')
		serializer = TagSerializer(tags, many=True)

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_list_own_user_tags(self):
		"""Test if listing tags all belong to user who created them"""
		# Create a new user
		new_user = mock_user(email='new_user', password='new_password')
		# Create tags for default user
		Tag.objects.create(name='tag_own_user', user=self.user)
		# Create tags for new user
		Tag.objects.create(name='tag_new_user', user=new_user)

		# List all tags
		res = self.client.get(TAG_URL)

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data[0]['name'], 'tag_own_user')

	def test_create_tag_success(self):
		"""Test if user can successfully create a tag."""
		payload = {'name': 'Tag1'}
		res = self.client.post(TAG_URL, payload)
		tag_exist = Tag.objects.filter(name=payload['name'], user=self.user).exists()

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		self.assertEqual(tag_exist, True)

	def test_create_tag_fail_with_invalid_payload(self):
		"""Test if create tag fails with invalid payload."""
		payload = {'name': ''}
		res = self.client.post(TAG_URL, payload)

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



