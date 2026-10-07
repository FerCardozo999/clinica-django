"""Vistas de la app novedades: listado y detalle de las notas del blog."""

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Novedad

NOVEDADES_POR_PAGINA = 6


def lista_novedades(request):
    """Muestra las novedades publicadas, de a seis por página."""
    paginador = Paginator(Novedad.publicadas(), NOVEDADES_POR_PAGINA)
    # get_page tolera números inválidos: muestra la primera o la última página.
    pagina = paginador.get_page(request.GET.get("pagina"))
    contexto = {"pagina": pagina}
    return render(request, "novedades/lista.html", contexto)


def detalle_novedad(request, slug):
    """Muestra una novedad publicada y otras notas recientes."""
    novedad = get_object_or_404(Novedad.publicadas(), slug=slug)
    otras = Novedad.publicadas().exclude(pk=novedad.pk)[:3]
    contexto = {"novedad": novedad, "otras": otras}
    return render(request, "novedades/detalle.html", contexto)
