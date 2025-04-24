from django.urls import path
from . import views

urlpatterns = [
    path('datos/', views.request_data, name='recibir_datos'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('latest/', views.latest_measurement, name='latest_measurement'),
]
