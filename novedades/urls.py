"""URLs de la app novedades: blog de la clínica."""

from django.urls import path

from . import views

app_name = "novedades"

urlpatterns = [
    path("", views.lista_novedades, name="lista"),
    path("<slug:slug>/", views.detalle_novedad, name="detalle"),
]
