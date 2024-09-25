import logging
from asyncio.log import logger
from email.mime.image import MIMEImage
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from PIL import Image, ImageDraw, ImageFont

from .models import Appointment, ContactCenter, VCitasUsuarios

logger = logging.getLogger(__name__)


class ContactCenterEmail:
    def __init__(self, contact_center: ContactCenter):
        # Store the appointment instance
        self.contact_center = contact_center
        self.email_template = "citas_mazda_col_pro/email/contact_center.html"

        # EmailMessage parameters
        self.subject = "Es necesario contactar al cliente"
        self.body = self.get_email_body()
        self.to: list = settings.CONTACT_CENTER_EMAIL

        self.email = EmailMessage(subject=self.subject, body=self.body, to=self.to)
        self.email.content_subtype = "html"
        self.email.mixed_subtype = "related"

    def get_email_body(self):
        message = "Es necesario contactar al cliente por la razón:"

        # Client needs other service
        if self.contact_center.cancellation_reason == 1:
            message += " Solicita otro servicio que no está en el catalogo"
            if self.contact_center.additional_service:
                message += f"\nServicio solicitado: {self.contact_center.additional_service}"

        # Client needs assistance because of a problem
        elif self.contact_center.cancellation_reason == 2:
            message += "El cliente presenta una novedad en el vehículo"

        html_content = render_to_string(
            self.email_template,
            {
                "contact_center": self.contact_center,
                "settings": settings,
                "message": message,
                "title": "Es necesario contactar al cliente",
            },
        )
        return html_content

    def send(self):
        try:
            self.email.send()
            logger.info("Email sent to contact center")
        except Exception as error:
            logger.exception(f"Error sending email to contact center: {error}", exc_info=True)


class ContactCenterAppointmentEmail:
    def __init__(self, appointment: Appointment):
        # Store the appointment instance
        self.appointment = appointment
        self.email_template = "citas_mazda_col_pro/email/contact_center.html"

        # EmailMessage parameters
        self.subject = "Nueva cita agendada"
        self.body = self.get_email_body()
        self.to: list = settings.CONTACT_CENTER_EMAIL

        self.email = EmailMessage(subject=self.subject, body=self.body, to=self.to)
        self.email.content_subtype = "html"
        self.email.mixed_subtype = "related"

    def get_email_body(self):
        message = ""

        html_content = render_to_string(
            self.email_template,
            {
                "appointment": self.appointment,
                "settings": settings,
                "message": message,
                "title": "Nueva cita agendada",
            },
        )
        return html_content

    def send(self):
        try:
            self.email.send()
            logger.info("Email sent to contact center")
        except Exception as error:
            logger.exception(f"Error sending email to contact center: {error}", exc_info=True)


class AppointmentClientEmail:
    def __init__(self, appointment: Appointment):
        # Store the appointment instance
        self.appointment = appointment
        self.email_template = "citas_mazda_col_pro/email/appointment_schedule.html"

        # Email image parameters
        self.font_title = ImageFont.truetype(
            str(Path(__file__).resolve().parent.absolute() / "email" / "MazdaType-Medium.otf"), size=32
        )
        self.font_subtitle = ImageFont.truetype(
            str(Path(__file__).resolve().parent.absolute() / "email" / "MazdaType-Medium.otf"), size=26
        )
        self.font_body = ImageFont.truetype(
            str(Path(__file__).resolve().parent.absolute() / "email" / "MazdaType-Medium.otf"), size=22
        )
        self.image_path = Path(__file__).resolve().parent.absolute() / "email" / "appointment_schedule.png"
        self.image_save_path = Path(__file__).resolve().parent.parent.absolute() / "appointment_schedule.png"

        # Email image
        self.image_context = {
            "title": f"BIENVENIDO A \n{settings.AGENCIA.upper()}",
            "client_first_name": f"\n{self.appointment.client_first_name.split(' ')[0]},",
            "greeting": (
                "Gracias por escogernos y poner en manos de nuestros expertos el "
                f"\ncuidado y mantenimiento de tu {self.appointment.car_model.name}. De "
                "\nacuerdo con tu solicitud hemos programado tu cita en nuestro "
                "\nconcesionario."
            ),
            "appointment_details": (
                f"Dia: {self.appointment.appointment_date}"
                f"\nHora: {self.appointment.appointment_time}"
                f"\nConcesionario: {settings.AGENCIA}"
                f"\nDirección: {settings.AGENCIA_DIRECCION}"
                f"\nAsesor: {VCitasUsuarios.objects.get(cveasesor=self.appointment.advisor_id).nombre}"
                f"\nServicio: {self.appointment.service.name}"
            ),
            "recommendations_title": ("AL MOMENTO DE INGRESAR" "\nTU VEHÍCULO RECUERDA:"),
            "recommendations": (
                # 1
                "\n\n- La puntualidad nos permite organizar mejor nuestra operación y "
                "\npoder prestarte un mejor servicio."
                # 2
                "\n\n- La recepción del vehículo toma aproximadamente 15 minutos. Es "
                "\nimportante que dispongas de este tiempo para asegurarnos de revisar "
                "\ncontigo el estado de tu vehículo y los servicios a realizar."
                # 3
                "\n\n- La persona que ingrese el vehículo al taller debe ser mayor de 18 y "
                "\nmenor de 60 años."
                # 4
                "\n\n- Por tu seguridad y la de nuestro equipo es obligatorio en todo "
                "\nmomento el uso de tapabocas y guantes."
                # 5
                "\n\n- No recibimos dinero en efectivo, únicamente por medios "
                "\nelectrónicos (Datáfono, PSE, PlaceToPay)."
                # 6
                "\n\n- Al llegar al taller, estacione el vehículo y deje el control sobre el "
                "\nparabrisas dentro de una bolsa transparente, procederemos con la "
                "\ndesinfección del mismo."
                # 7
                "\n\n- Preferiblemente no dejar objetos personales. Si es necesario, "
                "\nasegúrate de dejarlo registrado en la orden de trabajo."
            ),
            "footer": (
                "Si necesitas modificar o cancelar tu cita, por favor comunícate al "
                f"\nteléfono {settings.TELEFONO} o al correo electrónico "
                f"\n{settings.CORREO_CONTACTO}."
            ),
        }

        # Draw the text on the image
        self.image_draw_text()

        # EmailMessage parameters
        self.subject = "Su cita ha sido agendada"
        self.body = self.get_email_body()
        self.to: list = [self.appointment.client_email]

        self.email = EmailMessage(subject=self.subject, body=self.body, to=self.to)
        self.email.content_subtype = "html"
        self.email.mixed_subtype = "related"
        self.attach_image()

    def image_draw_text(self):
        with Image.open(self.image_path) as image:
            image_draw = ImageDraw.Draw(image)

            # Draw the title
            image_draw.text((50, 580), self.image_context["title"], font=self.font_title, fill="black")

            # Draw the client first name
            image_draw.text((50, 680), self.image_context["client_first_name"], font=self.font_body, fill="black")

            # Draw the greeting
            image_draw.text((50, 730), self.image_context["greeting"], font=self.font_body, fill="black")

            # Draw the appointment details
            image_draw.text((50, 890), self.image_context["appointment_details"], font=self.font_body, fill="black")

            # Draw the recommendations title
            image_draw.text(
                (50, 1100), self.image_context["recommendations_title"], font=self.font_subtitle, fill="black"
            )

            # Draw the recommendations
            image_draw.text((50, 1165), self.image_context["recommendations"], font=self.font_body, fill="black")

            # Draw the footer
            image_draw.text((70, 1820), self.image_context["footer"], font=self.font_body, fill="black", align="center")

            # Create a buffer to save the image
            stream_bytes = BytesIO()

            # Save the image to the buffer
            image.save(stream_bytes, format="png")

            # Seek the buffer to the beginning
            stream_bytes.seek(0)

            # Store the image data
            self.image = stream_bytes.read()

    def get_email_body(self):
        html_content = render_to_string(self.email_template)
        return html_content

    def attach_image(self):
        email_image = MIMEImage(self.image)
        email_image.add_header("Content-ID", "<appointment_schedule.png>")
        email_image.add_header("Content-Disposition", "inline", filename="appointment_schedule.png")
        self.email.attach(email_image)

    def send(self):
        try:
            self.email.send()
            logger.info("Email sent to client")
        except Exception as error:
            logger.exception(f"Error sending email to contact center: {error}", exc_info=True)
