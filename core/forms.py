"""Formularios de la app core."""

from django import forms

from .models import MensajeContacto


class ContactoForm(forms.ModelForm):
    """Formulario público para enviar un mensaje a la clínica."""

    class Meta:
        """Modelo, campos y controles del formulario."""

        model = MensajeContacto
        fields = ["nombre", "email", "telefono", "mensaje"]
        widgets = {"mensaje": forms.Textarea(attrs={"rows": 5})}

    def clean_mensaje(self):
        """Valida que el mensaje tenga un mínimo de contenido."""
        mensaje = self.cleaned_data["mensaje"]
        if len(mensaje) < 10:
            raise forms.ValidationError(
                "El mensaje es muy corto: contanos un poco más.")
        return mensaje
