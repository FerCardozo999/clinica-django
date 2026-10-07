"""Modelos de la app novedades: notas de salud y noticias de la clínica."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Novedad(models.Model):
    """Nota que la clínica publica en la sección Novedades."""

    titulo = models.CharField("título", max_length=100)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Se completa solo con el título. Es lo que va en la dirección.",
    )
    resumen = models.CharField(
        max_length=200,
        help_text="Una o dos oraciones. Se muestra en las tarjetas del listado.",
    )
    contenido = models.TextField(
        help_text="Dejá un renglón en blanco para separar los párrafos.",
    )
    imagen = models.ImageField(upload_to="novedades/", blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="novedades",
    )
    fecha_publicacion = models.DateField(
        "fecha de publicación",
        default=timezone.localdate,
    )
    publicada = models.BooleanField(
        default=True,
        help_text="Destildala para guardar la nota como borrador.",
    )

    class Meta:
        """Orden y nombres visibles de las novedades."""

        ordering = ["-fecha_publicacion", "-pk"]
        verbose_name = "novedad"
        verbose_name_plural = "novedades"

    @classmethod
    def publicadas(cls):
        """Devuelve las novedades visibles en el sitio."""
        return cls.objects.filter(
            publicada=True,
            fecha_publicacion__lte=timezone.localdate(),
        )

    def get_absolute_url(self):
        """Devuelve la dirección de la página de detalle de la novedad."""
        return reverse("novedades:detalle", kwargs={"slug": self.slug})

    def __str__(self):
        """Devuelve el título de la novedad."""
        return str(self.titulo)
