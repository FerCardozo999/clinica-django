"""Modelos de la app core: mensajes recibidos desde la web."""

from django.db import models


class MensajeContacto(models.Model):
    """Mensaje enviado por una persona desde el formulario de contacto."""

    nombre = models.CharField("nombre y apellido", max_length=100)
    email = models.EmailField("correo electrónico")
    telefono = models.CharField("teléfono", max_length=30, blank=True)
    mensaje = models.TextField("mensaje")
    creado = models.DateTimeField("fecha de envío", auto_now_add=True)
    leido = models.BooleanField("leído", default=False)

    class Meta:
        """Orden y nombres visibles de los mensajes."""

        ordering = ["-creado"]
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"

    def __str__(self):
        """Devuelve un texto que identifica al mensaje."""
        return f"Mensaje de {self.nombre}"
