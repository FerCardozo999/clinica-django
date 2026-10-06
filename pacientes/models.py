"""Modelos de la app pacientes: historia clínica de cada paciente."""

from django.conf import settings
from django.db import models
from django.utils import timezone

from clinica.models import Profesional


class EntradaHistoria(models.Model):
    """Registro de una consulta en la historia clínica de un paciente."""

    # PROTECT: una historia clínica no se borra junto con la cuenta.
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="entradas_historia",
    )
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.PROTECT,
        related_name="entradas_historia",
    )
    fecha = models.DateField("fecha de la consulta",
                             default=timezone.localdate)
    motivo = models.CharField("motivo de la consulta", max_length=200)
    diagnostico = models.TextField("diagnóstico")
    indicaciones = models.TextField("indicaciones", blank=True)
    creado = models.DateTimeField("cargado el", auto_now_add=True)

    class Meta:
        """Orden y nombres visibles de las entradas."""

        ordering = ["-fecha", "-creado"]
        verbose_name = "entrada de historia clínica"
        verbose_name_plural = "entradas de historia clínica"

    def __str__(self):
        """Devuelve la fecha, el paciente y el motivo de la consulta."""
        return f"{self.fecha:%d/%m/%Y} - {self.paciente}: {self.motivo}"
