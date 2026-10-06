"""Vistas de la app pacientes: panel de trabajo del profesional."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from turnos.models import Turno

from .forms import EntradaHistoriaForm
from .models import EntradaHistoria
from .permisos import obtener_profesional

User = get_user_model()


def pacientes_de(profesional):
    """Devuelve las cuentas que pidieron al menos un turno con el profesional."""
    # distinct() evita que un paciente con varios turnos aparezca repetido.
    return User.objects.filter(turnos__profesional=profesional).distinct()


@login_required
def agenda(request):
    """Muestra los turnos vigentes del profesional, de hoy y próximos."""
    profesional = obtener_profesional(request.user)
    hoy = timezone.localdate()
    # select_related trae la cuenta y el perfil del paciente en la misma consulta.
    vigentes = profesional.turnos.exclude(
        estado=Turno.Estado.CANCELADO
    ).select_related("paciente__perfil")
    contexto = {
        "profesional": profesional,
        "hoy": hoy,
        "turnos_hoy": vigentes.filter(fecha=hoy),
        "turnos_proximos": vigentes.filter(fecha__gt=hoy),
    }
    return render(request, "pacientes/agenda.html", contexto)


@login_required
@require_POST
def actualizar_turno(request, pk):
    """Confirma o cancela un turno de la agenda del profesional."""
    profesional = obtener_profesional(request.user)
    # Buscar por profesional evita modificar turnos de otros médicos.
    turno = get_object_or_404(Turno, pk=pk, profesional=profesional)
    accion = request.POST.get("accion")

    if not turno.puede_cancelarse:
        messages.error(request, "Ese turno ya no se puede modificar.")
    elif accion == "confirmar":
        turno.estado = Turno.Estado.CONFIRMADO
        turno.save()
        messages.success(request, "Turno confirmado.")
    elif accion == "cancelar":
        turno.estado = Turno.Estado.CANCELADO
        turno.save()
        messages.success(request, "Turno cancelado. El horario quedó libre.")
    else:
        messages.error(request, "No se reconoció la acción pedida.")

    return redirect("pacientes:agenda")


@login_required
def mis_pacientes(request):
    """Lista los pacientes del profesional, con búsqueda por nombre o DNI."""
    profesional = obtener_profesional(request.user)
    busqueda = request.GET.get("q", "").strip()
    pacientes = pacientes_de(profesional).select_related("perfil")

    if busqueda:
        pacientes = pacientes.filter(
            Q(first_name__icontains=busqueda)
            | Q(last_name__icontains=busqueda)
            | Q(perfil__dni__icontains=busqueda)
        )

    contexto = {
        "pacientes": pacientes.order_by("last_name", "first_name"),
        "busqueda": busqueda,
    }
    return render(request, "pacientes/lista.html", contexto)


@login_required
def ficha_paciente(request, pk):
    """Muestra los datos de un paciente y su historia clínica."""
    profesional = obtener_profesional(request.user)
    # Buscar entre sus pacientes evita abrir fichas de quien nunca atendió.
    paciente = get_object_or_404(pacientes_de(profesional), pk=pk)
    contexto = {
        "paciente": paciente,
        "entradas": paciente.entradas_historia.select_related(
            "profesional__especialidad"
        ),
    }
    return render(request, "pacientes/ficha.html", contexto)


@login_required
def nueva_entrada(request, pk):
    """Registra una consulta en la historia clínica de un paciente."""
    profesional = obtener_profesional(request.user)
    paciente = get_object_or_404(pacientes_de(profesional), pk=pk)
    # La entrada nace con paciente y profesional: el formulario completa el resto.
    entrada = EntradaHistoria(paciente=paciente, profesional=profesional)

    if request.method == "POST":
        form = EntradaHistoriaForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "La consulta quedó registrada en la historia clínica.",
            )
            return redirect("pacientes:ficha", pk=paciente.pk)
    else:
        form = EntradaHistoriaForm(instance=entrada)

    contexto = {"form": form, "paciente": paciente}
    return render(request, "pacientes/nueva_entrada.html", contexto)
