"""Modelos de la app cuentas: perfil con los datos personales."""

from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """Datos personales de una cuenta que el modelo User no guarda."""

    # CASCADE: si se borra la cuenta, se borra también su perfil.
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    dni = models.CharField("DNI", max_length=8, blank=True)
    fecha_nacimiento = models.DateField(
        "fecha de nacimiento",
        null=True,
        blank=True,
    )
    telefono = models.CharField("teléfono", max_length=30, blank=True)
    obra_social = models.CharField("obra social", max_length=100, blank=True)

    class Meta:
        """Nombres visibles del perfil."""

        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        """Devuelve a qué cuenta pertenece el perfil."""
        return f"Perfil de {self.usuario}"
