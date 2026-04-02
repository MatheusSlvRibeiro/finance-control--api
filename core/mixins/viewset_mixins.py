from rest_framework import permissions

class CreateAllowAnyMixin:
    create_serializer_classes = [permissions.AllowAny]
    default_serializer_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [permission() for permission in self.create_serializer_classes]
        return [permission() for permission in self.default_serializer_classes]
    

class CreateSerializerMixin:
    create_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'create' and self.create_serializer_class:
            return self.create_serializer_class
        return super().get_serializer_class()