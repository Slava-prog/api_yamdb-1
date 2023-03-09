import uuid

from django.core.mail import send_mail
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from users.models import CustomUser
from reviews.models import Category, Genre, Title, Comment, Review, Title
from .permissions import IsAdmin, IsAdminModeratorAuthororReadOnly
from .mixins import CreateDestroyListViewSet
# from .filters import TitleFilter
from .serializers import (SignUpSerializer, UserSerializer,
                          UserSerializerReadOnly, CategorySerializer,
                          GenreSerializer, TitleGETSerializer,
                          TitlePOSTSerializer, ReviewSerializer,
                          CommentSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['POST'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def create_user(self, request):
        serializer = UserSerializerReadOnly(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,),
            url_path='me')
    def change_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.role == 'admin' or request.user.is_staff:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserSerializerReadOnly(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APISignUp(APIView):
    def post(self, request):
        confirmation_code = str(uuid.uuid4())
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                username=request.data['username'],
                confirmation_code=confirmation_code
            )
            send_mail(
                'Код подтверждения на YamDB',
                f'Для подтверждения регистрации используйте код:'
                f'{confirmation_code}',
                'from@example.com',
                [serializer.data['email']],
                fail_silently=False
            )
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для объектов класса Category"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для объектов класса Genre"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов класса Title"""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminModeratorAuthororReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    # filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitlePOSTSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов класса Отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthororReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов класса комментариев к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthororReadOnly,)
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
