from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat, name='chat'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/chat-history/<str:session_id>/', views.get_chat_history, name='chat_history'),
    path('contacto/', views.contacto, name='contacto'),
]
