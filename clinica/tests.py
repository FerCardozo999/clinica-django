"""Pruebas automáticas de la app clinica."""

from django.test import TestCase
from django.urls import reverse

from .models import Especialidad, Profesional


class EspecialidadesYProfesionalesTests(TestCase):
    """Listados y fichas públicas: solo se muestra lo que está activo."""

    @classmethod
    def setUpTestData(cls):
        """Crea una especialidad activa, una inactiva y un médico en cada una."""
        cls.activa = Especialidad.objects.create(
            nombre="Cardiología", slug="cardiologia", descripcion="Corazón.")
        cls.inactiva = Especialidad.objects.create(
            nombre="Dermatología",
            slug="dermatologia",
            descripcion="Piel.",
            activa=False,
        )
        cls.medico = Profesional.objects.create(
            nombre="Laura", apellido="Gómez", especialidad=cls.activa, matricula="MP-1")
        cls.medico_inactivo = Profesional.objects.create(
            nombre="Pablo", apellido="Ruiz", especialidad=cls.inactiva, matricula="MP-2")

    def test_listado_muestra_solo_activas(self):
        """El listado de especialidades oculta las desactivadas."""
        respuesta = self.client.get(reverse("clinica:especialidades"))
        self.assertContains(respuesta, "Cardiología")
        self.assertNotContains(respuesta, "Dermatología")

    def test_detalle_muestra_especialidad_y_profesionales(self):
        """La ficha de una especialidad muestra su nombre y sus médicos."""
        url = reverse("clinica:especialidad_detalle", args=[self.activa.slug])
        respuesta = self.client.get(url)
        self.assertContains(respuesta, "Cardiología")
        self.assertContains(respuesta, "Laura Gómez")

    def test_detalle_de_especialidad_inactiva_da_404(self):
        """Una especialidad desactivada no se puede abrir."""
        url = reverse("clinica:especialidad_detalle", args=[self.inactiva.slug])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_profesional_de_especialidad_inactiva_da_404(self):
        """Un médico de una especialidad desactivada no tiene ficha pública."""
        url = reverse("clinica:profesional_detalle", args=[self.medico_inactivo.pk])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_ficha_de_profesional(self):
        """La ficha de un médico activo carga con su matrícula."""
        url = reverse("clinica:profesional_detalle", args=[self.medico.pk])
        self.assertContains(self.client.get(url), "MP-1")
