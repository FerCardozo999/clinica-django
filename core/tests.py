"""Pruebas automáticas de la app core."""

from django.test import TestCase
from django.urls import reverse

from .models import MensajeContacto


class PaginasPublicasTests(TestCase):
    """Las páginas institucionales cargan sin iniciar sesión."""

    def test_paginas_responden(self):
        """Inicio, Nosotros y Contacto devuelven 200."""
        for nombre in ("core:inicio", "core:nosotros", "core:contacto"):
            with self.subTest(pagina=nombre):
                respuesta = self.client.get(reverse(nombre))
                self.assertEqual(respuesta.status_code, 200)


class ContactoTests(TestCase):
    """Formulario de contacto."""

    def test_mensaje_valido_se_guarda(self):
        """Un mensaje completo se guarda y redirige a la misma página."""
        datos = {
            "nombre": "Ana Pérez",
            "email": "ana@ejemplo.com",
            "telefono": "",
            "mensaje": "Quería consultar por los horarios de pediatría.",
        }
        respuesta = self.client.post(reverse("core:contacto"), datos)
        self.assertRedirects(respuesta, reverse("core:contacto"))
        self.assertEqual(MensajeContacto.objects.count(), 1)

    def test_mensaje_corto_se_rechaza(self):
        """Un mensaje de menos de diez caracteres no se guarda."""
        datos = {"nombre": "Ana", "email": "ana@ejemplo.com", "mensaje": "Hola"}
        respuesta = self.client.post(reverse("core:contacto"), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertFormError(
            respuesta.context["form"],
            "mensaje",
            "El mensaje es muy corto: contanos un poco más.",
        )
        self.assertEqual(MensajeContacto.objects.count(), 0)
