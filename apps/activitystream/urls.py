from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActivityStreamViewSet

router = DefaultRouter()
router.register('activitystream', ActivityStreamViewSet)

app_name = 'activitystream'
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
