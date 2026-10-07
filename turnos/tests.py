"""Pruebas automáticas de la app turnos."""

from datetime import time, timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clinica.models import Especialidad, Profesional

from .forms import TurnoForm
from .models import Turno

User = get_user_model()


def proximo_dia_habil():
    """Devuelve el próximo día de lunes a viernes, a partir de mañana."""
    dia = timezone.localdate() + timedelta(days=1)
    # weekday() numera los días: 5 y 6 son sábado y domingo.
    while dia.weekday() >= 5:
        dia += timedelta(days=1)
    return dia


def proximo_sabado():
    """Devuelve el próximo sábado, a partir de mañana."""
    hoy = timezone.localdate()
    return hoy + timedelta(days=(5 - hoy.weekday()) % 7 or 7)


class TurnosTests(TestCase):
    """Pedido, listado y cancelación de turnos."""

    @classmethod
    def setUpTestData(cls):
        """Crea un médico y dos pacientes."""
        especialidad = Especialidad.objects.create(
            nombre="Pediatría", slug="pediatria", descripcion="Niños.")
        cls.medico = Profesional.objects.create(
            nombre="Laura", apellido="Gómez", especialidad=especialidad, matricula="MP-1")
        cls.paciente = User.objects.create_user("anaperez")
        cls.otro_paciente = User.objects.create_user("juanlopez")
        cls.fecha = proximo_dia_habil()

    def setUp(self):
        """Cada prueba arranca con la sesión del paciente iniciada."""
        self.client.force_login(self.paciente)

    def pedir(self, **cambios):
        """Envía el formulario de turno con datos válidos y los cambios pedidos."""
        datos = {
            "profesional": self.medico.pk,
            "fecha": self.fecha.isoformat(),
            "hora": "10:00",
            "motivo": "",
        }
        datos.update(cambios)
        return self.client.post(reverse("turnos:pedir"), datos)

    def test_pedir_turno_valido(self):
        """Un pedido válido crea el turno a nombre de quien inició sesión."""
        respuesta = self.pedir()
        self.assertRedirects(respuesta, reverse("turnos:mis_turnos"))
        turno = Turno.objects.get()
        self.assertEqual(turno.paciente, self.paciente)
        self.assertEqual(turno.estado, Turno.Estado.PENDIENTE)

    def test_fin_de_semana_se_rechaza(self):
        """La clínica no da turnos sábados ni domingos."""
        respuesta = self.pedir(fecha=proximo_sabado().isoformat())
        self.assertFormError(
            respuesta.context["form"], "fecha", "La clínica atiende de lunes a viernes.")

    def test_horario_ocupado_se_rechaza(self):
        """No se puede reservar un horario que ya tiene otro paciente."""
        Turno.objects.create(
            paciente=self.otro_paciente,
            profesional=self.medico,
            fecha=self.fecha,
            hora=time(10, 0),
        )
        respuesta = self.pedir()
        self.assertFormError(
            respuesta.context["form"], "hora", "Ese horario ya está ocupado. Probá con otro.")
        self.assertEqual(Turno.objects.count(), 1)

    def test_horario_de_turno_cancelado_queda_libre(self):
        """Un turno cancelado no bloquea su horario."""
        Turno.objects.create(
            paciente=self.otro_paciente,
            profesional=self.medico,
            fecha=self.fecha,
            hora=time(10, 0),
            estado=Turno.Estado.CANCELADO,
        )
        respuesta = self.pedir()
        self.assertRedirects(respuesta, reverse("turnos:mis_turnos"))

    def test_reserva_simultanea_no_da_error_500(self):
        """Si dos personas reservan a la vez, la segunda ve un aviso y no un error."""
        Turno.objects.create(
            paciente=self.otro_paciente,
            profesional=self.medico,
            fecha=self.fecha,
            hora=time(10, 0),
        )

        def clean_sin_cruce(form):
            """Simula que la validación no llegó a ver el turno de la otra persona."""
            return form.cleaned_data

        with mock.patch.object(TurnoForm, "clean", clean_sin_cruce):
            respuesta = self.pedir()

        self.assertEqual(respuesta.status_code, 200)
        self.assertFormError(
            respuesta.context["form"], "hora", "Ese horario ya está ocupado. Probá con otro.")
        self.assertEqual(Turno.objects.count(), 1)

    def test_cancelar_turno_propio(self):
        """El paciente puede cancelar su propio turno vigente."""
        turno = Turno.objects.create(
            paciente=self.paciente, profesional=self.medico, fecha=self.fecha, hora=time(9, 0))
        self.client.post(reverse("turnos:cancelar", args=[turno.pk]))
        turno.refresh_from_db()
        self.assertEqual(turno.estado, Turno.Estado.CANCELADO)

    def test_no_se_puede_cancelar_turno_ajeno(self):
        """Cancelar el turno de otra persona da 404 y no lo modifica."""
        turno = Turno.objects.create(
            paciente=self.otro_paciente, profesional=self.medico, fecha=self.fecha, hora=time(9, 0))
        respuesta = self.client.post(reverse("turnos:cancelar", args=[turno.pk]))
        self.assertEqual(respuesta.status_code, 404)
        turno.refresh_from_db()
        self.assertEqual(turno.estado, Turno.Estado.PENDIENTE)

    def test_cancelar_por_get_no_esta_permitido(self):
        """Cancelar exige POST: un link o un GET no cancela nada."""
        turno = Turno.objects.create(
            paciente=self.paciente, profesional=self.medico, fecha=self.fecha, hora=time(9, 0))
        respuesta = self.client.get(reverse("turnos:cancelar", args=[turno.pk]))
        self.assertEqual(respuesta.status_code, 405)
