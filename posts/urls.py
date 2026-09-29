from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca/', views.acerca, name='acerca'),
]
