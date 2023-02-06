from django.apps import AppConfig

# from django.conf import settings
# import beeline


class MainConfig(AppConfig):
    name = "antisocial.main"

    def ready(self):
        pass
