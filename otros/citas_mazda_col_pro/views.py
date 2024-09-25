import logging

from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .email import (
    AppointmentClientEmail,
    ContactCenterAppointmentEmail,
    ContactCenterEmail,
)
from .models import CarModel, DocumentType, Service, VCitasUsuarios
from .serializers import AppointmentSerializer, ContactCenterSerializer
from .services import AdvisorAvailability, APIBoard

logger = logging.getLogger(__name__)


class ScheduleAppointmentView(TemplateView):
    template_name = "citas_mazda_col_pro/appointment_schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        # Car Models
        context["car_models"] = CarModel.objects.all()
        # Document Types
        context["document_types"] = DocumentType.objects.all()
        # Services
        context["services"] = Service.objects.filter(others=False)
        context["other_services"] = Service.objects.filter(others=True)
        # Advisors
        context["advisors"] = VCitasUsuarios.objects.filter(cveperfil=2, cveasesor__isnull=False).exclude(cveasesor="")
        return context


class ReScheduleAppointmentView(TemplateView):
    template_name = "citas_mazda_col_pro/appointment_reschedule.html"


class CancelAppointmentView(TemplateView):
    template_name = "citas_mazda_col_pro/appointment_cancel.html"


class AppointmentAPIView(APIView):
    def post(self, request):
        data = request.data
        logger.info(f"Request data: {data}")

        request_type = data.get("type")
        logger.info(f"Request type: {request_type}")

        # Get available appointments
        if request_type == "availability":
            logger.info(f"Advisor ID: {data.get('advisor_id')}, Date: {data.get('date')}")

            advisor_availability = AdvisorAvailability(data.get("advisor_id"), data.get("date"))
            available_hours = advisor_availability.get_hours()

            logger.info(f"Available hours: {available_hours}")
            return Response(available_hours, status=status.HTTP_200_OK, content_type="application/json")

        # The appointment process was cancelled
        elif request_type == "other_service":
            contact_center_serializer = ContactCenterSerializer(data=data)

            if contact_center_serializer.is_valid():
                # Send email to contact center
                logger.info("Contact center data is valid")
                contact_center = contact_center_serializer.save()
                logger.info("Contact center instance created")

                # Send email to contact center
                logger.info("Sending email to contact center")
                contact_center_email = ContactCenterEmail(contact_center)
                contact_center_email.send()
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error(f"Invalid serializer data: {contact_center_serializer.errors}")
                return Response(status=status.HTTP_400_BAD_REQUEST)

        # The appointment process was completed
        elif request_type == "schedule":
            appointment_serializer = AppointmentSerializer(data=data)

            if appointment_serializer.is_valid():
                # Save appointment
                logger.info("Appointment data is valid")
                appointment = appointment_serializer.save()
                logger.info("Appointment instance created")

                # Send appointment to API Board
                logger.info("Sending appointment to API Board")
                api_board = APIBoard(appointment)
                api_board.schedule_to_board()

                # Send email to client
                logger.info("Sending email to client")
                email_client = AppointmentClientEmail(appointment)
                email_client.send()

                # Send email to contact center
                logger.info("Sending email to contact center")
                contact_center_email = ContactCenterAppointmentEmail(appointment)
                contact_center_email.send()

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
