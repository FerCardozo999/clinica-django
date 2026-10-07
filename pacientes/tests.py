"""Pruebas automáticas de la app pacientes."""

from datetime import time, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clinica.models import Especialidad, Profesional
from turnos.models import Turno

from .models import EntradaHistoria

User = get_user_model()


class PanelMedicoTests(TestCase):
    """Acceso al panel y manejo de la historia clínica."""

    @classmethod
    def setUpTestData(cls):
        """Crea dos médicos con cuenta, un paciente con turno y uno sin turno."""
        especialidad = Especialidad.objects.create(
            nombre="Clínica médica", slug="clinica-medica", descripcion="Adultos.")
        cls.cuenta_medico = User.objects.create_user("drgomez")
        cls.medico = Profesional.objects.create(
            nombre="Laura",
            apellido="Gómez",
            especialidad=especialidad,
            matricula="MP-1",
            usuario=cls.cuenta_medico,
        )
        cls.otro_medico = Profesional.objects.create(
            nombre="Pablo",
            apellido="Ruiz",
            especialidad=especialidad,
            matricula="MP-2",
            usuario=User.objects.create_user("drruiz"),
        )
        cls.paciente = User.objects.create_user("anaperez")
        cls.paciente_ajeno = User.objects.create_user("juanlopez")
        manana = timezone.localdate() + timedelta(days=1)
        cls.turno = Turno.objects.create(
            paciente=cls.paciente, profesional=cls.medico, fecha=manana, hora=time(10, 0))
        cls.turno_ajeno = Turno.objects.create(
            paciente=cls.paciente_ajeno,
            profesional=cls.otro_medico,
            fecha=manana,
            hora=time(10, 0),
        )

    def test_paciente_no_entra_al_panel(self):
        """Una cuenta que no es de un médico recibe un 403."""
        self.client.force_login(self.paciente)
        for nombre in ("pacientes:agenda", "pacientes:lista"):
            with self.subTest(pagina=nombre):
                self.assertEqual(self.client.get(reverse(nombre)).status_code, 403)

    def test_medico_ve_su_agenda(self):
        """El médico ve en su agenda el turno del paciente."""
        self.client.force_login(self.cuenta_medico)
        respuesta = self.client.get(reverse("pacientes:agenda"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(self.turno, respuesta.context["turnos_proximos"])

    def test_medico_no_abre_ficha_de_paciente_ajeno(self):
        """Un médico solo abre fichas de quienes pidieron turno con él."""
        self.client.force_login(self.cuenta_medico)
        propia = reverse("pacientes:ficha", args=[self.paciente.pk])
        ajena = reverse("pacientes:ficha", args=[self.paciente_ajeno.pk])
        self.assertEqual(self.client.get(propia).status_code, 200)
        self.assertEqual(self.client.get(ajena).status_code, 404)

    def test_medico_no_modifica_turnos_de_otro_medico(self):
        """Confirmar un turno de otro médico da 404 y no lo cambia."""
        self.client.force_login(self.cuenta_medico)
        url = reverse("pacientes:actualizar_turno", args=[self.turno_ajeno.pk])
        respuesta = self.client.post(url, {"accion": "confirmar"})
        self.assertEqual(respuesta.status_code, 404)
        self.turno_ajeno.refresh_from_db()
        self.assertEqual(self.turno_ajeno.estado, Turno.Estado.PENDIENTE)

    def test_medico_confirma_su_turno(self):
        """El médico puede confirmar un turno de su agenda."""
        self.client.force_login(self.cuenta_medico)
        url = reverse("pacientes:actualizar_turno", args=[self.turno.pk])
        self.client.post(url, {"accion": "confirmar"})
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.estado, Turno.Estado.CONFIRMADO)

    def test_nueva_entrada_de_historia_clinica(self):
        """Una consulta válida queda en la historia, firmada por el médico."""
        self.client.force_login(self.cuenta_medico)
        url = reverse("pacientes:nueva_entrada", args=[self.paciente.pk])
        datos = {
            "fecha": timezone.localdate().isoformat(),
            "motivo": "Control anual",
            "diagnostico": "Paciente en buen estado general.",
            "indicaciones": "",
        }
        respuesta = self.client.post(url, datos)
        self.assertRedirects(respuesta, reverse("pacientes:ficha", args=[self.paciente.pk]))
        entrada = EntradaHistoria.objects.get()
        self.assertEqual(entrada.profesional, self.medico)
        self.assertEqual(entrada.paciente, self.paciente)

    def test_entrada_con_fecha_futura_se_rechaza(self):
        """La fecha de una consulta no puede ser posterior a hoy."""
        self.client.force_login(self.cuenta_medico)
        url = reverse("pacientes:nueva_entrada", args=[self.paciente.pk])
        manana = timezone.localdate() + timedelta(days=1)
        datos = {
            "fecha": manana.isoformat(),
            "motivo": "Control",
            "diagnostico": "Paciente en buen estado general.",
        }
        respuesta = self.client.post(url, datos)
        self.assertFormError(
            respuesta.context["form"],
            "fecha",
            "La fecha de la consulta no puede ser posterior a hoy.",
        )
        self.assertFalse(EntradaHistoria.objects.exists())
