from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import os
import uuid

def get_recipe_image_path(instance, image_name):
	"""Normalize recipe image name and save it to correct location"""
	ext = image_name.split('.')[-1]
	file_name = f'{uuid.uuid4()}.{ext}'

	return os.path.join('uploads/recipe/', file_name)

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

class Recipe(models.Model):
	"""Recipe model"""
	title = models.CharField(max_length=20)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	time_minute = models.IntegerField()
	link = models.CharField(max_length=255, blank=True)
	ingredients = models.ManyToManyField('Ingredient')
	tags = models.ManyToManyField('Tag')
	image = models.ImageField(null=True, upload_to=get_recipe_image_path)

	def __str__(self):
		return self.title

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
