"""URLs principales del proyecto: admin, apps y archivos media."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Génesis Salud"
admin.site.site_title = "Génesis Salud"
admin.site.index_title = "Panel de administración"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("clinica.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
