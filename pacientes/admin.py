"""Configuración del panel admin para la app pacientes."""

from django.contrib import admin

from .models import EntradaHistoria


@admin.register(EntradaHistoria)
class EntradaHistoriaAdmin(admin.ModelAdmin):
    """Listado, filtros y búsqueda de entradas de historia clínica."""

    list_display = ("fecha", "paciente", "profesional", "motivo")
    list_filter = ("profesional", "fecha")
    search_fields = ("paciente__username", "paciente__last_name", "motivo")
