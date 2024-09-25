from django.db import models


class TrackerProActividadesCitas(models.Model):
    id = models.BigAutoField(primary_key=True)
    no_cita = models.BigIntegerField()
    id_tecnico = models.CharField(max_length=50, null=True, blank=True)
    id_asesor = models.CharField(max_length=50, null=True, blank=True)

    fecha_cita = models.DateField()
    no_placas = models.CharField(max_length=50)
    cliente = models.CharField(max_length=300)
    correo = models.CharField(max_length=300)
    modelo_vehiculo = models.CharField(max_length=100, null=True, blank=True)
    color_vehiculo = models.CharField(max_length=50, null=True, blank=True)
    tiempo = models.IntegerField()
    hora_rampa = models.TimeField()
    year_vehiculo = models.IntegerField()
    vin = models.CharField(max_length=50)
    servicio = models.CharField(max_length=300)
    telefono = models.CharField(max_length=50)
    hora_cita = models.TimeField()

    fecha_hora_fin = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fecha_hora_actualizacion = models.DateTimeField(auto_now=True, null=True, blank=True)

    status = models.CharField(max_length=50, null=True, blank=True)
    whatsapp = models.BooleanField(default=False)

    kilometraje = models.BigIntegerField(null=True, blank=True)
    id_hd = models.BigIntegerField(null=True, blank=True)
    id_estado = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "actividades_citas"


class TrackerProActividadesCitasServicios(models.Model):
    id = models.BigAutoField(primary_key=True)
    no_cita = models.BigIntegerField(blank=True, null=True)
    id_servicio = models.BigIntegerField(blank=True, null=True)
    servicio = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "actividades_citas_servicios"


class TrackerProListaItemsServicios(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_servicio = models.BigIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    familia = models.BigIntegerField(blank=True, null=True)
    orden = models.BigIntegerField(blank=True, null=True)
    costo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.descripcion)

    class Meta:
        managed = False
        db_table = "lista_items_servicios"
        verbose_name = "Lista de servicios"
        verbose_name_plural = "Lista de servicios"


class VTracker(models.Model):
    no_orden = models.CharField(max_length=25, blank=True, null=False, primary_key=True)
    placas = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    tecnico = models.CharField(max_length=60, blank=True, null=True)
    asesor = models.CharField(max_length=150, blank=True, null=True)
    vehiculo = models.CharField(max_length=250, blank=True, null=True)
    hora_llegada = models.DateTimeField(blank=True, null=True)
    hora_inicio_asesor = models.DateTimeField(blank=True, null=True)
    hora_fin_asesor = models.DateTimeField(blank=True, null=True)
    hora_promesa = models.DateTimeField(blank=True, null=True)
    hora_grabado = models.CharField(max_length=5, blank=True, null=True)
    inicio_tecnico = models.DateTimeField(blank=True, null=True)
    fin_tecnico = models.DateTimeField(blank=True, null=True)
    detenido = models.CharField(max_length=5)
    servicio_capturado = models.CharField(max_length=500, blank=True, null=True)
    inicio_tecnico_lavado = models.DateTimeField(blank=True, null=True)
    fin_tecnico_lavado = models.DateTimeField(blank=True, null=True)
    ultima_actualizacion = models.IntegerField(blank=True, null=True)
    motivo_paro = models.CharField(max_length=22, blank=True, null=True)
    id_hd = models.CharField(max_length=25, blank=False, null=False)
    telefono_agencia = models.CharField(max_length=25, blank=False, null=False)

    def __str__(self):
        return "Orden: " + str(self.no_orden) + " | Fecha: " + str(self.fecha)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "v_tracker"
        verbose_name = "Ordenes con tracker"
        verbose_name_plural = "Ordenes con tracker"


class ListaItemsFamiliasPreinventario(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "lista_items_familias_preinventario"


class ListaItemsPrediagnostico(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    familia = models.CharField(max_length=50, blank=True, null=True)
    orden = models.BigIntegerField(blank=True, null=True)
    comentarios = models.BooleanField(blank=True, null=True)
    evidencia = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "lista_items_prediagnostico"


class ListaItemsFamiliasPrediagnostico(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "lista_items_familias_prediagnostico"


class StatusCita(models.Model):
    id = models.BigAutoField(primary_key=True)
    no_cita = models.BigIntegerField(blank=True, null=True)
    fecha_hora_fin_cita = models.DateTimeField(blank=True, null=True)
    fecha_hora_confirmacion_cita = models.DateTimeField(blank=True, null=True)
    fecha_hora_fin_preinventario = models.DateTimeField(blank=True, null=True)
    fecha_hora_fin_prediagnostico = models.DateTimeField(blank=True, null=True)
    fecha_hora_fin_cancelacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "status_cita"


class EntrevistaProfesional(models.Model):
    no_cita = models.BigIntegerField(blank=True, null=True)
    id_hd = models.BigIntegerField(blank=True, null=True)
    novedad = models.CharField(max_length=200, null=True, blank=True)
    cuando = models.CharField(max_length=200, null=True, blank=True)
    veces = models.CharField(max_length=200, null=True, blank=True)
    donde = models.CharField(max_length=200, null=True, blank=True)
    accesorios_no_homologados = models.CharField(max_length=200, null=True, blank=True)
    testigos = models.JSONField(null=True, blank=True)
    otro_testigo = models.CharField(max_length=200, null=True, blank=True)
    es_evidente_en_recepcion = models.BooleanField(null=True, blank=True)
    requiere_prueba_de_carretera = models.BooleanField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "entrevista_profesional"


class VInformacionCitas(models.Model):
    id_hd = models.AutoField(primary_key=True)
    no_cita = models.CharField(max_length=25)
    no_orden = models.CharField(max_length=25)
    cliente = models.CharField(max_length=200, blank=True, null=True)
    hora_llegada = models.DateTimeField(blank=True, null=True)
    hora_retiro = models.DateTimeField(blank=True, null=True)
    placas = models.CharField(max_length=10, blank=True, null=True)
    vin = models.CharField(max_length=50, blank=True, null=True)
    vehiculo = models.CharField(max_length=250, blank=True, null=True)
    color = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "v_informacion_citas"


class VInformacionHistorica(models.Model):
    id_hd = models.AutoField(primary_key=True)
    numcita = models.CharField(db_column="NUMCITA", max_length=25)  # Field name made lowercase.
    noorden = models.CharField(db_column="NOORDEN", max_length=25)  # Field name made lowercase.
    fecha = models.DateTimeField()
    horaasesor = models.DateTimeField(db_column="horaAsesor", blank=True, null=True)  # Field name made lowercase.
    idasesor = models.CharField(max_length=10)
    noplacas = models.CharField(
        db_column="noPlacas", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    vin = models.CharField(max_length=50, blank=True, null=True)
    colorprisma = models.CharField(
        db_column="colorPrisma", max_length=25, blank=True, null=True
    )  # Field name made lowercase.
    vehiculo = models.CharField(
        db_column="Vehiculo", max_length=250, blank=True, null=True
    )  # Field name made lowercase.
    color = models.CharField(db_column="Color", max_length=25, blank=True, null=True)  # Field name made lowercase.
    ano = models.IntegerField(db_column="Ano", blank=True, null=True)  # Field name made lowercase.
    cilindros = models.IntegerField(db_column="Cilindros", blank=True, null=True)  # Field name made lowercase.
    kilometraje = models.IntegerField(db_column="Kilometraje", blank=True, null=True)  # Field name made lowercase.
    idcliente = models.CharField(
        db_column="idCliente", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    cliente = models.CharField(db_column="Cliente", max_length=200, blank=True, null=True)  # Field name made lowercase.
    tipocliente = models.CharField(
        db_column="tipoCliente", max_length=25, blank=True, null=True
    )  # Field name made lowercase.
    telefonos = models.CharField(max_length=50, blank=True, null=True)
    contactonombre = models.CharField(
        db_column="ContactoNombre", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    contactotelefono = models.CharField(
        db_column="ContactoTelefono", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    horatolerancia = models.DateTimeField(
        db_column="horaTolerancia", blank=True, null=True
    )  # Field name made lowercase.
    horallegada = models.DateTimeField(db_column="Horallegada", blank=True, null=True)  # Field name made lowercase.
    horairecepcion = models.DateTimeField(
        db_column="HoraIRecepcion", blank=True, null=True
    )  # Field name made lowercase.
    horafrecepcion = models.DateTimeField(
        db_column="HoraFRecepcion", blank=True, null=True
    )  # Field name made lowercase.
    horaientrega = models.DateTimeField(db_column="HoraIEntrega", blank=True, null=True)  # Field name made lowercase.
    horafentrega = models.DateTimeField(db_column="HoraFEntrega", blank=True, null=True)  # Field name made lowercase.
    horaretiro = models.DateTimeField(db_column="HoraRetiro", blank=True, null=True)  # Field name made lowercase.
    horarampa = models.DateTimeField(db_column="horaRampa", blank=True, null=True)  # Field name made lowercase.
    fechahorapromesa = models.DateTimeField(
        db_column="fechaHoraPromesa", blank=True, null=True
    )  # Field name made lowercase.
    status = models.CharField(db_column="Status", max_length=30, blank=True, null=True)  # Field name made lowercase.
    fecha_hora_status = models.DateTimeField(
        db_column="Fecha_hora_Status", blank=True, null=True
    )  # Field name made lowercase.
    idop = models.DecimalField(db_column="idOp", max_digits=18, decimal_places=0)  # Field name made lowercase.
    bahia = models.IntegerField(blank=True, null=True)
    observaciones = models.CharField(
        db_column="OBSERVACIONES", max_length=250, blank=True, null=True
    )  # Field name made lowercase.
    usuario = models.CharField(db_column="USUARIO", max_length=50, blank=True, null=True)  # Field name made lowercase.
    fecha_agendado = models.DateTimeField(
        db_column="FECHA_AGENDADO", blank=True, null=True
    )  # Field name made lowercase.
    fecha_original = models.DateTimeField(
        db_column="FECHA_ORIGINAL", blank=True, null=True
    )  # Field name made lowercase.
    fecha_hora_apertura_os = models.DateTimeField(blank=True, null=True)
    fecha_hora_cierre_os = models.DateTimeField(blank=True, null=True)
    fecha_hora_com = models.DateTimeField(
        db_column="Fecha_hora_com", blank=True, null=True
    )  # Field name made lowercase.
    status_os = models.CharField(
        db_column="Status_OS", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    seriecolorprisma = models.IntegerField(blank=True, null=True)
    testqa = models.DateTimeField(db_column="testQA", blank=True, null=True)  # Field name made lowercase.
    tipolavado = models.CharField(max_length=2, blank=True, null=True)
    comentarioslavado = models.CharField(max_length=250, blank=True, null=True)
    tipollegada = models.CharField(
        db_column="tipoLlegada", max_length=5, blank=True, null=True
    )  # Field name made lowercase.
    tiporetiro = models.CharField(
        db_column="tipoRetiro", max_length=5, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "v_informacion_historica"


# Tablas de otras apps
# Seguimiento en linea


class TrackerProRevisiones(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lista_revisiones"


class TrackerProListaItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    orden = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    familia = models.CharField(max_length=250, blank=True, null=True)
    multipuntos = models.BooleanField(blank=True, null=True)
    pagina = models.IntegerField(blank=True, null=True)
    revision = models.ForeignKey(TrackerProRevisiones, null=True, on_delete=models.SET_NULL)
    g_x = models.IntegerField(blank=True, null=True)
    g_y = models.IntegerField(blank=True, null=True)
    y_x = models.IntegerField(blank=True, null=True)
    y_y = models.IntegerField(blank=True, null=True)
    r_x = models.IntegerField(blank=True, null=True)
    r_y = models.IntegerField(blank=True, null=True)
    modificado_x = models.IntegerField(blank=True, null=True)
    modificado_y = models.IntegerField(blank=True, null=True)
    valor_x = models.IntegerField(blank=True, null=True)
    valor_y = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lista_items_tecnico"


class TrackerProItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_hd = models.BigIntegerField(blank=True, null=True)
    no_orden = models.CharField(max_length=25, blank=True, null=True)
    item = models.ForeignKey(TrackerProListaItems, null=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=25, blank=True, null=True)
    comentarios = models.CharField(max_length=500, blank=True, null=True)
    valor = models.CharField(max_length=50, blank=True, null=True)
    bateria_estado = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    bateria_nivel = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    cambiado = models.BooleanField(default=0)
    tecnico = models.CharField(max_length=50, blank=True, null=True)
    fecha_hora_fin = models.DateTimeField(auto_now_add=True)
    fecha_hora_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "actividades_tecnico"
