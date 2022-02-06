from django.apps import AppConfig


class RacingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sbyra_src.racing"

    def ready(self):
        import sbyra_src.racing.signals
