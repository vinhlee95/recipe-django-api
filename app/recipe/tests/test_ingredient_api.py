from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

def mock_user(email='test@example.com', password='helloworld'):
	return get_user_model().objects.create_user(email=email, password=password)

class PublicIngredientApiTests(TestCase):
	"""Test public ingredient API."""
	def setUp(self):
		self.client = APIClient()

	def test_authentication_required(self):
		res = self.client.get(INGREDIENT_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTests(TestCase):
	"""Test private ingredient API."""
	def setUp(self):
		self.user = mock_user()
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_list_all_ingredients(self):
		"""Test if authenticated user could list all ingredient"""
		# Create some ingredients
		Ingredient.objects.create(name='Ingredient 1', user=self.user)
		Ingredient.objects.create(name='Ingredient 2', user=self.user)

		res = self.client.get(INGREDIENT_URL)
		ingredients = Ingredient.objects.all().order_by('name')
		serializer = IngredientSerializer(ingredients, many=True)

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_list_own_user_ingredients(self):
		"""Test if listing ingredients all belong to user who created them"""
		# Create a new user
		new_user = mock_user(email='new_user', password='new_password')
		# Create ingredients for default user
		Ingredient.objects.create(name='ingredient_own_user', user=self.user)
		# Create ingredients for new user
		Ingredient.objects.create(name='ingredient_new_user', user=new_user)

		# List all ingredients
		res = self.client.get(INGREDIENT_URL)

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data[0]['name'], 'ingredient_own_user')