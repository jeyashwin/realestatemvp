from django.apps import AppConfig


class PropertyConfig(AppConfig):
    name = 'property'

    def ready(self):
        from .taskSchedulers import startScheduler
        startScheduler()
