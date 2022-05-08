from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sbyra_src.accounts"

    def ready(self):
        import sbyra_src.accounts.signals
