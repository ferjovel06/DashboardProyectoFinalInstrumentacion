from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import Measures

@csrf_exempt
def request_data(request):
    if request.method == "POST":
        temperature = float(request.POST.get("temperatura", 0))
        ph = float(request.POST.get("ph", 0))
        tds = float(request.POST.get("tds", 0))

        Measures.objects.create(temperature=temperature, ph=ph, tds=tds)
        return HttpResponse("Datos recibidos", status=201)
    return HttpResponse("Método no permitido", status=405)


def dashboard(request):
    measurements = Measures.objects.order_by('-timestamp')[:30]
    last_temp = measurements[0].temperature if measurements else None
    last_ph = measurements[0].ph if measurements else None
    last_tds = measurements[0].tds if measurements else None
    last_ec = measurements[0].ec if measurements else None

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
    }
    return render(request, 'dashboard.html', context)

def latest_measurement(request):
    last = Measures.objects.order_by('-timestamp').first()
    if last:
        data = {
            'temperature': last.temperature,
            'ph': last.ph,
            'tds': last.tds,
            'timestamp': last.timestamp.isoformat(),
        }
    else:
        data = {
            'temperature': None,
            'ph': None,
            'tds': None,
            'timestamp': None,
        }
    return JsonResponse(data)