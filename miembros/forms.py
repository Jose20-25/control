from django import forms
from .models import Miembro
from datetime import date

class NinoForm(forms.ModelForm):
    nombre_padre = forms.CharField(label='Nombre del Padre', required=False)
    edad = forms.IntegerField(label='Edad', required=False, disabled=True)
    class Meta:
        model = Miembro
        fields = ['iglesia', 'nombre', 'apellido', 'sexo', 'nombre_padre', 'nombre_madre', 'fecha_nacimiento', 'edad', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'onchange': 'calcularEdad(this)'}),
            'foto': forms.ClearableFileInput(attrs={'accept': 'image/*', 'capture': 'environment'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fecha = self.initial.get('fecha_nacimiento') or (self.instance.fecha_nacimiento if self.instance else None)
        self.fields['edad'].initial = self.calcular_edad(fecha)

    def calcular_edad(self, fecha):
        if not fecha:
            return ''
        if isinstance(fecha, str):
            try:
                fecha = date.fromisoformat(fecha)
            except Exception:
                return ''
        hoy = date.today()
        return hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))

class JovenForm(forms.ModelForm):
    nombre_padre = forms.CharField(label='Nombre del Padre', required=False)
    edad = forms.IntegerField(label='Edad', required=False, disabled=True)
    class Meta:
        model = Miembro
        fields = ['iglesia', 'cargo', 'otros_cargos', 'nombre', 'apellido', 'sexo', 'nombre_padre', 'nombre_madre', 'fecha_nacimiento', 'edad', 'telefono', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'onchange': 'calcularEdad(this)'}),
            'foto': forms.ClearableFileInput(attrs={'accept': 'image/*', 'capture': 'environment'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fecha = self.initial.get('fecha_nacimiento') or (self.instance.fecha_nacimiento if self.instance else None)
        self.fields['edad'].initial = self.calcular_edad(fecha)

    def calcular_edad(self, fecha):
        if not fecha:
            return ''
        if isinstance(fecha, str):
            try:
                fecha = date.fromisoformat(fecha)
            except Exception:
                return ''
        hoy = date.today()
        return hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))

class AdultoForm(forms.ModelForm):
    edad = forms.IntegerField(label='Edad', required=False, disabled=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cantidad = 0
        cantidad_hijos_val = self.data.get('cantidad_hijos')
        if cantidad_hijos_val:
            try:
                cantidad = int(cantidad_hijos_val or 0)
            except (ValueError, TypeError):
                cantidad = 0
        elif self.instance and self.instance.cantidad_hijos:
            cantidad = self.instance.cantidad_hijos
        for i in range(1, cantidad + 1):
            self.fields[f'nombre_hijo_{i}'] = forms.CharField(label=f'Nombre del Hijo {i}', required=False)
        # Si hay datos previos, rellenar los campos
        if self.instance and self.instance.nombres_hijos:
            nombres = self.instance.nombres_hijos.split(',')
            for idx, nombre in enumerate(nombres, 1):
                if f'nombre_hijo_{idx}' in self.fields:
                    self.fields[f'nombre_hijo_{idx}'].initial = nombre.strip()
        fecha = self.initial.get('fecha_nacimiento') or (self.instance.fecha_nacimiento if self.instance else None)
        self.fields['edad'].initial = self.calcular_edad(fecha)

    class Meta:
        model = Miembro
        fields = ['iglesia', 'cargo', 'otros_cargos', 'nombre', 'apellido', 'sexo', 'estado_civil', 'nombre_conyugue', 'cantidad_hijos', 'fecha_nacimiento', 'edad', 'telefono', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'onchange': 'calcularEdad(this)'}),
            'foto': forms.ClearableFileInput(attrs={'accept': 'image/*', 'capture': 'environment'})
        }

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad_hijos') or 0
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            cantidad = 0
        nombres = []
        for i in range(1, cantidad + 1):
            nombre = cleaned_data.get(f'nombre_hijo_{i}', '')
            if nombre:
                nombres.append(nombre)
        cleaned_data['nombres_hijos'] = ', '.join(nombres)
        return cleaned_data

    def save(self, commit=True):
        self.instance.nombres_hijos = self.cleaned_data.get('nombres_hijos', '')
        return super().save(commit=commit)

    def calcular_edad(self, fecha):
        if not fecha:
            return ''
        if isinstance(fecha, str):
            try:
                fecha = date.fromisoformat(fecha)
            except Exception:
                return ''
        hoy = date.today()
        return hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
