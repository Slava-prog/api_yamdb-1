from django.urls import path, include
from rest_framework import routers

from .views import (CategoryViewSet, TitleViewSet,
                    GenreViewSet, SignUpViewSet,
                    UserViewSet, CommentViewSet,
                    ReviewViewSet, TitleViewSet,
                    ObtainTokenViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/signup/',
        SignUpViewSet.as_view(),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        ObtainTokenViewSet.as_view({'post': 'create'}),
        name='token',
    ),
]
