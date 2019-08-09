from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='djshop RESTful API')

admin.site.site_header = "djshop Admin"
admin.site.site_title = "djshop Admin"
admin.site.index_title = "Welcome to djshop Admin"

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('admin/', admin.site.urls),
        path('api/docs/', schema_view),
        path('api/v1/',
             include('rest_framework.urls', namespace='rest_framework')),
        path('api/v1/jwt/token-auth/', obtain_jwt_token, name='token-auth'),
        path(
            'api/v1/jwt/token-refresh/',
            refresh_jwt_token,
            name='token-refresh'),
    ] + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/docs/', schema_view),
        path('api/v1/',
             include('rest_framework.urls', namespace='rest_framework')),
        path('api/v1/jwt/token-auth/', obtain_jwt_token, name='token-auth'),
        path(
            'api/v1/jwt/token-refresh/',
            refresh_jwt_token,
            name='token-refresh'),
    ] + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
