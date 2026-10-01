"""Configuración de la app clinica."""
from django.apps import AppConfig


class ClinicaConfig(AppConfig):
    """Registra la app clinica y su nombre visible en el admin."""
    name = "clinica"
    verbose_name = "Clínica"
