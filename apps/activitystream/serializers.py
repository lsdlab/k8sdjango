from rest_framework import serializers

from .models import ActivityStream


class ActivityStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityStream
        fields = ('id', 'actor', 'actor_id', 'verb', 'object', 'object_id',
                  'target', 'target_id', 'deleted', 'exchange', 'routing_key',
                  'ack', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ActivityStreamCreateSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(required=True)
    verb = serializers.CharField(required=True)

    class Meta:
        model = ActivityStream
        fields = ('id', 'actor', 'actor_id', 'verb', 'object', 'object_id',
                  'target', 'target_id', 'deleted', 'exchange', 'routing_key',
                  'ack', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
