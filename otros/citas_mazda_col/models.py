from django.db import models


class ActividadesCitas(models.Model):
    id = models.BigAutoField(primary_key=True)
    no_cita = models.BigIntegerField(null=True, blank=True)
    id_tecnico = models.CharField(max_length=50, null=True, blank=True)
    id_asesor = models.CharField(max_length=50, null=True, blank=True)
    fecha_cita = models.DateField(null=True, blank=True)
    no_placas = models.CharField(max_length=50)
    cliente = models.CharField(max_length=300)
    correo = models.CharField(max_length=300)
    modelo_vehiculo = models.CharField(max_length=100, null=True, blank=True)
    color_vehiculo = models.CharField(max_length=50, null=True, blank=True)
    tiempo = models.IntegerField(null=True, blank=True)
    hora_rampa = models.TimeField(null=True, blank=True)
    year_vehiculo = models.IntegerField(null=True, blank=True)
    vin = models.CharField(max_length=50)
    servicio = models.CharField(max_length=300)
    observaciones = models.CharField(max_length=500, blank=True, null=True)
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
        managed = True
        db_table = "actividades_citas"


class ActividadesCitasServicios(models.Model):
    id = models.BigAutoField(primary_key=True)
    no_cita = models.BigIntegerField(blank=True, null=True)
    id_servicio = models.BigIntegerField(blank=True, null=True)
    servicio = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "actividades_citas_servicios"


class ListaItemsModelos(models.Model):
    id_modelo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.nombre).title()

    class Meta:
        managed = True
        db_table = "lista_items_modelos"
        verbose_name = "Lista de modelos"
        verbose_name_plural = "Lista de modelos"


class ListaItemsYears(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        managed = True
        db_table = "lista_items_years"
        verbose_name = "Lista de años"
        verbose_name_plural = "Lista de años"


class ListaItemsFamiliasServicios(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.nombre) + " " + str(self.descripcion)

    class Meta:
        managed = True
        db_table = "lista_items_familias_servicios"
        verbose_name = "Lista de familias de servicios"
        verbose_name_plural = "Lista de familias de servicios"


class ListaItemsServicios(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_servicio = models.BigIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    familia = models.BigIntegerField(blank=True, null=True)
    orden = models.BigIntegerField(blank=True, null=True)
    costo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    express = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.descripcion)

    class Meta:
        managed = True
        db_table = "lista_items_servicios"
        verbose_name = "Lista de servicios"
        verbose_name_plural = "Lista de servicios"


class ListaItemsServiciosCostos(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_servicio = models.BigIntegerField(blank=True, null=True)
    id_modelo = models.BigIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    porcentaje_descuento = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Servicio: " + str(self.id_servicio) + " | Modelo: " + str(self.id_modelo)

    class Meta:
        managed = True
        db_table = "lista_items_servicios_costos"
        verbose_name = "Lista de costos de servicios"
        verbose_name_plural = "Lista de costos de servicios"


# VISTAS PROVENIENTES DE SSL
class VCitasTecnicos(models.Model):
    id_empleado = models.CharField(db_column="ID_EMPLEADO", max_length=10, primary_key=True)
    id_tipo_empleado = models.CharField(db_column="ID_TIPO_EMPLEADO", max_length=10, blank=True, null=True)
    nombre_empleado = models.CharField(db_column="NOMBRE_EMPLEADO", max_length=60, blank=True, null=True)
    nivel = models.CharField(db_column="NIVEL", max_length=1, blank=True, null=True)
    bahia = models.IntegerField(db_column="BAHIA", blank=True, null=True)
    express = models.BooleanField(db_column="EXPRESS", blank=True, null=True)
    color_tecnico = models.CharField(db_column="COLOR_TECNICO", max_length=25, blank=True, null=True)
    hora_ent_lv = models.CharField(db_column="HORA_ENT_LV", max_length=5, blank=True, null=True)
    hora_sal_lv = models.CharField(db_column="HORA_SAL_LV", max_length=5, blank=True, null=True)
    hora_comer = models.CharField(db_column="HORA_COMER", max_length=5, blank=True, null=True)
    hora_ent_s = models.CharField(db_column="HORA_ENT_S", max_length=5, blank=True, null=True)
    hora_sal_s = models.CharField(db_column="HORA_SAL_S", max_length=5, blank=True, null=True)
    id_asesor = models.CharField(db_column="ID_ASESOR", max_length=10, blank=True, null=True)
    nombre_asesor = models.CharField(db_column="NOMBRE_ASESOR", max_length=50, blank=True, null=True)
    no_emp_asesor = models.IntegerField(db_column="NO_EMP_ASESOR", blank=True, null=True)
    jefe_taller = models.BooleanField(db_column="JEFE_TALLER", blank=True, null=True)
    hora_ent_d = models.CharField(db_column="HORA_ENT_D", max_length=5, blank=True, null=True)
    hora_sal_d = models.CharField(db_column="HORA_SAL_D", max_length=5, blank=True, null=True)
    hora_comer_s = models.CharField(db_column="HORA_COMER_S", max_length=5, blank=True, null=True)
    hora_comer_d = models.CharField(db_column="HORA_COMER_D", max_length=5, blank=True, null=True)
    id_empleado_bi = models.CharField(db_column="ID_EMPLEADO_BI", max_length=10, blank=True, null=True)
    min_comer_lv = models.IntegerField(db_column="MIN_COMER_LV", blank=True, null=True)
    min_comer_s = models.IntegerField(db_column="MIN_COMER_S", blank=True, null=True)
    min_comer_d = models.IntegerField(db_column="MIN_COMER_D", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "V_tecnicos"


class VCitasUsuarios(models.Model):
    cvegrupo = models.IntegerField(db_column="cveGrupo")
    cveperfil = models.IntegerField(db_column="cvePerfil")
    cveusuario = models.CharField(db_column="cveUsuario", max_length=15)
    pass_field = models.CharField(db_column="Pass", max_length=100)
    nombre = models.CharField(db_column="Nombre", max_length=150, blank=True, null=True)
    correoe = models.CharField(db_column="correoE", max_length=100, blank=True, null=True)
    color = models.CharField(db_column="Color", max_length=50, blank=True, null=True)
    cveasesor = models.CharField(db_column="cveAsesor", max_length=20, blank=True, null=True)
    express = models.BooleanField(db_column="express", blank=True, null=True)
    activo = models.BooleanField(db_column="Activo")

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "v_usuarios"


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
        managed = False
        db_table = "v_informacion_citas"


class TiposDocumentos(models.Model):
    nombre = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "tipos_documentos"


# Tablas de otras apps
# Tracker Pro
class CitasStatusCita(models.Model):
    id = models.BigAutoField(primary_key=True)
    no_cita = models.BigIntegerField(blank=True, null=True)
    fecha_hora_fin_cita = models.DateTimeField(blank=True, null=True)
    fecha_hora_confirmacion_cita = models.DateTimeField(blank=True, null=True)
    fecha_hora_fin_preinventario = models.DateTimeField(blank=True, null=True)
    fecha_hora_fin_prediagnostico = models.DateTimeField(blank=True, null=True)
    fecha_hora_fin_cancelacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "status_cita"


class VCitasActividadesCitasTablero(models.Model):
    id = models.BigIntegerField(primary_key=True)
    no_cita = models.CharField(max_length=50, blank=True, null=True)
    id_asesor = models.CharField(max_length=1)
    fecha_cita = models.DateTimeField(blank=True, null=True)
    no_placas = models.CharField(max_length=10, blank=True, null=True)
    cliente = models.CharField(max_length=200, blank=True, null=True)
    correo = models.CharField(max_length=100, blank=True, null=True)
    modelo_vehiculo = models.CharField(max_length=25, blank=True, null=True)
    color_vehiculo = models.CharField(max_length=1)
    tiempo = models.IntegerField()
    year_vehiculo = models.IntegerField()
    vin = models.CharField(max_length=50, blank=True, null=True)
    servicio = models.CharField(max_length=500, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    hora_cita = models.TimeField(blank=True, null=True)
    kilometraje = models.CharField(max_length=1)
    id_hd = models.CharField(max_length=1)
    id_estado = models.IntegerField()
    id_estrategia = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "v_actividades_citas_tablero"
