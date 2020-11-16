from rest_framework import viewsets, mixins, authentication, permissions
from . import serializers
from core.models import Tag

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	"""Manage all tags in the db"""
	serializer_class = serializers.TagSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Tag.objects.all()

	def get_queryset(self):
		"""Return only tags belong to current authenticated user"""
		return self.queryset.filter(user=self.request.user).order_by('name')