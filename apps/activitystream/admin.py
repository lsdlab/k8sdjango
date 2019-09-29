from django.contrib import admin

from .models import ActivityStream


@admin.register(ActivityStream)
class ActivityStreamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'actor',
        'actor_id',
        'verb',
        'object',
        'object_id',
        'target',
        'target_id',
        'deleted',
        'exchange',
        'routing_key',
        'ack',
        'created_at',
        'updated_at',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
