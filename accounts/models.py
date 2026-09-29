from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    biografia = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)

    def __str__(self):
        return self.usuario.username
