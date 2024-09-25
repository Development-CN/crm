from django.db import models


class RevisionesAPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lista_revisiones"


class ListaItemsAPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    orden = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    familia = models.CharField(max_length=250, blank=True, null=True)
    multipuntos = models.BooleanField(blank=True, null=True)
    pagina = models.IntegerField(blank=True, null=True)
    revision = models.ForeignKey(RevisionesAPI, null=True, on_delete=models.SET_NULL)
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


class ItemsAPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_hd = models.BigIntegerField(blank=True, null=True)
    no_orden = models.CharField(max_length=25, blank=True, null=True)
    item = models.ForeignKey(ListaItemsAPI, null=True, on_delete=models.SET_NULL)
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


class EntrevistaProfesionalAPI(models.Model):
    id_hd = models.BigIntegerField(blank=True, null=True)
    no_cita = models.BigIntegerField(blank=True, null=True)
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
        managed = False
        db_table = "entrevista_profesional"


class TiposRefaccionesAPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lista_tipos_refacciones"


class RefaccionesAPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_hd = models.BigIntegerField(blank=True, null=True)
    no_orden = models.CharField(max_length=50, blank=True, null=True)
    item = models.ForeignKey(ItemsAPI, null=True, on_delete=models.SET_NULL)
    nombre = models.CharField(max_length=250, blank=True, null=True)
    no_parte = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    porcentaje_descuento = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    subtotal_iva = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    existencia = models.CharField(max_length=10, blank=True, null=True)
    localizacion = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.ForeignKey(TiposRefaccionesAPI, null=True, on_delete=models.SET_NULL)
    fecha_hora_fin = models.DateTimeField(auto_now_add=True)
    fecha_hora_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "actividades_refacciones"


class TiposCargosAPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "lista_tipos_cargos"


class ManoDeObraAPI(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_hd = models.BigIntegerField(blank=True, null=True)
    no_orden = models.CharField(max_length=50, blank=True, null=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    item = models.ForeignKey(ItemsAPI, null=True, on_delete=models.SET_NULL)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    cantidad_uts = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    precio_ut = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    porcentaje_descuento = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    subtotal_iva = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    cargo = models.ForeignKey(TiposCargosAPI, null=True, on_delete=models.SET_NULL)
    fecha_hora_fin = models.DateTimeField(auto_now_add=True)
    fecha_hora_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "actividades_mano_de_obra"
