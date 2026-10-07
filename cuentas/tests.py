"""Pruebas automáticas de la app cuentas."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Perfil

User = get_user_model()


class RegistroTests(TestCase):
    """Alta de cuentas nuevas."""

    def datos_registro(self, **cambios):
        """Devuelve los datos de un registro válido, con los cambios pedidos."""
        datos = {
            "username": "anaperez",
            "first_name": "Ana",
            "last_name": "Pérez",
            "email": "ana@ejemplo.com",
            "password1": "clave-segura-123",
            "password2": "clave-segura-123",
        }
        datos.update(cambios)
        return datos

    def test_registro_crea_cuenta_e_inicia_sesion(self):
        """Un registro válido crea la cuenta y deja la sesión iniciada."""
        respuesta = self.client.post(reverse("cuentas:registro"), self.datos_registro())
        self.assertRedirects(respuesta, reverse("core:inicio"))
        self.assertTrue(User.objects.filter(username="anaperez").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_correo_repetido_se_rechaza(self):
        """No se pueden crear dos cuentas con el mismo correo."""
        User.objects.create_user("otra", email="ana@ejemplo.com")
        datos = self.datos_registro(email="ANA@ejemplo.com")
        respuesta = self.client.post(reverse("cuentas:registro"), datos)
        self.assertFormError(
            respuesta.context["form"], "email", "Ya existe una cuenta con ese correo.")


class LoginTests(TestCase):
    """Ingreso con usuario y contraseña."""

    def test_login_correcto_redirige_al_inicio(self):
        """Con los datos correctos, la persona entra y vuelve al inicio."""
        User.objects.create_user("anaperez", password="clave-segura-123")
        datos = {"username": "anaperez", "password": "clave-segura-123"}
        respuesta = self.client.post(reverse("cuentas:login"), datos)
        self.assertRedirects(respuesta, reverse("core:inicio"))


class PerfilTests(TestCase):
    """Ver y editar los datos personales."""

    @classmethod
    def setUpTestData(cls):
        """Crea una cuenta de prueba."""
        cls.usuario = User.objects.create_user("anaperez", email="ana@ejemplo.com")

    def datos_perfil(self, **cambios):
        """Devuelve los datos de una edición válida, con los cambios pedidos."""
        datos = {
            "first_name": "Ana",
            "last_name": "Pérez",
            "email": "ana@ejemplo.com",
            "dni": "30123456",
            "fecha_nacimiento": "1990-05-10",
            "telefono": "",
            "obra_social": "",
        }
        datos.update(cambios)
        return datos

    def test_perfil_requiere_sesion(self):
        """Sin sesión, el perfil redirige al login."""
        respuesta = self.client.get(reverse("cuentas:perfil"))
        url_login = reverse("cuentas:login") + "?next=" + reverse("cuentas:perfil")
        self.assertRedirects(respuesta, url_login)

    def test_editar_perfil_guarda_los_datos(self):
        """Una edición válida guarda el DNI en el perfil."""
        self.client.force_login(self.usuario)
        respuesta = self.client.post(reverse("cuentas:editar_perfil"), self.datos_perfil())
        self.assertRedirects(respuesta, reverse("cuentas:perfil"))
        self.assertEqual(Perfil.objects.get(usuario=self.usuario).dni, "30123456")

    def test_dni_con_letras_se_rechaza(self):
        """El DNI tiene que tener solo números."""
        self.client.force_login(self.usuario)
        datos = self.datos_perfil(dni="30A23456")
        respuesta = self.client.post(reverse("cuentas:editar_perfil"), datos)
        self.assertFormError(
            respuesta.context["perfil_form"],
            "dni",
            "Ingresá el DNI sin puntos, solo números.",
        )
