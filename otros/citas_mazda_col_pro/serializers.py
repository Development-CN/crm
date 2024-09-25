from email.policy import default

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Appointment, ContactCenter


class ContactCenterSerializer(ModelSerializer):
    class Meta:
        model = ContactCenter
        exclude = ("created_at",)


class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ("created_at",)


class APIBoardSerializer(serializers.Serializer):
    no_placas = serializers.CharField(source="license_plate")
    vin = serializers.SerializerMethodField()

    modelo = serializers.CharField(source="car_model.name")
    ano = serializers.IntegerField(source="car_model_year")
    color = serializers.SerializerMethodField()
    kilometraje = serializers.IntegerField(source="car_mileage")

    cliente = serializers.SerializerMethodField()
    correo = serializers.EmailField(source="client_email")
    telefono = serializers.CharField(source="client_phone_number")

    servicio = serializers.CharField(source="service.name")
    tiempo = serializers.IntegerField(source="service_time", required=False)

    fecha = serializers.CharField(source="appointment_date")
    hora_cita = serializers.CharField(source="appointment_time")
    id_asesor = serializers.CharField(source="advisor_id")

    NumCita = serializers.CharField(source="appointment_number", required=False)

    def get_cliente(self, obj):
        return obj.client_first_name + " " + obj.client_last_name

    def get_color(self, obj):
        return "Sin color"

    def get_vin(self, obj):
        return "00000000000000000"
