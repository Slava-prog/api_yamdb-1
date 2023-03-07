from django.urls import path, include
from rest_framework import routers
from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TitleViewSet, GenreViewSet, APISignUp, UserViewSet, CommentViewSet, ReviewViewSet, TitleViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    'titles',
    TitleViewSet,
)
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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignUp.as_view()),
]
