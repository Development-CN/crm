from django.urls import path
from capnet_api import views

urlpatterns = [
    path("seguimiento/tecnico/", views.APITecnico.as_view(), name="api_seguimiento_tecnico"),
    path("seguimiento/cotizacion/", views.APICotizacion.as_view(), name="api_seguimiento_cotizacion"),
    path("tracker/entrevista/", views.APIEntrevista.as_view(), name="api_tracker_evidencia"),
]
