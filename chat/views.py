from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json, requests, uuid
from .models import ConversacionChat, Contacto
from datetime import datetime



def index(request):
    return render(request, 'hospital/index.html')

def chat(request):
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    return render(request, 'hospital/chat.html', {'session_id': session_id})

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        session_id = data.get('session_id', '').strip()

        if not message or not session_id:
            return JsonResponse({'error': 'Mensaje y session_id son requeridos'}, status=400)

        conversacion, _ = ConversacionChat.objects.get_or_create(
            session_id=session_id,
            defaults={'mensajes': []}
        )

        conversacion.mensajes.append({
            'role': 'user',
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        conversacion.save()

        webhook_url = "http://localhost:5678/webhook/chatbot-hospital"
        payload = {
            'message': message,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        }

        response = requests.post(webhook_url, json=payload, timeout=30)
        response.raise_for_status()
        bot_response = response.json()
        bot_message = bot_response.get('message', 'Lo siento, no pude procesar tu solicitud.')

        conversacion.mensajes.append({
            'role': 'assistant',
            'message': bot_message,
            'timestamp': datetime.now().isoformat()
        })
        conversacion.save()

        return JsonResponse({
            'success': True,
            'response': bot_message
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_chat_history(request, session_id):
    try:
        conversacion = get_object_or_404(ConversacionChat, session_id=session_id)
        return JsonResponse({
            'success': True,
            'messages': conversacion.mensajes
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('email')
        telefono = request.POST.get('telefono')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')


        if not all([nombre, correo, telefono, asunto, mensaje]):
            return render(request, 'hospital/contacto.html', {
                'mensaje': 'Todos los campos son requeridos.',
                'modal_type': 'error'
            })

        Contacto.objects.create(
            nombre=nombre,
            email=correo,
            telefono=telefono,
            asunto=asunto,
            mensaje=mensaje
        )

        mensaje = 'Mensaje enviado correctamente.'
        return render(request, 'hospital/contacto.html', {'mensaje': mensaje, 'modal_type': 'success'})

    return render(request, 'hospital/contacto.html')