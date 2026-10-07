# Génesis Salud

Sitio web y sistema de turnos online para una clínica, desarrollado con **Django**. Los pacientes reservan sus consultas desde la web, los médicos gestionan su agenda y la historia clínica de sus pacientes, y la administración maneja todo el contenido desde un panel propio.

**Sitio online:** https://fercardozo.pythonanywhere.com

Proyecto final del curso de Python de Coderhouse. Todos los datos cargados (profesionales, pacientes, turnos e historias clínicas) son ficticios.

---

## Funcionalidades

### Para cualquier visitante

- Página de inicio con las especialidades y las últimas novedades.
- Listado y detalle de **especialidades** y de **profesionales**.
- **Novedades:** blog de la clínica, con listado paginado y página de cada nota.
- Página institucional (**Nosotros**) y formulario de **Contacto** con validación.
- Páginas de error propias (403, 404 y 500).

### Para pacientes (con cuenta)

- **Registro**, inicio y cierre de sesión.
- **Perfil** con datos personales editables (DNI, fecha de nacimiento, teléfono, obra social).
- **Pedir turno** eligiendo profesional, día y horario. El formulario valida la fecha, el horario de atención y que el profesional no tenga otro turno en ese mismo momento.
- **Mis turnos:** listado de consultas con su estado y opción de cancelar.

### Para médicos (panel médico)

- **Agenda** con los turnos del día y de los próximos días.
- Confirmar o cancelar turnos.
- **Mis pacientes**, con buscador.
- **Ficha del paciente** con sus datos y su **historia clínica**.
- Carga de nuevas entradas en la historia clínica, con validación.
- Acceso restringido: solo entran las cuentas vinculadas a un profesional.

### Para la administración

- Panel de administración de Django personalizado para gestionar especialidades, profesionales, usuarios, perfiles, turnos, historias clínicas, novedades y mensajes de contacto, con listados, filtros y buscadores.

---

## Cuentas de prueba

Para recorrer el sitio online sin registrarse:

| Rol | Usuario | Contraseña | Qué se puede ver |
|---|---|---|---|
| Paciente | `paciente.demo` | `GenesisDemo2026` | Perfil, pedir turno, mis turnos |
| Médico | `dra.ruiz` | `GenesisDemo2026` | Panel médico: agenda, pacientes e historia clínica |

El acceso al panel de administración (`/admin/`) se comparte por separado.

---

## Tecnologías

- **Python 3** y **Django 6.1**
- **SQLite** como base de datos
- **Bootstrap 5**, Bootstrap Icons y Google Fonts (Poppins)
- **Sass** con metodología BEM para los estilos propios
- **Pillow** para el manejo de imágenes
- **python-dotenv** para las variables de entorno
- **Git** y **GitHub** para el control de versiones
- **PythonAnywhere** para el deploy

---

## Estructura del proyecto

```
clinica-django/
├── config/          Configuración del proyecto (settings, URLs principales)
├── core/            Inicio, Nosotros y Contacto
├── clinica/         Especialidades y profesionales
├── cuentas/         Registro, login, logout y perfil de usuario
├── turnos/          Pedido, listado y cancelación de turnos
├── pacientes/       Panel médico e historia clínica
├── novedades/       Blog de la clínica
├── templates/       Plantilla base, parciales y páginas de error
├── static/
│   ├── scss/        Estilos fuente (base, layouts, components, pages)
│   ├── css/         CSS compilado
│   └── img/         Imágenes del diseño
├── .env.example     Plantilla de variables de entorno
├── manage.py
└── requirements.txt
```

Cada app tiene sus propios modelos, vistas, formularios, URLs, configuración del admin y templates.

### Modelos principales

| Modelo | App | Qué representa |
|---|---|---|
| `Especialidad` | clinica | Área de atención de la clínica |
| `Profesional` | clinica | Médico, con su especialidad, matrícula, foto y cuenta de usuario |
| `Perfil` | cuentas | Datos personales del paciente, vinculados a su usuario |
| `Turno` | turnos | Consulta entre un paciente y un profesional, con fecha, hora y estado |
| `EntradaHistoria` | pacientes | Registro de una consulta en la historia clínica |
| `Novedad` | novedades | Nota del blog |
| `MensajeContacto` | core | Mensaje enviado desde el formulario de contacto |

---

## Instalación local

### Requisitos

- Python 3.12 o superior
- Git

### Pasos

**1. Clonar el repositorio**

```bash
git clone https://github.com/FerCardozo999/clinica-django.git
cd clinica-django
```

**2. Crear y activar el entorno virtual**

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar las variables de entorno**

Copiar la plantilla y renombrarla a `.env`.

En Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

Generar una clave secreta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Abrir el archivo `.env` y pegar la clave generada en `SECRET_KEY`, entre comillas simples:

| Variable | Descripción | Valor en desarrollo |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Django | La clave generada |
| `DEBUG` | Modo desarrollo | `True` |
| `ALLOWED_HOSTS` | Direcciones permitidas, separadas por coma | `127.0.0.1,localhost` |

**5. Crear la base de datos**

```bash
python manage.py migrate
```

**6. Crear un usuario administrador**

```bash
python manage.py createsuperuser
```

**7. Iniciar el servidor**

```bash
python manage.py runserver
```

El sitio queda disponible en http://127.0.0.1:8000 y el panel de administración en http://127.0.0.1:8000/admin/.

### Cargar contenido

La base de datos arranca vacía. Desde el panel de administración se cargan, en este orden:

1. **Especialidades.**
2. **Profesionales**, cada uno con su especialidad. Para que un profesional pueda entrar al panel médico hay que vincularlo a una cuenta de usuario.
3. **Novedades.**

Los pacientes se registran desde el propio sitio.

### Estilos

Los estilos se escriben en `static/scss/` y se compilan a `static/css/main.css`. El CSS compilado ya está incluido en el repositorio, así que **no hace falta compilar nada** para correr el proyecto. Para modificar los estilos se puede usar cualquier compilador de Sass (en el desarrollo se usó la extensión Live Sass Compiler de VS Code).

---

## Deploy

El sitio está publicado en PythonAnywhere. En producción se usa `DEBUG=False`, los archivos estáticos se reúnen con `python manage.py collectstatic` en la carpeta `staticfiles/`, y los valores sensibles (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) se leen de un archivo `.env` que no forma parte del repositorio.

---

## Autor

**Fernando Cardozo** — [GitHub](https://github.com/FerCardozo999)
