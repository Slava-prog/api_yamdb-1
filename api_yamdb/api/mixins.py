from rest_framework import filters, mixins, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminModeratorAuthororReadOnly


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet,):

    permission_classes = (IsAdminModeratorAuthororReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class CreateMixin(CreateModelMixin, viewsets.GenericViewSet):
    pass
