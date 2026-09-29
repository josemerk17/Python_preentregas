from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


class PostCrudTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user(username='editor'))
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        media_settings = self.settings(MEDIA_ROOT=directory.name)
        media_settings.enable()
        self.addCleanup(media_settings.disable)
        self.datos = {
            'titulo': 'Mi post', 'contenido': 'Contenido de prueba',
            'autor': 'Ana', 'estado': 'publicado',
        }

    def imagen(self, nombre):
        archivo = BytesIO()
        Image.new('RGB', (10, 10), 'blue').save(archivo, format='PNG')
        return SimpleUploadedFile(nombre, archivo.getvalue(), content_type='image/png')

    def test_crear_editar_imagen_y_eliminar(self):
        response = self.client.post(reverse('posts:crear_post'), {
            **self.datos, 'imagen': self.imagen('primera.png'),
        })
        post = Post.objects.get()
        detalle = reverse('posts:detalle_post', args=[post.pk])
        self.assertRedirects(response, detalle)
        self.assertContains(self.client.get(detalle), post.imagen.url)
        editar = reverse('posts:editar_post', args=[post.pk])
        self.assertContains(self.client.get(editar), 'multipart/form-data')
        response = self.client.post(editar, {
            **self.datos, 'titulo': 'Editado', 'imagen': self.imagen('segunda.png'),
        })
        self.assertRedirects(response, detalle)
        post.refresh_from_db()
        self.assertEqual(post.titulo, 'Editado')
        self.assertTrue(post.imagen.name.endswith('segunda.png'))
        nombre = post.imagen.name
        self.client.post(editar, self.datos)
        post.refresh_from_db()
        self.assertEqual(post.imagen.name, nombre)
        self.client.post(editar, {**self.datos, 'imagen-clear': 'on'})
        post.refresh_from_db()
        self.assertFalse(post.imagen)
        self.assertEqual(self.client.get(detalle).status_code, 200)
        eliminar = reverse('posts:eliminar_post', args=[post.pk])
        self.assertEqual(self.client.get(eliminar).status_code, 200)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertEqual(Client(enforce_csrf_checks=True).post(eliminar).status_code, 403)
        self.assertRedirects(self.client.post(eliminar), reverse('posts:lista_posts'))
        self.assertFalse(Post.objects.exists())

    def test_listado_y_paginas_existentes(self):
        anterior = Post.objects.create(**self.datos)
        reciente = Post.objects.create(**self.datos)
        borrador = Post.objects.create(**{**self.datos, 'estado': 'borrador'})
        archivado = Post.objects.create(**{**self.datos, 'estado': 'archivado'})
        url = reverse('posts:lista_posts')
        self.assertEqual(list(self.client.get(url).context['posts']), [reciente, anterior])
        self.assertEqual(set(self.client.get(url + '?todos=1').context['posts']),
                         {anterior, reciente, borrador, archivado})
        for nombre in ['inicio', 'acerca', 'crear_post']:
            self.assertEqual(self.client.get(reverse('posts:' + nombre)).status_code, 200)
        for nombre in ['detalle_post', 'editar_post', 'eliminar_post']:
            self.assertEqual(self.client.get(reverse('posts:' + nombre, args=[999])).status_code, 404)

    def test_formulario_invalido_y_sin_imagen(self):
        response = self.client.post(reverse('posts:crear_post'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        archivo = SimpleUploadedFile('falsa.png', b'no es imagen', content_type='image/png')
        response = self.client.post(reverse('posts:crear_post'), {**self.datos, 'imagen': archivo})
        self.assertIn('imagen', response.context['form'].errors)
        self.assertFalse(Post.objects.exists())
        self.client.post(reverse('posts:crear_post'), self.datos)
        post = Post.objects.get()
        self.assertFalse(post.imagen)
        self.assertEqual(self.client.get(reverse('posts:detalle_post', args=[post.pk])).status_code, 200)
