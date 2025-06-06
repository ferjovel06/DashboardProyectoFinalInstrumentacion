from django.urls import path
from . import views

urlpatterns = [
    path("datos/", views.request_data, name="recibir_datos"),
    path("", views.dashboard, name="dashboard"),
    path("ph/", views.ph, name="ph"),
    path("temperatura/", views.temperature, name="temperatura"),
    path("tds/", views.tds, name="tds"),
    path("latest/", views.latest_measurement, name="latest_measurement"),
    path("ph_data/", views.ph_data, name="ph_data"),
    path("temp_data/", views.temperature_data, name="temp_data"),
    path("tds_data/", views.tds_data, name="tds_data"),
    path("get_observations/", views.get_observations, name="get_observations"),
    path("get_motores/", views.get_motores, name="get_motores"),
    path("set_motor_state/", views.set_motor_state, name="set_motor_state"),
    path("set_auto_mode/", views.set_auto_mode, name="set_auto_mode"),
]
