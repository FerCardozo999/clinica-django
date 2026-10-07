"""Vistas de la app turnos: pedido, listado y cancelación de turnos."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import TurnoForm
from .models import Turno


@login_required
def mis_turnos(request):
    """Muestra los turnos de quien inició sesión, próximos y anteriores."""
    hoy = timezone.localdate()
    # select_related trae al profesional y su especialidad en la misma consulta.
    turnos = request.user.turnos.select_related("profesional__especialidad")
    contexto = {
        "proximos": turnos.filter(fecha__gte=hoy),
        "anteriores": turnos.filter(fecha__lt=hoy).order_by("-fecha", "-hora"),
    }
    return render(request, "turnos/mis_turnos.html", contexto)


@login_required
def pedir_turno(request):
    """Muestra el formulario de turnos y guarda los pedidos válidos."""
    # El turno nace con el paciente puesto: el formulario completa el resto.
    turno = Turno(paciente=request.user)

    if request.method == "POST":
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            try:
                # Si otra persona reservó el mismo horario entre la validación y
                # el guardado, la base lo rechaza: se avisa en vez de dar un error 500.
                with transaction.atomic():
                    form.save()
            except IntegrityError:
                form.add_error(
                    "hora", "Ese horario ya está ocupado. Probá con otro.")
            else:
                messages.success(
                    request,
                    "¡Listo! Tu turno quedó reservado. Te avisamos cuando esté confirmado.",
                )
                return redirect("turnos:mis_turnos")
    else:
        # Si se llega desde la ficha de un médico, viene elegido en la dirección.
        inicial = {"profesional": request.GET.get("profesional")}
        form = TurnoForm(instance=turno, initial=inicial)

    contexto = {"form": form}
    return render(request, "turnos/pedir_turno.html", contexto)


@login_required
@require_POST
def cancelar_turno(request, pk):
    """Cancela un turno propio que todavía está vigente."""
    # Buscar por paciente evita que alguien cancele turnos ajenos.
    turno = get_object_or_404(Turno, pk=pk, paciente=request.user)

    if turno.puede_cancelarse:
        turno.estado = Turno.Estado.CANCELADO
        turno.save()
        messages.success(request, "Tu turno fue cancelado.")
    else:
        messages.error(request, "Ese turno ya no se puede cancelar.")

    return redirect("turnos:mis_turnos")
