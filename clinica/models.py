"""Modelos de la app clinica: especialidades y profesionales de Génesis Salud."""

from django.conf import settings
from django.db import models


class Especialidad(models.Model):
    """Área médica de la clínica, por ejemplo Odontología o Pediatría."""

    nombre = models.CharField(
        max_length=100, unique=True, verbose_name="nombre")
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(verbose_name="descripción")
    icono = models.CharField(
        max_length=50,
        default="bi-heart-pulse",
        verbose_name="ícono",
        help_text="Nombre de un ícono de Bootstrap Icons, ej: bi-heart-pulse",
    )
    activa = models.BooleanField(default=True)

    class Meta:
        """Orden y nombres visibles de las especialidades."""

        ordering = ["nombre"]
        verbose_name = "especialidad"
        verbose_name_plural = "especialidades"

    def __str__(self):
        """Devuelve el nombre de la especialidad."""
        return str(self.nombre)


class Profesional(models.Model):
    """Médico de la clínica, asignado a una especialidad."""

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    # PROTECT impide borrar una especialidad que todavía tiene médicos.
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name="profesionales",
    )
    matricula = models.CharField(
        max_length=20, unique=True, verbose_name="matrícula")
    foto = models.ImageField(upload_to="profesionales/", blank=True)
    biografia = models.TextField(blank=True, verbose_name="biografía")
    activo = models.BooleanField(default=True)
    # Cuenta para entrar al panel médico. Es opcional: se asigna más adelante.
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profesional",
    )

    class Meta:
        """Orden y nombres visibles de los profesionales."""

        ordering = ["apellido", "nombre"]
        verbose_name = "profesional"
        verbose_name_plural = "profesionales"

    @property
    def nombre_completo(self):
        """Devuelve el nombre y el apellido juntos."""
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        """Devuelve el nombre del profesional con su título."""
        return f"Dr/a. {self.nombre_completo}"
