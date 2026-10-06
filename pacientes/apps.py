"""Configuración de la app pacientes."""

from django.apps import AppConfig


class PacientesConfig(AppConfig):
    """Registra la app pacientes y su nombre visible en el admin."""

    name = "pacientes"
    verbose_name = "Pacientes"
