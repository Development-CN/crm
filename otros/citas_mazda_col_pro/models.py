from django.db import models


class Appointment(models.Model):
    id = models.BigAutoField(primary_key=True)
    license_plate = models.CharField(max_length=20, null=True, blank=True, verbose_name="Placa")

    car_model = models.ForeignKey("CarModel", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Modelo")
    car_model_year = models.IntegerField(null=True, blank=True, verbose_name="Año")
    car_mileage = models.IntegerField(null=True, blank=True, verbose_name="Kilometraje")

    client_first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre")
    client_last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Apellidos")
    client_document_type = models.ForeignKey(
        "DocumentType", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de documento"
    )
    client_document_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Número de documento")
    client_email = models.EmailField(max_length=250, null=True, blank=True, verbose_name="Correo electrónico")
    client_phone_country_code = models.CharField(max_length=3, null=True, blank=True, verbose_name="Código de país")
    client_phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Número de teléfono")

    service = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Servicio")
    other_services = models.ManyToManyField(
        "Service", blank=True, related_name="other_services", verbose_name="Otros servicios"
    )
    car_condition = models.BooleanField(default=False, null=True, blank=True, verbose_name="Condición del auto")
    additional_service = models.CharField(max_length=250, null=True, blank=True, verbose_name="Servicio adicional")

    waiting_room = models.BooleanField(default=False, null=True, blank=True, verbose_name="Espera")

    appointment_date = models.DateField(null=True, blank=True, verbose_name="Fecha")
    appointment_time = models.TimeField(null=True, blank=True, verbose_name="Hora")
    advisor_id = models.IntegerField(null=True, blank=True, verbose_name="ID del asesor")

    id_hd = models.CharField(max_length=100, null=True, blank=True, verbose_name="ID HD")
    appointment_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Número de cita")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Cita de servicio"
        verbose_name_plural = "Citas de servicio"


class CarModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre")
    year_start = models.IntegerField(null=True, blank=True, verbose_name="Año de inicio")
    year_end = models.IntegerField(null=True, blank=True, verbose_name="Año de fin")
    mechanical_model = models.CharField(max_length=100, null=True, blank=True, verbose_name="Modelo mecánico")
    active = models.BooleanField(default=True, null=True, blank=True, verbose_name="Activo")

    def __str__(self):
        return self.mechanical_model + " - " + self.name

    class Meta:
        verbose_name = "Modelo de auto"
        verbose_name_plural = "Modelos de auto"


class DocumentType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre")
    active = models.BooleanField(default=True, null=True, blank=True, verbose_name="Activo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de documento de identidad"
        verbose_name_plural = "Tipos de documento de identidad"


class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre")
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name="Descripción")
    service_id = models.CharField(max_length=20, null=True, blank=True, verbose_name="ID del servicio")
    order = models.IntegerField(null=True, blank=True, verbose_name="Orden")
    wait = models.BooleanField(default=False, null=True, blank=True, verbose_name="Espera")
    time = models.IntegerField(null=True, blank=True, verbose_name="Tiempo")
    others = models.BooleanField(default=False, null=True, blank=True, verbose_name="Otros")
    active = models.BooleanField(default=True, null=True, blank=True, verbose_name="Activo")

    def __str__(self):
        return self.service_id + " - " + self.name

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"


class ContactCenter(models.Model):
    id = models.BigAutoField(primary_key=True)

    CANCELLATION_REASONS = [(1, "Otro Servicio"), (2, "Novedad/Condición")]

    license_plate = models.CharField(max_length=20, null=True, blank=True, verbose_name="Placa")

    car_model = models.ForeignKey("CarModel", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Modelo")
    car_model_year = models.IntegerField(null=True, blank=True, verbose_name="Año")
    car_mileage = models.IntegerField(null=True, blank=True, verbose_name="Kilometraje")

    client_first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombres")
    client_last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Apellidos")
    client_document_type = models.ForeignKey(
        "DocumentType", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de documento"
    )
    client_document_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Número de documento")
    client_email = models.EmailField(max_length=250, null=True, blank=True, verbose_name="Correo electrónico")
    client_phone_country_code = models.CharField(max_length=3, null=True, blank=True, verbose_name="Código de país")
    client_phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Número de teléfono")

    additional_service = models.CharField(max_length=250, null=True, blank=True, verbose_name="Servicio adicional")

    cancellation_reason = models.IntegerField(
        null=True, blank=True, choices=CANCELLATION_REASONS, verbose_name="Razón de cancelación"
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Contact Center"
        verbose_name_plural = "Contact Center"
        ordering = ["-created_at"]


class ServicePrice(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_model = models.ForeignKey("CarModel", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Modelo")
    service = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Servicio")
    price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, verbose_name="Precio")

    class Meta:
        verbose_name = "Precio de servicio"
        verbose_name_plural = "Precios de servicio"


class VCitasUsuarios(models.Model):
    cvegrupo = models.IntegerField(db_column="cveGrupo")
    cveperfil = models.IntegerField(db_column="cvePerfil")
    cveusuario = models.CharField(db_column="cveUsuario", max_length=15)
    pass_field = models.CharField(db_column="Pass", max_length=100)
    nombre = models.CharField(db_column="Nombre", max_length=150, blank=True, null=True)
    correoe = models.CharField(db_column="correoE", max_length=100, blank=True, null=True)
    color = models.CharField(db_column="Color", max_length=50, blank=True, null=True)
    cveasesor = models.CharField(db_column="cveAsesor", max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "v_usuarios"
