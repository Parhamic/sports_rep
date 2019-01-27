from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'sports_app'

    def ready(self):
        from . import signals
