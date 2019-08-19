from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

app_name = 'users'
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
