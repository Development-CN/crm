import asyncio
import json
import logging
from datetime import datetime

import requests as api
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from citas_mazda_col.models import *
from citas_mazda_col.utils import (
    NotificacionCorreo,
    correo_citas,
    get_data_api,
    get_data_api_mazda,
    whatsapp_citas,
)

logger = logging.getLogger(__name__)

CITA_CREAR = settings.CITAS_TABLEROAPI + "/api/nueva_cita/"
CITA_CREAR_MAZDA = "http://capnet.ddns.net/capnet_dotnet_services/api/capnet_servicios/SetCita"
CITA_BORRAR = settings.CITAS_TABLEROAPI + "/api/cancelar_cita/"
CITA_REAGENDAR = settings.CITAS_TABLEROAPI + "/api/reagendar_cita/"
DISPONIBILIDAD_ASESOR = settings.CITAS_TABLEROAPI + "/api/disponibilidad_asesor"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


class ClienteNuevaCita(TemplateView):
    template_name = "citas_mazda_col/cliente_nueva_cita.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agencia_nombre"] = settings.AGENCIA
        context["core_api"] = settings.COREAPI

        context["lista_asesores"] = VCitasUsuarios.objects.filter(activo=True)
        context["politica_privacidad_link"] = settings.AVISO_PRIVACIDAD
        context["modelos"] = ListaItemsModelos.objects.all()
        context["años"] = ListaItemsYears.objects.all().values_list("year", flat=True)

        context["familias_servicios"] = ListaItemsFamiliasServicios.objects.exclude(id=1)
        context["familia_kilometraje"] = ListaItemsFamiliasServicios.objects.filter(id=1).first()
        context["servicios"] = ListaItemsServicios.objects.exclude(familia=1)
        context["kilometrajes"] = ListaItemsServicios.objects.filter(familia=1)
        context["tipos_documentos"] = TiposDocumentos.objects.all()
        return context

    def post(self, request):
        r = request.POST
        if r.get("validacion_placas", None):
            cita = ActividadesCitas.objects.filter(no_placas=r["placas"]).exclude(id_estado=3).order_by("-fecha_cita").first()
            if cita:
                if cita.id_estado in [1, 2, 4]:
                    return HttpResponse(status=404)
                else:
                    return HttpResponse(status=200)
            else:
                return HttpResponse(status=200)

        if r.get("servicios", None):
            id_modelo = r.get("id_modelo", None)
            print(id_modelo)
            kilometrajes = ListaItemsServicios.objects.filter(familia=1).order_by("orden")
            costos_servicios = ListaItemsServiciosCostos.objects.filter(id_modelo=id_modelo)

            data = []
            for servicio in kilometrajes:
                try:
                    servicio_response = {}
                    servicio_response["id"] = servicio.id_servicio
                    servicio_response["nombre"] = servicio.nombre
                    servicio_response["descripcion"] = servicio.descripcion
                    servicio_response["costo"] = costos_servicios.get(
                        id_servicio=servicio.id_servicio, id_modelo=id_modelo
                    ).precio
                    servicio_response["express"] = servicio.express
                    data.append(servicio_response)
                except Exception as error:
                    print(error)

            return JsonResponse(data, safe=False)

        if r.get("asesor"):
            servicio_express: bool = True if r.get("express") == "true" else False

            asesores = VCitasUsuarios.objects.filter(activo=True, express=servicio_express).exclude(cveasesor="")

            return JsonResponse(list(asesores.values("cveasesor", "nombre")), safe=False)


class ClienteCancelarCita(LoginRequiredMixin, TemplateView):
    login_url = "tracker_pro_login"
    template_name = "citas_mazda_col/cliente_cancelar_cita.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agencia_nombre"] = "Capital Network"

        cliente = self.request.user
        no_cita = cliente.username

        if isinstance(no_cita, str):
            cita = ActividadesCitas.objects.filter(no_cita=no_cita).exclude(id_estado=3).first()
            context["fecha_hora_cita"] = str(cita.fecha_cita) + " " + str(cita.hora_cita)

        return context

    def post(self, request):
        if request.POST.get("cancelar_cita", None):
            try:
                cliente = request.user
                no_cita = cliente.username

                DATA = {"NumCita": int(no_cita)}

                post = api.post(url=CITA_BORRAR, data=json.dumps(DATA), headers=HEADERS)
                print(post.text)
                if post.status_code == 200:
                    update = CitasStatusCita.objects.get(no_cita=no_cita)
                    update.fecha_hora_fin_cancelacion = datetime.now()
                    update.save()

                    try:
                        update_cita = ActividadesCitas.objects.filter(no_cita=no_cita).exclude(id_estado=3).first()
                        update_cita.id_estado = 3
                        update_cita.save()
                    except Exception as error:
                        print(error)

                    asesor = VCitasUsuarios.objects.filter(cveasesor=update_cita.id_asesor).first().nombre

                    # Correo al contact center para notificar la cancelación de la cita
                    nuevo_correo = NotificacionCorreo(
                        direccion_email=settings.CITAS_CORREOS_INTERNOS,
                        titulo="Solicitud de cancelación de cita",
                        mensaje="Se ha solicitado la cancelación de la cita con los siguientes datos:",
                        cita=update_cita,
                        asesor=asesor,
                        preview="",
                    )
                    nuevo_correo.enviar()

                    logout(request)
                    return redirect("tracker_pro_login")
            except Exception:
                return HttpResponse(status=400)

class ClienteReagendarCita(LoginRequiredMixin, TemplateView):
    login_url = "tracker_pro_login"
    template_name = "citas_mazda_col/cliente_reagendar_cita.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user
        no_cita = cliente.username

        servicios = ActividadesCitasServicios.objects.filter(no_cita=no_cita).values_list("id_servicio", flat=True)
        servicios_no_express = ListaItemsServicios.objects.filter(id_servicio__in=servicios, express=False)

        if servicios.count() > 1 or servicios_no_express.exists():
            context["lista_asesores"] = VCitasUsuarios.objects.filter(activo=True, express=False)
        else:
            context["lista_asesores"] = VCitasUsuarios.objects.filter(activo=True, express=True)

        context["agencia_nombre"] = settings.AGENCIA

        context["modelos"] = ListaItemsModelos.objects.all().values_list("nombre", flat=True)
        context["años"] = ListaItemsYears.objects.all().values_list("year", flat=True)

        if isinstance(no_cita, str):
            cita = ActividadesCitas.objects.filter(no_cita=no_cita).exclude(id_estado=3).first()
            print(cita)
            context["fecha_hora_cita"] = str(cita.fecha_cita) + " " + str(cita.hora_cita)

        return context

    def post(self, request):
        r = request.POST
        cliente = self.request.user
        no_cita = cliente.username

        DATA = {
            "no_cita": int(no_cita),
            "fecha": r["fecha"].replace("/", "-"),
            "hora": r["hora"],
            "id_asesor": r["id_asesor"],
        }

        post = api.post(url=CITA_REAGENDAR, data=json.dumps(DATA), headers=HEADERS)
        print(post.text)

        if post.status_code == 200:
            update = ActividadesCitas.objects.filter(no_cita=no_cita).exclude(id_estado=3).first()
            update.fecha_cita = r["fecha"].replace("/", "-")
            update.hora_cita = r["hora"]
            update.id_asesor = r["id_asesor"]
            update.id_estado = 4
            update.save()

            datos_cita = {}
            datos_cita["fecha"] = update.fecha_cita
            datos_cita["hora"] = update.hora_cita
            datos_cita["no_placas"] = update.no_placas

            try:
                asesor = VCitasUsuarios.objects.filter(cveasesor=update.id_asesor).first().nombre
            except Exception:
                asesor = ""

            # Correo al asesor/contact center
            nueva_notificacion_correo = NotificacionCorreo(
                settings.CITAS_CORREOS_INTERNOS,
                titulo="Cita reagendada",
                mensaje="",
                cita=update,
                asesor=asesor,
            )
            nueva_notificacion_correo.enviar()

            # Correo al cliente
            asyncio.run(
                correo_citas(
                    fase=0,
                    direccion_correo=cliente.email,
                    datos_cita=datos_cita,
                    asesor=asesor,
                )
            )

            # Whatsapp al cliente
            if update.whatsapp:
                datos_cita["asesor"] = asesor
                asyncio.run(
                    whatsapp_citas(
                        1,
                        update.telefono,
                        datos_cita,
                    )
                )
            return HttpResponse(status=200)


class ManualView(TemplateView):
    template_name = "citas_mazda_col/manual.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AppointmentsView(APIView):
    def get(self, request):
        r = request.GET
        if r.get("id_asesor", None):
            date = r["date"]
            consultant = r["id_asesor"]
            print(f"CONSULTA | ID ASESOR: {consultant} | FECHA: {date}")

            DATA = {"id_asesor": consultant, "fecha": date.replace("/", "-")}

            try:
                get = api.get(DISPONIBILIDAD_ASESOR, data=json.dumps(DATA), headers=HEADERS)
                logger.warning("Respuesta de API Tablero")
                logger.warning(get.text)
                respuesta_api = json.loads(get.text)
                disponibilidad = []
            except Exception as error:
                logger.warning(error)

            for element in respuesta_api:
                disponibilidad.append(element["hora"])

            return Response(json.dumps(disponibilidad))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        r = request.POST
        logger.debug("Nueva cita")

        if r.get("id_asesor", None) and r.get("fecha", None) and r.get("hora", None):

            servicios_peticion = r.getlist("servicio")
            datos_cita = get_data_api(r)

            for servicio in servicios_peticion:
                datos_cita["servicio"] = ListaItemsServicios.objects.get(id=servicio).nombre

                logger.debug("Datos de la cita:")
                logger.debug(datos_cita)

                try:
                    post = api.post(url=CITA_CREAR, data=json.dumps(datos_cita), headers=HEADERS)
                    logger.debug("Respuesta de API tablero:")
                    logger.debug(post.text)
                    logger.debug(post.status_code)
                except Exception as error:
                    logger.error(error)

                if post.status_code == 200:
                    respuesta = json.loads(post.text)
                    no_cita = respuesta["details"]["no_cita"]
                    id_hd = respuesta["details"]["id_hd"]
                    datos_cita["NumCita"] = no_cita

            if post.status_code == 200:
                logger.debug("Cita creada en tablero")
                for id_servicio in servicios_peticion:
                    servicio = ListaItemsServicios.objects.get(id=id_servicio).nombre
                    ActividadesCitasServicios.objects.create(
                        no_cita=no_cita, servicio=servicio, id_servicio=id_servicio
                    )

            if post.status_code == 200:
                logger.debug("Servicios creados")
                respuesta = json.loads(post.text)
                nueva_cita = ActividadesCitas.objects.create(
                    no_cita=no_cita,
                    id_hd=id_hd,
                    id_asesor=datos_cita["id_asesor"],
                    fecha_cita=datos_cita["fecha"].replace("/", "-"),
                    no_placas=datos_cita["no_placas"],
                    cliente=datos_cita["cliente"],
                    correo=datos_cita["correo"],
                    modelo_vehiculo=datos_cita["modelo"],
                    color_vehiculo=datos_cita["color"],
                    tiempo=datos_cita["tiempo"],
                    observaciones=r["servicio_otros"],
                    year_vehiculo=datos_cita["ano"],
                    vin=datos_cita["vin"],
                    telefono=datos_cita["telefono"],
                    hora_cita=datos_cita["hora_cita"],
                    status="0",
                    whatsapp=datos_cita["whatsapp"],
                    kilometraje=datos_cita["kilometraje"],
                    id_estado=1,
                )
                logger.debug("Cita creada en capnet apps")

                try:
                    asesor = VCitasUsuarios.objects.filter(cveasesor=datos_cita["id_asesor"]).first().nombre
                except Exception:
                    asesor = ""

                datos_cita["asesor"] = asesor
                servicios = ListaItemsServicios.objects.filter(id__in=servicios_peticion).values_list(
                    "nombre", flat=True
                )

                print("r")
                print(r)

                #datos_cita_zapata = get_data_api_mazda(r, no_cita)
                #print(datos_cita_zapata)
                #post_mazda = api.post(url=CITA_CREAR_MAZDA, data=json.dumps(datos_cita_zapata), headers=HEADERS, auth=('S0022951509', 'Cpi@012@21User*'))
                #print(post_mazda.text)

                # Correo al cliente
                asyncio.run(
                    correo_citas(
                        fase=0,
                        direccion_correo=datos_cita["correo"],
                        datos_cita=datos_cita,
                        asesor=asesor,
                    )
                )

                # Correo a asesor/contact center
                nueva_notificacion_correo = NotificacionCorreo(
                    settings.CITAS_CORREOS_INTERNOS,
                    titulo="Nueva cita creada",
                    mensaje="",
                    cita=nueva_cita,
                    asesor=asesor,
                    servicios=servicios,
                )
                nueva_notificacion_correo.enviar()

                # Whatsapp al cliente
                if datos_cita["whatsapp"]:
                    asyncio.run(whatsapp_citas(0, datos_cita["telefono"], datos_cita))

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
