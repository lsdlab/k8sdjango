from django.db import models
from apps.core.models import TimestampedModel


class Action(TimestampedModel):
    TOPIC = '1'
    DIRECT = '2'
    FANOUT = '3'
    EXCHANGE_CHOICES = (
        (TOPIC, '主题'),
        (DIRECT, '直连'),
        (FANOUT, '扇形'),
    )

    actor = models.CharField(max_length=255, blank=False)
    actor_id = models.CharField(max_length=255, blank=False)
    verb = models.CharField(max_length=255, blank=False)
    object = models.CharField(max_length=255, blank=True, default='')
    object_id = models.CharField(max_length=255, blank=True, default='')
    target = models.CharField(max_length=255, blank=True, default='')
    target_id = models.CharField(max_length=255, blank=True, default='')
    deleted = models.BooleanField(default=False)

    exchange = models.TextField(max_length=1, choices=EXCHANGE_CHOICES, blank=True, null=True)
    routing_key = models.CharField(max_length=255, blank=True, null=True)
    ack = models.NullBooleanField(default=null)

    def __str__(self):
        return self.actor + '_' + self.verb

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = '动态'
        verbose_name_plural = verbose_name
