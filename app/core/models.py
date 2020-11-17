from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):

	def create_user(self, email, password=None, **extra_fields):
		"""OUR OWN method to Create and save a new User"""
		if not email:
			raise ValueError('Invalid email')

		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		"""Create and save new superuser"""
		if not email:
			raise ValueError('Invalid email')

		user = self.create_user(email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user

class User(AbstractBaseUser, PermissionsMixin):
	"""Custom user model that supports using email instead of username"""
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'

class Tag(models.Model):
	"""Tag model"""
	name = models.CharField(max_length=40)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

	def __str__(self):
		return self.name

class Ingredient(models.Model):
	"""Ingredient model"""
	name = models.CharField(max_length=40)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

	def __str__(self):
		return self.name