from django.contrib import admin
from django.urls import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.urls import path

from CRMmodule import settings
from CRMmodule.authentication import BearerTokenAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version='v1',
        description="API для модуля CRM",
    ),
    public=True,
    authentication_classes=(BearerTokenAuthentication,),
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

