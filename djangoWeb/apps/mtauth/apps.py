from django.apps import AppConfig


class MtAuthConfig(AppConfig):
    name = 'apps.mtauth'

    def ready(self):
        from . import signals
