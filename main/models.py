from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de Empresa")
    mission = models.TextField(verbose_name="Mision de Empresa") 
    vision = models.TextField(verbose_name="Vision de Empresa") 
    general_manager = models.CharField(max_length=100, verbose_name="Gerente General") 
    location = models.CharField(max_length=100, verbose_name="Ubicacion de Empresa") 
    fundation_date = models.DateField(verbose_name="Fecha de Fundacion") 
    ruc = models.CharField(max_length=11, verbose_name="Ruc de Empresa") 
    phone = models.CharField(max_length=20, verbose_name="Telefono de Empresa")
    email = models.EmailField(max_length=100, verbose_name="Correo de Empresa") 
    password = models.CharField(max_length=100, verbose_name="Contraseña", null=True) #QUITAR el null true cuando se reinicie TODOS los modelos
    
    def __str__(self):
        return self.name