from django.core.cache import cache
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ActivityStream
from .serializers import ActivityStreamSerializer, ActivityStreamCreateSerializer

def cache_acitivty_stream(user):
    actor_id = str(user.id)
    cache_key = actor_id + '_activitystream'
    queryset = ActivityStream.objects.filter(actor_id=actor_id)[:10]
    serializer = ActivityStreamSerializer(queryset, many=True)
    cache.set(cache_key, serializer.data, timeout=None)

class ActivityStreamViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = ActivityStream.objects.all()
    serializer_class = ActivityStreamSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'create':
            return ActivityStreamCreateSerializer
        else:
            return ActivityStreamSerializer

    def perform_create(self, serializer):
        cache_acitivty_stream(self.request.user)
        serializer.save()

    def list(self, request):
        user = request.user
        actor_id = str(user.id)
        cache_key = str(user.id) + '_activitystream'
        cache_value = cache.get(cache_key)
        if cache_value:
            return Response(cache_value, status=status.HTTP_200_OK)
        else:
            queryset = ActivityStream.objects.filter(actor_id=actor_id)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ActivityStreamSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ActivityStreamSerializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=None)
            return Response(serializer.data, status=status.HTTP_200_OK)
