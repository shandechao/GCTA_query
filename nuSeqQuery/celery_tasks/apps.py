from django.apps import AppConfig

class CeleryTasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_tasks'

    