from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import (UserSerializer, UserCreateSerializer)
from core.swagger import USER_TAGS
from core.mixins.viewset_helpers import swagger_viewset_methods

User = get_user_model()

class  UserViewSet(viewsets.ModelViewSet):
    """ Viewset para gerenciar usuários """
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.filter(deleted_at__isnull=True)
        return User.objects.filter(pk=self.request.user.pk, deleted_at__isnull=True)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_staff']
    search_fields = ['name', 'email',]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    locals().update(swagger_viewset_methods(USER_TAGS, 'usuário'))

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
