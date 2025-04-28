from django.urls import path
from . import views

urlpatterns = [
    path("datos/", views.request_data, name="recibir_datos"),
    path("", views.dashboard, name="dashboard"),
    path("latest/", views.latest_measurement, name="latest_measurement"),
    path("get_observations/", views.get_observations, name="get_observations"),
    path("get_motores/", views.get_motores, name="get_motores"),
    path("set_motor_state/", views.set_motor_state, name="set_motor_state"),
]
