from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import PerfilForm, RegistroForm
from .models import Perfil

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()
                Perfil.objects.create(usuario=usuario)
            return redirect('accounts:login')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, 'accounts/perfil.html', {'perfil': perfil})


@login_required
def editar_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('accounts:perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'accounts/editar_perfil.html', {'form': form})
