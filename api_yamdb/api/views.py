from django.shortcuts import render
from .mixins import CreateDestroyListViewSet
from reviews.models import Category, Genre, Title
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleGETSerializer,
                          TitlePOSTSerializer)
from django.db.models import Avg
from .filters import TitleFilter
from rest_framework import viewsets


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
    permission_classes  = ...
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitlePOSTSerializer
