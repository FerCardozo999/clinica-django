"""Control de acceso al panel médico."""

from django.core.exceptions import PermissionDenied


def obtener_profesional(usuario):
    """Devuelve el profesional vinculado a la cuenta o corta con un 403."""
    # getattr con None evita el error cuando la cuenta no es de un médico.
    profesional = getattr(usuario, "profesional", None)
    if profesional is None or not profesional.activo:
        raise PermissionDenied
    return profesional
