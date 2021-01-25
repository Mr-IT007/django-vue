from django.apps import AppConfig


class UserAuthConfig(AppConfig):
    name = 'apps.userAuth'

    def ready(self):
        from . import signals
