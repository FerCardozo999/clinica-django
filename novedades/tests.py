"""Pruebas automáticas de la app novedades."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Novedad

User = get_user_model()


class NovedadesTests(TestCase):
    """Listado y detalle del blog: solo se ven las notas publicadas."""

    @classmethod
    def setUpTestData(cls):
        """Crea una nota publicada, un borrador y una nota programada."""
        autor = User.objects.create_user("redaccion")
        datos = {"resumen": "Resumen.", "contenido": "Contenido.", "autor": autor}
        cls.publicada = Novedad.objects.create(
            titulo="Vacunación antigripal", slug="vacunacion", **datos)
        cls.borrador = Novedad.objects.create(
            titulo="Nota en borrador", slug="borrador", publicada=False, **datos)
        cls.programada = Novedad.objects.create(
            titulo="Nota programada",
            slug="programada",
            fecha_publicacion=timezone.localdate() + timedelta(days=7),
            **datos,
        )

    def test_str_devuelve_el_titulo(self):
        """En el admin, cada novedad se ve con su título."""
        self.assertEqual(str(self.publicada), "Vacunación antigripal")

    def test_listado_muestra_solo_publicadas(self):
        """El listado oculta los borradores y las notas con fecha futura."""
        respuesta = self.client.get(reverse("novedades:lista"))
        self.assertContains(respuesta, "Vacunación antigripal")
        self.assertNotContains(respuesta, "Nota en borrador")
        self.assertNotContains(respuesta, "Nota programada")

    def test_detalle_de_borrador_da_404(self):
        """Un borrador no se puede abrir escribiendo su dirección."""
        respuesta = self.client.get(self.borrador.get_absolute_url())
        self.assertEqual(respuesta.status_code, 404)

    def test_detalle_de_nota_publicada(self):
        """Una nota publicada se abre con su contenido."""
        respuesta = self.client.get(self.publicada.get_absolute_url())
        self.assertContains(respuesta, "Contenido.")
