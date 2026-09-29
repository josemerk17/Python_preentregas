# Blog Django

Proyecto base de un blog web desarrollado con Django.

## Descripción

Este proyecto contiene la estructura inicial de una aplicación web desarrollada con Django.

El proyecto principal se llama `blog_project` y contiene una aplicación llamada `posts`, que será utilizada para gestionar las publicaciones del blog.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/josemerk17/Python_entrega_7.git
```

Entrar a la carpeta del proyecto:

```bash
cd Python_entrega_7
```

Crear un entorno virtual:

```bash
python -m venv .venv-1
```

Activar el entorno virtual en Windows:

```bash
.venv-1\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar el proyecto

En este equipo, el entorno que tiene Django y Pillow instalados es `../.venv`.
Desde `pre_entrega_7`, puedes activarlo en PowerShell con:

```powershell
..\.venv\Scripts\Activate.ps1
```

Si usas otro entorno, instala primero `python -m pip install -r requirements.txt`.

Desde la carpeta que contiene `manage.py`, con el entorno virtual activado,
aplicar las migraciones y crear un usuario administrador (si aún no existe):

```bash
python manage.py migrate
```

Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

Abrir en el navegador:

http://127.0.0.1:8000/

Las publicaciones están en http://127.0.0.1:8000/posts/.
Solo se muestran los posts con estado `publicado`, del más reciente al más antiguo.

Para agregar o editar posts, entrar a http://127.0.0.1:8000/admin/ con el
superusuario creado. En Posts se pueden completar título, contenido, autor y
estado; la fecha de creación se asigna automáticamente. Los posts nuevos tienen
estado `borrador` de forma predeterminada: cambiarlo a `publicado` para verlos
en el listado público. Inicio y Acerca de siguen disponibles.

El panel admin es opcional. Si necesitas un administrador, ejecuta
`python manage.py createsuperuser`. Desde la Pre-Entrega 11, crear, editar y
eliminar posts requiere iniciar sesión.

## Pre-Entrega 10: CRUD e imágenes

- `/posts/`: publicaciones, con un enlace a **Todos los posts** (`?todos=1`)
  para gestionar también borradores y archivados.
- `/posts/crear/`: crear un post.
- `/posts/<id>/`: ver el detalle y su imagen, si tiene una.
- `/posts/<id>/editar/`: editar los datos y cambiar o quitar la imagen.
- `/posts/<id>/eliminar/`: ver la confirmación; solo se elimina al enviar el formulario.

Pillow es la dependencia que permite validar las imágenes del `ImageField` y
está incluida en `requirements.txt`. La imagen es opcional.
`MEDIA_URL = '/media/'` y `MEDIA_ROOT = BASE_DIR / 'media'` guardan las imágenes
en `media/posts/`. Django las sirve durante desarrollo cuando `DEBUG=True`.
La carpeta `media/`, la base `db.sqlite3` y el entorno virtual se excluyen de Git.

Para probar: inicia el servidor, inicia sesión, entra a **Crear post**, completa los campos,
elige estado `publicado`, selecciona una imagen PNG o JPG y guarda.
El detalle debe mostrar la imagen. Usa **Editar** para subir otra imagen y
**Eliminar** para comprobar la página de confirmación (Cancelar conserva el post).
También puedes crear un post sin imagen. Los borradores y archivados se encuentran
en **Todos los posts**. Al cambiar o eliminar un post, los archivos de imágenes
anteriores permanecen en `media/`; no hay limpieza automática de archivos.

## Pre-Entrega 11: usuarios y perfiles

Con el entorno activado y desde la carpeta que contiene `manage.py`, ejecuta:

```bash
python manage.py migrate
python manage.py runserver
```

- `/accounts/registro/`: registra username, email y contraseña. Se crea el perfil
  asociado explícitamente y se redirige al login.
- `/accounts/login/`: inicia sesión y abre el perfil, o vuelve a la página
  protegida que se intentó visitar.
- **Cerrar sesión**: el botón envía un formulario POST con CSRF a
  `/accounts/logout/` y vuelve a Inicio.
- `/accounts/perfil/`: muestra username, email, biografía y avatar del usuario.
- `/accounts/perfil/editar/`: permite editar biografía y subir, cambiar o quitar
  el avatar. Si un usuario anterior no tiene perfil, se crea al acceder.

El perfil y su edición requieren sesión. Crear, editar y eliminar posts también;
el listado y el detalle siguen siendo públicos. Cualquier usuario autenticado
puede gestionar posts: no se añadieron permisos por autor.

Para probar el avatar, inicia sesión, abre **Mi perfil**, pulsa **Editar perfil**,
escribe una biografía y selecciona una imagen PNG o JPG. Al guardar debe aparecer
en el perfil. Los avatares opcionales se guardan en `media/avatares/`, usando
Pillow y la configuración media existente. `media/` sigue excluida de Git.

## Aplicación principal

- `posts`: aplicación utilizada para gestionar las publicaciones del blog.

## Configuración

El proyecto utiliza:

- Django como framework web.
- Español como idioma del proyecto.
- Zona horaria de México.
- `requirements.txt` para gestionar las dependencias.
- `.gitignore` para excluir el entorno virtual, archivos temporales y la base de datos local.
