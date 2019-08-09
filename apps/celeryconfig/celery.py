from celery import Celery, platforms
platforms.C_FORCE_ROOT = True
from django.apps import apps, AppConfig
from django.conf import settings


app = Celery('apps')
app.config_from_object('django.conf:settings')


class CeleryConfig(AppConfig):
    name = 'apps.celeryconfig'
    verbose_name = 'Celery Config'

    def ready(self):
        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()
        ]
        app.autodiscover_tasks(lambda: installed_apps, force=True)
