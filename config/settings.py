"""Configuración del proyecto Génesis Salud.

Los datos sensibles y los que cambian entre la compu local y el servidor
(clave secreta, modo debug y dominios permitidos) se leen del archivo .env.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# Seguridad

# Sin valor por defecto: si falta en el .env, Django no arranca.
SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# Los formularios enviados por HTTPS desde el dominio público pasan el control CSRF.
CSRF_TRUSTED_ORIGINS = [
    f"https://{host}"
    for host in ALLOWED_HOSTS
    if host not in ("127.0.0.1", "localhost")
]

if not DEBUG:
    # PythonAnywhere atiende el HTTPS y le pasa el pedido a Django por HTTP.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Aplicaciones

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps propias
    "core",
    "clinica",
    "cuentas",
    "turnos",
    "pacientes",
    "novedades",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Base de datos

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


# Contraseñas

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Autenticación

LOGIN_URL = "cuentas:login"
LOGIN_REDIRECT_URL = "core:inicio"
LOGOUT_REDIRECT_URL = "core:inicio"


# Idioma y zona horaria

LANGUAGE_CODE = "es-ar"

TIME_ZONE = "America/Argentina/Salta"

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, imágenes de la marca)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# Carpeta donde collectstatic junta todo para el servidor.
STATIC_ROOT = BASE_DIR / "staticfiles"


# Archivos subidos por los usuarios

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# Correo

# En desarrollo los correos se muestran en la consola. El sitio todavía no
# envía correos, así que en producción no hace falta configurar un servidor.
if DEBUG:
    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.console.EmailBackend",
        },
    }
