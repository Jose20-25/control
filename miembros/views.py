from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Miembro, Familia
from .serializers import MiembroSerializer, FamiliaSerializer
from .forms import NinoForm, JovenForm, AdultoForm
from datetime import date
from django.db.models import Q

# Create your views here.

class MiembroViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer

class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer

def home(request):
    return render(request, 'home.html')

def ninos_form(request):
    if request.method == 'POST':
        form = NinoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NinoForm()
    return render(request, 'ninos_form.html', {'form': form})

def jovenes_form(request):
    if request.method == 'POST':
        form = JovenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JovenForm()
    return render(request, 'jovenes_form.html', {'form': form})

def adultos_form(request):
    if request.method == 'POST':
        form = AdultoForm(request.POST, request.FILES)
        # Si el usuario presionó el botón de actualizar hijos, solo renderiza el formulario con los campos de hijos
        if 'Actualizar hijos' in request.POST.values():
            return render(request, 'adultos_form.html', {'form': form})
        # Si es guardar, valida y guarda
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AdultoForm()
    return render(request, 'adultos_form.html', {'form': form})

def lista_miembros(request, iglesia):
    from .models import Miembro
    miembros = Miembro.objects.filter(iglesia=iglesia)
    return render(request, 'lista_miembros.html', {'miembros': miembros, 'iglesia': iglesia})

def cumpleaneros_mes(request):
    mes_actual = date.today().month
    cumpleaneros = Miembro.objects.filter(fecha_nacimiento__month=mes_actual)
    return render(request, 'cumpleaneros_mes.html', {'cumpleaneros': cumpleaneros, 'mes': mes_actual})

def editar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    # Seleccionar el formulario según la edad
    edad = None
    if miembro.fecha_nacimiento:
        from datetime import date
        hoy = date.today()
        edad = hoy.year - miembro.fecha_nacimiento.year - ((hoy.month, hoy.day) < (miembro.fecha_nacimiento.month, miembro.fecha_nacimiento.day))
    if edad is not None and edad < 13:
        FormClass = NinoForm
    elif edad is not None and edad < 18:
        FormClass = JovenForm
    else:
        FormClass = AdultoForm
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=miembro)
        if form.is_valid():
            form.save()
            return redirect('lista_miembros', iglesia=miembro.iglesia)
    else:
        form = FormClass(instance=miembro)
    return render(request, 'editar_miembro.html', {'form': form, 'miembro': miembro})

def eliminar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    iglesia = miembro.iglesia
    if request.method == 'POST':
        miembro.delete()
        return redirect('lista_miembros', iglesia=iglesia)
    return render(request, 'eliminar_miembro.html', {'miembro': miembro})
