# Django
from django.contrib.auth.models import User
from django.db import models

# Utilities
from datetime import date, datetime, timedelta

class Catalogo(models.Model):
    # Modelo del Catalogo

    descripcion = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)

    def __str__(self):
        # Retorna la descripcion
        return self.descripcion
    class Meta:
        verbose_name_plural = "Catalogos"

class CatalogoModelo(models.Model):
    # Modelo del CatalogoModelo

    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)

    def __str__(self):
        # Retorna el nombre
        return self.nombre
    class Meta:
        verbose_name_plural = "CatalogoModelo"


class CatalogoEmpleados(models.Model):
    # Modelo del Catalogo Empleados

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    sala = models.CharField(max_length=50)
    puesto = models.CharField(max_length=50)
    division = models.CharField(max_length=50, null=True)
    correo = models.CharField(max_length=100, null=True)

    def __str__(self):
        # Retorna el nombre
        return self.nombre
    class Meta:
        verbose_name_plural = "Catalogo Empleados"

class CatalogoRespuestasByEtapa(models.Model):
    # Modelo del Catalogo Respuestas By Etapa

    respuesta = models.CharField(max_length=50)
    etapa_choices = (("No contactado", "No contactado"),
                     ("Interaccion", "Interaccion"),
                     ("Oportunidad", "Oportunidad"),
                     ("Pedido", "Pedido"),
                     ("Desistido", "Desistido"))
    etapa = models.CharField(max_length=50, choices=etapa_choices)
    estado = models.CharField(max_length=50, null=True, blank=True)
    tipos_choices = (("normal", "normal"),
                     ("compra", "compra"),
                     ("peritaje", "peritaje"))
    tipo = models.CharField(max_length=50, choices=tipos_choices, null=True, blank=True)

    def __str__(self):
        # Retorna la respuesta
        return self.respuesta
    class Meta:
        verbose_name_plural = "Catalogo Respuestas By Etapa"

class CatalogoStockVehiculos(models.Model):
    # Modelo del Catalogo Stock Vehiculos

    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)

    def __str__(self):
        # Retorna la respuesta
        return f"{self.modelo} " + f"{self.marca}"
    class Meta:
        verbose_name_plural = "Catalogo Stock Vehiculos"

class Compra(models.Model):
    # Modelo de la Compra

    prospecto = models.ForeignKey("Prospecto", on_delete=models.CASCADE)
    fecha_apertura = models.DateField()
    origen_lead = models.CharField(max_length=50)
    nombre_comprador = models.CharField(max_length=100, null=True)
    fecha_hora_asignacion_comprador = models.DateTimeField(null=True)
    nombre_anfitrion = models.CharField(max_length=100, null=True)
    etapa = models.CharField(max_length=100)
    respuesta = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fecha_ultimaaccion = models.DateField(null=True)
    fecha_hora_accionsiguiente = models.DateTimeField(null=True)
    tipo_interes = models.CharField(max_length=100, null=True)
    comentario_apertura = models.CharField(max_length=2000, null=True)
    compania = models.CharField(max_length=100, null=True)
    tipo_documento = models.CharField(max_length=60, null=True)
    documento = models.CharField(max_length=60, null=True)
    marca = models.CharField(max_length=50, null=True)
    modelo = models.CharField(max_length=50, null=True)
    anio = models.CharField(max_length=50, null=True)
    version = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)
    kilometraje = models.CharField(max_length=50, null=True)
    cilindraje = models.CharField(max_length=50, null=True)
    unique_owner = models.CharField(max_length=2, null=True)
    caja = models.CharField(max_length=50, null=True)
    placa = models.CharField(max_length=7, null=True)
    ciudad_placa = models.CharField(max_length=100, null=True)
    peritaje_lugar_cita = models.CharField(max_length=50, null=True)
    peritaje_fecha_hora_cita = models.DateTimeField(null=True)
    peritaje_direccion_cita = models.CharField(max_length=100, null=True)
    peritaje_ciudad_cita = models.CharField(max_length=50, null=True)
    oferta_madiautos = models.FloatField(null=True)
    oferta_revista = models.FloatField(null=True)
    pretension_cliente = models.FloatField(null=True)
    estado_vehiculo = models.CharField(max_length=100, null=True)
    reclamacion_siniestros = models.CharField(max_length=100, null=True)
    observacion_vehiculo = models.CharField(max_length=100, null=True)
    peritaje_correo = models.CharField(max_length=100, null=True)
    peritaje_carroceria = models.CharField(max_length=50, null=True)
    peritaje_combustible = models.CharField(max_length=50, null=True)
    fecha_primer_contacto = models.DateField(null=True)
    fecha_peritaje = models.DateField(null=True)
    fecha_cierre = models.DateField(null=True)
    status = models.CharField(max_length=50, null=True)
    forma_pago = models.CharField(max_length=50, null=True)
    activo = models.BooleanField(null=True)
    concretada = models.BooleanField(null=True)
    valor_final = models.FloatField(null=True)
    

    def __str__(self):
        # Retorna el id
        return self.id
    class Meta:
        verbose_name_plural = "Compras"

class Historial(models.Model):
    # Modelo del Historial
    lead = models.ForeignKey("Lead", on_delete=models.CASCADE)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True)
    responsable = models.CharField(max_length=100, null=True)
    operacion = models.CharField(max_length=3000, null=True)
    comentarios = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"
    class Meta:
        verbose_name_plural = "Historial"

class HistorialCompleto(models.Model):
    # Modelo del Historial Completo

    ingreso = models.DateTimeField(null=True)
    respuesta = models.CharField(max_length=255, null=True)
    etapa = models.CharField(max_length=255, null=True)
    origen = models.CharField(max_length=255, null=True)
    nombres = models.CharField(max_length=255, null=True)
    apellidos = models.CharField(max_length=255, null=True)
    anfitrion = models.CharField(max_length=255, null=True)
    sala = models.CharField(max_length=255, null=True)
    asesor = models.CharField(max_length=255, null=True)
    telefonos = models.CharField(max_length=255, null=True)
    correos = models.CharField(max_length=255, null=True)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"

class HistorialProspectos(models.Model):
    # Modelo del Historial Prospectos

    ingreso = models.DateTimeField(null=True)
    estado = models.CharField(max_length=255, null=True)
    etapa = models.CharField(max_length=255, null=True)
    medio = models.CharField(max_length=255, null=True)
    fuente = models.CharField(max_length=255, null=True)
    nombres = models.CharField(max_length=255, null=True)
    apellidos = models.CharField(max_length=255, null=True)
    tipo_modulo = models.CharField(max_length=255, null=True)
    modulo = models.CharField(max_length=255, null=True)
    actividad = models.CharField(max_length=255, null=True)
    documento = models.CharField(max_length=255, null=True)
    telefonos = models.CharField(max_length=255, null=True)
    correos = models.CharField(max_length=255, null=True)
    ciudad_nacimiento = models.CharField(max_length=255, null=True)
    ciudad_vive = models.CharField(max_length=255, null=True)
    total_gestiones = models.CharField(max_length=255, null=True)
    usuario = models.CharField(max_length=255, null=True)
    vinculos = models.CharField(max_length=255, null=True)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"
    class Meta:
        verbose_name_plural = "HistorialProspectos"

class HistorialVerificaciones(models.Model):
    # Modelo del Historial Verificaciones

    lead = models.ForeignKey("Lead", on_delete=models.CASCADE)
    estado_llamada = models.CharField(max_length=50, null=True)
    tipo_solicitud = models.CharField(max_length=50, null=True)
    responsable = models.CharField(max_length=50, null=True)
    reasignado = models.CharField(max_length=50, null=True, blank=True)
    observaciones = models.CharField(max_length=50, null=True)
    fecha_hora_verificacion = models.DateTimeField()
    responsable_original_lead = models.CharField(max_length=50, null=True, blank=True)
    tipos_choices = (("venta", "venta"),
                     ("compra", "compra"),
                     ("peritaje", "peritaje"))
    tipo = models.CharField(max_length=50, choices=tipos_choices, null=True, blank=True)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"
    class Meta:
        verbose_name_plural = "HistorialVerificaciones"

class InteresesDesistidos(models.Model):
    # Modelo de Intereses Desistidos

    id_vehiculo_interes = models.IntegerField()
    comentario = models.CharField(max_length=255)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"
    class Meta:
        verbose_name_plural = "InteresesDesistidos"

class Lead(models.Model):
    # Modelo de Lead

    prospecto = models.ForeignKey("Prospecto", on_delete=models.CASCADE)
    origen_lead = models.CharField(max_length=50)
    marcas_interes = models.CharField(max_length=3000, null=True, blank=True)
    forma_pago = models.CharField(max_length=50, null=True, blank=True)
    sala = models.CharField(max_length=50, null=True)
    etapa = models.CharField(max_length=100, null=True)
    respuesta = models.CharField(max_length=100, null=True)
    fecha_hora_reasignacion = models.DateTimeField(null=True, blank=True)
    fecha_hora_accion_siguiente = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    fecha_apertura = models.DateTimeField(null=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    fecha_cambio_de_etapa = models.DateTimeField(null=True, blank=True)
    tiempo_cambio_de_etapa = models.IntegerField(null=True, blank=True)
    fecha_ultima_accion = models.DateField(null=True, blank=True)
    fecha_primer_contacto = models.DateTimeField(null=True, blank=True)
    tiempo_primer_contacto = models.IntegerField(null=True, blank=True)
    fecha_contacto_asesor = models.DateTimeField(null=True, blank=True)
    fecha_cita = models.DateField(null=True, blank=True)
    fecha_aprobacion_credito = models.DateField(null=True, blank=True)
    fecha_recepcion_documentos = models.DateField(null=True, blank=True)
    fecha_aprobacion_documentos = models.DateField(null=True, blank=True)
    activo = models.BooleanField()
    interes = models.CharField(max_length=50, null=True)
    estado_llamada_verificacion = models.CharField(max_length=100, null=True, blank=True)
    tipo_solicitud_verificacion = models.CharField(max_length=100, null=True, blank=True)
    plazo_pago = models.CharField(max_length=100, null=True, blank=True)
    comentario = models.CharField(max_length=2000, null=True, blank=True)
    campania = models.CharField(max_length=100, null=True)
    tipo_documento = models.CharField(max_length=60, null=True)
    documento = models.CharField(max_length=60, null=True)
    test_drive = models.BooleanField()
    nombre_asesor = models.CharField(max_length=100, null=True)
    nombre_asesor_original = models.CharField(max_length=100, null=True)
    fecha_hora_asignacion_asesor = models.DateTimeField(null=True)
    nombre_anfitrion = models.CharField(max_length=100, null=True)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"

class LeadPeritaje(models.Model):
    # Modelo de Lead Peritaje

    c_nombre = models.CharField(max_length=50)
    c_primer_apellido = models.CharField(max_length=50)
    c_segundo_apellido = models.CharField(max_length=50)
    c_correo = models.CharField(max_length=200)
    c_tipo_documento = models.CharField(max_length=10)
    c_cedula_nit = models.CharField(max_length=50)
    c_numero_telefonico = models.CharField(max_length=13)
    l_etapa = models.CharField(max_length=50)
    l_respuesta = models.CharField(max_length=50)
    l_estado = models.CharField(max_length=50)
    l_nombre_asesor = models.CharField(max_length=100)
    l_vitrina_sala = models.CharField(max_length=50)
    v_marca = models.CharField(max_length=50)
    v_linea = models.CharField(max_length=50)
    v_caja = models.CharField(max_length=50)
    v_placa = models.CharField(max_length=50)
    v_ciudad_placa = models.CharField(max_length=50)
    v_modelo = models.CharField(max_length=50)
    v_kilometraje = models.CharField(max_length=50)
    v_color = models.CharField(max_length=50)
    v_lugar_mto = models.CharField(max_length=500)
    v_reclamaciones_siniestros = models.BooleanField()
    v_peritaje_anterior = models.BooleanField()
    v_valor_revista_motor = models.FloatField()
    v_valor_esperado_cliente = models.FloatField()
    v_valor_aproximado = models.FloatField()
    activa = models.BooleanField()
    fecha_cierre = models.DateField(null=True)
    l_nombre_perito = models.CharField(max_length=50, null=True)
    l_origen_lead = models.CharField(max_length=50)
    l_comentario_inicial = models.CharField(max_length=500, null=True)
    p_version_formato = models.IntegerField(null=True)
    p_fecha_hora = models.DateTimeField(null=True)
    
    def __str__(self):
        # Retorna el id
        return f"{self.id}"
    class Meta:
        verbose_name_plural = "LeadsPeritaje"

class Log(models.Model):
    # Modelo de Log

    id_lead_o_compra = models.IntegerField()
    fecha = models.DateField()
    hora = models.TimeField()
    responsable = models.CharField(max_length=100)
    operacion_realizada = models.CharField(max_length=100, null=True)
    comentarios = models.CharField(max_length=2000, null=True)
    tipos_choices = (("normal", "normal"),
                     ("compra", "compra"),
                     ("peritaje", "peritaje"))
    tipo = models.CharField(max_length=50, choices=tipos_choices)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"
    class Meta:
        verbose_name_plural = "Logs"


class Prospecto(models.Model):
    # Modelo del Prospecto

    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    celular = models.CharField(max_length=15, null=True, blank=True)
    correo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    ciudad = models.CharField(max_length=50, null=True, blank=True)
    departamento = models.CharField(max_length=50, null=True, blank=True)
    localidad = models.CharField(max_length=50, null=True, blank=True)
    profesion = models.CharField(max_length=100, null=True, blank=True)
    ingresos = models.CharField(max_length=50, null=True, blank=True)
    vehiculo_actual = models.CharField(max_length=100, null=True, blank=True)
    interes_deporte = models.CharField(max_length=50, null=True, blank=True)
    interes_mascotas = models.CharField(max_length=50, null=True, blank=True)
    contacto_nombre = models.CharField(max_length=50, null=True, blank=True)
    contacto_telefono = models.CharField(max_length=50, null=True, blank=True)
    fecha_captura = models.DateTimeField()
    nombre_asesor = models.CharField(max_length=100, null=True)
    correo_asesor = models.CharField(max_length=100, null=True, blank=True)
    anfitrion = models.CharField(max_length=50)
    fecha_hora_asignacion_asesor = models.DateTimeField(null=True, blank=True)
    cliente = models.BooleanField(null=True)
    politica_privacidad = models.BooleanField()

    def __str__(self):
        # Retorna el nombre
        return f"{self.nombre}"


class Retomas(models.Model):
    # Modelo del Retomas

    lead = models.ForeignKey("Lead", on_delete=models.CASCADE)
    modelo = models.CharField(max_length=500)
    valor = models.FloatField()
    total = models.FloatField()
    total_restante = models.FloatField()

    def __str__(self):
        # Retorna el id
        return str(self.id)
    class Meta:
        verbose_name_plural = "Retomas"

class VehiculosInteresLead(models.Model):
    # Modelo del VehiculoInteresLead

    lead = models.ForeignKey("Lead", on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    comentario = models.CharField(max_length=2000, null=True, blank=True)
    peritaje = models.BooleanField(null=True)
    cotizar = models.BooleanField()
    aprobacion = models.BooleanField()
    fecha = models.DateField(null=True, blank=True)
    precio = models.FloatField(null=True)
    codigo_vehiculo = models.CharField(max_length=50, null=True)
    separado = models.BooleanField(null=True)
    facturado = models.BooleanField(null=True)
    mostrado = models.BooleanField(null=True)

    def __str__(self):
        # Retorna el nombre
        return f"{self.id}" + f"{self.lead}"
    class Meta:
        verbose_name_plural = "VehiculosInteresLeads"
        
class Usados2021(models.Model):
    # Modelo de Usados2021

    mes = models.CharField(max_length=255, null=True)
    origen = models.CharField(max_length=255, null=True)
    reclasificacion_origen_anfitrion_digital = models.DateTimeField()
    fecha = models.DateTimeField()
    hora_militar = models.DateTimeField()
    recibida_por = models.CharField(max_length=255, null=True)
    nombre_de_cliente = models.CharField(max_length=255, null=True)
    celular = models.CharField(max_length=15, null=True)
    correo = models.CharField(max_length=255, null=True)
    interesado_en = models.CharField(max_length=255, null=True)
    referencia = models.CharField(max_length=255, null=True)
    enviado_a = models.CharField(max_length=255, null=True)
    asesor_asignado = models.CharField(max_length=255, null=True)
    hora_correo = models.DateTimeField()
    observaciones = models.CharField(max_length=255, null=True)
    fecha_verificacion = models.DateTimeField()
    estatus = models.CharField(max_length=255, null=True)
    verificado_por = models.CharField(max_length=255, null=True)
    observaciones_1 = models.CharField(max_length=255, null=True)
    f20 = models.CharField(max_length=255, null=True)
    def __str__(self):
        # Retorna el id
        return f"{self.id}"
    class Meta:
        verbose_name_plural = "Usados2021"

class Usados19_22(models.Model):
    # Modelo de Usados19_22

    mes = models.CharField(max_length=255, null=True)
    origen = models.CharField(max_length=255, null=True)
    fecha = models.DateTimeField()
    hora_militar = models.DateTimeField()
    recibida_por = models.CharField(max_length=255, null=True)
    nombre_de_cliente = models.CharField(max_length=255, null=True)
    celular = models.CharField(max_length=15, null=True)
    correo = models.CharField(max_length=255, null=True)
    interesado_en = models.CharField(max_length=255, null=True)
    referencia = models.CharField(max_length=255, null=True)
    enviado_a = models.CharField(max_length=255, null=True)
    asesor_asignado = models.CharField(max_length=255, null=True)
    hora_correo = models.DateTimeField()
    observaciones = models.CharField(max_length=255, null=True)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"

class Asesor(models.Model):
    # Modelo de Asesores

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=255, null=True)
    sala = models.CharField(max_length=255, null=True)
    habilitado = models.BooleanField(default=True, null=True)

    def __str__(self):
        # Retorna el id
        return f"{self.nombre}"
    class Meta:
        verbose_name_plural = "Asesores"

class Evento(models.Model):
    # Modelo de Eventos

    nombre = models.CharField(max_length=255, null=True)
    lead = models.ForeignKey("Lead", on_delete=models.CASCADE)
    choices_tipo = (("Testdrive", "Testdrive"),
                     ("Peritaje", "Peritaje"),
                     ("Whatsapp", "Whatsapp"),
                     ("Llamada", "Llamada"),
                     ("Cita Vitrina", "Cita Vitrina"))
    tipo = models.CharField(max_length=255, null=True, choices=choices_tipo)
    cliente = models.CharField(max_length=255, null=True)
    telefono_cliente = models.CharField(max_length=255, null=True)
    observaciones = models.CharField(max_length=255)
    asesor = models.ForeignKey("Asesor", on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    tiempo_evento = models.CharField(max_length=255, null=True)
    cumplido = models.BooleanField(null=True, default=False)
    fecha_hora_cumplido = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        # Retorna el id
        return f"{self.id}"

"""p_codigo = models.CharField(max_length=50)
    p_fh = models.CharField(max_length=50)
    p_perito = models.CharField(max_length=50)
    p_transmision = models.CharField(max_length=50)
    p_motor_rubio = models.CharField(max_length=50)
    p_motor_lodo = models.CharField(max_length=50)
    p_motor_fuga_carter = models.CharField(max_length=50)
    p_motor_fuga_tapa_valvulas = models.CharField(max_length=50)
    p_motor_soportes = models.CharField(max_length=50)
    p_motor_fuga_retenedores = models.CharField(max_length=50)
    p_motor_cambiar_aceite = models.CharField(max_length=50)
    p_suspension_delantera = models.CharField(max_length=50)
    p_suspension_trasera = models.CharField(max_length=50)
    p_direccion_tipo_direccion = models.CharField(max_length=50)
    p_direccion_columna = models.CharField(max_length=50)
    p_direccion_fugas = models.CharField(max_length=50)
    p_direccion_bomba = models.CharField(max_length=50)
    p_direccion_alineacion = models.CharField(max_length=50)
    p_direccion_caja = models.CharField(max_length=50)
    p_interior_tapiceria = models.CharField(max_length=50)
    p_interior_timon = models.CharField(max_length=50)
    p_interior_millare = models.CharField(max_length=50)
    p_interior_alfombra_piso = models.CharField(max_length=50)
    p_interior_radio = models.CharField(max_length=50)
    p_interior_manijas = models.CharField(max_length=50)
    p_interior_parasol = models.CharField(max_length=50)
    p_interior_pito = models.CharField(max_length=50)
    p_interior_tarjeta_sd = models.CharField(max_length=50)
    p_interior_asientos = models.CharField(max_length=50)
    p_interior_cinturones = models.CharField(max_length=50)
    p_interior_mandos = models.CharField(max_length=50)
    p_interior_tablero = models.CharField(max_length=50)
    p_interior_pal_selector = models.CharField(max_length=50)
    p_interior_sun_roof = models.CharField(max_length=50)
    p_aire_acondicionado_aplica = models.CharField(max_length=50)
    p_aire_acondicionado_rejillas = models.CharField(max_length=50)"""



"""v_carroceria = models.CharField(max_length=50)
    v_cilindraje = models.CharField(max_length=50)
    v_transmision = models.CharField(max_length=50)
    v_motor_ruido = models.CharField(max_length=50)
    v_motor_lodo = models.CharField(max_length=50)
    v_motor_fuga_carter = models.CharField(max_length=50)
    v_motor_fuga_tapa_valvulas = models.CharField(max_length=50)
    v_motor_soportes = models.CharField(max_length=50)
    v_motor_fuga_retenedores = models.CharField(max_length=50)
    v_motor_cambiar_aceite = models.CharField(max_length=50)
    v_suspension_delantera = models.CharField(max_length=50)
    v_suspension_trasera = models.CharField(max_length=50)
    v_direccion_tipo_direccion = models.CharField(max_length=50)
    v_direccion_columna = models.CharField(max_length=50)
    v_direccion_fugas = models.CharField(max_length=50)
    v_direccion_bomba = models.CharField(max_length=50)
    v_direccion_alineacion = models.CharField(max_length=50)
    v_direccion_caja = models.CharField(max_length=50)
    v_interior_tapiceria = models.CharField(max_length=50)"""
    