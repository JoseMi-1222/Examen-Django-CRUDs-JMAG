from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

admin.site.register(Usuario, UserAdmin)
admin.site.register(Investigador)
admin.site.register(Paciente)
admin.site.register(Farmaco)
admin.site.register(EnsayoClinico)  