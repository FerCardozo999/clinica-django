"""Configuracion del panel admin para la app novedades"""

from django.contrib import admin

from .models import Novedad


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    """Listado, filtros y carga de novedades en el panel"""

    list_display = ("titulo", "fecha_publicacion", "autor", "publicada")
    list_filter = ("publicada", "fecha_publicacion")
    list_editable = ("publicada",)
    search_fields = ("titulo", "resumen", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "fecha_publicacion"
    exclude = ("autor",)

    def save_model(self, request, obj, form, change):
        """Asigna como autor a quien carga la novedad por primera vez"""
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)
