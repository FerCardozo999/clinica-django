"""Formularios de la app turnos."""

from datetime import time, timedelta

from django import forms
from django.utils import timezone

from clinica.models import Profesional

from .models import Turno

# Reglas de atención de la clínica: lunes a viernes de 8 a 20 h.
HORA_APERTURA = 8
HORA_CIERRE = 20
DIAS_ANTICIPACION = 60


def generar_horarios():
    """Devuelve los horarios de atención, cada media hora, como opciones."""
    horarios = [("", "Elegí un horario")]
    for hora in range(HORA_APERTURA, HORA_CIERRE):
        for minutos in (0, 30):
            horario = time(hora, minutos)
            horarios.append((f"{horario:%H:%M}", f"{horario:%H:%M} h"))
    return horarios


class ProfesionalChoiceField(forms.ModelChoiceField):
    """Desplegable de profesionales que muestra también la especialidad."""

    def label_from_instance(self, obj):
        """Devuelve el texto de cada opción del desplegable."""
        return f"{obj.especialidad} - {obj}"


class TurnoForm(forms.ModelForm):
    """Formulario para que un paciente pida un turno."""

    profesional = ProfesionalChoiceField(
        queryset=(
            Profesional.objects.filter(activo=True, especialidad__activa=True)
            .select_related("especialidad")
            .order_by("especialidad__nombre", "apellido", "nombre")
        ),
        empty_label="Elegí un profesional",
    )
    hora = forms.ChoiceField(label="Horario", choices=generar_horarios())

    class Meta:
        """Modelo, campos y controles del formulario."""

        model = Turno
        fields = ["profesional", "fecha", "hora", "motivo"]
        widgets = {
            "fecha": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }

    def clean_fecha(self):
        """Valida que la fecha sea un día hábil dentro del plazo permitido."""
        fecha = self.cleaned_data["fecha"]
        hoy = timezone.localdate()
        if fecha < hoy:
            raise forms.ValidationError(
                "La fecha no puede ser anterior a hoy.")
        if fecha > hoy + timedelta(days=DIAS_ANTICIPACION):
            raise forms.ValidationError(
                f"Los turnos se piden con hasta {DIAS_ANTICIPACION} días de anticipación."
            )
        # weekday() numera los días: 0 es lunes y 6 es domingo.
        if fecha.weekday() >= 5:
            raise forms.ValidationError(
                "La clínica atiende de lunes a viernes.")
        return fecha

    def clean_hora(self):
        """Convierte el horario elegido, que llega como texto, en una hora."""
        return time.fromisoformat(self.cleaned_data["hora"])

    def clean(self):
        """Valida las reglas que cruzan profesional, fecha y hora."""
        datos = super().clean()
        profesional = datos.get("profesional")
        fecha = datos.get("fecha")
        hora = datos.get("hora")

        # Si algún campo ya tiene un error, no hay nada que cruzar.
        if not (profesional and fecha and hora):
            return datos

        ahora = timezone.localtime()
        if fecha == ahora.date() and hora <= ahora.time():
            self.add_error("hora", "Ese horario ya pasó. Elegí uno más tarde.")

        vigentes = Turno.objects.filter(fecha=fecha, hora=hora).exclude(
            estado=Turno.Estado.CANCELADO
        )
        if vigentes.filter(profesional=profesional).exists():
            self.add_error(
                "hora", "Ese horario ya está ocupado. Probá con otro.")
        elif vigentes.filter(paciente=self.instance.paciente).exists():
            self.add_error("hora", "Ya tenés otro turno en ese día y horario.")

        return datos
