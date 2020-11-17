from rest_framework import viewsets, mixins, authentication, permissions
from . import serializers
from core.models import Tag, Ingredient

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	"""Manage all tags in the db"""
	serializer_class = serializers.TagSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Tag.objects.all()

	# Overwrite default method
	def get_queryset(self):
		"""Return only tags belong to current authenticated user"""
		return self.queryset.filter(user=self.request.user).order_by('name')

	def perform_create(self, serializer):
		"""Create a new tag for an user"""
		serializer.save(user=self.request.user)

class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	"""Manage all ingredients in the db"""
	serializer_class = serializers.IngredientSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Ingredient.objects.all()

	# Overwrite default method
	def get_queryset(self):
		"""Return only ingredients belong to current authenticated user"""
		return self.queryset.filter(user=self.request.user).order_by('name')