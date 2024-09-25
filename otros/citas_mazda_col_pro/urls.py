from django.urls import path

from citas_mazda_col_pro.views import *

urlpatterns = [
    path("schedule", ScheduleAppointmentView.as_view(), name="schedule"),
    path("reschedule/<int:pk>", ReScheduleAppointmentView.as_view(), name="reschedule"),
    path("cancel/<int:pk>", CancelAppointmentView.as_view(), name="cancel"),
    path("api/appointment", AppointmentAPIView.as_view(), name="api_appointment"),
]
