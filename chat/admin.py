from django.contrib import admin
from .models import ConversacionChat, Contacto

@admin.register(ConversacionChat)
class ConversacionChatAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'estado', 'fecha_inicio', 'fecha_ultima_actividad')
    list_filter = ('estado', 'fecha_inicio')
    readonly_fields = ('fecha_inicio', 'fecha_ultima_actividad')


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'fecha_envio', 'asunto', 'mensaje')
    list_filter = ('fecha_envio',)
    search_fields = ('nombre', 'email', 'telefono')
    readonly_fields = ('fecha_envio',)
