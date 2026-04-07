from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (TransactionSerializer, TransactionCreateSerializer)
from core.mixins.viewset_mixins import CreateSerializerMixin
from core.swagger import TRANSACTION_TAGS
from core.mixins.viewset_helpers import swagger_viewset_methods
from transactions.models.transaction_models import Transaction

class TransactionViewSet(
    CreateSerializerMixin,
    viewsets.ModelViewSet
):

    queryset = Transaction.objects.none()
    serializer_class = TransactionSerializer
    create_serializer_class = TransactionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TransactionCreateSerializer
        return TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            account__user=self.request.user,
            deleted_at__isnull=True
        ).select_related('category')

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'category', 'date']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    locals().update(swagger_viewset_methods(TRANSACTION_TAGS, 'Contas'))