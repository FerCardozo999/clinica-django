"""URLs de la app pacientes: panel del profesional."""

from django.urls import path

from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.agenda, name="agenda"),
    path(
        "turnos/<int:pk>/actualizar/",
        views.actualizar_turno,
        name="actualizar_turno",
    ),
    path("pacientes/", views.mis_pacientes, name="lista"),
    path("pacientes/<int:pk>/", views.ficha_paciente, name="ficha"),
    path(
        "pacientes/<int:pk>/consulta/",
        views.nueva_entrada,
        name="nueva_entrada",
    ),
]
