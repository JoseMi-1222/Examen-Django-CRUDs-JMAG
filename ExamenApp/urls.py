from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'ExamenApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('listado_ensayos/', views.listado_ensayos, name='listado_ensayos'),
    path('ensayo/<int:ensayo_id>/', views.detalle_ensayo, name='detalle_ensayo'),
    path('ensayo/crear/', views.crear_ensayo, name='crear_ensayo'),
    path('ensayo/buscar/', views.buscar_ensayo, name='buscar_ensayo'),
    path('ensayo/editar/<int:ensayo_id>/', views.editar_ensayo, name='editar_ensayo'),
    path('ensayo/eliminar/<int:ensayo_id>/', views.eliminar_ensayo, name='eliminar_ensayo'),
]