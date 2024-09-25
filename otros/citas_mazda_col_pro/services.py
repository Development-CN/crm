import asyncio
import logging

import httpx
from asgiref.sync import sync_to_async
from django.conf import settings
from rest_framework.renderers import JSONRenderer

from .models import Appointment
from .serializers import APIBoardSerializer

logger = logging.getLogger(__name__)


class AdvisorAvailability:
    def __init__(self, advisor_id, date):
        self.url = settings.CITAS_TABLEROAPI + "/api/disponibilidad_asesor"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.data = {
            "id_asesor": advisor_id,
            "fecha": date,
        }
        self.available_hours = []
        self.response = httpx.request(method="GET", url=self.url, json=self.data, headers=self.headers)

    def get_hours(self):
        self.available_hours = []
        for element in self.response.json():
            self.available_hours.append(element["hora"])
        return self.available_hours


class APIBoard:
    def __init__(self, appointment: Appointment):
        self.appointment = appointment

        self.schedule_url = settings.CITAS_TABLEROAPI + "/api/nueva_cita/"
        self.reschedule_url = settings.CITAS_TABLEROAPI + "/api/reagendar_cita/"
        self.cancel_url = settings.CITAS_TABLEROAPI + "/api/cancelar_cita/"

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def send_other_service_request(self, client: httpx.AsyncClient, data: bytes):
        response = await client.post(self.schedule_url, content=data)
        logger.info(f"Other service response status code: {response.status_code}")
        logger.info(f"Other service response: {response.text}")

    async def schedule_other_services(self):
        # Initialize client session
        async with httpx.AsyncClient(headers=self.headers, timeout=None) as client:
            # Synchronously get the list of secondary services
            other_services = await sync_to_async(list)(self.appointment.other_services.all())

            # Initialize a list of tasks
            tasks = []

            # Iterate over the secondary services
            for other_service in other_services:
                # Get the service's data
                serializer = APIBoardSerializer(self.appointment)
                serializer_data = serializer.data
                serializer_data["NumCita"] = self.appointment_number
                serializer_data["servicio"] = other_service.name

                # Render the data to JSON
                data = JSONRenderer().render(serializer_data)
                logger.info(f"Other service data: {data}")

                # Append the task to the list
                tasks.append(asyncio.ensure_future(self.send_other_service_request(client, data)))

            # Wait for all tasks to finish
            await asyncio.gather(*tasks)

    def schedule_service(self):
        # Get the service's data
        serializer = APIBoardSerializer(self.appointment)

        # Render the data to JSON
        data = JSONRenderer().render(serializer.data)
        logger.info(f"Main service data: {data}")

        # Synchronously schedule the service on the API
        response = httpx.post(url=self.schedule_url, content=data, headers=self.headers, timeout=None)
        logger.info(f"Main service response: {response.text}")
        logger.info(f"Main service response status code: {response.status_code}")

        # Store the relevant response data
        self.appointment_number = response.json()["details"]["no_cita"]
        logger.info(f"Appointment number from API: {self.appointment_number}")

        self.id_hd = response.json()["details"]["id_hd"]
        logger.info(f"ID HD from API: {self.id_hd}")

    def schedule_to_board(self):
        # Schedule appointment's main service
        logger.info("Scheduling main service...")
        self.schedule_service()
        logger.info("Main service scheduled.")

        # Schedule appointment's secondary services
        logger.info("Scheduling secondary services...")
        asyncio.run(self.schedule_other_services())
        logger.info("Secondary services scheduled.")

        # Update the appointment instance
        logger.info("Updating appointment...")
        self.appointment.appointment_number = self.appointment_number
        self.appointment.id_hd = self.id_hd
        self.appointment.save()
        logger.info("Appointment updated.")
