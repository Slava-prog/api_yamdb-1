from django.urls import path, include
from rest_framework import routers
from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TitleViewSet, GenreViewSet, APISignUp, UserViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignUp.as_view()),
]