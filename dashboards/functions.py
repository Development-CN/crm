from django.db.models import F
from django.utils.timezone import make_aware

from dashboards.models import Prospecto, Asesor, Catalogo, CatalogoModelo, Lead, CatalogoRespuestasByEtapa, Historial, HistorialVerificaciones, Retomas, VehiculosInteresLead, Evento
from datetime import date, datetime, timedelta
import re
import openpyxl

from django.contrib.auth.models import User, Group
from django.db import IntegrityError

def verificar_primer_contacto(lead, prospecto, tiempo_diferencia):
    """if lead.tiempo_primer_contacto:
        if lead.tiempo_primer_contacto >= 60:
            print("aver esto otro")
            lead.nombre_asesor = None
            prospecto.nombre_asesor = None
            lead.save()
            prospecto.save()
    else:
        if tiempo_diferencia >= 60:
            print("aver esto")
            lead.nombre_asesor = None
            prospecto.nombre_asesor = None
            lead.save()
            prospecto.save()"""


def verificar_primer_contacto_todos_los_leads(leads):
    
    """for lead in leads:
        try:
            tiempo_diferencia = int((datetime.now() - lead.fecha_hora_asignacion_asesor.replace(tzinfo=None)).total_seconds() / 60)
            
            prospecto = Prospecto.objects.get(id=lead.prospecto.id)
            if lead.tiempo_primer_contacto or tiempo_diferencia:
                if lead.tiempo_primer_contacto:
                    if lead.tiempo_primer_contacto >= 60:
                        print("aver esto otro")
                        lead.nombre_asesor = None
                        prospecto.nombre_asesor = None
                        lead.save()
                        prospecto.save()
                else:
                    if tiempo_diferencia >= 60:
                        print("aver esto")
                        lead.nombre_asesor = None
                        prospecto.nombre_asesor = None
                        lead.save()
                        prospecto.save()
        except:
            pass"""
    pass


def arreglar_marcas_nuevos_leads(leads):
    
    """for lead in leads:
        try:
            tiempo_diferencia = int((datetime.now() - lead.fecha_hora_asignacion_asesor.replace(tzinfo=None)).total_seconds() / 60)
            
            prospecto = Prospecto.objects.get(id=lead.prospecto.id)
            if lead.tiempo_primer_contacto or tiempo_diferencia:
                if lead.tiempo_primer_contacto:
                    if lead.tiempo_primer_contacto >= 60:
                        print("aver esto otro")
                        lead.nombre_asesor = None
                        prospecto.nombre_asesor = None
                        lead.save()
                        prospecto.save()
                else:
                    if tiempo_diferencia >= 60:
                        print("aver esto")
                        lead.nombre_asesor = None
                        prospecto.nombre_asesor = None
                        lead.save()
                        prospecto.save()
        except:
            pass"""
    pass


def separar_nombre(nombre):
    patron = r'(\w)([A-Z])'

    return re.sub(patron, r'\1 \2', nombre)



def funciones_migracion():
    leads = Lead.objects.all()
    # PASO 1
    leads = Lead.objects.filter(marcas_interes__isnull=False).exclude(marcas_interes__startswith='{')
    leads.update(marcas_interes=None)

    # PASO 2
    leads = Lead.objects.filter(marcas_interes__isnull=True)
    leads.update(marcas_interes='{"marcas": []}')

    # PASO 3
    leads = Lead.objects.all()
    for lead in leads:
        lead.tiempo_cambio_de_etapa = None
        print(lead)
        if lead.etapa == "Contacto Asesor" and lead.respuesta == "No contesta / volver a llamar":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto Asesor" and lead.respuesta == "Llamada realizada":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto Asesor" and lead.respuesta == "Llamada Realizada":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto Asesor" and lead.respuesta == "Mensaje enviado a whatsapp":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto Asesor" and lead.respuesta == "Se deja mensaje de voz":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto Asesor":
            lead.etapa = "Interaccion"
        elif lead.etapa == "Contacto asesor" and lead.respuesta == "No contesta / volver a llamar":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto asesor" and lead.respuesta == "Llamada realizada":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto asesor" and lead.respuesta == "Llamada Realizada":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto asesor" and lead.respuesta == "Mensaje enviado a whatsapp":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto asesor" and lead.respuesta == "Se deja mensaje de voz":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto asesor" and lead.respuesta == "N/A":
            lead.etapa = "No contactado"
        elif lead.etapa == "Contacto asesor":
            lead.etapa = "Interaccion"
        elif lead.etapa == "Seguimiento" and lead.respuesta == "Espera de aprobacion de Credito":
            lead.etapa = "Oportunidad"
        elif lead.etapa == "Seguimiento" and lead.respuesta == "Aceptacion de documentos":
            lead.etapa = "Oportunidad"
        elif lead.etapa == "Seguimiento" and lead.respuesta == "Test drive":
            lead.etapa = "Oportunidad"
        elif lead.etapa == "Seguimiento" and lead.respuesta == "Negociacion":
            lead.etapa = "Oportunidad"
        elif lead.etapa == "Seguimiento":
            lead.etapa = "Interaccion"
        elif lead.etapa == "Venta y Entrega":
            lead.etapa = "Pedido"
        elif lead.etapa == "Venta y entrega":
            lead.etapa = "Pedido"
        if lead.respuesta == "Agenda cita":
            lead.respuesta = "Enviar información"
        elif lead.respuesta == "Enviar catalogo / Informacion":
            lead.respuesta = "Enviar información"
        elif lead.respuesta == "Hacer una nueva llamada_ Cita // fecha":
            lead.respuesta = "Llamada de seguimiento"
        elif lead.respuesta == "Interes mediano plazo / Fecha":
            lead.respuesta = "Interés mediano plazo / Fecha"
        elif lead.respuesta == "Interes largo plazo / Fecha":
            lead.respuesta = "Interés a largo plazo / Fecha"
        elif lead.respuesta == "En otra ciudad posibilidad traslado":
            lead.respuesta = "Llamada de seguimiento"
        elif lead.respuesta == "Vh excede su presupuesto":
            lead.respuesta = "En el momento no hay vh de interés"
        elif lead.respuesta == "No contesta / volver a llamar":
            lead.respuesta = "No contesta / Volver a llamar"
        elif lead.respuesta == "No esta el vh de su interes":
            lead.respuesta = "En el momento no hay vh de interés"
        elif lead.respuesta == "Llamada realizada" or lead.respuesta == "Llamada Realizada":
            lead.respuesta = "No contesta / Volver a llamar"
        elif lead.respuesta == "Mensaje enviado a whatsapp":
            lead.respuesta = "Esperando respuesta WhatsApp"
        elif lead.respuesta == "Se deja mensaje de voz":
            lead.respuesta = "Esperando respuesta WhatsApp"
        elif lead.respuesta == "Interes mediano plazo / Fecha":
            lead.respuesta = "Interés mediano plazo / Fecha"
        elif lead.respuesta == "Interes largo plazo / Fecha":
            lead.respuesta = "Interés a largo plazo / Fecha"
        elif lead.respuesta == "Esta interesado en otro vehiculo":
            lead.respuesta = "En el momento no hay vh de interés"
        elif lead.respuesta == "En el momento no hay vh de interes":
            lead.respuesta = "En el momento no hay vh de interés"
        elif lead.respuesta == "Espera de aprobacion de Credito":
            lead.respuesta = "En estudio de crédito"
        elif lead.respuesta == "Aceptacion de documentos":
            lead.respuesta = "En estudio de crédito"
        elif lead.respuesta == "Test drive":
            lead.respuesta = "Negociación"
        elif lead.respuesta == "Negociacion":
            lead.respuesta = "Negociación"
        elif lead.respuesta == "Marca/ Modelo no se encuntra disponible":
            lead.respuesta = "En el momento no hay vh de interés"
        elif lead.respuesta == "Alistamiento mecanico basico":
            lead.respuesta = "Alistamiento"
        elif lead.respuesta == "Entrega del vehiculo":
            lead.respuesta = "Verificación"
        elif lead.respuesta == "Entregado":
            lead.respuesta = "Entrega finalizada"
        elif lead.respuesta == "Separación":
            lead.respuesta = "Separación"

        historial = Historial.objects.filter(lead=lead, operacion__startswith="El cliente a dado una respuesta").order_by("id")
        if historial.exists():
            print(lead)
            fecha_primer_contacto = historial.first().fecha
            hora_primer_contacto = historial.first().hora

            datetime_primer_contacto = datetime.combine(fecha_primer_contacto, hora_primer_contacto)
            if lead.fecha_hora_asignacion_asesor:
                tiempo_primer_contacto = datetime_primer_contacto - lead.fecha_hora_asignacion_asesor.replace(tzinfo=None)

                lead.fecha_primer_contacto = datetime_primer_contacto
                lead.tiempo_primer_contacto = tiempo_primer_contacto.total_seconds() / 60
        try:
            lead.save()
        except:
            lead.delete()


    # PASO 4
    # vehiculos = VehiculosInteresLead.objects.filter(cotizar=True).select_related('lead')
    # for vehiculo in vehiculos:
    #     lead = vehiculo.lead
        
    #     # Crear un diccionario con los datos del vehículo
    #     marca_info = {
    #         "marca": vehiculo.marca,
    #         "modelo": vehiculo.modelo,
    #         "color": vehiculo.color,
    #         "marca_comentario": vehiculo.comentario,
    #         "codigo": vehiculo.codigo_vehiculo,
    #         "precio": vehiculo.precio
    #     }
        
    #     # Obtener la lista de marcas de interés actual, o inicializarla si es None
    #     if lead.marcas_interes is None:
    #         lead.marcas_interes = {"marcas": []}
        
    #     # Agregar el nuevo vehículo a la lista de marcas de interés
    #     lead.marcas_interes["marcas"].append(marca_info)
        
    #     # Guardar el lead
    #     lead.save()


def subir_usuarios():
    wb = openpyxl.load_workbook(r'c:\Users\cnsoporte\Documents\Hoja de cálculo sin título (1).xlsx')
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2):
        username = row[0].value
        full_name = row[1].value
        password = row[2].value
        perfil = row[3].value
        new_password = row[4].value

        if not username or str(username).lower() == 'null':
            continue  # Ignorar filas sin un nombre de usuario válido

        first_name = full_name

        try:
            user, created = User.objects.get_or_create(username=username)
            user.first_name = first_name
            if password and str(password).lower() != 'null':
                user.set_password(password)
            user.is_active = perfil.lower() != 'inactivo'
            if perfil.lower() != 'inactivo':
                gr = Group.objects.get(name__iexact=perfil)
                user.groups.add(gr)
            user.save()

            try:
                asesor = Asesor.objects.get(nombre=first_name)
                asesor.user = user
                asesor.save()
            except:
                pass

            print(user)

            # Si se proporciona una nueva contraseña, actualizarla
            if new_password and str(new_password).lower() != 'null':
                user.set_password(new_password)
                user.save()

        except IntegrityError as e:
            print(f"Error creando el usuario {username}: {e}")




def function_recover_leads():
    full_historial = Historial.objects.filter(fecha=datetime(2024, 8, 21), operacion="Creación Lead")
    for historial in full_historial:
        fecha_bien = make_aware(datetime.combine(historial.fecha, historial.hora).replace(microsecond=0))
        fecha_fin = make_aware(datetime.combine(historial.fecha, historial.hora).replace(microsecond=0) + timedelta(seconds=1))
        print(historial.id)
        try:
            prospecto = Prospecto.objects.get(fecha_captura__gte=fecha_bien, fecha_captura__lt=fecha_fin)
            sala = Asesor.objects.get(nombre=prospecto.nombre_asesor).sala
            sala = Asesor.objects.get(nombre=prospecto.nombre_asesor).sala
            nombre_asesor = prospecto.nombre_asesor

        except:
            prospecto = None

        if prospecto:
        
            try:
                vehiculo = VehiculosInteresLead.objects.get(lead_id=historial.lead_id)
                marcas_interes = {'marcas': [{'marca': vehiculo.marca, 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]}
            except:
                marcas_interes = {'marcas': []}

            lead = Lead.objects.create(
                prospecto=prospecto,
                # origenes_lead="",
                marcas_interes=marcas_interes,
                sala=sala,
                etapa="No contactado",
                respuesta="Sin contactar",
                estado="No contactado",
                status="Frío",
                interes="Venta",
                activo=True,
                fecha_apertura=make_aware(datetime.combine(historial.fecha, historial.hora)),
                comentario=historial.comentarios,
                # campania="",
                # tipo_documento="",
                # documento="",
                test_drive=False,
                nombre_asesor=nombre_asesor,
                nombre_asesor_original=nombre_asesor,
                fecha_hora_asignacion_asesor=make_aware(datetime.combine(historial.fecha, historial.hora)),
                nombre_anfitrion=historial.responsable,
            )
            historiales = Historial.objects.filter(lead_id=historial.lead_id).update(lead=lead)

            historial.lead = lead
            historial.save()
            try:
                vehiculo.lead = lead
                vehiculo.save()
            except:
                pass



def function_recover_leads_2():
    dictrionary = [
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T13:08:32.8271850+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Gustavo Parraga",
            "fecha_hora_asignacion_asesor": "2024-08-22T13:08:32.8271850+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93526,
            "nombre_asesor_original": "Gustavo Parraga",
            "id": 91100
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T12:32:47.6064110+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jenny Angel",
            "fecha_hora_asignacion_asesor": "2024-08-22T12:32:47.6064110+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93523,
            "nombre_asesor_original": "Jenny Angel",
            "id": 91099
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T12:00:54.7925800+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jaime Murcia",
            "fecha_hora_asignacion_asesor": "2024-08-22T12:00:54.7925800+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93522,
            "nombre_asesor_original": "Jaime Murcia",
            "id": 91098
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T11:58:48.4367090+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jenny Angel",
            "fecha_hora_asignacion_asesor": "2024-08-22T11:58:48.4367090+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93521,
            "nombre_asesor_original": "Jenny Angel",
            "id": 91097
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{"marca": "MAZDA", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T11:15:37.1403910+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jenny Angel",
            "fecha_hora_asignacion_asesor": "2024-08-22T11:15:37.1403910+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93520,
            "nombre_asesor_original": "Jenny Angel",
            "id": 91096
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T11:15:28.7152520+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Margy Barrios",
            "fecha_hora_asignacion_asesor": "2024-08-22T11:15:28.7152520+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93519,
            "nombre_asesor_original": "Margy Barrios",
            "id": 91095
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{"marca": "HYUNDAI", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T10:11:05.7505400+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Margy Barrios",
            "fecha_hora_asignacion_asesor": "2024-08-22T10:11:05.7505400+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93518,
            "nombre_asesor_original": "Margy Barrios",
            "id": 91094
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{"marca": "MITSUBISHI", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T10:10:04.3532720+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jaime Murcia",
            "fecha_hora_asignacion_asesor": "2024-08-22T10:10:04.3532720+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93517,
            "nombre_asesor_original": "Jaime Murcia",
            "id": 91093
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{"marca": "MAZDA", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T10:09:26.5871600+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Margy Barrios",
            "fecha_hora_asignacion_asesor": "2024-08-22T10:09:26.5871600+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93516,
            "nombre_asesor_original": "Margy Barrios",
            "id": 91092
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T09:44:57.8563500+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jaime Murcia",
            "fecha_hora_asignacion_asesor": "2024-08-22T09:44:57.8563500+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93515,
            "nombre_asesor_original": "Jaime Murcia",
            "id": 91091
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T09:44:56.4692810+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jaime Murcia",
            "fecha_hora_asignacion_asesor": "2024-08-22T09:44:56.4692810+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93514,
            "nombre_asesor_original": "Jaime Murcia",
            "id": 91090
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T09:18:02.8737720+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Margy Barrios",
            "fecha_hora_asignacion_asesor": "2024-08-22T09:18:02.8737720+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93513,
            "nombre_asesor_original": "Margy Barrios",
            "id": 91089
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-22T09:18:00.3838620+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Gustavo Parraga",
            "fecha_hora_asignacion_asesor": "2024-08-22T09:18:00.3838620+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93512,
            "nombre_asesor_original": "Gustavo Parraga",
            "id": 91088
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{"marca": "MAZDA", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T16:40:01.7189680+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jefferson Naranjo",
            "fecha_hora_asignacion_asesor": "2024-08-21T16:40:01.7189680+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93508,
            "nombre_asesor_original": "Jefferson Naranjo",
            "id": 91087
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{"marca": "CHEVROLET", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T16:20:48.1678190+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Morelia tobar",
            "fecha_hora_asignacion_asesor": "2024-08-21T16:20:48.1678190+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93507,
            "nombre_asesor_original": "Morelia tobar",
            "id": 91086
        },
        {
            "origen_lead": "",
            "marcas_interes": {'marcas': [{'marca': 'HYUNDAI', 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T16:19:52.6602400+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Consuelo Izquierdo",
            "fecha_hora_asignacion_asesor": "2024-08-21T16:19:52.6602400+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93506,
            "nombre_asesor_original": "Consuelo Izquierdo",
            "id": 91085
        },
        {
            "origen_lead": "",
            "marcas_interes": {'marcas': []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T16:19:02.6000080+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Freddy Cardenas",
            "fecha_hora_asignacion_asesor": "2024-08-21T16:19:02.6000080+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93505,
            "nombre_asesor_original": "Freddy Cardenas",
            "id": 91084
        },
        {
            "origen_lead": "",
            "marcas_interes": {'marcas': []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T16:17:56.2784550+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jefferson Naranjo",
            "fecha_hora_asignacion_asesor": "2024-08-21T16:17:56.2784550+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93504,
            "nombre_asesor_original": "Jefferson Naranjo",
            "id": 91083
        },
        {
            "origen_lead": "",
            "marcas_interes": {'marcas': []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T16:17:52.6279660+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Maryluz Anzola",
            "fecha_hora_asignacion_asesor": "2024-08-21T16:17:52.6279660+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93503,
            "nombre_asesor_original": "Maryluz Anzola",
            "id": 91082
        },
        {
            "origen_lead": "",
            "marcas_interes": {'marcas': []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T15:54:27.7612900+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Paola Galindez",
            "fecha_hora_asignacion_asesor": "2024-08-21T15:54:27.7612900+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93502,
            "nombre_asesor_original": "Paola Galindez",
            "id": 91081
        },
        {
            "origen_lead": None,
            "marcas_interes": {"marcas": [{"marca": "MITSUBISHI", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T12:45:30.4862210+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jenny Angel",
            "fecha_hora_asignacion_asesor": "2024-08-21T12:45:30.4862210+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93501,
            "nombre_asesor_original": "Jenny Angel",
            "id": 91080
        },
        {
            "origen_lead": None,
            "marcas_interes": {"marcas": [{"marca": "MAZDA", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T12:40:30.0967010+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Freddy Cardenas",
            "fecha_hora_asignacion_asesor": "2024-08-21T12:40:30.0967010+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93499,
            "nombre_asesor_original": "Freddy Cardenas",
            "id": 91079
        },
        {
            "origen_lead": None,
            "marcas_interes": {"marcas": [{"marca": "HYUNDAI", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T12:40:28.9817990+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Freddy Cardenas",
            "fecha_hora_asignacion_asesor": "2024-08-21T12:40:28.9817990+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93498,
            "nombre_asesor_original": "Freddy Cardenas",
            "id": 91078
        },
        {
            "origen_lead": None,
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T12:10:43.2186310+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Freddy Cardenas",
            "fecha_hora_asignacion_asesor": "2024-08-21T12:10:43.2186310+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93497,
            "nombre_asesor_original": "Freddy Cardenas",
            "id": 91077
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T12:10:07.3970620+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jenny Angel",
            "fecha_hora_asignacion_asesor": "2024-08-21T12:10:07.3970620+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93496,
            "nombre_asesor_original": "Jenny Angel",
            "id": 91076
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T12:09:36.5430000+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Freddy Cardenas",
            "fecha_hora_asignacion_asesor": "2024-08-21T12:09:36.5430000+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93495,
            "nombre_asesor_original": "Freddy Cardenas",
            "id": 91075
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T12:09:11.1775030+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Freddy Cardenas",
            "fecha_hora_asignacion_asesor": "2024-08-21T12:09:11.1775030+00:00",
            "nombre_anfitrion": "DanielSanchez",
            "prospecto_id": 93494,
            "nombre_asesor_original": "Freddy Cardenas",
            "id": 91074
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{"marca": "CITROEN", "modelo": "", "color": "", "marca_comentario": None, "codigo": "", "precio": ""}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T11:14:39.2169900+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Maryluz Anzola",
            "fecha_hora_asignacion_asesor": "2024-08-21T11:14:39.2169900+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93492,
            "nombre_asesor_original": "Maryluz Anzola",
            "id": 91073
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T11:13:20.2375830+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jefferson Naranjo",
            "fecha_hora_asignacion_asesor": "2024-08-21T11:13:20.2375830+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93493,
            "nombre_asesor_original": "Jefferson Naranjo",
            "id": 91072
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T11:13:19.0283970+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jefferson Naranjo",
            "fecha_hora_asignacion_asesor": "2024-08-21T11:13:19.0283970+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93490,
            "nombre_asesor_original": "Jefferson Naranjo",
            "id": 91071
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T11:05:26.9873440+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Maryluz Anzola",
            "fecha_hora_asignacion_asesor": "2024-08-21T11:05:26.9873440+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93489,
            "nombre_asesor_original": "Maryluz Anzola",
            "id": 91070
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{'marca': 'HYUNDAI', 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T11:02:36.0444440+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Oscar Lopez",
            "fecha_hora_asignacion_asesor": "2024-08-21T11:02:36.0444440+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93488,
            "nombre_asesor_original": "Oscar Lopez",
            "id": 91069
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{'marca': 'MAZDA', 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T10:57:55.8030010+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jenny Angel",
            "fecha_hora_asignacion_asesor": "2024-08-21T10:57:55.8030010+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93487,
            "nombre_asesor_original": "Jenny Angel",
            "id": 91068
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{'marca': 'CHEVROLET', 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T10:57:54.1934450+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jenny Angel",
            "fecha_hora_asignacion_asesor": "2024-08-21T10:57:54.1934450+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93486,
            "nombre_asesor_original": "Jenny Angel",
            "id": 91067
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T10:55:53.6876520+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jefferson Naranjo",
            "fecha_hora_asignacion_asesor": "2024-08-21T10:55:53.6876520+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93485,
            "nombre_asesor_original": "Jefferson Naranjo",
            "id": 91066
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": []},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T10:55:51.9632850+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jefferson Naranjo",
            "fecha_hora_asignacion_asesor": "2024-08-21T10:55:51.9632850+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93484,
            "nombre_asesor_original": "Jefferson Naranjo",
            "id": 91065
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{'marca': 'SUZUKI', 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T10:15:42.1724650+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Jefferson Naranjo",
            "fecha_hora_asignacion_asesor": "2024-08-21T10:15:42.1724650+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93483,
            "nombre_asesor_original": "Jefferson Naranjo",
            "id": 91064
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{'marca': 'MAZDA', 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]},
            "forma_pago": None,
            "sala": "127",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T10:10:20.9285950+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Morelia tobar",
            "fecha_hora_asignacion_asesor": "2024-08-21T10:10:20.9285950+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93482,
            "nombre_asesor_original": "Morelia tobar",
            "id": 91063
        },
        {
            "origen_lead": "",
            "marcas_interes": {"marcas": [{'marca': 'HYUNDAI', 'modelo': '', 'color': '', 'marca_comentario': None, 'codigo': '', 'precio': ''}]},
            "forma_pago": None,
            "sala": "Morato",
            "etapa": "No contactado",
            "respuesta": "Sin contactar",
            "fecha_hora_reasignacion": None,
            "fecha_hora_accion_siguiente": None,
            "estado": "No contactado",
            "status": "Frío",
            "fecha_apertura": "2024-08-21T09:41:58.5984700+00:00",
            "fecha_cierre": None,
            "fecha_cambio_de_etapa": None,
            "tiempo_cambio_de_etapa": None,
            "fecha_ultima_accion": None,
            "fecha_primer_contacto": None,
            "tiempo_primer_contacto": None,
            "fecha_contacto_asesor": None,
            "fecha_cita": None,
            "fecha_aprobacion_credito": None,
            "fecha_recepcion_documentos": None,
            "fecha_aprobacion_documentos": None,
            "activo": 1,
            "interes": "Venta",
            "estado_llamada_verificacion": None,
            "tipo_solicitud_verificacion": None,
            "plazo_pago": None,
            "comentario": None,
            "campania": None,
            "tipo_documento": None,
            "documento": None,
            "test_drive": None,
            "nombre_asesor": "Maryluz Anzola",
            "fecha_hora_asignacion_asesor": "2024-08-21T09:41:58.5984700+00:00",
            "nombre_anfitrion": "CristianGuzman",
            "prospecto_id": 93481,
            "nombre_asesor_original": "Maryluz Anzola",
            "id": 91062
        }
    ]

    for i in dictrionary:
        dt = datetime.fromisoformat(i["fecha_apertura"])

        # Extraer la fecha y la hora por separado
        date = dt.date()
        time = dt.time()

        lead = Lead.objects.create(
            prospecto=Prospecto.objects.get(id=i["prospecto_id"]),
            marcas_interes=i["marcas_interes"],
            sala=i["sala"],
            etapa="No contactado",
            respuesta="Sin contactar",
            estado="No contactado",
            status="Frío",
            interes="Venta",
            activo=True,
            fecha_apertura=i["fecha_apertura"],
            comentario=i["comentario"],
            test_drive=False,
            nombre_asesor=i["nombre_asesor"],
            nombre_asesor_original=i["nombre_asesor"],
            fecha_hora_asignacion_asesor=i["fecha_hora_asignacion_asesor"],
            nombre_anfitrion=i["nombre_anfitrion"],
        )

        Historial.objects.create(
            fecha=date,
            responsable=i["nombre_anfitrion"],
            operacion="Creación Lead",
            comentarios=i["comentario"],
            lead=lead,
            hora=time
        )

        try:
            marca = i["marcas_interes"]["marcas"][0]["marca"]

            VehiculosInteresLead.objects.create(
                lead=lead,
                marca=marca,
                peritaje=False,
                cotizar=False,
                aprobacion=False,
                precio=None,
                separado=False,
                facturado=False,
                mostrado=True,
                fecha=date,
            )
        except:
            pass
