from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (CategorySerializer, CategoryCreateSerializer)
from core.mixins.viewset_mixins import (
    CreateAllowAnyMixin,
    CreateSerializerMixin
)
from core.swagger import CATEGORY_TAGS
from core.mixins.viewset_helpers import swagger_viewset_methods
from categories.models.category_models import Category

class CategoryViewSet(
    CreateAllowAnyMixin,
    CreateSerializerMixin,
    viewsets.ModelViewSet
):

    queryset = Category.objects.none()
    serializer_class = CategorySerializer
    create_serializer_class = CategoryCreateSerializer

    def get_queryset(self):
        return Category.objects.filter(
            user=self.request.user,
            deleted_at__isnull=True
        )

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'category_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    locals().update(swagger_viewset_methods(CATEGORY_TAGS, 'Categorias'))
