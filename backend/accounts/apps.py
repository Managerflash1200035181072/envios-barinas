from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuración de la aplicación de autenticación y roles."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
