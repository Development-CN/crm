from rest_framework import serializers
from capnet_api.models import EntrevistaProfesionalAPI, ItemsAPI


class TecnicoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="item.descripcion", read_only=True)

    class Meta:
        model = ItemsAPI
        exclude = ["id", "id_hd", "fecha_hora_actualizacion"]


class EntrevistaProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrevistaProfesionalAPI
        fields = "__all__"


class CotizacionSerializer(serializers.Serializer):
    pass
