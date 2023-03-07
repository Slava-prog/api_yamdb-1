from rest_framework import mixins, viewsets, filters
from rest_framework import PageNumberPagination
from .permissions import ...

class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet,):

    permission_classes = ...
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination