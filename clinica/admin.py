"""Configuración del panel de administración de la app clinica."""

from django.contrib import admin

from .models import Especialidad, Profesional


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    """Panel de especialidades: alta, baja y slug automático."""

    list_display = ("nombre", "slug", "activa")
    list_editable = ("activa",)
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    """Panel de profesionales: alta, baja y asignación a especialidades."""

    list_display = ("apellido", "nombre", "especialidad",
                    "matricula", "activo")
    list_editable = ("activo",)
    list_filter = ("especialidad", "activo")
    search_fields = ("nombre", "apellido", "matricula")
