"""Vistas de la app core: páginas públicas de Génesis Salud."""
from django.shortcuts import render


def inicio(request):
    """Muestra la pagina de inicio de la clinica."""
    return render(request, "core/inicio.html")
