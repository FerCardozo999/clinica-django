"""Configuración del panel admin para la app core."""

from django.contrib import admin

from .models import MensajeContacto


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    """Listado de los mensajes recibidos desde la web."""

    list_display = ("nombre", "email", "creado", "leido")
    list_filter = ("leido",)
    list_editable = ("leido",)
    search_fields = ("nombre", "email", "mensaje")
    readonly_fields = ("nombre", "email", "telefono", "mensaje", "creado")
