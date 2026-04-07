from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Finance Control API",
        default_version='v1',
        description="API REST para gestão de despesas pessoais do sistema Finance Control",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

system_patterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Endpoints v1

    path('api/v1/', include([
        path('', include('users.urls')),
        path('', include('accounts.urls')),
        path('', include('categories.urls')),
        path('', include('transactions.urls')),
    ]))

]

swaggerpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 
]

urlpatterns = swaggerpatterns + system_patterns