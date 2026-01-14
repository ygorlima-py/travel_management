from django.apps import AppConfig


class BillingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billings'

    def ready(self):
        import billings.signals  # ensure your signals are imported