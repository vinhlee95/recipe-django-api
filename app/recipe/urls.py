from rest_framework import routers
from django.urls import path, include
from . import views

app_name = 'recipe'
router = routers.DefaultRouter(trailing_slash=False)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

urlpatterns = [
	path('', include(router.urls))
]