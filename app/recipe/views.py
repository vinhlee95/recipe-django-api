from rest_framework import viewsets, mixins, authentication, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from core.models import Tag, Ingredient, Recipe

class BaseRecipeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	"""Base configurations for Recipe attributes (Tags, Ingredients,...)"""
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	# Overwrite default method
	def get_queryset(self):
		"""Return only tags belong to current authenticated user"""
		return self.queryset.filter(user=self.request.user).order_by('name')

	def perform_create(self, serializer):
		"""Create a new tag for an user"""
		serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeViewSet):
	"""Manage all tags in the db"""
	serializer_class = serializers.TagSerializer
	queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeViewSet):
	"""Manage all ingredients in the db"""
	serializer_class = serializers.IngredientSerializer
	queryset = Ingredient.objects.all()

class RecipeViewSet(viewsets.ModelViewSet):
	"""
	Manage all recipes in the db
	We are using ModelViewSet for having a set of "actions" by default
	Such as: .list(), .retrieve(), .create(), .update() and .destroy()
	"""
	serializer_class = serializers.RecipeSerializer
	queryset = Recipe.objects.all()
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		"""Return recipe belongs to an user"""
		return self.queryset.filter(user=self.request.user).order_by('title')

	def get_serializer_class(self):
		"""Return proper serializer class for action"""
		if self.action == 'retrieve':
			return serializers.RecipeDetailSerializer
		elif self.action == 'upload_image':
			return serializers.RecipeImageSerializer

		return self.serializer_class

	def perform_create(self, serializer):
		"""Create a new recipe for own user"""
		serializer.save(user=self.request.user)

	@action(detail=True, methods=['post'], url_path='upload-image')
	def upload_image(self, request, pk=None):
		recipe = self.get_object()
		# Get serializer instance
		# get_serializer(self, instance=None, data=None, many=False, partial=False) - Returns a serializer instance.
		# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
		serializer = self.get_serializer(recipe, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_200_OK)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
