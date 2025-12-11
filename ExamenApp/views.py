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

# -------------------------------
# VISTA: Página de inicio
# -------------------------------
def index(request):
    return render(request, 'examen/index.html')



