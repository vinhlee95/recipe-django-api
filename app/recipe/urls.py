from rest_framework import routers
from django.urls import path, include
from recipe import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
	path('', include(router.urls))
]