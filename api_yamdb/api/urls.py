from django.urls import include, path
from rest_framework import routers

from .views import APISignUp, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignUp.as_view()),
]
