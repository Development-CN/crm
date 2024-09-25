from django.contrib import admin

from citas_mazda_col_pro.models import (
    Appointment,
    CarModel,
    DocumentType,
    Service,
    ServicePrice,
)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "license_plate",
        "car_model",
        "client_first_name",
        "client_last_name",
        "appointment_date",
        "appointment_time",
    )


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active")


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year_start", "year_end", "active")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "order", "wait", "time", "active")


@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ("id", "car_model", "service", "price")
