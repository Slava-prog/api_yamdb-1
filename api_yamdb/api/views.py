from rest_framework import viewsets
# from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from reviews.models import Comment, Review, Title
from .serializers import (
    ReviewSerializer,
    CommentSerializer
)
# from .permissions import ...


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов класса Отзывов."""
    serializer_class = ReviewSerializer
    # permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=2, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов класса комментариев к отзывам."""
    serializer_class = CommentSerializer
    # permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=1, review=review)
