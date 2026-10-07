"""Configuración de la app novedades."""

from django.apps import AppConfig


class NovedadesConfig(AppConfig):
    """Registra la app novedades y su nombre visible en el admin."""

    name = "novedades"
    verbose_name = "Novedades"
