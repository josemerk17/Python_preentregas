from io import BytesIO
from secrets import token_urlsafe
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post
from .models import Perfil


class AccountsTests(TestCase):
    def test_registro_login_y_logout(self):
        clave = token_urlsafe(24)
        datos = {'username': 'ana', 'email': 'ana@example.com',
                 'password1': clave, 'password2': clave}
        response = self.client.post(reverse('accounts:registro'), datos)
        self.assertRedirects(response, reverse('accounts:login'))
        usuario = User.objects.get(username='ana')
        self.assertEqual(usuario.email, datos['email'])
        self.assertTrue(usuario.check_password(clave))
        self.assertTrue(Perfil.objects.filter(usuario=usuario).exists())
        response = self.client.post(reverse('accounts:registro'), datos)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(reverse('accounts:login'), {
            'username': 'ana', 'password': token_urlsafe(24),
        })
        self.assertTrue(response.context['form'].errors)
        response = self.client.post(reverse('accounts:login'), {
            'username': 'ana', 'password': clave,
        })
        self.assertRedirects(response, reverse('accounts:perfil'))
        self.assertContains(self.client.get(reverse('posts:inicio')), 'Hola, ana')
        self.assertEqual(self.client.get(reverse('accounts:logout')).status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertRedirects(self.client.post(reverse('accounts:logout')), reverse('posts:inicio'))
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.post(reverse('accounts:login'), {
            'username': 'ana', 'password': clave, 'next': reverse('posts:crear_post'),
        })
        self.assertRedirects(response, reverse('posts:crear_post'))
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(usuario)
        self.assertEqual(csrf_client.post(reverse('accounts:logout')).status_code, 403)
        page = csrf_client.get(reverse('accounts:perfil'))
        token = page.cookies['csrftoken'].value
        self.assertRedirects(csrf_client.post(reverse('accounts:logout'),
                                             {'csrfmiddlewaretoken': token}), reverse('posts:inicio'))

    def test_rutas_publicas_y_protegidas(self):
        post = Post.objects.create(titulo='Publico', contenido='Texto', autor='Ana', estado='publicado')
        for nombre in ['inicio', 'acerca', 'lista_posts']:
            self.assertEqual(self.client.get(reverse('posts:' + nombre)).status_code, 200)
        self.assertEqual(self.client.get(reverse('posts:detalle_post', args=[post.pk])).status_code, 200)
        rutas = [reverse('accounts:perfil'), reverse('accounts:editar_perfil'),
                 reverse('posts:crear_post'), reverse('posts:editar_post', args=[post.pk]),
                 reverse('posts:eliminar_post', args=[post.pk])]
        for ruta in rutas:
            for metodo in [self.client.get, self.client.post]:
                self.assertRedirects(metodo(ruta), reverse('accounts:login') + '?next=' + ruta)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertEqual(Perfil.objects.count(), 0)

    def test_perfil_anterior_y_avatar(self):
        usuario = User.objects.create_user(username='anterior', email='anterior@example.com')
        otro = User.objects.create_user(username='otro')
        otro_perfil = Perfil.objects.create(usuario=otro, biografia='No cambiar')
        self.client.force_login(usuario)
        editar = reverse('accounts:editar_perfil')
        with TemporaryDirectory() as directory, self.settings(MEDIA_ROOT=directory):
            self.assertContains(self.client.get(editar), 'multipart/form-data')
            perfil = Perfil.objects.get(usuario=usuario)
            for nombre in ['avatar.png', 'nuevo.png']:
                archivo = BytesIO()
                Image.new('RGB', (8, 8), 'blue').save(archivo, format='PNG')
                avatar = SimpleUploadedFile(nombre, archivo.getvalue(), content_type='image/png')
                response = self.client.post(editar, {'biografia': 'Mi historia', 'avatar': avatar,
                                                   'usuario': otro.pk})
                self.assertRedirects(response, reverse('accounts:perfil'))
                perfil.refresh_from_db()
                self.assertEqual(perfil.biografia, 'Mi historia')
                self.assertTrue(perfil.avatar.name.startswith('avatares/'))
                self.assertContains(self.client.get(reverse('accounts:perfil')), perfil.avatar.url)
            self.client.post(editar, {'biografia': 'Actualizada'})
            perfil.refresh_from_db()
            self.assertTrue(perfil.avatar)
            invalido = SimpleUploadedFile('falso.png', b'invalido', content_type='image/png')
            response = self.client.post(editar, {'biografia': 'Texto', 'avatar': invalido})
            self.assertIn('avatar', response.context['form'].errors)
            self.client.post(editar, {'biografia': 'Sin avatar', 'avatar-clear': 'on'})
            perfil.refresh_from_db()
            self.assertFalse(perfil.avatar)
            self.assertContains(self.client.get(reverse('accounts:perfil')), usuario.email)
        otro_perfil.refresh_from_db()
        self.assertEqual(otro_perfil.biografia, 'No cambiar')
        perfil.delete()
        self.assertEqual(self.client.get(reverse('accounts:perfil')).status_code, 200)
        self.assertTrue(Perfil.objects.filter(usuario=usuario).exists())
