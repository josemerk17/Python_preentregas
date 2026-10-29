# Blog Django

Blog web desarrollado con Django para crear, publicar y consultar artículos. Incluye autenticación, perfiles con avatar y gestión de imágenes.

## Tecnologías

- Python y Django
- SQLite
- Pillow para validar y procesar imágenes
- HTML y CSS

## Funcionalidades

- Listado público de publicaciones y página de detalle.
- Crear, editar y eliminar publicaciones desde la interfaz web tras iniciar sesión.
- Estados de publicación: borrador, publicado y archivado.
- Imágenes opcionales para posts y avatares; el detalle funciona también sin imagen.
- Registro, inicio y cierre de sesión.
- Perfil con biografía y avatar.
- Protección de las acciones de escritura y edición de perfil para usuarios autenticados.

## Requisitos

Python 3.12 o posterior. Las dependencias se instalan desde `requirements.txt`.

## Instalación y ejecución

Clona el repositorio y entra a su carpeta:

```bash
git clone https://github.com/josemerk17/Python_entrega_7.git
cd Python_entrega_7
```

Crea y activa un entorno virtual. En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala dependencias, prepara la base de datos e inicia el servidor:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visita <http://127.0.0.1:8000/>. Las rutas principales son `/posts/`, `/accounts/registro/` y `/accounts/login/`.

Para probar el panel administrativo, crea un superusuario con `python manage.py createsuperuser` y visita `/admin/`. El panel es opcional; las publicaciones se pueden gestionar desde la interfaz del blog.

## Imágenes y archivos locales

Las imágenes se guardan bajo `media/`. En desarrollo, Django las sirve con `MEDIA_URL = '/media/'` y `MEDIA_ROOT = BASE_DIR / 'media'`. `media/` y `db.sqlite3` no se versionan; ambos se crean al ejecutar el proyecto y las migraciones. Para probar imágenes, inicia sesión y sube una imagen desde el formulario de creación de posts o edición del perfil.

## Configuración y seguridad

`SECRET_KEY` puede definirse como variable de entorno. Si no está definida, Django usa una clave de desarrollo local que no debe utilizarse en producción. Para desplegar, establece una clave privada y configura `DEBUG=False` y `ALLOWED_HOSTS` para el entorno correspondiente. No guardes claves reales en el repositorio.

## Autor

José (josemerk17).
