from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class ConversacionChat(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    mensajes = models.JSONField(default=list)
    estado = models.CharField(max_length=50, default='activa')
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_ultima_actividad = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversación {self.session_id}"
    
    class Meta:
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    asunto = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Contacto de {self.nombre}"
    
    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['-fecha_envio']