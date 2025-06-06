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
    if request.method == "POST":
        temperature = float(request.POST.get("temperatura", 0))
        ph = float(request.POST.get("ph", 0))
        tds = float(request.POST.get("tds", 0))
        ec = float(request.POST.get("ec", 0))  # Optional field for electrical conductivity
        motor_ph_alcalino = request.POST.get('motor_ph_alcalino', '').strip()  # Strip any unwanted spaces
        motor_ph_acido = request.POST.get('motor_ph_acido', '').strip()
        motor_tds_altos = request.POST.get('motor_tds_altos', '').strip()

        motor_ph_alcalino = motor_ph_alcalino == '1'
        motor_ph_acido = motor_ph_acido == '1'
        motor_tds_altos = motor_tds_altos == '1'

        Measure.objects.create(temperature=temperature, ph=ph, tds=tds, ec=ec, motor_ph_alcalino=motor_ph_alcalino, motor_ph_acido=motor_ph_acido, motor_tds_altos=motor_tds_altos)
        return HttpResponse("Datos recibidos", status=201)
    return HttpResponse("Método no permitido", status=405)


def dashboard(request):
    measurements = Measure.objects.order_by('-timestamp')[:30]
    last_temp = measurements[0].temperature if measurements else None
    last_ph = measurements[0].ph if measurements else None
    last_tds = measurements[0].tds if measurements else None
    last_ec = measurements[0].ec if measurements else None
    suggestions = Suggestion.objects.order_by('-timestamp')[:5]

    context = {
        'measurements': measurements,
        'last_temp': last_temp,
        'last_ph': last_ph,
        'last_tds': last_tds,
        'last_ec': last_ec,
        'suggestions': suggestions,
    }
    return render(request, 'dashboard.html', context)

def latest_measurement(request):
    last = Measure.objects.order_by('-timestamp').first()
    if last:
        data = {
            'temperature': last.temperature,
            'ph': last.ph,
            'tds': last.tds,
            'ec': last.ec,
            'timestamp': last.timestamp.isoformat(),
        }
    else:
        data = {
            'temperature': None,
            'ph': None,
            'tds': None,
            'ec': None,
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

        last_ph = measurements[0].ph
        last_temp = measurements[0].temperature
        last_tds = measurements[0].tds

        if last_ph is not None:
            if last_ph < 6.5:
                observations.append({"text": "Nivel de pH bajo", "timestamp": time_str})
            elif 6.5 <= last_ph <= 8.5:
                observations.append({"text": "Nivel de pH ideal", "timestamp": time_str})
            else:
                observations.append({"text": "Nivel de pH alto", "timestamp": time_str})

        if last_temp is not None:
            if last_temp < 20:
                observations.append({"text": "Temperatura baja", "timestamp": time_str})
            elif 20 <= last_temp <= 30:
                observations.append({"text": "Temperatura ideal", "timestamp": time_str})
            else:
                observations.append({"text": "Temperatura alta", "timestamp": time_str})

        if last_tds is not None:
            if last_tds < 400:
                observations.append({"text": "Nivel de solidos disueltos aceptable", "timestamp": time_str})
            else:
                observations.append({"text": "Nivel de solidos disueltos alto", "timestamp": time_str})

    return JsonResponse({'observations': observations})

def get_motores(request):
    motor_ph_alcalino = Measure.objects.latest('id').motor_ph_alcalino
    motor_ph_acido = Measure.objects.latest('id').motor_ph_acido
    motor_tds_altos = Measure.objects.latest('id').motor_tds_altos

    # Devolver los datos en formato JSON
    return JsonResponse({
        'motor_ph_alcalino': motor_ph_alcalino,
        'motor_ph_acido': motor_ph_acido,
        'motor_tds_altos': motor_tds_altos,
    })

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
