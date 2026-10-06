"""Formularios de la app pacientes."""

from django import forms
from django.utils import timezone

from .models import EntradaHistoria

LARGO_MINIMO_DIAGNOSTICO = 10


class EntradaHistoriaForm(forms.ModelForm):
    """Formulario para registrar una consulta en la historia clínica."""

    class Meta:
        """Modelo, campos y controles del formulario."""

        model = EntradaHistoria
        fields = ["fecha", "motivo", "diagnostico", "indicaciones"]
        widgets = {
            "fecha": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "diagnostico": forms.Textarea(attrs={"rows": 4}),
            "indicaciones": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_fecha(self):
        """Valida que la consulta no tenga una fecha futura."""
        fecha = self.cleaned_data["fecha"]
        if fecha > timezone.localdate():
            raise forms.ValidationError(
                "La fecha de la consulta no puede ser posterior a hoy."
            )
        return fecha

    def clean_diagnostico(self):
        """Valida que el diagnóstico tenga un mínimo de detalle."""
        diagnostico = self.cleaned_data["diagnostico"]
        if len(diagnostico) < LARGO_MINIMO_DIAGNOSTICO:
            raise forms.ValidationError(
                "El diagnóstico es muy corto: sumá un poco más de detalle."
            )
        return diagnostico
