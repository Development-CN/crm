import base64
import calendar
import hashlib
import json
import logging
import mimetypes
import os
from datetime import date, datetime
from decimal import Decimal
from multiprocessing import context
from pathlib import Path

import numpy as np
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMessage
from django.db.models import Avg, ExpressionWrapper, F, Sum, fields
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from excel_response.response import ExcelResponse
from PIL import Image
from requests import request
from webpush import send_user_notification

from .models import *
from .pdf_calidad import get_pdf_calidad
from .pdf_cotizacion import cotizacion_pdf
from .utils import *

BASE_DIR = settings.BASE_DIR
HEADERS = {"Content-Type": "application/json"}

FOLDER_GUIAS_MANTENIMIENTO = Path(settings.MEDIA_ROOT) / "guias_mantenimiento"
FOLDER_GUIAS_MANTENIMIENTO.mkdir(exist_ok=True, parents=True)

logger = logging.getLogger(__name__)

# Login
def staff_login(request):
    context = {}
    form = AuthenticationForm()
    context["form"] = form
    context["titulo"] = "Seguimiento en Línea"
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        # if form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]
        password_view = hashlib.sha1(bytes(password, encoding="utf-8"))
        user_in_local = authenticate(username=username, password=password)
        try:
            user_in_view = VUsuarios.objects.get(cveusuario=username, pass_field=str(password_view.hexdigest()).upper())
        except Exception:
            logger.info("USUARIO NO RECONOCIDO")
            user_in_view = False
        if user_in_view and user_in_local:
            if user_in_view.cveperfil == 1:
                group = Group.objects.get_or_create(name="administradores")[0]
                user_in_local.groups.add(group)
                login(request, user_in_local)
                return redirect("ordenes")
            elif user_in_view.cveperfil == 2:
                group = Group.objects.get_or_create(name="asesores")[0]
                user_in_local.groups.add(group)
                login(request, user_in_local)
                return redirect("ordenes")
            elif user_in_view.cveperfil == 3:
                group = Group.objects.get_or_create(name="jefe de taller")[0]
                user_in_local.groups.add(group)
                login(request, user_in_local)
                return redirect("ordenes")
            elif user_in_view.cveperfil == 5:
                group = Group.objects.get_or_create(name="administradores")[0]
                user_in_local.groups.add(group)
                login(request, user_in_local)
                return redirect("ordenes")
            elif user_in_view.cveperfil == 7:
                group = Group.objects.get_or_create(name="refacciones")[0]
                user_in_local.groups.add(group)
                login(request, user_in_local)
                return redirect("refacciones")
            elif user_in_view.cveperfil == 13:
                group = Group.objects.get_or_create(name="asesores")[0]
                user_in_local.groups.add(group)
                login(request, user_in_local)
                return redirect("ordenes")
        elif user_in_view and not user_in_local:
            logger.info("CREANDO USUARIO")
            new_local_user = User.objects.create_user(
                username=username, password=password, first_name=user_in_view.nombre
            )
            login(request, new_local_user)
            return redirect("ordenes")
        else:
            if username == "admin":
                try:
                    logger.info("CREANDO USUARIO")
                    new_local_user = User.objects.create_user(
                        username=username, password=password, first_name="Administrador", last_login=datetime.now()
                    )
                    group = Group.objects.get_or_create(name="administradores")[0]
                    new_local_user.groups.add(group)
                    login(request, new_local_user)
                except Exception:
                    logger.info("LOGIN USUARIO LOCAL")
                    login(request, user_in_local)
                return redirect("ordenes")
            logger.info("USUARIO NO RECONOCIDO")
    return render(request, "seguimientolite_mazda_col/login.html", context)


# Técnico
def tecnico(request, id_tecnico, no_orden):
    """
    Pantalla de técnico
    """
    context = {}
    if request.method == "GET":
        # Logs
        try:
            log = LogGeneral.objects.get(no_orden=no_orden)
            if not log.fin_tecnico:
                log.inicio_tecnico = datetime.now()
                log.save()
        except Exception:
            LogGeneral.objects.create(no_orden=no_orden, inicio_tecnico=datetime.now())

        # Titulo de la pagina
        context["titulo"] = "Tecnico"

        # Informacion de orden
        try:
            info = VInformacion.objects.filter(no_orden=no_orden).first()
            context["info"] = info
        except Exception as error:
            logger.error(error)

        # Evidencias
        context["filas_media"] = []
        context["filas_video"] = []
        media = Evidencias.objects.filter(no_orden=no_orden)
        for file in media:
            file_type = mimetypes.guess_type(file.evidencia)[0]
            try:
                if "video" in file_type:
                    context["filas_video"].append(file)
                else:
                    context["filas_media"].append(file)
            except Exception as error:
                logger.error(error)

        # Historial
        context["filas"] = Items.objects.filter(no_orden=no_orden).order_by("id")
        context["revisiones"] = Revisiones.objects.all()

        # Recuperacion de estado para cada item
        context["items_guardados"] = Items.objects.filter(no_orden=no_orden)
        context["lista_items_guardados"] = Items.objects.filter(no_orden=no_orden).values_list("item", flat=True)

        # Listado de items
        items_adicionales_guardados = context["items_guardados"].filter(item__familia="Otros").values_list("item")
        items_adicionales_orden = ListaItems.objects.filter(id__in=items_adicionales_guardados)

        query_lista_items_tecnico = ListaItems.objects.all()
        context["lista_items"] = query_lista_items_tecnico.exclude(familia="Otros").union(items_adicionales_orden)
        context["items_adicionales"] = ListaItems.objects.filter(familia="Otros")
        context["familias_items"] = query_lista_items_tecnico.values_list("familia", "revision").distinct()
        context["items_extra_forms"] = (
            query_lista_items_tecnico.filter(valor_x__isnull=False).values_list("descripcion", flat=True).distinct()
        )

        # Comentarios hoja multipuntos
        try:
            context["comentario_inferior_guardado"] = ActividadesTecnicoCaptura.objects.get(
                no_orden=no_orden, item="comentario_inferior"
            ).valor
        except Exception:
            pass
        try:
            context["sintoma_guardado"] = ActividadesTecnicoCaptura.objects.get(no_orden=no_orden, item="sintoma").valor
        except Exception:
            pass
        try:
            context["raiz_guardado"] = ActividadesTecnicoCaptura.objects.get(no_orden=no_orden, item="raiz").valor
        except Exception:
            pass
        try:
            context["componente_guardado"] = ActividadesTecnicoCaptura.objects.get(
                no_orden=no_orden, item="componente"
            ).valor
        except Exception:
            pass

        # Crear o actalizar la informacion de la orden
        crear_actualizar_info(no_orden)

    if request.method == "POST":
        r = request.POST

        # Obtención de la informacion
        try:
            info = Informacion.objects.get(no_orden=no_orden)
        except Exception:
            pass

        notif = r.get("notif", None)

        # ACTUALIZAR ESTADO
        if r.get("update", None):
            try:
                update = Items.objects.get(no_orden=no_orden, item=r["item"])
                update.estado = str(r["estado"]).strip()
                update.fecha_hora_actualizacion = datetime.now()
                update.cambiado = True
                update.save()
                return HttpResponse(status=200)
            except Exception:
                pass

        # REMOVER REGISTRO
        if r.get("remove", None):
            try:
                Items.objects.get(no_orden=no_orden, item=r["item"]).delete()
                return HttpResponse(status=200)
            except Exception as error:
                logger.error(error)

        # GUARDAR INSPECCION
        if r.get("inspeccion", None):
            # ITEMS
            logger.info("GUARDADO DE ITEM")
            item = ListaItems.objects.get(id=r["id_item"])
            item_defaults = {
                "estado": str(r["estado"]).strip(),
                "comentarios": str(r["comentario"]).strip(),
                "valor": str(r.get("valor")),
                "tecnico": id_tecnico,
                "bateria_estado": r.get("bateria_estado"),
                "bateria_nivel": r.get("bateria_nivel"),
            }
            item_tecnico, created = Items.objects.update_or_create(no_orden=no_orden, item=item, defaults=item_defaults)

            # EVIDENCIAS
            if r.get("evidencias[]", False):
                logger.info("SE ENCUENTRAN EVIDENCIAS")
                logger.info(r["evidencias[]"])
                for filename in r.getlist("evidencias[]"):
                    logger.info(filename)
                    try:
                        Evidencias.objects.create(
                            no_orden=no_orden,
                            item=item_tecnico,
                            evidencia=filename,
                        )
                        logger.info("EVIDENCIA GUARDADA")
                    except Exception as error:
                        logger.error(error)
            if r.get("fp_id[]", False):
                logger.info("CODIGOS DE FILEPOND")
                save_filepond(r.getlist("fp_id[]"))

            # LOG
            log = LogGeneral.objects.get(no_orden=no_orden)
            if not log.fin_tecnico:
                log.fin_tecnico = datetime.now()
                log.save()

            # NOTIFICATIONS
            if notif:
                lista_correos = [
                    "eliu.gutierrez@capitalnetwork.com.mx",
                    "eglenelid.gamaliel@gmail.com",
                ]
                push_groups(no_orden, ["repuestos"])
                mail_groups(no_orden, ["repuestos"], lista_correos)

        # GUARDAR COMENTARIOS DE DIAGNOSTICO
        if r.get("observaciones", None):
            try:
                update = ActividadesTecnicoCaptura.objects.get(no_orden=no_orden, item="comentario_inferior")
                update.valor = r["comentario_inferior"]
                update.save()
            except Exception:
                ActividadesTecnicoCaptura.objects.create(
                    no_orden=no_orden,
                    item="comentario_inferior",
                    valor=r["comentario_inferior"],
                )

        # Guardar items adicionales nuevos
        if r.get("items_adicionales_nuevos"):
            logger.info("Items adicionales nuevos")
            nuevos_items_adicionales = json.loads(r["items"])

            for item in nuevos_items_adicionales:
                # Se crea nuevo registro en la tabla de lista items
                revision = Revisiones.objects.get(id=item["revision_id"])
                nuevo_item, creado = ListaItems.objects.get_or_create(
                    descripcion=item["nombre"], familia="Otros", revision=revision
                )
                if creado:
                    logger.info("Item creado en lista items")
                else:
                    logger.info("Item ya existe en lista items")

                # Se crea nuevo registro en la tabla de items tecnico
                item_tecnico_defaults = {
                    "estado": item["estado"],
                    "comentarios": item["comentarios"],
                    "tecnico": id_tecnico,
                }
                nuevo_item_tecnico, creado = Items.objects.update_or_create(
                    no_orden=no_orden, item=nuevo_item, defaults=item_tecnico_defaults
                )
                if creado:
                    logger.info("Item creado en actividades tecnico")
                else:
                    logger.info("Item ya existe en actividades tecnico")

                # Evidencias
                if item.get("evidencias"):
                    logger.info("Se encuentran evidencias")
                    for filename in item["evidencias"]:
                        try:
                            Evidencias.objects.create(
                                no_orden=no_orden,
                                item=nuevo_item_tecnico,
                                evidencia=filename,
                            )
                            logger.info("Evidencia guardada")
                        except Exception as error:
                            logger.error(error)
                if item.get("fp_id"):
                    save_filepond(item["fp_id"])

        # GUARDADO DE FIRMA
        if r.get("firma"):
            sign = r["firma"]
            data = sign[22:].encode()
            with open(os.path.join(BASE_DIR, "media", "tmp.png"), "wb") as fh:
                fh.write(base64.decodebytes(data))

            threshold = 100
            dist = 5
            img_buffer = Image.open(os.path.join(BASE_DIR, "media", "tmp.png")).convert("RGBA")
            arr = np.array(np.asarray(img_buffer))
            r, g, b, a = np.rollaxis(arr, axis=-1)
            mask = (
                (r > threshold)
                & (g > threshold)
                & (b > threshold)
                & (np.abs(r - g) < dist)
                & (np.abs(r - b) < dist)
                & (np.abs(g - b) < dist)
            )
            arr[mask, 3] = 0
            img_buffer = Image.fromarray(arr, mode="RGBA")
            img_buffer.save(os.path.join(settings.MEDIA_ROOT, f"{no_orden}_firma_tecnico.png"))
            os.remove(os.path.join(BASE_DIR, "media", "tmp.png"))

            try:
                f = ActividadesAsesorFirmas.objects.get(no_orden=no_orden)
                f.firma = f"{no_orden}_firma_tecnico.png"
                f.tipo = "tecnico"
                f.save()
            except Exception:
                ActividadesAsesorFirmas.objects.create(
                    no_orden=no_orden, firma=f"{no_orden}_firma_tecnico.png", tipo="tecnico"
                )

        return HttpResponse(status=200)
    return render(request, "seguimientolite_mazda_col/tecnico.html", context)


# Listado de refacciones
def refacciones(request):
    context = {}

    context["filas"] = []
    context["titulo"] = "Repuestos"

    # Verificación de login
    grupos = request.user.groups.values_list("name", flat=True)
    if not request.user.is_authenticated or "cliente" in grupos:
        return redirect("staff_login")
    notificaciones_push(request, context)

    query_refacciones = VOperacionesRefacciones.objects.order_by("-fecha_ingreso")

    # Creación de tabla
    no_ordenes = query_refacciones.values_list("no_orden", flat=True).distinct()

    # Queries generales
    query_tecnico = Items.objects.filter(no_orden__in=no_ordenes)
    query_ref = Refacciones.objects.filter(no_orden__in=no_ordenes)

    for no_orden in no_ordenes:
        try:
            info = query_refacciones.filter(no_orden=no_orden).first()
            try:
                modificacion = query_ref.filter(no_orden=no_orden).order_by("-fecha_hora_fin").first().fecha_hora_fin
            except Exception:
                modificacion = ""
            inmediatos = query_tecnico.filter(no_orden=no_orden, estado="Inmediato").count()
            recomendados = query_tecnico.filter(no_orden=no_orden, estado="Recomendado").count()

            context["filas"].append(
                {
                    "no_orden": no_orden,
                    "vin": info.vin,
                    "placas": info.placas,
                    "vehiculo": info.vehiculo,
                    "asesor": info.asesor,
                    "tecnico": info.tecnico,
                    "fecha_ingreso": info.fecha_ingreso,
                    "fin_tecnico": info.fin_tecnico,
                    "modificacion": modificacion,
                    "inmediatos": inmediatos,
                    "recomendados": recomendados,
                }
            )
        except Exception as error:
            logger.error(error)
    return render(request, "seguimientolite_mazda_col/refacciones.html", context)


# Detalle de refacciones
def refacciones_detalle(request, no_orden):

    if request.method == "GET":
        context = {}
        context["titulo"] = "Repuestos"

        grupos = request.user.groups.values_list("name", flat=True)
        if not request.user.is_authenticated or "cliente" in grupos:
            return redirect("staff_login")
        notificaciones_push(request, context)
        crear_actualizar_info(no_orden)
        get_evidencias(context, no_orden)

        # Log
        try:
            log = LogGeneral.objects.get(no_orden=no_orden)
            if not log.inicio_refacciones and not log.fin_refacciones:
                log.inicio_refacciones = datetime.now()
                log.save()
        except Exception:
            pass

        # Informacion de orden
        try:
            context["orden"] = Informacion.objects.get(no_orden=no_orden)
            context["tecnicos"] = VTecnicos.objects.all()
        except Exception as error:
            logger.error(error)

        queryset_tecnico = Items.objects.filter(no_orden=no_orden)
        queryset_refacciones = Refacciones.objects.filter(no_orden=no_orden)

        context["items_tecnico"] = queryset_tecnico.exclude(estado="Buen Estado").exclude(estado="Corregido")
        context["fin_tecnico"] = queryset_tecnico.first().fecha_hora_fin
        context["refacciones"] = queryset_refacciones
        context["iva"] = settings.SEGUIMIENTOLITE_IVA

        return render(request, "seguimientolite_mazda_col/refacciones_detalle.html", context)

    if request.method == "POST":
        r = request.POST
        logger.info(r)

        # Guardado de inspección
        if r.get("guardar_inspeccion"):
            refacciones = json.loads(r["refacciones"])
            logger.info("Guardado de inspeccion de refacciones")
            for refaccion in refacciones:
                # Log
                try:
                    log = LogGeneral.objects.get(no_orden=no_orden)
                    if not log.fin_refacciones:
                        log.fin_refacciones = datetime.now()
                        log.save()
                except Exception:
                    pass

                item = Items.objects.get(no_orden=no_orden, id=refaccion["item_id"])

                subtotal_no_descuento_iva = Decimal(refaccion["cantidad"]) * Decimal(refaccion["precio_unitario"])
                porcentaje_descuento = Decimal(refaccion["porcentaje_descuento"])

                defaults_refacciones = {
                    "nombre": refaccion["nombre"],
                    "cantidad": refaccion["cantidad"],
                    "precio_unitario": refaccion["precio_unitario"],
                    "porcentaje_descuento": porcentaje_descuento,
                    "subtotal": round(
                        subtotal_no_descuento_iva - ((subtotal_no_descuento_iva / 100) * porcentaje_descuento), 2
                    ),
                    "porcentaje_iva": settings.SEGUIMIENTOLITE_IVA,
                    "subtotal_iva": Decimal(refaccion["subtotal"]),
                    "existencia": refaccion["existencia"],
                    "localizacion": refaccion["localizacion"],
                }

                Refacciones.objects.update_or_create(
                    no_orden=no_orden, item=item, no_parte=refaccion["no_parte"], defaults=defaults_refacciones
                )
            lista_correos = [
                "eliu.gutierrez@capitalnetwork.com.mx",
            ]
            push_groups(no_orden, ["repuestos"])
            logger.info("NOTIFICACION PUSH ENVIADA")
            mail_groups(no_orden, ["repuestos"], lista_correos)
            logger.info("NOTIFICACION POR CORREO ENVIADA")

        # Borrado individual de refacciones
        if r.get("borrado_refaccion"):
            Refacciones.objects.get(no_orden=no_orden, id=r["refaccion_id"]).delete()

        return HttpResponse(status=200)


# Listado de cotización
def cotizaciones(request):
    context = {}

    context["filas"] = []
    context["titulo"] = "Cotización"

    # Verificación de login
    grupos = request.user.groups.values_list("name", flat=True)
    if not request.user.is_authenticated or "cliente" in grupos:
        return redirect("staff_login")
    notificaciones_push(request, context)

    query_refacciones = VOperacionesRefacciones.objects.order_by("-fecha_ingreso")

    # Creación de tabla
    no_ordenes = query_refacciones.values_list("no_orden", flat=True).distinct()

    # Queries generales
    query_tecnico = Items.objects.filter(no_orden__in=no_ordenes)
    query_ref = Refacciones.objects.filter(no_orden__in=no_ordenes)

    for no_orden in no_ordenes:
        try:
            info = query_refacciones.filter(no_orden=no_orden).first()
            try:
                modificacion = query_ref.filter(no_orden=no_orden).order_by("-fecha_hora_fin").first().fecha_hora_fin
            except Exception:
                modificacion = ""
            inmediatos = query_tecnico.filter(no_orden=no_orden, estado="Inmediato").count()
            recomendados = query_tecnico.filter(no_orden=no_orden, estado="Recomendado").count()

            context["filas"].append(
                {
                    "no_orden": no_orden,
                    "vin": info.vin,
                    "placas": info.placas,
                    "vehiculo": info.vehiculo,
                    "asesor": info.asesor,
                    "tecnico": info.tecnico,
                    "fecha_ingreso": info.fecha_ingreso,
                    "fin_tecnico": info.fin_tecnico,
                    "modificacion": modificacion,
                    "inmediatos": inmediatos,
                    "recomendados": recomendados,
                }
            )
        except Exception as error:
            logger.error(error)
    return render(request, "seguimientolite_mazda_col/cotizacion.html", context)


# Detalle de cotizaciones -- Nueva pantalla para rediseño
def cotizaciones_detalle(request, no_orden):

    if request.method == "GET":
        context = {}
        context["titulo"] = "Cotizaciones"

        grupos = request.user.groups.values_list("name", flat=True)
        if not request.user.is_authenticated or "cliente" in grupos:
            return redirect("staff_login")
        notificaciones_push(request, context)
        crear_actualizar_info(no_orden)
        get_evidencias(context, no_orden)

        # Log
        try:
            log = LogGeneral.objects.get(no_orden=no_orden)
            if not log.inicio_refacciones and not log.fin_refacciones:
                log.inicio_refacciones = datetime.now()
                log.save()
        except Exception:
            pass

        # Informacion de orden
        try:
            context["orden"] = Informacion.objects.get(no_orden=no_orden)
            context["tecnicos"] = VTecnicos.objects.all()
        except Exception as error:
            logger.error(error)

        queryset_tecnico = Items.objects.filter(no_orden=no_orden)
        queryset_refacciones = Refacciones.objects.filter(no_orden=no_orden)

        context["items_tecnico"] = queryset_tecnico.exclude(estado="Buen Estado").exclude(estado="Corregido")
        context["fin_tecnico"] = queryset_tecnico.first().fecha_hora_fin
        context["refacciones"] = Cotizaciones.objects.filter(no_orden=no_orden)
        context["iva"] = settings.SEGUIMIENTOLITE_IVA

        return render(request, "seguimientolite_mazda_col/cotizacion_detalle.html", context)

    if request.method == "POST":
        r = request.POST
        logger.info(r)

        # Guardado de inspección
        if r.get("guardar_inspeccion"):
            refacciones = json.loads(r["refacciones"])
            logger.info("Guardado de inspeccion de refacciones")
            for refaccion in refacciones:
                if refaccion.get("id"):
                    id_refaccion = refaccion["id"]
                    del refaccion["id"]
                    Cotizaciones.objects.filter(id=id_refaccion).update(**refaccion, fuente="PLATFORM")
                else:
                    Cotizaciones.objects.create(no_orden=no_orden, **refaccion, fuente="PLATFORM")
            lista_correos = [
                "eliu.gutierrez@capitalnetwork.com.mx",
            ]

            try:
                log = LogGeneral.objects.filter(no_orden=no_orden).first()
                if not log.fin_cotizacion:
                    log.fin_cotizacion = datetime.now()
                    log.save()
            except Exception as error:
                logger.error(error)

            push_groups(no_orden, ["repuestos"])
            logger.info("NOTIFICACION PUSH ENVIADA")
            mail_groups(no_orden, ["repuestos"], lista_correos)
            logger.info("NOTIFICACION POR CORREO ENVIADA")

        # Borrado individual de refacciones
        if r.get("borrado_refaccion"):
            Refacciones.objects.get(no_orden=no_orden, id=r["refaccion_id"]).delete()

        return HttpResponse(status=200)


# Listado mano de obra
def mano_de_obra(request):
    context = {}

    context["filas"] = []
    context["titulo"] = "Mano de obra"

    # Verificación de login
    grupos = request.user.groups.values_list("name", flat=True)
    if not request.user.is_authenticated or "cliente" in grupos:
        return redirect("staff_login")
    notificaciones_push(request, context)

    query_refacciones = VOperacionesRefacciones.objects.all().order_by("-fecha_ingreso")

    # Creación de tabla
    no_ordenes = query_refacciones.values_list("no_orden", flat=True).distinct()

    # Queries generales
    query_tecnico = Items.objects.filter(no_orden__in=no_ordenes)
    query_mo = ManoDeObra.objects.filter(no_orden__in=no_ordenes)

    for no_orden in no_ordenes:
        try:
            info = query_refacciones.filter(no_orden=no_orden).first()
            try:
                modificacion = query_mo.filter(no_orden=no_orden).order_by("-fecha_hora_fin").first().fecha_hora_fin
            except Exception:
                modificacion = ""
            inmediatos = query_tecnico.filter(no_orden=no_orden, estado="Inmediato").count()
            recomendados = query_tecnico.filter(no_orden=no_orden, estado="Recomendado").count()

            context["filas"].append(
                {
                    "no_orden": no_orden,
                    "vin": info.vin,
                    "placas": info.placas,
                    "vehiculo": info.vehiculo,
                    "asesor": info.asesor,
                    "tecnico": info.tecnico,
                    "fecha_ingreso": info.fecha_ingreso,
                    "fin_tecnico": info.fin_tecnico,
                    "modificacion": modificacion,
                    "inmediatos": inmediatos,
                    "recomendados": recomendados,
                }
            )
        except Exception as error:
            logger.error(error)
    return render(request, "seguimientolite_mazda_col/refacciones.html", context)


# Detalle de mano de obra
def mano_de_obra_detalle(request, no_orden):

    if request.method == "GET":
        context = {}
        context["titulo"] = "Mano de obra"

        grupos = request.user.groups.values_list("name", flat=True)
        if not request.user.is_authenticated or "cliente" in grupos:
            return redirect("staff_login")
        notificaciones_push(request, context)
        crear_actualizar_info(no_orden)
        get_evidencias(context, no_orden)

        # Log
        try:
            log = LogGeneral.objects.get(no_orden=no_orden)
            if not log.inicio_mano_de_obra and not log.fin_mano_de_obra:
                log.inicio_mano_de_obra = datetime.now()
                log.save()
        except Exception:
            pass

        # Informacion de la orden
        try:
            context["orden"] = Informacion.objects.get(no_orden=no_orden)
            context["tecnicos"] = VTecnicos.objects.all()
        except Exception:
            pass

        queryset_tecnico = Items.objects.filter(no_orden=no_orden)
        queryset_refacciones = Refacciones.objects.filter(no_orden=no_orden)
        queryset_mano_de_obra = ManoDeObra.objects.filter(no_orden=no_orden)

        context["items_tecnico"] = queryset_tecnico.exclude(estado="Buen Estado").exclude(estado="Corregido")
        context["fin_tecnico"] = queryset_tecnico.first().fecha_hora_fin
        context["refacciones"] = queryset_refacciones
        context["mano_de_obra"] = queryset_mano_de_obra
        context["iva"] = settings.SEGUIMIENTOLITE_IVA
        context["precio_ut"] = settings.SEGUIMIENTOLITE_PRECIO_UT
        context["cargos"] = TiposCargos.objects.all()

        return render(request, "seguimientolite_mazda_col/mano_de_obra_detalle.html", context)

    if request.method == "POST":
        r = request.POST
        logger.info(r)

        # Guardado de inspección
        if r.get("guardar_inspeccion"):
            mano_de_obra = json.loads(r["mano_de_obra"])
            logger.info("Guardado de inspeccion de mano de obra")
            for m_obra in mano_de_obra:

                # Log
                try:
                    log = LogGeneral.objects.get(no_orden=no_orden)
                    if not log.fin_mano_de_obra:
                        log.fin_mano_de_obra = datetime.now()
                        log.save()
                except Exception:
                    pass

                item = Items.objects.get(no_orden=no_orden, id=m_obra["item_id"])
                cargo = TiposCargos.objects.get(id=m_obra["cargo"])
                subtotal_no_descuento_iva = Decimal(m_obra["uts"]) * Decimal(m_obra["precio_ut"])
                porcentaje_descuento = Decimal(m_obra["porcentaje_descuento"])

                defaults_mo = {
                    "nombre": m_obra["nombre"],
                    "cantidad_uts": m_obra["uts"],
                    "precio_ut": m_obra["precio_ut"],
                    "porcentaje_descuento": porcentaje_descuento,
                    "subtotal": round(
                        subtotal_no_descuento_iva - ((subtotal_no_descuento_iva / 100) * porcentaje_descuento), 2
                    ),
                    "porcentaje_iva": settings.SEGUIMIENTOLITE_IVA,
                    "subtotal_iva": Decimal(m_obra["subtotal"]),
                    "cargo": cargo,
                }

                ManoDeObra.objects.update_or_create(
                    no_orden=no_orden, item=item, codigo=m_obra["codigo"], defaults=defaults_mo
                )
            lista_correos = [
                "eliu.gutierrez@capitalnetwork.com.mx",
            ]
            push_groups(no_orden, ["repuestos"])
            logger.info("NOTIFICACION PUSH ENVIADA")
            mail_groups(no_orden, ["repuestos"], lista_correos)
            logger.info("NOTIFICACION POR CORREO ENVIADA")

        # Borrado individual de refacciones
        if r.get("borrado_mano_de_obra"):
            ManoDeObra.objects.get(no_orden=no_orden, id=r["mano_de_obra_id"]).delete()

        return HttpResponse(status=200)


# Listado de asesor
def asesor(request):
    context = {}
    context["titulo"] = "Asesor"
    context["settings"] = settings

    grupos = request.user.groups.values_list("name", flat=True)
    if not request.user.is_authenticated or "cliente" in grupos:
        return redirect("staff_login")
    notificaciones_push(request, context)

    # Construcción de la tabla
    if str(request.user.groups.first()) == "administradores":
        filas_ordenes = VOperacionesAsesorAlt.objects.order_by("-no_orden").all()
        ordenes = filas_ordenes.values_list("no_orden", flat=True).distinct()
    else:
        asesor_name = VUsuarios.objects.get(cveusuario=request.user.username)
        filas_ordenes = VOperacionesAsesorAlt.objects.order_by("no_orden").filter(asesor=asesor_name.nombre).distinct()
        ordenes = filas_ordenes.values_list("no_orden", flat=True).distinct()

    context["filas"] = []

    query_tecnico = Items.objects.filter(no_orden__in=ordenes)
    for orden in ordenes:
        log = LogGeneral.objects.get(no_orden=orden)

        try:
            order_info = filas_ordenes.filter(no_orden=orden)[0]
            visits = LogCliente.objects.filter(no_orden=orden).count()
            if visits > 0:
                state = "Visto por el Cliente"

            autorizaciones = Autorizaciones.objects.filter(no_orden=orden)

            tecnico = VOperacionesRefacciones.objects.filter(no_orden=orden).first().tecnico

            informacion = Informacion.objects.filter(no_orden=orden).first()

            try:
                revision_limpia = VRevisionesLimpias.objects.get(no_orden=orden)
            except Exception:
                revision_limpia = None

            context["filas"].append(
                {
                    "no_orden": order_info.no_orden,
                    "no_placas": informacion.placas,
                    "cliente": informacion.cliente,
                    "telefono": informacion.telefono,
                    "vehiculo": informacion.vehiculo,
                    "asesor": order_info.asesor,
                    "tecnico": tecnico,
                    "fecha_hora_cotizacion": log.fin_cotizacion,
                    "revision_limpia": revision_limpia,
                    "estado": {
                        "log": log,
                        "items": query_tecnico.filter(no_orden=orden, estado__in=["Inmediato", "Recomendado"]),
                        "aceptados": autorizaciones.filter(autorizacion=True).count(),
                    },
                    "email": informacion.email,
                    "telefono": informacion.telefono,
                }
            )
        except Exception as error:
            logger.error(error)

    if request.method == "POST":
        data = request.POST

        # Envio de correo
        if data.get("email"):
            no_orden = data["no_orden"]
            logger.info("ENVIANDO CORREO")
            # LOG
            template_context = {}
            template_context["cotizacion"] = True
            template_context["asunto"] = "Cotizacion"
            template_context["preview"] = settings.AGENCIA + " | Su vehículo ha sido revisado"
            template_context["nombre_agencia"] = settings.AGENCIA
            template_context[
                "cotizacion_url"
            ] = f"http://{settings.DOMINIO}:{settings.PUERTO}/seguimiento/cliente/{no_orden}"
            template_context["telefono_agencia"] = settings.TELEFONO
            template_context["privacy_url"] = settings.AVISO_PRIVACIDAD

            template_context["logo"] = "https://logodownload.org/wp-content/uploads/2019/11/mazda-logo-0.png"
            html_content = render_to_string("seguimientolite_mazda_col/mail-template.html", template_context)

            client_mail = data["email_cliente"]

            email = EmailMessage(
                settings.AGENCIA,
                html_content,
                settings.EMAIL_HOST_USER,
                [client_mail],
            )

            email.content_subtype = "html"
            email.send()
            logger.info("CORREO ENVIADO")

            # LOG
            LogEnvios.objects.create(
                no_orden=no_orden,
                medio="E-Mail",
                fecha_hora_envio=datetime.now(),
                correo=data["email_cliente"],
            )
            try:
                log = LogGeneral.objects.get(no_orden=no_orden)
                if not log.fin_asesor:
                    log.fin_asesor = datetime.now()
                    log.save()
            except Exception:
                pass
            return HttpResponse(status=200)

        # Envio de WhatsApp
        if data.get("whatsapp"):
            # LOG
            try:
                no_orden = data["no_orden"]
                enviar_whatsapp(data["prefijo"], data["telefono"], data["mensaje"])

                log = LogGeneral.objects.get(no_orden=no_orden)
                if not log.fin_asesor:
                    log.fin_asesor = datetime.now()
                    log.save()

                LogEnvios.objects.create(
                    no_orden=no_orden,
                    medio="WhatsApp",
                    fecha_hora_envio=datetime.now(),
                    telefono=data["telefono"],
                )
                return HttpResponse(status=200)
            except Exception:
                return HttpResponse(status=500)

        if data.get("whatsapp_manual"):
            log = LogGeneral.objects.get(no_orden=data["no_orden"])
            if not log.fin_asesor:
                log.fin_asesor = datetime.now()
                log.save()
            LogEnvios.objects.create(
                no_orden=data["no_orden"],
                medio="WhatsApp",
                fecha_hora_envio=datetime.now(),
                telefono=data["telefono"],
            )
            return HttpResponse(status=200)
    return render(request, "seguimientolite_mazda_col/asesor.html", context)


# Detalle de asesor
def asesor_detalle(request, no_orden):

    if request.method == "GET":
        context = {}
        context["titulo"] = "Asesor"
        context["no_orden"] = no_orden
        context["settings"] = settings

        grupos = request.user.groups.values_list("name", flat=True)
        if not request.user.is_authenticated or "cliente" in grupos:
            return redirect("staff_login")
        notificaciones_push(request, context)
        get_evidencias(context, no_orden)

        # Log
        try:
            log = LogGeneral.objects.get(no_orden=no_orden)
            if not log.inicio_asesor and not log.fin_asesor:
                log.inicio_asesor = datetime.now()
                log.save()
        except Exception as error:
            logger.error(error)

        # Informacion de refacciones y mano de obra
        query_tecnico = Items.objects.filter(no_orden=no_orden).exclude(estado__in=("Buen Estado", "Corregido"))
        query_autorizaciones = Autorizaciones.objects.filter(no_orden=no_orden)
        query_cotizaciones = Cotizaciones.objects.filter(no_orden=no_orden)

        context["orden"] = Informacion.objects.get(no_orden=no_orden)
        context["tecnicos"] = VTecnicos.objects.all()

        try:
            context["revision_limpia"] = VRevisionesLimpias.objects.get(no_orden=no_orden)
        except Exception:
            context["revision_limpia"] = None

        try:
            context["fin_tecnico"] = query_tecnico.first().fecha_hora_fin
        except Exception:
            context["fin_tecnico"] = Items.objects.filter(no_orden=no_orden).first().fecha_hora_fin

        context["guias_mantenimiento"] = query_tecnico.values("item__revision__id", "item__revision__nombre").distinct()
        context["autorizaciones"] = query_autorizaciones

        # Inspeccion de cotizaciones
        context["items_tecnico"] = []
        for item in query_tecnico:
            refacciones = Cotizaciones.objects.filter(no_orden=no_orden, item=item)

            total_ref = refacciones.aggregate(Sum("costo_repuesto"))["costo_repuesto__sum"]
            if not total_ref:
                total_ref = 0

            total_mo = refacciones.aggregate(Sum("costo_mano_obra"))["costo_mano_obra__sum"]
            if not total_mo:
                total_mo = 0

            total_subtotal = refacciones.aggregate(Sum("subtotal"))["subtotal__sum"]
            if not total_subtotal:
                total_subtotal = 0

            total_iva = refacciones.aggregate(Sum("monto_iva"))["monto_iva__sum"]
            if not total_iva:
                total_iva = 0

            total = refacciones.aggregate(Sum("total"))["total__sum"]
            if not total:
                total = 0

            context["items_tecnico"].append(
                {
                    "item": item,
                    "refacciones": refacciones,
                    "total_ref": total_ref,
                    "total_mo": total_mo,
                    "total_iva": total_iva,
                    "total_subtotal": total_subtotal,
                    "total": total,
                }
            )

        # Totales
        context["total_refacciones"] = query_cotizaciones.aggregate(Sum("costo_repuesto"))["costo_repuesto__sum"]
        if not context["total_refacciones"]:
            context["total_refacciones"] = 0

        context["total_mano_de_obra"] = query_cotizaciones.aggregate(Sum("costo_mano_obra"))["costo_mano_obra__sum"]
        if not context["total_mano_de_obra"]:
            context["total_mano_de_obra"] = 0

        context["total_iva"] = query_cotizaciones.aggregate(Sum("monto_iva"))["monto_iva__sum"]
        if not context["total_iva"]:
            context["total_iva"] = 0

        context["total_cotizado"] = context["total_refacciones"] + context["total_mano_de_obra"] + context["total_iva"]

        items_autorizados = query_autorizaciones.filter(autorizacion=True).values_list("item", flat=True)
        cotizaciones_autorizadas = query_cotizaciones.filter(item_id__in=items_autorizados)

        context["total_refacciones_autorizadas"] = cotizaciones_autorizadas.aggregate(Sum("costo_repuesto"))[
            "costo_repuesto__sum"
        ]
        if not context["total_refacciones_autorizadas"]:
            context["total_refacciones_autorizadas"] = 0

        context["total_mano_de_obra_autorizada"] = cotizaciones_autorizadas.aggregate(Sum("costo_mano_obra"))[
            "costo_mano_obra__sum"
        ]
        if not context["total_mano_de_obra_autorizada"]:
            context["total_mano_de_obra_autorizada"] = 0

        context["total_iva_autorizado"] = cotizaciones_autorizadas.aggregate(Sum("monto_iva"))["monto_iva__sum"]
        if not context["total_iva_autorizado"]:
            context["total_iva_autorizado"] = 0

        context["total_autorizado"] = (
            context["total_refacciones_autorizadas"]
            + context["total_mano_de_obra_autorizada"]
            + context["total_iva_autorizado"]
        )

        context["total_refacciones_no_autorizadas"] = (
            context["total_refacciones"] - context["total_refacciones_autorizadas"]
        )
        context["total_mano_de_obra_no_autorizada"] = (
            context["total_mano_de_obra"] - context["total_mano_de_obra_autorizada"]
        )
        context["total_no_autorizado"] = context["total_cotizado"] - context["total_autorizado"]

        context["items_autorizados"] = query_autorizaciones.filter(autorizacion=True)
        context["items_no_autorizados"] = query_tecnico.exclude(
            id__in=context["items_autorizados"].values_list("item_id")
        )

        context["nombre_agencia"] = settings.AGENCIA
        context["prefijo"] = settings.TELEFONO
        context["precio_ut"] = settings.SEGUIMIENTOLITE_PRECIO_UT
        context["iva"] = settings.SEGUIMIENTOLITE_IVA
        context["link"] = f"http://{settings.DOMINIO}:{settings.PUERTO}/seguimiento/cliente/{no_orden}"

        return render(request, "seguimientolite_mazda_col/asesor_detalle.html", context)

    if request.method == "POST":
        context = {}
        context["no_orden"] = no_orden
        r = request.POST
        metodo = r.get("metodo", None)

        # ENVIO DE WHATSAPP
        if metodo == "WhatsApp":
            # LOG
            try:
                enviar_whatsapp(r["prefijo"], r["telefono"], r["mensaje"])

                log = LogGeneral.objects.get(no_orden=no_orden)
                if not log.fin_asesor:
                    log.fin_asesor = datetime.now()
                    log.save()

                LogEnvios.objects.create(
                    no_orden=no_orden,
                    medio=request.POST["metodo"],
                    fecha_hora_envio=datetime.now(),
                    telefono=request.POST["telefono"],
                )
                return HttpResponse(status=200)
            except Exception:
                return HttpResponse(status=500)

        # ENVIO DE CORREO
        if metodo == "E-Mail":
            logger.info("ENVIANDO CORREO")
            # LOG
            template_context = {}
            template_context["cotizacion"] = True
            template_context["asunto"] = "Cotizacion"
            template_context["preview"] = settings.AGENCIA + " | Su vehículo ha sido revisado"
            template_context["nombre_agencia"] = settings.AGENCIA
            template_context[
                "cotizacion_url"
            ] = f"http://{settings.DOMINIO}:{settings.PUERTO}/seguimiento/cliente/{no_orden}"
            template_context["telefono_agencia"] = settings.TELEFONO
            template_context["privacy_url"] = settings.AVISO_PRIVACIDAD

            template_context["logo"] = "https://logodownload.org/wp-content/uploads/2019/11/mazda-logo-0.png"
            html_content = render_to_string("seguimientolite_mazda_col/mail-template.html", template_context)

            client_mail = request.POST.get("mail", None)

            email = EmailMessage(
                settings.AGENCIA,
                html_content,
                settings.EMAIL_HOST_USER,
                [client_mail],
            )

            email.content_subtype = "html"
            email.send()
            logger.info("CORREO ENVIADO")

            # LOG
            LogEnvios.objects.create(
                no_orden=no_orden,
                medio=request.POST["metodo"],
                fecha_hora_envio=datetime.now(),
                correo=request.POST["mail"],
            )
            try:
                log = LogGeneral.objects.get(no_orden=no_orden)
                if not log.fin_asesor:
                    log.fin_asesor = datetime.now()
                    log.save()
            except Exception:
                pass

        # GUARDADO DE FIRMA
        if r.get("firma"):
            sign = r.get("firma", None)
            data = sign[22:].encode()
            with open(os.path.join(BASE_DIR, "media", "tmp.png"), "wb") as fh:
                fh.write(base64.decodebytes(data))

            threshold = 100
            dist = 5
            img_buffer = Image.open(os.path.join(BASE_DIR, "media", "tmp.png")).convert("RGBA")
            arr = np.array(np.asarray(img_buffer))
            r, g, b, a = np.rollaxis(arr, axis=-1)
            mask = (
                (r > threshold)
                & (g > threshold)
                & (b > threshold)
                & (np.abs(r - g) < dist)
                & (np.abs(r - b) < dist)
                & (np.abs(g - b) < dist)
            )
            arr[mask, 3] = 0
            name = f"{datetime.now()}.png"
            img_buffer = Image.fromarray(arr, mode="RGBA")
            img_buffer.save(os.path.join(settings.MEDIA_ROOT, f"{no_orden}.png"))
            os.remove(os.path.join(BASE_DIR, "media", "tmp.png"))

            try:
                f = ActividadesAsesorFirmas.objects.get(no_orden=no_orden)
                f.firma = f"{no_orden}.png"
                f.save()
            except Exception:
                ActividadesAsesorFirmas.objects.create(no_orden=no_orden, firma=f"{no_orden}.png")

        r = request.POST
        if r.get("cotizacion_pdf"):
            refacciones_ids = json.loads(r["ids_ref"])
            mano_de_obra_ids = json.loads(r["ids_mo"])
            pdf = cotizacion_pdf(no_orden, refacciones_ids, mano_de_obra_ids)
            response = HttpResponse(pdf)
            response["Content-Disposition"] = 'attachment; filename="cotizacion.pdf"'
            response["Content-Type"] = "application/octet-stream"
            return response

        return HttpResponse(status=200)


class HistorialCotizaciones(TemplateView):
    template_name = "seguimientolite_mazda_col/historial_cotizaciones.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["titulo"] = "Historial de Autorizaciones"

        request = self.request

        inicio = datetime(2022, 8, 15)

        # Construcción de la tabla
        ordenes = Items.objects.filter(fecha_hora_fin__gte=inicio).values_list("no_orden", flat=True).distinct()

        context["filas"] = []

        for orden in ordenes:
            log = LogGeneral.objects.get(no_orden=orden)

            informacion = Informacion.objects.filter(no_orden=orden).first()
            if informacion:
                query_autorizaciones = Autorizaciones.objects.filter(no_orden=orden)
                query_cotizaciones = Cotizaciones.objects.filter(no_orden=orden)

                items_autorizados = query_autorizaciones.filter(autorizacion=True).values_list("item", flat=True)
                cotizaciones_autorizadas = query_cotizaciones.filter(item_id__in=items_autorizados)

                monto_cotizado = query_cotizaciones.aggregate(Sum("total"))["total__sum"]
                if not monto_cotizado:
                    monto_cotizado = 0

                monto_autorizado = cotizaciones_autorizadas.aggregate(Sum("total"))["total__sum"]
                if not monto_autorizado:
                    monto_autorizado = 0

                monto_no_autorizado = monto_cotizado - monto_autorizado

                revision_limpia = VRevisionesLimpias.objects.filter(no_orden=orden).first()

                tecnico_query = VTecnicos.objects.filter(id_empleado=informacion.tecnico).first()
                if tecnico_query:
                    tecnico = tecnico_query.nombre_empleado
                else:
                    tecnico = ""

                context["filas"].append(
                    {
                        "no_orden": orden,
                        "no_placas": informacion.placas,
                        "cliente": informacion.cliente,
                        "telefono": informacion.telefono,
                        "vehiculo": informacion.vehiculo,
                        "asesor": informacion.asesor,
                        "tecnico": tecnico,
                        "fecha_hora_cotizacion": log.fin_cotizacion,
                        "revision_limpia": revision_limpia,
                        "monto_cotizado": monto_cotizado,
                        "monto_autorizado": monto_autorizado,
                        "monto_no_autorizado": monto_no_autorizado,
                    }
                )

        return context

    def post(self, request, *args, **kwargs):
        r = request.POST
        if r.get("reporte_autorizaciones"):
            ordenes = json.loads(r["ordenes"])
            query_cotizaciones = Cotizaciones.objects.filter(no_orden__in=ordenes)
            query_autorizaciones = Autorizaciones.objects.filter(no_orden__in=ordenes)
            query_informacion = Informacion.objects.filter(no_orden__in=ordenes)

            data = [
                [
                    "Orden",
                    "Placas",
                    "Item",
                    "Estado",
                    "Repuesto",
                    "Costo Repuesto",
                    "Costo Mano de Obra",
                    "Subtotal",
                    "IVA",
                    "Monto IVA",
                    "Total",
                    "Fecha Cotización",
                    "Autorizado",
                    "Fecha Autorización",
                ]
            ]
            for cotizacion in query_cotizaciones:
                try:
                    autorizacion = query_autorizaciones.get(item=cotizacion.item).autorizacion
                    autorizacion_fecha_hora_fin = query_autorizaciones.get(item=cotizacion.item).fecha_hora_fin
                except Exception as error:
                    logger.error(error)
                    autorizacion = ""
                    autorizacion_fecha_hora_fin = ""

                try:
                    informacion = query_informacion.get(no_orden=cotizacion.no_orden)
                    placas = informacion.placas
                except Exception as error:
                    logger.error(error)
                    placas = ""

                data.append(
                    [
                        cotizacion.no_orden,
                        placas,
                        cotizacion.item.item.descripcion,
                        cotizacion.item.estado,
                        cotizacion.repuesto,
                        cotizacion.costo_repuesto,
                        cotizacion.costo_mano_obra,
                        cotizacion.subtotal,
                        cotizacion.iva,
                        cotizacion.monto_iva,
                        cotizacion.total,
                        str(cotizacion.fecha_hora_fin)[0:19],
                        autorizacion,
                        str(autorizacion_fecha_hora_fin)[0:19],
                    ]
                )

            excel = ExcelResponse(data, output_filename="reporte_autorizaciones").content

            response = HttpResponse(excel)
            response["Content-Disposition"] = 'attachment; filename="reporte_autorizaciones.xlsx"'
            response["Content-Type"] = "application/octet-stream"
        return response


class HistorialCotizacionesDetalle(TemplateView):
    template_name = "seguimientolite_mazda_col/historial_cotizaciones_detalle.html"

    def get_context_data(self, **kwargs):
        no_orden = self.kwargs["no_orden"]
        request = self.request

        context = {}
        context["titulo"] = "Historial de Autorizaciones"
        context["no_orden"] = no_orden
        context["settings"] = settings

        notificaciones_push(request, context)
        get_evidencias(context, no_orden)

        # Log
        try:
            log = LogGeneral.objects.get(no_orden=no_orden)
            if not log.inicio_asesor and not log.fin_asesor:
                log.inicio_asesor = datetime.now()
                log.save()
        except Exception as error:
            logger.error(error)

        # Informacion de refacciones y mano de obra
        query_tecnico = Items.objects.filter(no_orden=no_orden).exclude(estado__in=("Buen Estado", "Corregido"))
        query_autorizaciones = Autorizaciones.objects.filter(no_orden=no_orden)
        query_cotizaciones = Cotizaciones.objects.filter(no_orden=no_orden)

        context["orden"] = Informacion.objects.get(no_orden=no_orden)
        context["tecnicos"] = VTecnicos.objects.all()
        context["guias_mantenimiento"] = query_tecnico.values("item__revision__id", "item__revision__nombre").distinct()
        context["autorizaciones"] = query_autorizaciones

        try:
            context["fin_tecnico"] = query_tecnico.first().fecha_hora_fin
        except Exception:
            context["fin_tecnico"] = Items.objects.filter(no_orden=no_orden).first().fecha_hora_fin

        try:
            context["revision_limpia"] = VRevisionesLimpias.objects.get(no_orden=no_orden)
        except Exception:
            context["revision_limpia"] = None

        # Inspeccion de cotizaciones
        context["items_tecnico"] = []
        for item in query_tecnico:
            refacciones = Cotizaciones.objects.filter(no_orden=no_orden, item=item)

            total_ref = refacciones.aggregate(Sum("costo_repuesto"))["costo_repuesto__sum"]
            if not total_ref:
                total_ref = 0

            total_mo = refacciones.aggregate(Sum("costo_mano_obra"))["costo_mano_obra__sum"]
            if not total_mo:
                total_mo = 0

            total_subtotal = refacciones.aggregate(Sum("subtotal"))["subtotal__sum"]
            if not total_subtotal:
                total_subtotal = 0

            total_iva = refacciones.aggregate(Sum("monto_iva"))["monto_iva__sum"]
            if not total_iva:
                total_iva = 0

            total = refacciones.aggregate(Sum("total"))["total__sum"]
            if not total:
                total = 0

            context["items_tecnico"].append(
                {
                    "item": item,
                    "refacciones": refacciones,
                    "total_ref": total_ref,
                    "total_mo": total_mo,
                    "total_iva": total_iva,
                    "total_subtotal": total_subtotal,
                    "total": total,
                }
            )

        # Totales
        context["total_refacciones"] = query_cotizaciones.aggregate(Sum("costo_repuesto"))["costo_repuesto__sum"]
        if not context["total_refacciones"]:
            context["total_refacciones"] = 0

        context["total_mano_de_obra"] = query_cotizaciones.aggregate(Sum("costo_mano_obra"))["costo_mano_obra__sum"]
        if not context["total_mano_de_obra"]:
            context["total_mano_de_obra"] = 0

        context["total_iva"] = query_cotizaciones.aggregate(Sum("monto_iva"))["monto_iva__sum"]
        if not context["total_iva"]:
            context["total_iva"] = 0

        context["total_cotizado"] = context["total_refacciones"] + context["total_mano_de_obra"] + context["total_iva"]
        if not context["total_cotizado"]:
            context["total_cotizado"] = 0

        items_autorizados = query_autorizaciones.filter(autorizacion=True).values_list("item", flat=True)
        cotizaciones_autorizadas = query_cotizaciones.filter(item_id__in=items_autorizados)

        context["total_refacciones_autorizadas"] = cotizaciones_autorizadas.aggregate(Sum("costo_repuesto"))[
            "costo_repuesto__sum"
        ]
        if not context["total_refacciones_autorizadas"]:
            context["total_refacciones_autorizadas"] = 0

        context["total_mano_de_obra_autorizada"] = cotizaciones_autorizadas.aggregate(Sum("costo_mano_obra"))[
            "costo_mano_obra__sum"
        ]
        if not context["total_mano_de_obra_autorizada"]:
            context["total_mano_de_obra_autorizada"] = 0

        context["total_iva_autorizado"] = cotizaciones_autorizadas.aggregate(Sum("monto_iva"))["monto_iva__sum"]
        if not context["total_iva_autorizado"]:
            context["total_iva_autorizado"] = 0

        context["total_autorizado"] = (
            context["total_refacciones_autorizadas"]
            + context["total_mano_de_obra_autorizada"]
            + context["total_iva_autorizado"]
        )

        context["total_refacciones_no_autorizadas"] = (
            context["total_refacciones"] - context["total_refacciones_autorizadas"]
        )
        context["total_mano_de_obra_no_autorizada"] = (
            context["total_mano_de_obra"] - context["total_mano_de_obra_autorizada"]
        )
        context["total_no_autorizado"] = context["total_cotizado"] - context["total_autorizado"]

        context["items_autorizados"] = query_autorizaciones.filter(autorizacion=True)
        context["items_no_autorizados"] = query_tecnico.exclude(
            id__in=context["items_autorizados"].values_list("item_id")
        )

        context["nombre_agencia"] = settings.AGENCIA
        context["prefijo"] = settings.TELEFONO
        context["precio_ut"] = settings.SEGUIMIENTOLITE_PRECIO_UT
        context["iva"] = settings.SEGUIMIENTOLITE_IVA
        context["link"] = f"http://{settings.DOMINIO}:{settings.PUERTO}/seguimiento/cliente/{no_orden}"
        return context


# Listado de historial
def historial(request):
    grupos = request.user.groups.values_list("name", flat=True)
    if not request.user.is_authenticated or "cliente" in grupos:
        return redirect("staff_login")

    try:
        context = {}
        orders_to_exclude = VOperacionesTecnico.objects.values_list("no_orden", flat=True)
        orders = Informacion.objects.order_by("-fecha_hora_ingreso").exclude(no_orden__in=orders_to_exclude)
        context["filas"] = orders
        context["tecnicos"] = VTecnicos.objects.all()
        context["titulo"] = "Historial"
    except Exception as error:
        logger.error(error)

    notificaciones_push(request, context)

    return render(request, "seguimientolite_mazda_col/historial.html", context)


# Detalle de historial
def historial_detalle(request, no_orden):
    # Login
    grupos = request.user.groups.values_list("name", flat=True)
    if not request.user.is_authenticated or "cliente" in grupos:
        return redirect("staff_login")

    context = {}
    context["titulo"] = "Historial"

    notificaciones_push(request, context)

    try:
        if LogEnvios.objects.filter(no_orden=no_orden).exists():
            context["envios"] = True
        if ActividadesCalidad.objects.filter(no_orden=no_orden).exists():
            context["calidad"] = True
        context["log"] = LogGeneral.objects.get(no_orden=no_orden)
    except Exception as error:
        logger.error(error)

    try:
        context["no_orden"] = no_orden
        context["tecnicos"] = VTecnicos.objects.all()
        try:
            context["fin_tecnico"] = (
                Items.objects.filter(no_orden=no_orden).order_by("fecha_hora_fin").first().fecha_hora_fin
            )
        except Exception as error:
            logger.error(error)
            context["fin_tecnico"] = "Sin revision tecnica"
        context["precio_ut"] = settings.SEGUIMIENTOLITE_PRECIO_UT
        context["iva"] = settings.SEGUIMIENTOLITE_IVA
        # context['orden'] = VOperacionesRefacciones.objects.get(no_orden=no_orden)
        context["orden"] = Informacion.objects.get(no_orden=no_orden)
        # context['filas_media'] = Evidencias.objects.filter(no_orden=no_orden)
        context["filas_media"] = []
        context["filas_video"] = []
        media = Evidencias.objects.filter(no_orden=no_orden)
        for file in media:
            file_type = mimetypes.guess_type(file.evidencia)[0]
            try:
                if "video" in file_type:
                    context["filas_video"].append(file)
                else:
                    context["filas_media"].append(file)
            except Exception as error:
                logger.error(error)

        context["items_mo"] = context["filas"].values_list("item", flat=True).distinct()
    except Exception as error:
        logger.error(error)
    return render(request, "seguimientolite_mazda_col/historial_detalle.html", context)


# Login automatico para clientes
def client_autologin(request, no_orden):
    try:
        client = User.objects.get(username=no_orden)
        login(request, client)
        return redirect("cliente_cotizacion", no_orden=no_orden)
    except Exception:
        client = User.objects.create_user(username=no_orden, first_name=no_orden)
        group = Group.objects.get_or_create(name="cliente")[0]
        password = User.objects.make_random_password(length=12)
        client.set_password(password)
        client.groups.add(group)
        client.save()
        login(request, client)
        return redirect("cliente_cotizacion", no_orden=no_orden)


# Detalle de cliente
def cliente_detalle(request, no_orden):

    if request.method == "GET":
        # Login de cliente
        try:
            client = User.objects.get(username=no_orden)
            login(request, client)
        except Exception:
            client = User.objects.create_user(username=no_orden, first_name=no_orden)
            group = Group.objects.get_or_create(name="cliente")[0]
            password = User.objects.make_random_password(length=12)
            client.set_password(password)
            client.groups.add(group)
            client.save()
            login(request, client)

        context = {}
        context["titulo"] = "Cliente"
        context["settings"] = settings

        # Notificaciones push
        notificaciones_push(request, context)
        get_evidencias(context, no_orden)

        # Log
        try:
            LogCliente.objects.create(
                no_orden=no_orden,
                fecha_hora_visita=datetime.now(),
            )
        except Exception as error:
            logger.error(error)

        context["no_orden"] = no_orden
        try:
            context["orden"] = Informacion.objects.get(no_orden=no_orden)
        except Exception:
            pass

        # Items
        queryset_tecnico = Items.objects.filter(no_orden=no_orden).order_by("-item__descripcion")
        context["items"] = queryset_tecnico
        context["items_inmediatos"] = queryset_tecnico.filter(estado="Inmediato")
        context["items_recomendados"] = queryset_tecnico.filter(estado="Recomendado")
        context["items_corregidos"] = queryset_tecnico.filter(estado="Corregido")
        context["items_buen_estado"] = queryset_tecnico.filter(estado="Buen Estado")

        # Totales
        context["totales_items"] = []
        for item in context["items"]:
            cotizaciones_item = Cotizaciones.objects.filter(item=item)
            subtotal_ref = cotizaciones_item.aggregate(Sum("costo_repuesto"))["costo_repuesto__sum"]
            subtotal_mo = cotizaciones_item.aggregate(Sum("costo_mano_obra"))["costo_mano_obra__sum"]

            if not subtotal_ref:
                subtotal_ref = 0
            if not subtotal_mo:
                subtotal_mo = 0

            try:
                total_ref = subtotal_ref + (subtotal_ref * (cotizaciones_item.first().iva / 100))
                total_mo = subtotal_mo + (subtotal_mo * (cotizaciones_item.first().iva / 100))

                total = total_ref + total_mo
                context["totales_items"].append(
                    {
                        "item": item,
                        "total_ref": round(total_ref, 2),
                        "total_mo": round(total_mo, 2),
                        "total": round(total, 2),
                    }
                )
            except Exception as error:
                logger.error(error)
                context["totales_items"].append(
                    {
                        "item": item,
                        "total_ref": 0,
                        "total_mo": 0,
                        "total": 0,
                    }
                )

        context["total_orden"] = 0
        for item in context["totales_items"]:
            context["total_orden"] += item["total"]

        # Items autorizados
        query_autorizaciones = Autorizaciones.objects.filter(no_orden=no_orden)
        context["items_autorizados"] = query_autorizaciones.filter(autorizacion=True).values_list("item_id", flat=True)

        # TABLAS EN FRONT-END
        query_refacciones = Refacciones.objects.filter(no_orden=no_orden)
        query_mano_de_obra = ManoDeObra.objects.filter(no_orden=no_orden)
        context["refacciones"] = query_refacciones
        context["mano_de_obra"] = query_mano_de_obra

        return render(request, "seguimientolite_mazda_col/cliente_detalle.html", context)

    if request.method == "POST":
        r = request.POST

        items_autorizados = json.loads(r.get("items_autorizados"))
        for item_id in items_autorizados:
            item = Items.objects.get(id=item_id)
            defaults = {"autorizacion": True}
            Autorizaciones.objects.update_or_create(no_orden=no_orden, item=item, defaults=defaults)
        if r.get("notif", None):
            template_context = {}
            template_context["autorizacion"] = True
            template_context["asunto"] = "Confirmación de Autorización"
            template_context["preview"] = settings.AGENCIA + " | Su vehículo ha sido revisado"
            template_context["nombre_agencia"] = settings.AGENCIA
            template_context["cotizacion_url"] = f"http://{settings.DOMINIO}:{settings.PUERTO}/cliente/{no_orden}/"
            template_context["items"] = Autorizaciones.objects.filter(no_orden=no_orden, autorizacion="Autorizado")
            template_context["telefono_agencia"] = settings.TELEFONO
            template_context["privacy_url"] = settings.AVISO_PRIVACIDAD

            template_context["logo"] = "https://logos-marcas.com/wp-content/uploads/2020/04/Toyota-Emblema-650x366.png"

            html_content = render_to_string("seguimientolite_mazda_col/mail-template.html", template_context)

            client_mail = LogEnvios.objects.filter(no_orden=no_orden).order_by("-fecha_hora_envio").first().correo

            # CORREO DE CONFIRMACION PARA CLIENTE
            try:
                email = EmailMessage(
                    f"{settings.AGENCIA} | Su autorización ha sido procesada",
                    html_content,
                    settings.EMAIL_HOST_USER,
                    [client_mail],
                )
                email.content_subtype = "html"
                email.send()
            except Exception as error:
                logger.error(error)

            # CORREO DE CONFIRMACION PARA PERSONAL
            template_context["preview"] = ""
            template_context["cotizacion_url"] = f"http://{settings.DOMINIO}:{settings.PUERTO}/seguimiento/login"
            html_content = render_to_string("seguimientolite_mazda_col/mail-template.html", template_context)

            try:
                email = EmailMessage(
                    f"{settings.AGENCIA} | La orden {no_orden} ha sido autorizada",
                    html_content,
                    settings.EMAIL_HOST_USER,
                    ["eglenelid.gamaliel@gmail.com", "eliu.hepher@gmail.com"],
                )
                email.content_subtype = "html"
                email.send()
            except Exception as error:
                logger.error(error)

        try:
            if r.get("notf", None):
                payload = {
                    "head": settings.AGENCIA,
                    "body": f"La orden {no_orden} tiene nuevos items autorizados",
                    "icon": "https://logos-marcas.com/wp-content/uploads/2020/04/Toyota-Emblema-650x366.png",
                    "url": f"https://{settings.DOMINIO}:{settings.PUERTO}/asesor/{no_orden}/",
                }
                asesor = Informacion.objects.get(no_orden=no_orden).asesor
                receiver = User.objects.filter(first_name=asesor)

                send_user_notification(user=receiver, payload=payload, ttl=1000)
        except Exception as error:
            logger.error(error)
        return HttpResponse(status=200)


# Hoja multipuntos
def hoja_multipuntos_pdf(request, no_orden):
    buffer = get_pdf_calidad(no_orden)
    return FileResponse(buffer, as_attachment=False, filename=f"multipuntos_{no_orden}.pdf")


# KPIS Resumen
def kpis_resumen(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("staff_login")

        context = {}
        context["titulo"] = "KPIS"
        context["años"] = VInformacion.objects.datetimes("fecha_hora_ingreso", "year").distinct()
        notificaciones_push(request, context)

        return render(request, "kpis/resumen.html", context)

    if request.method == "POST":
        request_body = request.POST
        tipo = request_body.get("tipo")

        if tipo == "hoy":
            fecha = str(date.today())
            queryset_header = VInformacion.objects.filter(
                fecha_hora_ingreso__isnull=False, fecha_hora_ingreso__date=fecha
            )
        if tipo == "mes":
            fecha = request_body.get("fecha")
            queryset_header = VInformacion.objects.filter(
                fecha_hora_ingreso__isnull=False,
                fecha_hora_ingreso__date__year=fecha[0:4],
                fecha_hora_ingreso__date__month=fecha[5:7],
            )
        if tipo == "año":
            fecha = request_body.get("fecha")
            queryset_header = VInformacion.objects.filter(
                fecha_hora_ingreso__isnull=False,
                fecha_hora_ingreso__date__year=fecha[0:4],
            )
        if tipo == "rango":
            queryset_header = VInformacion.objects.filter(
                fecha_hora_ingreso__range=(request_body["inicio"], request_body["fin"])
            )

        no_ordenes_all = queryset_header.exclude(no_orden=0).values_list("no_orden").distinct()

        tarjetas_tecnico = Items.objects.filter(no_orden__in=no_ordenes_all)
        tarjetas_refacciones = Refacciones.objects.filter(no_orden__in=no_ordenes_all)
        tarjetas_asesor = ManoDeObra.objects.filter(no_orden__in=no_ordenes_all)
        tarjetas_visitas = LogCliente.objects.filter(no_orden__in=no_ordenes_all)
        queryset_tiempos = LogGeneral.objects.filter(no_orden__in=no_ordenes_all)
        queryset_envios = LogEnvios.objects.filter(no_orden__in=no_ordenes_all)
        queryset_autorizaciones = Autorizaciones.objects.filter(no_orden__in=no_ordenes_all)

        response = {}
        response["total_entradas"] = no_ordenes_all.count()
        response["finalizados_tecnico"] = tarjetas_tecnico.values("no_orden").distinct().count()
        response["finalizados_refacciones"] = tarjetas_refacciones.values("no_orden").distinct().count()
        response["finalizados_asesor"] = tarjetas_asesor.values("no_orden").distinct().count()
        response["tarjeta_ordenes_enviadas"] = queryset_envios.values("no_orden").distinct().count()
        response["tarjeta_vistas"] = tarjetas_visitas.values("no_orden").distinct().count()
        response["finalizados_cliente"] = queryset_autorizaciones.values("no_orden").distinct().count()

        # Tiempo promedio de tecnico
        duracion_tecnico_func = ExpressionWrapper(
            F("fin_tecnico") - F("inicio_tecnico"), output_field=fields.DurationField()
        )
        duracion_tecnico = queryset_tiempos.annotate(duracion_tecnico=duracion_tecnico_func)
        if tiempo_tecnico := duracion_tecnico.aggregate(promedio=Avg("duracion_tecnico"))["promedio"]:
            response["tiempo_tecnico"] = round(tiempo_tecnico.seconds / 60, 2)
        else:
            response["tiempo_tecnico"] = 0

        # Tiempo promedio de refacciones
        duracion_ref_func = ExpressionWrapper(
            F("fin_refacciones") - F("inicio_refacciones"), output_field=fields.DurationField()
        )
        duracion_ref = queryset_tiempos.annotate(duracion_ref=duracion_ref_func)
        if tiempo_cotizacion_refacciones := duracion_ref.aggregate(promedio=Avg("duracion_ref"))["promedio"]:
            response["tiempo_refacciones"] = round(tiempo_cotizacion_refacciones.seconds / 60, 2)
        else:
            response["tiempo_refacciones"] = 0

        # Tiempo promedio de mano de obra
        duracion_mo_func = ExpressionWrapper(
            F("fin_mano_de_obra") - F("inicio_mano_de_obra"), output_field=fields.DurationField()
        )
        duracion_mo = queryset_tiempos.annotate(duracion_mo=duracion_mo_func)
        if tiempo_mo := duracion_mo.aggregate(promedio=Avg("duracion_mo"))["promedio"]:
            response["tiempo_mo"] = round(tiempo_mo.seconds / 60, 2)
        else:
            response["tiempo_mo"] = 0

        # Tiempo promedio de asesor
        duracion_asesor_func = ExpressionWrapper(
            F("fin_asesor") - F("inicio_asesor"), output_field=fields.DurationField()
        )
        duracion_asesor = queryset_tiempos.annotate(duracion_asesor=duracion_asesor_func)
        if tiempo_asesor := duracion_asesor.aggregate(promedio=Avg("duracion_asesor"))["promedio"]:
            response["tiempo_asesor"] = round(tiempo_asesor.seconds / 60, 2)
        else:
            response["tiempo_asesor"] = 0

        if no_wa := queryset_envios.filter(medio="WhatsApp").count():
            response["no_wa"] = no_wa
        else:
            response["no_wa"] = 0

        if no_mail := queryset_envios.filter(medio="E-Mail").count():
            response["no_mail"] = no_mail
        else:
            response["no_mail"] = 0

        finalizados_envios = queryset_envios.values_list("no_orden").distinct().count()
        response["finalizados_envios"] = finalizados_envios

        return HttpResponse(json.dumps(response), content_type="application/json")


def kpis_financiero(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("staff_login")
        context = {}
        context["titulo"] = "KPIS"
        context["años"] = VInformacion.objects.datetimes("fecha_hora_ingreso", "year").distinct()
        context["asesores"] = (
            VUsuarios.objects.filter(cveasesor__isnull=False).exclude(cveasesor="").values_list("nombre", flat=True)
        )
        notificaciones_push(request, context)
        return render(request, "kpis/financiero.html", context)

    if request.method == "POST":
        request_body = request.POST

        tipo = request_body.get("tipo")
        header_filtros = {}

        if request_body.get("asesor"):
            header_filtros["asesor"] = request_body["asesor"]
        if tipo == "hoy":
            fecha = date.today()
            header_filtros["fecha_hora_ingreso__isnull"] = False
            header_filtros["fecha_hora_ingreso__date"] = fecha
            no_dias = calendar.monthrange(fecha.year, fecha.month)[1]
            categorias = list(range(1, no_dias + 1))
        if tipo == "mes":
            fecha = request_body.get("fecha")
            header_filtros["fecha_hora_ingreso__isnull"] = False
            header_filtros["fecha_hora_ingreso__date__year"] = fecha[0:4]
            header_filtros["fecha_hora_ingreso__date__month"] = fecha[5:7]
            no_dias = calendar.monthrange(int(fecha[0:4]), int(fecha[5:7]))[1]
            categorias = list(range(1, no_dias + 1))
        if tipo == "año":
            fecha = request_body.get("fecha")
            header_filtros["fecha_hora_ingreso__isnull"] = False
            header_filtros["fecha_hora_ingreso__date__year"] = fecha[0:4]
            no_meses = 12
            categorias = list(range(1, no_meses + 1))
        if tipo == "rango":
            header_filtros["fecha_hora_ingreso__range"] = (request_body["inicio"], request_body["fin"])
            no_meses = 12
            categorias = list(range(1, no_meses + 1))

        queryset_header = VInformacion.objects.filter(**header_filtros)
        no_ordenes_all = queryset_header.values_list("no_orden", flat=True)

        queryset_general = Autorizaciones.objects.filter(no_orden__in=no_ordenes_all)
        queryset_envios = LogEnvios.objects.filter(no_orden__in=no_ordenes_all)

        # Construccion de la respuesta
        # Tarjetas de cabecera
        response = {}
        response["categories"] = categorias
        response["no_ordenes_totales"] = queryset_header.exclude(no_orden=0).count()
        response["no_ordenes_enviadas"] = queryset_envios.values("no_orden").distinct().count()
        response["no_ordenes_autorizadas"] = queryset_general.exclude(autorizacion=False).values("no_orden").count()

        monto_ref = Refacciones.objects.filter(no_orden__in=no_ordenes_all).aggregate(sum=Sum("subtotal_iva"))["sum"]
        if not monto_ref:
            monto_ref = 0
        monto_mo = ManoDeObra.objects.filter(no_orden__in=no_ordenes_all).aggregate(sum=Sum("subtotal_iva"))["sum"]
        if not monto_mo:
            monto_mo = 0
        response["total_autorizado"] = str(monto_ref + monto_mo)

        promedio_ordenes = queryset_general.values("no_orden").annotate(promedio=Sum("autorizacion"))
        try:
            response["items_promedio"] = round(promedio_ordenes.aggregate(avg=Avg("promedio"))["avg"], 2)
        except Exception:
            response["items_promedio"] = 0

        # Graficas
        response["tarjetas_asesor"] = []
        series = []
        nombres_asesores = queryset_header.exclude(asesor__isnull=True).values_list("asesor", flat=True).distinct()
        for nombre_asesor in nombres_asesores:
            asesor_no_ordenes = (
                queryset_header.filter(asesor=nombre_asesor).values_list("no_orden", flat=True).distinct()
            )
            ordenes_enviadas = (
                queryset_envios.filter(no_orden__in=asesor_no_ordenes).values("no_orden").distinct().count()
            )
            ordenes_autorizadas = (
                queryset_general.filter(no_orden__in=asesor_no_ordenes)
                .exclude(autorizacion=False)
                .values("no_orden")
                .count()
            )

            # Monto de refacciones
            monto_asesor_ref = Refacciones.objects.filter(no_orden__in=asesor_no_ordenes).aggregate(
                sum=Sum("subtotal_iva")
            )["sum"]
            if not monto_asesor_ref:
                monto_asesor_ref = 0
            # Monto de mano de obra
            monto_asesor_mo = ManoDeObra.objects.filter(no_orden__in=asesor_no_ordenes).aggregate(
                sum=Sum("subtotal_iva")
            )["sum"]
            if not monto_asesor_mo:
                monto_asesor_mo = 0

            # Monto total
            monto_total = monto_asesor_mo + monto_asesor_ref
            if not monto_total:
                monto_total = 0
            monto_ssl = round(monto_total, 2)

            if not ordenes_enviadas:
                porcentaje_efectividad = 0
            else:
                porcentaje_efectividad = round((100 / ordenes_enviadas) * ordenes_autorizadas, 2)

            response["tarjetas_asesor"].append(
                {
                    "asesor_nombre": nombre_asesor,
                    "asesor_ordenes": queryset_header.filter(asesor=nombre_asesor).count(),
                    "asesor_ordenes_enviadas": ordenes_enviadas,
                    "asesor_ordenes_autorizadas": ordenes_autorizadas,
                    "asesor_porcentaje_efectividad": porcentaje_efectividad,
                    "asesor_monto_ssl": str(monto_ssl),
                    "asesor_monto_total": str(monto_total),
                }
            )

            data = []
            for categoria in categorias:
                if categoria < 10:
                    categoria = "0" + str(categoria)
                if tipo in ("hoy", "mes"):
                    categoria_filter = {"fecha_hora_fin__day": categoria}
                if tipo in ("año", "rango"):
                    categoria_filter = {"fecha_hora_fin__month": categoria}

                # Monto de refacciones
                monto_dia_asesor_ref = Refacciones.objects.filter(
                    no_orden__in=asesor_no_ordenes, **categoria_filter
                ).aggregate(sum=Sum("subtotal_iva"))["sum"]
                if not monto_dia_asesor_ref:
                    monto_dia_asesor_ref = 0

                # Monto de mano de obra
                monto_dia_asesor_mo = ManoDeObra.objects.filter(
                    no_orden__in=asesor_no_ordenes, **categoria_filter
                ).aggregate(sum=Sum("subtotal_iva"))["sum"]
                if not monto_dia_asesor_mo:
                    monto_dia_asesor_mo = 0

                monto_dia_asesor_total = monto_dia_asesor_mo + monto_dia_asesor_ref
                data.append(monto_dia_asesor_total)
            series.append({"name": nombre_asesor, "data": data})

        response["series"] = series
        return JsonResponse(response)
