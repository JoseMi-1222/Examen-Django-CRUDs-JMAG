from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'ExamenApp'

urlpatterns = [
    path('', views.index, name='index'),
]