from datetime import datetime
from django import forms
from .models import *
from datetime import datetime
from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

# -------------------------------------------------------------------
# Formulario de registro de usuario personalizado
# -------------------------------------------------------------------
class RegistroForm(UserCreationForm):
    roles = (
        (Usuario.INVESTIGADOR, 'Investigador'),
        (Usuario.PACIENTE, 'Paciente'),
    )
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol')
        
# -------------------------------------------------------------------
# Formulario para crear un Ensayo Clínico
# -------------------------------------------------------------------
class EnsayoClinicoForm(ModelForm):
    class Meta:
        model = EnsayoClinico
        fields = ['nombre', 'descripcion', 'farmaco', 'pacientes', 'nivel_seguimiento', 'fecha_inicio', 'fecha_fin', 'activo', 'creado_por']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        descripcion = cleaned_data.get("descripcion")
        farmaco = cleaned_data.get("farmaco")
        nivel_seguimiento = cleaned_data.get("nivel_seguimiento")
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
            
        if nombre and EnsayoClinico.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("El nombre del ensayo clínico ya existe.")
            
        if descripcion and len(descripcion) < 100:
            raise forms.ValidationError("La descripción debe tener al menos 100 caracteres.")
            
        if farmaco and not farmaco.apto_para_ensayos:
            raise forms.ValidationError("El fármaco seleccionado no es apto para ensayos clínicos.")
            
        if nivel_seguimiento is not None and (nivel_seguimiento < 1 or nivel_seguimiento > 10):
            raise forms.ValidationError("El nivel de seguimiento debe estar entre 1 y 10.")
            
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
            
        if fecha_fin and fecha_fin > datetime.now().date():
            raise forms.ValidationError("La fecha de fin no puede ser posterior a la fecha actual.")
            
        return cleaned_data
    
# -------------------------------------------------------------------
# Formulario de búsqueda avanzada de Ensayos Clínicos
# -------------------------------------------------------------------
class BusquedaEnsayoForm(forms.Form):
    nombre = forms.CharField(required=True, max_length=100)
    fecha_inicio_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_inicio_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    nivel_seguimiento = forms.IntegerField(required=False, min_value=1, max_value=10)
    pacientes = forms.ModelMultipleChoiceField(queryset=Paciente.objects.all(), required=False)
    activo = forms.NullBooleanField(required=False, widget=forms.Select(choices=[(True, 'Sí'), (False, 'No')]))
    
    def clean(self):
        cleaned_data = super().clean()
        
        fecha_inicio= cleaned_data.get("fecha_inicio_desde")
        fecha_fin= cleaned_data.get("fecha_inicio_hasta")
        nivel_seguimiento= cleaned_data.get("nivel_seguimiento_min")
        activo= cleaned_data.get("activo")
        
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
            
        if fecha_fin and fecha_fin > datetime.now().date():
            raise forms.ValidationError("La fecha de fin no puede ser posterior a la fecha actual.")
        
        if nivel_seguimiento is not None and (nivel_seguimiento < 5 or nivel_seguimiento > 10):
            raise forms.ValidationError("El nivel de seguimiento debe estar entre 5 y 10.")
        
        if activo is not None and activo is False:
            raise forms.ValidationError("El ensayo clínico debe estar activo.")  
        
        return cleaned_data
    
    

