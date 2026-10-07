"""Configuración de la app cuentas."""

from django.apps import AppConfig


class CuentasConfig(AppConfig):
    """Registra la app cuentas y su nombre visible en el admin."""

    name = "cuentas"
    verbose_name = "Cuentas"
