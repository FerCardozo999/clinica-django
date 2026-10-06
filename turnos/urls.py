"""URLs de la app turnos: listado y cancelación."""

from django.urls import path

from . import views

app_name = "turnos"

urlpatterns = [
    path("", views.mis_turnos, name="mis_turnos"),
    path("nuevo/", views.pedir_turno, name="pedir"),
    path("<int:pk>/cancelar/", views.cancelar_turno, name="cancelar"),
]
