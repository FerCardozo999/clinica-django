"""Vistas de la app clinica: especialidades y profesionales."""

from django.shortcuts import get_object_or_404, render

from .models import Especialidad, Profesional


def lista_especialidades(request):
    """Muestra todas las especialidades activas."""
    especialidades = Especialidad.objects.filter(activa=True)
    contexto = {"especialidades": especialidades}
    return render(request, "clinica/especialidades.html", contexto)


def detalle_especialidad(request, slug):
    """Muestra una especialidad con sus profesionales activos."""
    especialidad = get_object_or_404(Especialidad, slug=slug, activa=True)
    # select_related evita una consulta extra por tarjeta al mostrar la especialidad.
    profesionales = especialidad.profesionales.filter(
        activo=True,
    ).select_related("especialidad")
    contexto = {"especialidad": especialidad, "profesionales": profesionales}
    return render(request, "clinica/especialidad_detalle.html", contexto)


def lista_profesionales(request):
    """Muestra todos los profesionales activos de especialidades activas."""
    profesionales = Profesional.objects.filter(
        activo=True,
        especialidad__activa=True,
    ).select_related("especialidad")
    contexto = {"profesionales": profesionales}
    return render(request, "clinica/profesionales.html", contexto)


def detalle_profesional(request, pk):
    """Muestra la ficha de un profesional activo de una especialidad activa."""
    profesional = get_object_or_404(
        Profesional.objects.select_related("especialidad"),
        pk=pk,
        activo=True,
        especialidad__activa=True,
    )
    contexto = {"profesional": profesional}
    return render(request, "clinica/profesional_detalle.html", contexto)
