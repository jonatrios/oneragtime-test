from django.apps import AppConfig


class InvestmentsFeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.investments_fees'

    def ready(self) -> None:
        import apps.investments_fees.signals
