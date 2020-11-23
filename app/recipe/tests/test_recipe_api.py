from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def get_detail_url(recipe_id):
	"""Return recipe detail URL"""
	return reverse('recipe:recipe-detail', args=[recipe_id])

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

def mock_tag(user, name='tag'):
	"""Mock a tag"""
	return Tag.objects.create(user=user, name=name)

def mock_ingredient(user, name='ingredient'):
	"""Mock an ingredient"""
	return Ingredient.objects.create(user=user, name=name)

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

	def test_retrieve_recipe_details(self):
		"""Test list details of 1 recipe"""
		recipe = mock_recipe(self.user)
		recipe.tags.add(mock_tag(self.user))
		recipe.ingredients.add(mock_ingredient(self.user))
		url = get_detail_url(recipe.id)
		res = self.client.get(url)
		serializer = RecipeDetailSerializer(recipe)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_create_basic_recipe(self):
		"""Test if user can create a recipe"""
		payload = {
			'title': 'My new recipe',
			'price': 10,
			'time_minute': 20,
			'link': 'https://www.google.com'
		}
		res = self.client.post(RECIPE_URL, payload)
		created_recipe = Recipe.objects.get(id=res.data['id'])

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		for key in payload.keys():
			self.assertEqual(payload[key], getattr(created_recipe, key))

	def test_create_recipe_with_tags(self):
		"""Test if user can create recipe with tags"""
		tag1 = mock_tag(self.user, 'tag1')
		tag2 = mock_tag(self.user, 'tag2')
		payload = {
			'title': 'My new recipe',
			'price': 10,
			'time_minute': 20,
			'tags': [tag1.id, tag2.id]
		}
		res = self.client.post(RECIPE_URL, payload)
		created_recipe = Recipe.objects.get(id=res.data['id'])
		recipe_tags = created_recipe.tags.all()

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		self.assertEqual(len(recipe_tags), 2)
		self.assertIn(tag1, recipe_tags)
		self.assertIn(tag2, recipe_tags)

	def test_create_recipe_with_ingredients(self):
		"""Test if user can create recipe with ingredients"""
		ingredient_1 = mock_ingredient(self.user, 'i1')
		ingredient_2 = mock_ingredient(self.user, 'i2')
		payload = {
			'title': 'My new recipe',
			'price': 10,
			'time_minute': 20,
			'ingredients': [ingredient_1.id, ingredient_2.id]
		}
		res = self.client.post(RECIPE_URL, payload)
		created_recipe = Recipe.objects.get(id=res.data['id'])
		recipe_ingredients = created_recipe.ingredients.all()

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		self.assertEqual(len(recipe_ingredients), 2)
		self.assertIn(ingredient_1, recipe_ingredients)
		self.assertIn(ingredient_2, recipe_ingredients)

	def test_partial_update_recipe(self):
		"""Test if user can partially update a recipe"""
		recipe = mock_recipe(self.user)
		recipe.tags.add(mock_tag(self.user))
		new_tag = mock_tag(self.user, 'New tag')
		payload = {
			'title': 'Updated recipe',
			'tags': [new_tag.id]
		}
		res = self.client.patch(get_detail_url(recipe.id), payload)
		recipe.refresh_from_db()
		recipe_tags = recipe.tags.all()

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(recipe.title, payload['title'])
		self.assertEqual(len(recipe_tags), 1)
		self.assertIn(new_tag, recipe_tags)

	def test_full_update_recipe(self):
		"""Test if user can fully update a recipe"""
		recipe = mock_recipe(self.user)
		recipe.tags.add(mock_tag(self.user, 'Super tag tag'))
		# Remove tags from recipe
		payload = {
			'title': 'Fully updated recipe',
			'price': 10,
			'time_minute': 15
		}
		res = self.client.put(get_detail_url(recipe.id), payload)
		recipe.refresh_from_db()
		recipe_tags = recipe.tags.all()

		# Assertions
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(recipe.title, payload['title'])
		self.assertEqual(recipe.price, payload['price'])
		self.assertEqual(recipe.time_minute, payload['time_minute'])
		self.assertEqual(len(recipe_tags), 0)
