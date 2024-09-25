import asyncio
from datetime import datetime, timedelta

import httpx
from django.conf import settings
from django.urls import reverse

from .models import (
    ActividadesCitas,
    VCitasActividadesCitasTablero,
    VCitasUsuarios,
    VInformacionCitas,
)

COREAPI_URL = settings.COREAPI_MENSAJES_RECORDATORIOS
HEADERS = {"Content-Type": "application/json"}
URL_LISTADO_CITAS = settings.CITAS_TABLEROAPI + "/api/lista_citas/"


# Actualización de estado de las citas
def actualizacion_estado_citas():
    print("Tarea programada: Actualización de estado de las citas")

    ahora = datetime.now().date()
    citas_actualizar = []

    for cita in ActividadesCitas.objects.filter(id_estado__in=[1, 2, 4]).iterator():
        # Citas atendidas
        if VInformacionCitas.objects.filter(id_hd=cita.id_hd).exists():
            print("Cita atendida")
            cita.id_estado = 6
            citas_actualizar.append(cita)

        # Citas no atendidas
        else:
            diferencia = ahora - cita.fecha_cita
            if diferencia.days >= 1:
                print("Cita no atendida")
                cita.id_estado = 5
                citas_actualizar.append(cita)

    # Hacer bulk update
    ActividadesCitas.objects.bulk_update(citas_actualizar, ["id_estado"])
    print("Bulk update terminado")


# Envío de recordatorios de citas
def envio_recordatorios_citas():
    print("Tarea programada: Envío de recordatorios de citas")
    asyncio.run(recordatorios_whatsapp())


async def recordatorios_whatsapp():
    ahora = datetime.now().date()
    mañana = ahora + timedelta(1)

    citas = ActividadesCitas.objects.filter(fecha_cita=mañana)
    citas_tablero = VCitasActividadesCitasTablero.objects.filter(fecha_cita__date=mañana)

    asesores = VCitasUsuarios.objects.all()

    async with httpx.AsyncClient(headers=HEADERS, timeout=None) as client:
        # Inicializar lista de tareas
        tasks = []

        # Se itera sobre las citas
        await gather_requests(citas, asesores, tasks, client)
        await gather_requests(citas_tablero, asesores, tasks, client)

        # Wait for all tasks to finish
        await asyncio.gather(*tasks)


async def gather_requests(citas, asesores, tasks, client):
    async for cita in citas.aiterator():
        try:
            asesor = await asesores.aget(cveasesor=cita.id_asesor).nombre
        except Exception:
            asesor = ""

        mensaje = (
            f"{settings.AGENCIA}"
            + "\n"
            + f"Le recuerda que tiene una cita para el dia de mañana para su vehiculo {cita.modelo_vehiculo}, con placas {cita.no_placas}"
            + "\n"
            + f"*Fecha:* {cita.fecha_cita}"
            + "\n"
            + f"*Hora:* {cita.hora_cita}"
            + "\n"
            + f"*Asesor:* {asesor.title()}"
            + "\n"
            + "\n"
            + "Para confirmar su cita ingrese al siguiente enlace e inicie sesión con las placas de su vehículo: \n"
            + f"http://{settings.DOMINIO}:{settings.PUERTO}{reverse('tracker_pro_login')}"
        )

        # Cuerpo de la petición
        data = {
            "phone": "52" + str(cita.telefono),
            "body": mensaje,
            "id_estrategia": cita.id_estrategia,
            "vin": cita.vin,
            "tipo": "recordatorio",
        }

        # Agregar la funcion al grupo de tareas
        tasks.append(peticion_coreapi(client, data))


async def peticion_coreapi(client: httpx.AsyncClient, data: dict):
    print(f"Data: {data}")
    response = await client.post(COREAPI_URL, json=data)
    print(f"Recordatorio WhatsApp status code: {response.status_code}")
    print(f"Recordatorio WhatsApp response: {response.text}")


# Agendar citas del tablero
def agendar_citas_tablero():
    print("Tarea: Agendar registros sin cita")

    # Consultar API tablero
    response = httpx.get(URL_LISTADO_CITAS)
    citas_tablero = response.json()

    for cita_tablero in citas_tablero:
        # Valores por defecto de la cita
        defaults_citas = {
            "id_asesor": cita_tablero["id_asesor"],
            "fecha_cita": cita_tablero["fecha_cita"],
            "no_placas": cita_tablero["no_placas"],
            "cliente": cita_tablero["cliente"],
            "correo": cita_tablero["email"],
            "modelo_vehiculo": cita_tablero["modelo_vehiculo"],
            "color_vehiculo": cita_tablero[""],
            "tiempo": 0,
            "year_vehiculo": cita_tablero["year_vehiculo"],
            "vin": cita_tablero["vin"],
            "servicio": cita_tablero["servicio"],
            "telefono": cita_tablero["telefono"],
            "hora_cita": cita_tablero["hora_cita"],
            "fecha_hora_fin": datetime.now(),
            "status": "0",
            "whatsapp": True,
            "kilometraje": cita_tablero["kilometraje"],
            "id_hd": cita_tablero["id_hd"],
        }

        # Actualizar o crear citas
        ActividadesCitas.objects.update_or_create(no_cita=cita_tablero["No_Cita"], defaults=defaults_citas)
