"""Formularios de la app cuentas."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Perfil

User = get_user_model()


class RegistroForm(UserCreationForm):
    """Formulario para que una persona cree su cuenta en la clínica."""

    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    email = forms.EmailField(label="Correo electrónico")

    class Meta(UserCreationForm.Meta):
        """Modelo y campos del formulario."""

        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_email(self):
        """Valida que el correo no pertenezca a otra cuenta."""
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo.")
        return email


class UsuarioForm(forms.ModelForm):
    """Formulario para editar el nombre, el apellido y el correo."""

    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    email = forms.EmailField(label="Correo electrónico")

    class Meta:
        """Modelo y campos del formulario."""

        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        """Valida que el correo no pertenezca a otra cuenta."""
        email = self.cleaned_data["email"].lower()
        otras_cuentas = User.objects.exclude(pk=self.instance.pk)
        if otras_cuentas.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo.")
        return email


class PerfilForm(forms.ModelForm):
    """Formulario para editar los datos personales del perfil."""

    class Meta:
        """Modelo, campos y controles del formulario."""

        model = Perfil
        fields = ["dni", "fecha_nacimiento", "telefono", "obra_social"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }

    def clean_dni(self):
        """Valida que el DNI tenga solo números y no esté repetido."""
        dni = self.cleaned_data["dni"]
        if not dni:
            return dni
        if not dni.isdigit() or len(dni) < 7:
            raise forms.ValidationError(
                "Ingresá el DNI sin puntos, solo números.")
        otros_perfiles = Perfil.objects.exclude(pk=self.instance.pk)
        if otros_perfiles.filter(dni=dni).exists():
            raise forms.ValidationError(
                "Ese DNI ya está cargado en otra cuenta.")
        return dni

    def clean_fecha_nacimiento(self):
        """Valida que la fecha de nacimiento no sea futura."""
        fecha = self.cleaned_data["fecha_nacimiento"]
        if fecha and fecha > timezone.localdate():
            raise forms.ValidationError(
                "La fecha de nacimiento no puede ser futura.")
        return fecha
