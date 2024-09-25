import logging
from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker_pro_mazda_col.models import *
from tracker_pro_mazda_col.utils import entrevista_profesional_data, tracker_login

logger = logging.getLogger(__name__)


# LOGIN
class TrackerProLogin(TemplateView):
    template_name = "tracker_pro_mazda_col/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agencia_nombre"] = settings.AGENCIA
        return context

    def post(self, request):
        no_placas = request.POST["placas"]

        context = {}
        context["agencia_nombre"] = settings.AGENCIA
        context["error"] = "Ingrese un numero de placa valido"
        # HACER LOGIN DE CLIENTE
        if no_placas:
            login = tracker_login(request, no_placas)
            logger.warning("Login: {}".format(login))
            if login == True:
                logger.warning("Login correcto")
                return redirect("tracker_pro")
            elif login:
                logger.warning("Login sin cita")
                return redirect("tracker_pro_loginless", no_orden=login)
            else:
                logger.warning("Login incorrecto")
                return render(request, "tracker_pro_mazda_col/login.html", context)
        else:
            logger.warning("Login sin placa")
            return render(request, "tracker_pro_mazda_col/login.html", context)


# Pantalla principal
class TrackerProView(LoginRequiredMixin, TemplateView):
    login_url = "tracker_pro_login"
    template_name = "tracker_pro_mazda_col/cliente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.request.user
        no_cita = cliente.username

        # Status citas
        if isinstance(no_cita, str):
            try:
                StatusCita.objects.get(no_cita=no_cita)
            except Exception:
                fecha_hora_fin_cita = TrackerProActividadesCitas.objects.filter(no_cita=no_cita).first().fecha_hora_fin
                StatusCita.objects.create(no_cita=no_cita, fecha_hora_fin_cita=fecha_hora_fin_cita)

            context["log"] = StatusCita.objects.get(no_cita=no_cita)
            context["agencia_nombre"] = settings.AGENCIA
            context["agencia_nombre_maps"] = str(settings.AGENCIA).replace(" ", "+")
            context["agencia_correo"] = settings.EMAIL_HOST_USER
            context["agencia_telefono"] = settings.TELEFONO
            context["cliente"] = cliente

            context["cita"] = TrackerProActividadesCitas.objects.filter(no_cita=no_cita).first()

            # Tracker clasico
            try:
                context["fecha_hora_llegada"] = VInformacionCitas.objects.get(no_cita=no_cita)
                context["tracker"] = tracker_clasico(context["fecha_hora_llegada"].no_orden)
                context["documentos_digitales"] = {}

                for boton, url in settings.TRACKER_PRO_DOCUMENTOS.items():
                    context["documentos_digitales"][boton] = str(url).replace(
                        "{{id_hd}}", str(context["tracker"]["details"].id_hd)
                    )
            except Exception as e:
                print(e)

            # Seguimiento en linea
            try:
                no_orden = VInformacionCitas.objects.get(no_cita=no_cita).no_orden
                hoja_multipuntos = TrackerProItems.objects.filter(no_orden=no_orden)
                if hoja_multipuntos:
                    context["hoja_multipuntos"] = True
            except Exception as e:
                print(e)

            # Entrevista Profesional
            try:
                context["entrevista"] = EntrevistaProfesional.objects.get(no_cita=no_cita)
            except Exception as error:
                logger.warning("Entrevista no encontrada")

        return context

    def post(self, request):
        cliente = self.request.user
        no_cita = cliente.username

        if request.POST.get("confirmar_cita", None):
            update = StatusCita.objects.get(no_cita=no_cita)
            update.fecha_hora_confirmacion_cita = datetime.now()
            update.save()

            try:
                update_cita = TrackerProActividadesCitas.objects.filter(no_cita=no_cita).exclude(id_estado=3).first()
                update_cita.id_estado = 2
                update_cita.save()
            except Exception as error:
                print(error)
            return HttpResponse(status=200)


# Tracker pro loginless
class TrackerProLoginlessView(TemplateView):
    template_name = "tracker_pro_mazda_col/cliente.html"

    def get_context_data(self, **kwargs):
        no_orden = self.kwargs["no_orden"]

        context = super().get_context_data(**kwargs)
        context["agencia_nombre"] = settings.AGENCIA
        context["agencia_nombre_maps"] = str(settings.AGENCIA).replace(" ", "+")
        context["agencia_correo"] = settings.EMAIL_HOST_USER
        context["agencia_telefono"] = settings.TELEFONO

        # Tracker clasico
        try:
            context["fecha_hora_llegada"] = VInformacionCitas.objects.get(no_orden=no_orden)
            context["tracker"] = tracker_clasico(no_orden)
            context["documentos_digitales"] = {}

            for boton, url in settings.TRACKER_PRO_DOCUMENTOS_DIGITALES.items():
                context["documentos_digitales"][boton] = str(url).replace(
                    "{{id_hd}}", str(context["tracker"]["details"].id_hd)
                )
        except Exception as error:
            logger.warning(error)

        # Seguimiento en linea
        try:
            hoja_multipuntos = TrackerProItems.objects.filter(no_orden=no_orden)
            if hoja_multipuntos:
                context["hoja_multipuntos"] = True
        except Exception as e:
            logger.warning(error)
        return context


# Entrevista Profesional
class EntrevistaProfesionalView(LoginRequiredMixin, TemplateView):
    template_name = "tracker_pro_mazda_col/entrevista_profesional.html"

    def post(self, request):
        try:
            request_body = request.POST
            cliente = request.user
            no_cita = cliente.username

            # Limpiar datos del front
            entrevista_profesional_info = entrevista_profesional_data(request_body)
            logger.warning(entrevista_profesional_info)

            cita = TrackerProActividadesCitas.objects.filter(no_cita=no_cita).exclude(id_estado=3).first()
            nueva_entrevista_profesional = EntrevistaProfesional(
                no_cita=no_cita, id_hd=cita.id_hd, **entrevista_profesional_info
            )
            nueva_entrevista_profesional.save()

            return HttpResponse(status=200)
        except Exception as error:
            logger.warning(error)
            return HttpResponse(status=500)


# LOGOUT
class TrackerProLogout(LogoutView):
    next_page = "tracker_pro_login"


# TRACKER CLASICO
def tracker_clasico(no_orden):
    query = VTracker.objects.filter(pk=no_orden)
    chips = int(query.count())
    operaciones = None
    if chips == 1:
        details = query.get()
    elif chips > 1:
        details = query.order_by("-inicio_tecnico")[:1].get()
        operaciones = query.order_by("inicio_tecnico")[0 : (chips - 1)]

    e_recepcion = "completed"
    e_asesor = "inactive"
    e_tecnico = "inactive"
    e_lavado = "inactive"
    e_entrega = "inactive"

    estados = [
        details.hora_inicio_asesor,
        details.hora_fin_asesor,
        details.inicio_tecnico,
        details.fin_tecnico,
        details.inicio_tecnico_lavado,
        details.fin_tecnico_lavado,
    ]

    mensajes = [
        "Su vehículo se encuentra en manos de un asesor.",
        "En breve su vehículo ingresará al taller de servicio.",
        "Su vehículo se encuentra en manos de un experto técnico",
        "Su vehículo ha salido del taller de servicio,  ingresara al area de lavado en breve.",
        "En unos momentos mas su vehículo estará listo para ser entregado.",
        "Su vehículo esta listo",
        "Su vehículo se encuentra detenido",
        "Su vehículo se encuentra detenido debido a que se necesita su autorización para continuar el proceso.",
        "En breve su asesor se comunicara con usted",
        "(Mensaje de pruebaruta)",
        "(Mensaje de cal+idad)",
        "(Mensaje de tot)",
    ]

    inactivos = [i for i, x in enumerate(estados) if not x]

    if details.ultima_actualizacion < 60:
        min = details.ultima_actualizacion
        if min == 1:
            u_actualizacion = f"{min:.0f} Minuto"
        else:
            u_actualizacion = f"{min:.0f} Minutos"
    elif details.ultima_actualizacion > 60 and details.ultima_actualizacion < 1440:
        min = details.ultima_actualizacion / 60
        if min < 2:
            u_actualizacion = f"{min:.0f} Hora"
        else:
            u_actualizacion = f"{min:.0f} Horas"
    elif details.ultima_actualizacion > 1440:
        min = details.ultima_actualizacion / 1440
        if min < 2:
            u_actualizacion = f"{min:.0f} Dia"
        else:
            u_actualizacion = f"{min:.0f} Dias"

    if inactivos == []:
        e_recepcion = "completed"
        e_asesor = "completed"
        e_tecnico = "completed"
        e_lavado = "completed"
        if details.motivo_paro is None:
            e_entrega = "active"
            serv_actual = "Status Actual: Listo Para Entrega"
            m_actual = mensajes[5]
        elif details.motivo_paro == "Autorización":
            e_entrega = "inactive"
            serv_actual = "Status actual: Detenido Por Autorización"
            m_actual = mensajes[7]
        else:
            e_entrega = "inactive"
            serv_actual = "Status actual: Detenido"
            m_actual = mensajes[6]

    elif inactivos[0] == 1:
        if details.motivo_paro is None:
            e_asesor = "active"
            serv_actual = "Status Actual: Asesor"
            m_actual = mensajes[0]
        elif details.motivo_paro == "Autorización":
            e_asesor = "inactive"
            serv_actual = "Status Actual: Detenido Por Autorización"
            m_actual = mensajes[7]
        else:
            e_asesor = "inactive"
            serv_actual = "Status Actual: Detenido"
            m_actual = mensajes[6]

    elif inactivos[0] == 2:
        if details.motivo_paro is None:
            e_asesor = "completed"
            serv_actual = "Ultimo Status: Asesor"
            m_actual = mensajes[1]
        elif details.motivo_paro == "Autorización":
            e_asesor = "inactive"
            serv_actual = "Status Actual: Detenido Por Autorización"
            m_actual = mensajes[7]
        else:
            e_asesor = "inactive"
            serv_actual = "Ultimo Status: Detenido"
            m_actual = mensajes[6]

    elif inactivos[0] == 3:
        e_asesor = "completed"
        if details.motivo_paro is None:
            e_tecnico = "active"
            serv_actual = "Status Actual: Servicio"
            m_actual = mensajes[2]
        elif details.motivo_paro == "Autorización":
            e_tecnico = "inactive"
            serv_actual = "Status Actual: Detenido Por Autorización"
            m_actual = mensajes[7]
        else:
            e_tecnico = "inactive"
            serv_actual = "Status Actual: Detenido"
            m_actual = mensajes[6]

    elif inactivos[0] == 4:
        e_asesor = "completed"
        if details.motivo_paro is None:
            e_tecnico = "completed"
            serv_actual = "Ultimo Status: Servicio"
            m_actual = mensajes[3]
        elif details.motivo_paro == "Autorización":
            e_tecnico = "inactive"
            serv_actual = "Status Actual: Detenido Por Autorización"
            m_actual = mensajes[7]
        else:
            e_tecnico = "inactive"
            serv_actual = "Ultimo Status: Detenido"
            m_actual = mensajes[6]

    elif inactivos[0] == 5:
        e_asesor = "completed"
        e_tecnico = "completed"
        if details.motivo_paro is None:
            e_lavado = "active"
            serv_actual = "Status Actual: Lavado"
            m_actual = mensajes[4]
        elif details.motivo_paro == "Autorización":
            e_lavado = "inactive"
            serv_actual = "Status Actual: Detenido Por Autorización"
            m_actual = mensajes[7]
        else:
            e_lavado = "inactive"
            serv_actual = "Status Actual: Detenido"
            m_actual = mensajes[6]

    context_tracker = {
        "chips": chips,
        "details": details,
        "e_recepcion": e_recepcion,
        "e_asesor": e_asesor,
        "e_tecnico": e_tecnico,
        "e_lavado": e_lavado,
        "e_entrega": e_entrega,
        "serv_actual": serv_actual,
        "m_actual": m_actual,
        "u_actualizacion": u_actualizacion,
        "range": range(1, (chips)),
        "operaciones": operaciones,
    }

    return context_tracker


# API DE CONSULTA
class TrackerProAPI(APIView):
    # CONSULTA DE INFORMACION
    def post(self, request):
        r = request.data
        if r.get("no_cita", None):
            no_cita = r.get("no_cita", None)
            cita = TrackerProActividadesCitas.objects.filter(no_cita=no_cita).exclude(id_estado=3).first()
            status_general = StatusCita.objects.filter(no_cita=no_cita).first()

            servicios = TrackerProActividadesCitasServicios.objects.filter(no_cita=no_cita).values_list("id_servicio")
            query_servicios = TrackerProListaItemsServicios.objects.filter(id__in=servicios).values(
                "nombre", "descripcion", "costo"
            )

            if status_general:
                if status_general.fecha_hora_fin_cita and not status_general.fecha_hora_confirmacion_cita:
                    status_cita = "NO CONFIRMADA"
                if status_general.fecha_hora_confirmacion_cita:
                    status_cita = "CONFIRMADA"
                if status_general.fecha_hora_fin_cancelacion:
                    status_cita = "CANCELADA"
            else:
                status_cita = "SIN ESTATUS"

            response = {}
            response["no_cita"] = no_cita
            response["id_estado"] = cita.id_estado
            response["cliente"] = cita.cliente
            response["kilometraje"] = cita.kilometraje
            response["telefono"] = cita.telefono
            response["email"] = cita.correo
            response["fecha_cita"] = cita.fecha_cita
            response["hora_cita"] = cita.hora_cita
            response["status"] = status_cita
            response["servicios"] = query_servicios

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"error": "no se encontro el numero de cita"},
                status=status.HTTP_404_NOT_FOUND,
            )


class TrackerProEstados(APIView):
    def post(self, request):
        r = request.data
        lista_vin = r.get("lista_vin", None)
        if isinstance(lista_vin, (list, tuple)):
            informacion_citas = TrackerProActividadesCitas.objects.filter(vin__in=lista_vin).values()
            if informacion_citas:
                return Response(data=informacion_citas, status=status.HTTP_200_OK)
            else:
                return Response(data={"error": "no results"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"error": "invalid data type"}, status=status.HTTP_400_BAD_REQUEST)
