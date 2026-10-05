"""Vistas de la app cuentas: registro y perfil de usuarios."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PerfilForm, RegistroForm, UsuarioForm
from .models import Perfil


def registro(request):
    """Crea una cuenta nueva y deja a la persona con la sesión iniciada."""
    if request.user.is_authenticated:
        return redirect("core:inicio")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(
                request,
                f"¡Hola, {usuario.first_name}! Tu cuenta ya está creada.",
            )
            return redirect("core:inicio")
    else:
        form = RegistroForm()

    contexto = {"form": form}
    return render(request, "cuentas/registro.html", contexto)


@login_required
def perfil(request):
    """Muestra los datos personales de quien inició sesión."""
    perfil_usuario, _ = Perfil.objects.get_or_create(usuario=request.user)
    contexto = {"perfil": perfil_usuario}
    return render(request, "cuentas/perfil.html", contexto)


@login_required
def editar_perfil(request):
    """Permite a la persona modificar sus datos personales."""
    perfil_usuario, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, instance=perfil_usuario)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Tus datos se guardaron correctamente.")
            return redirect("cuentas:perfil")
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil_usuario)

    contexto = {"usuario_form": usuario_form, "perfil_form": perfil_form}
    return render(request, "cuentas/editar_perfil.html", contexto)
