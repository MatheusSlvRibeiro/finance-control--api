from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (AccountSerializer, AccountCreateSerializer)
from core.mixins.viewset_mixins import (
    CreateAllowAnyMixin,
    CreateSerializerMixin
)
from core.swagger import ACCOUNT_TAGS
from core.mixins.viewset_helpers import swagger_viewset_methods
from accounts.models.account_models import Account

class AccountViewSet(
    CreateAllowAnyMixin,
    CreateSerializerMixin,
    viewsets.ModelViewSet
):

    queryset = Account.objects.none()
    serializer_class = AccountSerializer
    create_serializer_class = AccountCreateSerializer

    def get_queryset(self):
        return Account.objects.filter(
            user=self.request.user,
            deleted_at__isnull=True
        )

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return AccountCreateSerializer
        return super().get_serializer_class()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'account_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    locals().update(swagger_viewset_methods(ACCOUNT_TAGS, 'Contas'))
