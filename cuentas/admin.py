"""Configuración del panel admin para la app cuentas."""

from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """Listado y búsqueda de perfiles en el panel admin."""

    list_display = ("usuario", "dni", "telefono", "obra_social")
    search_fields = ("usuario__username", "usuario__last_name", "dni")
