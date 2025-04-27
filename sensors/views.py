from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

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

        # Verifica los valores de los motores
        print(f"motor_ph_alcalino: '{motor_ph_alcalino}'")
        print(f"motor_ph_acido: '{motor_ph_acido}'")
        print(f"motor_tds_altos: '{motor_tds_altos}'")

        # Compara después de eliminar espacios
        motor_ph_alcalino = motor_ph_alcalino == '1'
        motor_ph_acido = motor_ph_acido == '1'
        motor_tds_altos = motor_tds_altos == '1'

        # Verifica los valores de los motores
        print(f"Motor PH Alcalino: {motor_ph_alcalino}")
        print(f"Motor PH Ácido: {motor_ph_acido}")
        print(f"Motor TDS Altos: {motor_tds_altos}")

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

    # Extraer los valores de cada medición para pasar al frontend
    data = [
        {
            'timestamp': measurement.timestamp.strftime('%Y-%m-%d %H:%M'),
            'temperature': measurement.temperature,
            'ph': measurement.ph,
            'tds': measurement.tds,
        } for measurement in measurements
    ]

    context = {
        'measurements': measurements,
        'last_temp': last_temp,
        'last_ph': last_ph,
        'last_tds': last_tds,
        'last_ec': last_ec,
        'data': json.dumps(data),
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
