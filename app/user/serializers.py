from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
	"""Serializer from the user object"""
	class Meta:
		model = get_user_model()
		fields = ('email', 'password', 'name')
		extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

	def create(self, validated_data):
		"""Create a new user and return it"""
		return get_user_model().objects.create_user(**validated_data)

	def update(self, instance, validated_data):
		"""Update user data and return updated data"""
		user = super().update(instance, validated_data)
		return user

class AuthTokenSerializer(serializers.Serializer):
	"""Serializer to authenticate user"""
	email = serializers.CharField()
	password = serializers.CharField(
		style={'input-style': 'password'},
		min_length=8
	)

	def validate(self, attrs):
		"""Validate and authenticate user"""
		email = attrs.get('email')
		password = attrs.get('password')
		user = authenticate(
			request = self.context.get('request'),
			username = email,
			password = password
		)
		if not user:
			msg = 'Unable to authenticate'
			raise serializers.ValidationError(msg, code='authentication')
		attrs['user'] = user
		return attrs
