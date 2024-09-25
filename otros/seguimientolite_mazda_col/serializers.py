from rest_framework import serializers
from .models import Cotizaciones


class CotizacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizaciones
        fields = [
            "no_orden",
            "item",
            "repuesto",
            "costo_repuesto",
            "costo_mano_obra",
            "subtotal",
            "iva",
            "monto_iva",
            "total",
            "fuente",
        ]
