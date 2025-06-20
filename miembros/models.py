from django.db import models

# Create your models here.

class Miembro(models.Model):
    IGLESIA_CHOICES = [
        ('Central', 'Iglesia Central'),
        ('Tekera', 'Filial La Tekera'),
        ('Pital', 'Filial El Pital'),
        ('Sauce', 'Filial El Sauce'),
    ]
    ESTADO_CIVIL_CHOICES = [
        ('Casado', 'Casado'),
        ('Acompañado', 'Acompañado'),
        ('Viudo', 'Viudo'),
    ]
    iglesia = models.CharField(max_length=20, choices=IGLESIA_CHOICES, default='Central')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True, null=True)
    nombre_conyugue = models.CharField(max_length=100, blank=True, null=True)
    cantidad_hijos = models.PositiveIntegerField(blank=True, null=True)
    nombres_hijos = models.TextField(blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M')
    nombre_padre = models.CharField(max_length=100, blank=True, null=True)
    nombre_madre = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    otros_cargos = models.CharField(max_length=200, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_miembros/', null=True, blank=True)

class Familia(models.Model):
    miembro = models.ForeignKey(Miembro, related_name='familia', on_delete=models.CASCADE)
    nombre_familiar = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
