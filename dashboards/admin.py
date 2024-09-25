# Django
from django.apps import AppConfig
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import RelatedField
from dashboards.models import Asesor, CatalogoRespuestasByEtapa, Catalogo, CatalogoModelo, Prospecto, Lead, Historial, HistorialVerificaciones, Retomas, VehiculosInteresLead, Evento

admin.site.register(ContentType)


class UserAdmin(BaseUserAdmin):
    # Admin del UserAdmin
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'

    def sala(self, user):
        # Obtiene el asesor relacionado y muestra la sala
        asesor = user.asesor_set.first()  # Ajusta el nombre del método si es necesario
        return asesor.sala if asesor else 'No disponible'
    sala.short_description = 'Sala'

    list_display = ('id', 'username', "first_name", "group", "is_active", "sala")
    list_filter = ('groups',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    # Admin del Permission
    list_display = ('id', 'name')
    list_filter = ('content_type',)
    ordering = ('-id',)

@admin.register(Asesor)
class AsesorAdmin(admin.ModelAdmin):
    # Admin del Asesor
    list_display = ('id', 'nombre', 'sala', "habilitado")
    list_filter = ('sala', "habilitado")

@admin.register(CatalogoRespuestasByEtapa)
class CatalogoRespuestasByEtapaAdmin(admin.ModelAdmin):
    # Admin del CatalogoRespuestasByEtapa
    list_display = ('id', 'respuesta', 'etapa')
    list_filter = ('etapa',)

@admin.register(CatalogoModelo)
class CatalogoModeloAdmin(admin.ModelAdmin):
    # Admin del CatalogoModelo
    list_display = ('nombre', 'marca')
    list_filter = ('marca',)

@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    # Admin del Catalogo
    list_display = ('descripcion', 'clasificacion')
    list_filter = ('clasificacion',)

@admin.register(Prospecto)
class ProspectoAdmin(admin.ModelAdmin):
    # Admin del Prospecto
    list_display = ('id', 'nombre', "apellido_paterno", "fecha_captura", "nombre_asesor", "anfitrion")
    list_filter = ('nombre', "celular")
    search_fields= ["id", "celular", "nombre"]

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # Admin del Lead
    list_display = ('id', 'prospecto', "nombre_asesor", "etapa", "respuesta", "activo", "fecha_apertura", "fecha_hora_asignacion_asesor", "marcas_interes")
    list_filter = ("nombre_asesor", ("nombre_asesor", admin.EmptyFieldListFilter), "activo", "etapa", "respuesta", 'origen_lead', "tiempo_cambio_de_etapa")
    search_fields= ["id",]

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    # Admin del Historial
    list_display = ('id', "lead", 'responsable', "fecha", "operacion")

@admin.register(HistorialVerificaciones)
class HistorialVerificacionesAdmin(admin.ModelAdmin):
    # Admin del HistorialVerificaciones
    list_display = ('id', 'responsable', "tipo_solicitud")

@admin.register(Retomas)
class RetomasAdmin(admin.ModelAdmin):
    # Admin del Retomas
    list_display = ('id', 'lead',)

@admin.register(VehiculosInteresLead)
class VehiculosInteresLeadAdmin(admin.ModelAdmin):
    # Admin del VehiculosInteresLead
    list_display = ('id', 'lead', "mostrado", "cotizar")
    search_fields= ["id", 'lead__id']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    # Admin del Evento
    list_display = ('id', 'nombre', "tipo", "asesor", "lead", "telefono_cliente", "cumplido")