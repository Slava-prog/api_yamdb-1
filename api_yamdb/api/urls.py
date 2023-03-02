from django.urls import path, include
from rest_framework import routers

from .views import CategoryViewSet, TitleViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='titles')
