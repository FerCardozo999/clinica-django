"""URLs de la app clinica: especialidades y profesionales."""

from django.urls import path

from . import views

app_name = "clinica"

urlpatterns = [
    path("especialidades/", views.lista_especialidades, name="especialidades"),
    path(
        "especialidades/<slug:slug>/",
        views.detalle_especialidad,
        name="especialidad_detalle",
    ),
    path("profesionales/", views.lista_profesionales, name="profesionales"),
    path(
        "profesionales/<int:pk>/",
        views.detalle_profesional,
        name="profesional_detalle",
    ),
]
