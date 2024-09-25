from django.urls import path

from .views import *

urlpatterns = [
    path("nuevacita/", ClienteNuevaCita.as_view(), name="client_new"),
    path("cancelar/", ClienteCancelarCita.as_view(), name="client_delete"),
    path("reagendar/", ClienteReagendarCita.as_view(), name="client_reschedule"),
    path("agenda/", AppointmentsView.as_view(), name="api_agenda"),
    path("captura/", ManualView.as_view(), name="agenda"),
]
