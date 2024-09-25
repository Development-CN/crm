import base64
import json
import logging
import os
from pathlib import Path

import numpy as np
import requests as api
from PIL import Image
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django_drf_filepond.models import TemporaryUpload
from tracker_pro_mazda_col.models import StatusCita, TrackerProActividadesCitas, VTracker

BASE_DIR: Path = settings.BASE_DIR
COREAPI_URL = settings.COREAPI
DIST = 5
HEADERS = {"Content-Type": "application/json"}
THRESHOLD = 100

MEDIA_DIR: Path = settings.MEDIA_ROOT
AUTH_DIR: Path = settings.MEDIA_ROOT / "auth"

AUTH_DIR.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger(__name__)


def tracker_login(request, no_placas):
    # Revisar si el cliente tiene cita
    try:
        cita = TrackerProActividadesCitas.objects.filter(no_placas=no_placas).exclude(id_estado=3).order_by("-fecha_hora_fin")[0]
        print(cita)
    except Exception as error:
        logging.warning(error)
        try:
            cita = VTracker.objects.filter(placas=no_placas).first()
        except Exception as error:
            logging.warning(error)

    print("hola0")
    print(cita)
    if cita and isinstance(cita, TrackerProActividadesCitas):
        status_cita = StatusCita.objects.filter(no_cita=cita.no_cita).first()
        # Revisar si el cliente esta registrado
        try:
            cliente = User.objects.get(username=cita.no_cita)
        except Exception as error:
            logger.warning(error)
            group = Group.objects.get_or_create(name="cliente")[0]
            cliente = User.objects.create(
                username=cita.no_cita,
                first_name=cita.cliente,
                email=cita.correo,
                is_staff=False,
            )
            cliente.groups.add(group)
        
        # Iniciar sesion de cliente
        if cliente:
            login(request, cliente)
            return True
        else:
            return False
    elif cita and isinstance(cita, VTracker):
        print("hola00")
        return cita.no_orden
    else:
        print("hola0000")
        return None


def guardar_base_64(base_64_str, no_unico, razon):
    data = base_64_str[22:].encode()

    with open(os.path.join(AUTH_DIR, "tmp.png"), "wb") as tmp:
        tmp.write(base64.decodebytes(data))

    img_buffer = Image.open(os.path.join(AUTH_DIR, "tmp.png")).convert("RGBA")
    arr = np.array(np.asarray(img_buffer))

    r, g, b, a = np.rollaxis(arr, axis=-1)

    mask = (
        (r > THRESHOLD)
        & (g > THRESHOLD)
        & (b > THRESHOLD)
        & (np.abs(r - g) < DIST)
        & (np.abs(r - b) < DIST)
        & (np.abs(g - b) < DIST)
    )
    arr[mask, 3] = 0
    img_buffer = Image.fromarray(arr, mode="RGBA")
    img_buffer.save(os.path.join(AUTH_DIR, f"{no_unico}-{razon}.png"))
    os.remove(os.path.join(BASE_DIR, "media", "auth", "tmp.png"))


def save_filepond(saving_list):
    """SAVES FILEPOND UPLOADS

    Args:
        saving_list (LIST): FILE'S SERVER ID LIST
    """
    elements = TemporaryUpload.objects.filter(upload_id=saving_list)
    for element in elements:
        os.rename(element.get_file_path(), os.path.join(MEDIA_DIR, element.upload_name))
        element.delete()
        print("FILEPOND ACTUALIZADO")


def enviar_whatsapp(prefijo, telefono, mensaje):
    DATA = {
        "phone": f"{prefijo}{telefono}",
        "body": mensaje,
    }
    try:
        post = api.post(url=COREAPI_URL, data=json.dumps(DATA), headers=HEADERS)
        if post.status_code == 200:
            return "CORE API: MENSAJE DE WHATSAPP ENVIADO"
        else:
            return "CORE API: ERROR"
    except Exception as e:
        return e


def entrevista_profesional_data(request_data: dict):
    data = request_data.copy()

    del data["no_homologados_check"]

    for key, value in data.items():
        if value == "no":
            data[key] = False
        elif value == "si":
            data[key] = True

    testigos = data.getlist("testigos", [])
    data = data.dict()
    data["testigos"] = testigos

    return data
