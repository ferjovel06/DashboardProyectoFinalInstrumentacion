from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.http import require_POST
from paho.mqtt import publish

from .models import Measure, Suggestion
from django.utils import timezone

@csrf_exempt
def request_data(request):
    print("Solicitud de datos recibida")
    print(request.body)
    if request.method == "POST":
        print("Datos recibidos:")
        print(request.POST)
        caudal = float(request.POST.get("caudal", 0))
        velocidad_motor = float(request.POST.get("velocidad_motor", 0))

        Measure.objects.create(caudal=caudal, velocidad_motor=velocidad_motor)
        return HttpResponse("Datos recibidos", status=201)
    return HttpResponse("Método no permitido", status=405)


def dashboard(request):
    measurements = Measure.objects.order_by('-timestamp')[:30]
    last_velocidad_motor = measurements[0].velocidad_motor if measurements else None
    last_caudal = measurements[0].caudal if measurements else None
    last_botellas = measurements[0].cant_botellas if measurements else None
    last_cant_liquido = measurements[0].cant_liquido if measurements else None

    suggestions = Suggestion.objects.order_by('-timestamp')[:5]

    context = {
        'measurements': measurements,
        'last_velocidad_motor': last_velocidad_motor,
        'last_caudal': last_caudal,
        'last_botellas': last_botellas,
        'last_cant_liquido': last_cant_liquido,
        'suggestions': suggestions,
    }
    return render(request, 'dashboard.html', context)

def latest_measurement(request):
    last = Measure.objects.order_by('-timestamp').first()
    if last:
        data = {
            'last_velocidad_motor': last.velocidad_motor,
            'last_caudal': last.caudal,
            'last_botellas': last.cant_botellas,
            'last_cant_liquido': last.cant_liquido,
            'timestamp': last.timestamp.isoformat(),
        }
    else:
        data = {
            'velocidad_motor': None,
            'caudal': None,
            'cant_botellas': None,
            'cant_liquido': None,
            'timestamp': None,
        }
    return JsonResponse(data)

def get_observations(request):
    measurements = Measure.objects.order_by('-timestamp')[:1]
    observations = []

    if measurements:
        now = timezone.now()
        timestamp = measurements[0].timestamp
        minutes_ago = int((now - timestamp).total_seconds() // 60)
        time_str = f"Hace {minutes_ago} minutos" if minutes_ago > 0 else "Hace menos de 1 minuto"

        last_velocidad_motor = measurements[0].velocidad_motor

        if last_velocidad_motor is not None:
            if last_velocidad_motor < 6.5:
                observations.append({"text": "Nivel de pH bajo", "timestamp": time_str})
            elif 6.5 <= last_velocidad_motor <= 8.5:
                observations.append({"text": "Nivel de pH ideal", "timestamp": time_str})
            else:
                observations.append({"text": "Nivel de pH alto", "timestamp": time_str})

    return JsonResponse({'observations': observations})

def ph(request):
    measurements = Measure.objects.order_by('-timestamp')[:30]
    last_ph = measurements[0].ph if measurements else None

    context = {
        'measurements': measurements,
        'last_ph': last_ph,
    }
    return render(request, 'ph.html', context)

def ph_data(request):
    measurements = Measure.objects.order_by("-timestamp")[:30]
    data = [
        {
            "timestamp": measurement.timestamp.strftime("%Y-%m-%d %H:%M"),
            "ph": measurement.ph,
        }
        for measurement in measurements
    ]
    return JsonResponse({"data": data})

def temperature(request):
    measurements = Measure.objects.order_by('-timestamp')[:30]
    last_temp = measurements[0].temperature if measurements else None

    context = {
        'measurements': measurements,
        'last_temp': last_temp,
    }
    return render(request, 'temperature.html', context)

def temperature_data(request):
    measurements = Measure.objects.order_by("-timestamp")[:30]
    data = [
        {
            "timestamp": measurement.timestamp.strftime("%Y-%m-%d %H:%M"),
            "temp": measurement.temperature,
        }
        for measurement in measurements
    ]
    return JsonResponse({"data": data})

def tds(request):
    measurements = Measure.objects.order_by('-timestamp')[:30]
    last_tds = measurements[0].tds if measurements else None

    context = {
        'measurements': measurements,
        'last_tds': last_tds,
    }
    return render(request, 'tds.html', context)

def tds_data(request):
    measurements = Measure.objects.order_by("-timestamp")[:30]
    data = [
        {
            "timestamp": measurement.timestamp.strftime("%Y-%m-%d %H:%M"),
            "tds": measurement.tds,
        }
        for measurement in measurements
    ]
    return JsonResponse({"data": data})

@csrf_exempt
@require_POST
def set_auto_mode(request):
    data = json.loads(request.body)
    mode = data.get("mode")
    if mode not in ["auto", "manual"]:
        return JsonResponse({"error": "Modo inválido"}, status=400)

    topic = "sistema/auto_mode"
    payload = "ON" if mode == "auto" else "OFF"
    publish.single(topic, payload, hostname="192.168.177.32", port=1883)

    return JsonResponse({"success": True})

@csrf_exempt
@require_POST
def set_motor_state(request):
    data = json.loads(request.body)
    motor = data.get("motor")
    state = data.get("state")  # True o False

    # Define el topic y payload según el motor
    if motor == "ph_alcalino":
        topic = "sistema/motor_ph_alcalino"
    elif motor == "ph_acido":
        topic = "sistema/motor_ph_acido"
    elif motor == "tds_altos":
        topic = "sistema/motor_tds_altos"
    else:
        return JsonResponse({"error": "Motor inválido"}, status=400)

    payload = "ON" if state else "OFF"

    publish.single(topic, payload, hostname="192.168.177.32", port=1883)
    return JsonResponse({"success": True})
