"""Configuración de la app core."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Registra la app core y su nombre visible en el admin."""

    name = "core"
    verbose_name = "Sitio web"
