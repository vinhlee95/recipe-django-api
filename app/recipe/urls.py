from rest_framework import routers
from django.urls import path, include
from . import views

app_name = 'recipe'
router = routers.DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)

urlpatterns = [
	path('', include(router.urls))
]