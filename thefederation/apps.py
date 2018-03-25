from django.apps import AppConfig


class TheFederationConfig(AppConfig):
    name = "thefederation"
    verbose_name = "The Federation"

    def ready(self):
        """Import our signals."""
        pass
