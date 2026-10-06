"""Modelos de la app turnos: reservas de atención con un profesional."""

from django.conf import settings
from django.db import models
from django.utils import timezone

from clinica.models import Profesional


class Turno(models.Model):
    """Reserva de un paciente con un profesional en un día y horario."""

    class Estado(models.TextChoices):
        """Estados posibles de un turno."""

        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADO = "confirmado", "Confirmado"
        CANCELADO = "cancelado", "Cancelado"

    # CASCADE: si se borra la cuenta, se borran también sus turnos.
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="turnos",
    )
    # PROTECT impide borrar un profesional que tiene turnos cargados.
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.PROTECT,
        related_name="turnos",
    )
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(
        "motivo de la consulta",
        max_length=200,
        blank=True,
    )
    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    creado = models.DateTimeField("creado el", auto_now_add=True)

    class Meta:
        """Orden, nombres visibles y reglas de los turnos."""

        ordering = ["fecha", "hora"]
        verbose_name = "turno"
        verbose_name_plural = "turnos"
        constraints = [
            # Un profesional no puede tener dos turnos vigentes a la misma hora.
            models.UniqueConstraint(
                fields=["profesional", "fecha", "hora"],
                condition=~models.Q(estado="cancelado"),
                name="turno_unico_por_profesional",
                violation_error_message=(
                    "Ese profesional ya tiene un turno en ese día y horario."
                ),
            ),
        ]

    @property
    def puede_cancelarse(self):
        """Indica si el turno sigue vigente: no está cancelado ni pasó."""
        no_cancelado = self.estado != self.Estado.CANCELADO
        return no_cancelado and self.fecha >= timezone.localdate()

    def __str__(self):
        """Devuelve la fecha, la hora y el profesional del turno."""
        return f"{self.fecha:%d/%m/%Y} {self.hora:%H:%M} - {self.profesional}"
