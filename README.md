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

Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

Abrir en el navegador:

http://127.0.0.1:8000/

## Aplicación principal

- `posts`: aplicación utilizada para gestionar las publicaciones del blog.

## Configuración

El proyecto utiliza:

- Django como framework web.
- Español como idioma del proyecto.
- Zona horaria de México.
- `requirements.txt` para gestionar las dependencias.
- `.gitignore` para excluir el entorno virtual, archivos temporales y la base de datos local.