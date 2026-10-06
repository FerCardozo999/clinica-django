"""Configuración del panel admin para la app turnos."""

from django.contrib import admin

from .models import Turno


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    """Listado, filtros y búsqueda de turnos en el panel admin."""

    list_display = ("fecha", "hora", "profesional", "paciente", "estado")
    list_filter = ("estado", "fecha", "profesional")
    list_editable = ("estado",)
    search_fields = (
        "paciente__username",
        "paciente__last_name",
        "profesional__apellido",
    )
    date_hierarchy = "fecha"
