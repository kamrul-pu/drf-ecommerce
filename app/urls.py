

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-user/', include('admin_user.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
    ),
    path('user/', include('user.urls')),
    path('store/', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),

"""DRF yasg"""


# schema_view = get_schema_view(
#     openapi.Info(
#         title="Ecommerce API",
#         default_version='v1',
#         description="Sample Description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     re_path(r'^swagger(?P<format>\.json|\.yaml)$',
#             schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     path('api/docs/', schema_view.with_ui('swagger',
#                                           cache_timeout=0), name='schema-swagger-ui'),
#     path('api/schema/', schema_view.with_ui('redoc',
#                                             cache_timeout=0), name='schema-redoc'),
#     path('api/user/', include('user.urls')),
#     path('api/store/', include('store.urls')),
# ]
