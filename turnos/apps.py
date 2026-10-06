"""Configuración de la app turnos."""

from django.apps import AppConfig


class TurnosConfig(AppConfig):
    """Registra la app turnos y su nombre visible en el admin."""

    name = "turnos"
    verbose_name = "Turnos"
