from django.db import models 
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    INVESTIGADOR = 2
    PACIENTE = 3
    ROLES = (
        (ADMINISTRADOR, 'administrador'),
        (INVESTIGADOR, 'investigador'),
        (PACIENTE, 'paciente'),
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES, default=1
    )

class Investigador(models.Model):
   usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True)
   
   def __str__(self):
       return self.usuario.username
   
class Paciente(models.Model):
   usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True)
   
   def __str__(self):
       return self.usuario.username
   
class Farmaco(models.Model):
   nombre = models.CharField(max_length=100)
   apto_para_ensayos = models.BooleanField()
   
   def __str__(self):
       return self.nombre
   
class EnsayoClinico(models.Model):
   nombre = models.CharField(max_length=100)
   descripcion = models.TextField()
   farmaco = models.ForeignKey(Farmaco, on_delete=models.CASCADE)
   pacientes = models.ManyToManyField('Paciente')
   nivel_seguimiento = models.IntegerField()
   fecha_inicio = models.DateField()
   fecha_fin = models.DateField()
   activo = models.BooleanField(default=True)
   creado_por = models.ForeignKey('Investigador', on_delete=models.CASCADE)  
   
   def __str__(self):
       return self.nombre