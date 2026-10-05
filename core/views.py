"""Vistas de la app core: páginas públicas de Génesis Salud."""

from django.contrib import messages
from django.shortcuts import redirect, render

from clinica.models import Especialidad, Profesional

from .forms import ContactoForm


def inicio(request):
    """Muestra la página de inicio con las especialidades destacadas."""
    especialidades = Especialidad.objects.filter(activa=True)[:6]
    contexto = {"especialidades": especialidades}
    return render(request, "core/inicio.html", contexto)


def nosotros(request):
    """Muestra la página institucional con los números de la clínica."""
    contexto = {
        "total_especialidades": Especialidad.objects.filter(activa=True).count(),
        "total_profesionales": Profesional.objects.filter(
            activo=True,
            especialidad__activa=True,
        ).count(),
    }
    return render(request, "core/nosotros.html", contexto)


def contacto(request):
    """Muestra el formulario de contacto y guarda los mensajes válidos."""
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "¡Gracias! Recibimos tu mensaje y te vamos a responder pronto.",
            )
            return redirect("core:contacto")
    else:
        form = ContactoForm()

    contexto = {"form": form}
    return render(request, "core/contacto.html", contexto)
