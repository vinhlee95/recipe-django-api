from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def mock_user(email='test@example.com', password='helloworld'):
	return get_user_model().objects.create_user(email=email, password=password)

def mock_recipe(user, **params):
	"""Mock a recipe"""
	default = {
		'title': 'Mock recipe',
		'price': 10,
		'time_minute': 15
	}
	default.update(params)
	return Recipe.objects.create(user=user, **default)

class PublicRecipeApiTest(TestCase):
	"""Test public recipe API"""
	def setUp(self):
		self.client = APIClient()

	def test_authentication_required(self):
		res = self.client.get(RECIPE_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeTest(TestCase):
	"""Test private recipe API"""
	def setUp(self):
		self.user = mock_user()
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_list_all_recipes(self):
		"""Test if authenticated user could list all recipes"""
		# Create some recipes
		mock_recipe(self.user)
		mock_recipe(self.user)

		res = self.client.get(RECIPE_URL)
		recipes = Recipe.objects.all()
		serializer = RecipeSerializer(recipes, many=True)

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_list_own_recipes(self):
		"""Test if listing recipes belong to user who created them"""
		mock_recipe(self.user)
		new_user = mock_user(email='new_user@test.com', password='hitherwoow')
		mock_recipe(new_user)

		res = self.client.get(RECIPE_URL)
		recipes = Recipe.objects.filter(user=self.user)
		serializer = RecipeSerializer(recipes, many=True)

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data, serializer.data)