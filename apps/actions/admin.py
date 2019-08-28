from django.contrib import admin

from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
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
        'created_at',
        'updated_at',
    )
    list_filter = ('created_at', 'updated_at', 'deleted')
    date_hierarchy = 'created_at'
