from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Modulo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    texto = models.TextField()
    opcion_a = models.CharField(max_length=200)
    opcion_b = models.CharField(max_length=200)
    opcion_c = models.CharField(max_length=200)
    opcion_d = models.CharField(max_length=200)
    respuesta_correcta = models.CharField(max_length=1) # A, B, C, etc.
    def __str__(self):
        return self.texto

class Progreso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    puntaje = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username} - {self.modulo.nombre}"
