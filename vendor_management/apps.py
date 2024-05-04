from django.apps import AppConfig


class VendorManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendor_management'

    def ready(self):
        from . import signals
        signals.metric_update.connect(signals.process_po_info)
