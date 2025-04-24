from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
    context = {
        'measurements': measurements,
        'last_temp': last_temp,
    }
    return render(request, 'dashboard.html', context)

