import json
import requests as api
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from citas_mazda_col.models import ListaItemsModelos
from datetime import datetime

COREAPI = settings.COREAPI
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


class NotificacionCorreo:
    def __init__(
        self, direccion_email=None, titulo=None, mensaje=None, cita=None, asesor=None, servicios=None, preview=None
    ):
        self.direccion_email = direccion_email
        self.mensaje = mensaje
        self.context = {
            # INFORMACION GENERICA
            "preview": preview,
            "titulo": titulo,
            "mensaje": mensaje,
            # ELEMENTOS UI
            "asesor": asesor,
            "cita": cita,
            "servicios": servicios,
        }
        self.html = self.render(self.context)

    def render(self, context):
        html = render_to_string("citas_mazda_col/correo.html", context)
        return html

    def enviar(self):
        try:
            asunto_email = "Notificaciones Citas"
            email = EmailMessage(subject=asunto_email, body=self.html, to=self.direccion_email)
            email.content_subtype = "html"
            email.send(fail_silently=False)
            return True, self.mensaje
        except Exception as error:
            return False, self.mensaje


def get_data_api(request_body):
    if request_body.get("notificaciones-whatsapp") == "on":
        notificaciones = True
    else:
        notificaciones = False
    modelo_nombre = ListaItemsModelos.objects.get(id_modelo=request_body["modelo"]).nombre
    parsed_data = {
        "id_asesor": request_body["id_asesor"],
        "no_placas": request_body["no_placas"],
        "fecha": request_body["fecha"].replace("/", "-"),
        "cliente": request_body["cliente"],
        "modelo": modelo_nombre,
        "color": request_body.get("color", "SIN COLOR"),
        "tiempo": 60,
        "ano": int(request_body["año"]),
        "vin": request_body.get("vin", "00000000000000000"),
        "telefono": request_body["telefono"],
        "hora_cita": request_body["hora"],
        "correo": request_body["correo"],
        "whatsapp": notificaciones,
        "servicio": "",
        "kilometraje": int(request_body["kilometraje"]),
    }
    if not parsed_data["vin"]:
        parsed_data["vin"] = "00000000000000000"
    if not parsed_data["color"]:
        parsed_data["color"] = "SIN COLOR"
    return parsed_data

def get_data_api_mazda(request_body, no_cita):
    if request_body.get("notificaciones-whatsapp") == "on":
        notificaciones = True
    else:
        notificaciones = False
    modelo_nombre = ListaItemsModelos.objects.get(id_modelo=request_body["modelo"]).nombre
    print(datetime.strptime(request_body["fecha"].replace("/", "-"), "%Y-%M-%d").isoformat(sep="T", timespec="minutes"))
    parsed_data = {
        "id_Concesionario": "0001",
        "id_Sucursal": "AA",
        "num_cita": str(no_cita),
        "fecha_cita": datetime.strptime(request_body["fecha"].replace("/", "-"), "%Y-%M-%d").isoformat(sep="T", timespec="minutes"),
        "Hora_Recepcion": request_body["hora"],
        "tipo_unidad": modelo_nombre,
        "cliente": request_body["cliente"],
        "asesor": str(request_body["id_asesor"]),
        "id_asesor": str(request_body["id_asesor"]),
        "id_cliente": request_body["cliente"],
        "vin": request_body.get("vin", "00000000000000000"),
        "observaciones": request_body["servicio_otros"],
        "placas": request_body["no_placas"],
    }
    if not parsed_data["vin"]:
        parsed_data["vin"] = "00000000000000000"
    return parsed_data

async def whatsapp_citas(fase, telefono, datos_cita=None, mensaje=None):
    if fase == 0:
        mensaje = (
            f"{settings.AGENCIA}\n"
            + "Le recuerda que su cita ha quedado agendada.\n"
            + f"*Fecha:* {datos_cita['fecha']} \n"
            + f"*Hora:* {datos_cita['hora_cita']} \n"
            + f"*Asesor:* {str(datos_cita['asesor']).title()} \n"
        )
    elif fase == 1:
        mensaje = (
            f"{settings.AGENCIA}\n"
            + "Le recuerda que su cita ha sido reagendada.\n"
            + f"*Fecha:* {datos_cita['fecha']}\n"
            + f"*Hora:* {datos_cita['hora']}\n"
            + f"*Asesor:* {str(datos_cita['asesor']).title()}\n"
        )

    data = {
        "phone": "52" + str(telefono),
        "body": mensaje,
    }
    try:
        post = api.post(url=COREAPI, data=json.dumps(data), headers=HEADERS)
        if post.status_code == 200:
            print("CORE API: MENSAJE DE WHATSAPP ENVIADO")
        else:
            print("CORE API: ERROR")
    except Exception as error:
        print(error)


async def correo_citas(fase, direccion_correo, datos_cita=None, asesor=None):
    template_context = {}

    template_context["asunto"] = "Seguimiento en Línea"
    template_context["nombre_agencia"] = settings.AGENCIA
    template_context["cotizacion_url"] = f"http://{settings.DOMINIO}:{settings.PUERTO}/tracking/login/"
    template_context["telefono_agencia"] = settings.TELEFONO
    template_context["privacy_url"] = settings.AVISO_PRIVACIDAD
    template_context["logo"] = "https://logodownload.org/wp-content/uploads/2019/11/mazda-logo-0.png"
    template_context["link_tracker_pro"] = f"http://{settings.DOMINIO}:{settings.PUERTO}/tracker/login/"

    if datos_cita:
        template_context["cita"] = datos_cita
    if asesor:
        template_context["asesor"] = asesor

    if fase == 0:
        template_context["notif"] = True
        asunto = "Su cita ha quedado agendada"
    if fase == 1:
        template_context["notif"] = True

    html_content = render_to_string("citas_mazda_col/mail-template.html", template_context)

    client_mail = direccion_correo

    try:
        email = EmailMessage(
            f"{settings.AGENCIA} | {asunto}",
            html_content,
            settings.EMAIL_HOST_USER,
            [client_mail],
        )
        email.content_subtype = "html"
        email.send()

        print("CORREO ENVIADO")
    except Exception as error:
        print(error)
