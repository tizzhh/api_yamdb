from rest_framework import filters, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)

from api.permissions import IsAdminOrSuperUserReadOnly


class CategoryGenreBaseViewSet(
        ListModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet,
):
    permission_classes = (IsAdminOrSuperUserReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
