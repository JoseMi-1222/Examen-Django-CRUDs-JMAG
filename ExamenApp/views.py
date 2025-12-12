from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Avg, Max, Min, Count, Sum
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import *
from .form import *
import ExamenApp.form as form_module 
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout

# -------------------------------
# VISTA: Errores
# -------------------------------
def mi_error_404(request, exception=None):
    return render(request, "errores/404.html", status=404)

def mi_error_500(request):
    return render(request, "errores/500.html", status=500)

def mi_error_403(request, exception=None):
    return render(request, "errores/403.html", status=403)

def mi_error_400(request, exception=None):
    return render(request, "errores/400.html", status=400)

# -------------------------------------------------------------------
# Registro de Usuario (Público)
# -------------------------------------------------------------------
def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            # Asignar grupo y crear perfil según el rol
            if rol == Usuario.INVESTIGADOR:
                grupo, _ = Group.objects.get_or_create(name='Investigadores')
                user.groups.add(grupo)
                Investigador.objects.create(usuario=user)
            elif rol == Usuario.PACIENTE:
                grupo, _ = Group.objects.get_or_create(name='Pacientes')
                user.groups.add(grupo)
                Paciente.objects.create(usuario=user)
            messages.success(request, "Registrado correctamente.")
            login(request, user)
            return redirect('ExamenApp:index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

# -------------------------------
# VISTA: Página de inicio
# -------------------------------
def index(request):
    # VARIABLE SESIÓN 1: Fecha inicio (Global)
    if "fecha_inicio" not in request.session:
        request.session["fecha_inicio"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
    return render(request, 'examen/index.html')

# -------------------------------------------------------------------
# VISTA: Listado de Ensayos Clínicos 
# -------------------------------------------------------------------
@login_required
def listado_ensayos(request):
    qs=EnsayoClinico.objects.all()
    if request.user.rol == Usuario.PACIENTE:
        paciente = get_object_or_404(Paciente, usuario=request.user)
        qs = qs.filter(pacientes=paciente)
    elif request.user.rol == Usuario.INVESTIGADOR:
        investigador = get_object_or_404(Investigador, usuario=request.user)
        qs = qs.filter(creado_por=investigador)
    return render(request, 'examen/lista_ensayos.html', {'ensayos': qs.all()})

# -------------------------------------------------------------------
# VISTA: Detalle de Ensayo Clínico
# -------------------------------------------------------------------
@login_required
def detalle_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(EnsayoClinico, id=ensayo_id)
    return render(request, 'examen/ensayo_detail.html', {'ensayo': ensayo})

# -------------------------------------------------------------------
# VISTA: Crear Ensayo Clínico
# -------------------------------------------------------------------
@login_required
@permission_required('ExamenApp.add_ensayoclinico')
def crear_ensayo(request):
    if request.method == 'POST':
        formulario = EnsayoClinicoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Ensayo Clínico creado correctamente.")
            return redirect('ExamenApp:listado_ensayos')
    else:
        formulario = EnsayoClinicoForm()
    return render(request, 'Crud_EnsayoClinico/crear_ensayo.html', {'formulario': formulario})

# -------------------------------------------------------------------
# VISTA: Búsqueda avanzada de Ensayos Clínicos 
# -------------------------------------------------------------------
@login_required
@permission_required('ExamenApp.view_ensayoclinico')
def buscar_ensayo(request):
    formulario = form_module.BusquedaEnsayoForm(request.GET or None)
    resultados = []
    if formulario.is_valid():
        nombre = formulario.cleaned_data.get('nombre')
        qs = EnsayoClinico.objects.filter(nombre__icontains=nombre)
        if request.user.rol == Usuario.PACIENTE:
            paciente = get_object_or_404(Paciente, usuario=request.user)
            qs = qs.filter(pacientes=paciente)
        elif request.user.rol == Usuario.INVESTIGADOR:
            investigador = get_object_or_404(Investigador, usuario=request.user)
            qs = qs.filter(creado_por=investigador)
        resultados = qs
        
        return render(request, 'Crud_EnsayoClinico/ensayo_busqueda.html', {'formulario': formulario, 'resultados': resultados})
    
    return render(request, 'Crud_EnsayoClinico/buscar_ensayo.html', {'formulario': formulario, 'resultados': resultados})

# -------------------------------------------------------------------
# VISTA: Editar Ensayo Clínico
# -------------------------------------------------------------------
@login_required
@permission_required('ExamenApp.change_ensayoclinico')
def editar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(EnsayoClinico, id=ensayo_id)
    if request.method == 'POST':
        formulario = EnsayoClinicoForm(request.POST, instance=ensayo)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Ensayo Clínico actualizado correctamente.")
            return redirect('ExamenApp:listado_ensayos')
    else:
        formulario = EnsayoClinicoForm(instance=ensayo)
    return render(request, 'Crud_EnsayoClinico/editar_ensayo.html', {'formulario': formulario, 'ensayo': ensayo})

# -------------------------------------------------------------------
# VISTA: Eliminar Ensayo Clínico
# -------------------------------------------------------------------
@login_required
@permission_required('ExamenApp.delete_ensayoclinico')
def eliminar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(EnsayoClinico, id=ensayo_id)
    ensayo.delete()
    messages.success(request, "Ensayo Clínico eliminado.")
    return redirect('ExamenApp:listado_ensayos')


