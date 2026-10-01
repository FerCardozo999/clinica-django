"""URLs de la app core: páginas públicas del sitio."""
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.inicio, name="inicio"),
]
