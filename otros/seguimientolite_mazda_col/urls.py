# chat/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import services, views

urlpatterns = [
    # Login
    path("login", views.staff_login, name="staff_login"),
    path("logout", LogoutView.as_view(), name="logout"),
    # Técnico
    path("tecnico/<str:id_tecnico>/<str:no_orden>", views.tecnico, name="tecnico"),
    # Refacciones
    path("refacciones", views.refacciones, name="refacciones"),
    path("refacciones/<str:no_orden>", views.refacciones_detalle, name="refacciones_detalle"),
    # Cotizaciones Mini
    path("cotizaciones", views.cotizaciones, name="cotizaciones"),
    path("cotizaciones/<str:no_orden>", views.cotizaciones_detalle, name="cotizaciones_detalle"),
    # Mano de obra
    path("mano_de_obra", views.mano_de_obra, name="mano_de_obra"),
    path("mano_de_obra/<str:no_orden>", views.mano_de_obra_detalle, name="mano_de_obra_detalle"),
    # Asesor
    path("asesor", views.asesor, name="ordenes"),
    path("asesor/<str:no_orden>", views.asesor_detalle, name="detalle_ordenes"),
    # Historial de cotizaciones
    path("historial_cotizaciones", views.HistorialCotizaciones.as_view(), name="historial_cotizaciones"),
    path(
        "historial_cotizaciones/<str:no_orden>",
        views.HistorialCotizacionesDetalle.as_view(),
        name="historial_cotizaciones_detalle",
    ),
    # PDF Calidad
    path("calidad_pdf/<str:no_orden>", views.hoja_multipuntos_pdf, name="pdf_multipuntos"),
    # Historial
    path("historial", views.historial, name="historial"),
    path("historial/<str:no_orden>", views.historial_detalle, name="historial_detalle"),
    # Cliente
    path("cliente/<str:no_orden>", views.client_autologin, name="cliente_login"),
    path("cotizacion/<str:no_orden>", views.cliente_detalle, name="cliente_cotizacion"),
    # Redirigir a login
    path("", views.staff_login, name="re_login"),
    # KPIs
    path("kpis/resumen", views.kpis_resumen, name="kpis_resumen"),
    path("kpis/financiero", views.kpis_financiero, name="kpis_financiero"),
    # APIs
    path("api/insertar_cotizacion", services.APICotizaciones.as_view(), name="insertar_cotizacion"),
]
