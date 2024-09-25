import io
import logging
from capnet_api.models import ItemsAPI, EntrevistaProfesionalAPI, ManoDeObraAPI, RefaccionesAPI
from capnet_api.serializers import *
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class APITecnico(APIView):
    def post(self, request):
        no_orden = request.data.get("no_orden")
        queryset = ItemsAPI.objects.filter(no_orden=no_orden)
        serializer = TecnicoSerializer(queryset, many=True)
        return Response(serializer.data)


class APICotizacion(APIView):
    def post(self, request):
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)

        no_orden = data["no_orden"]
        item = ItemsAPI.objects.get(id=data["item"])

        for repuesto in data["repuestos"]:
            nuevo_repuesto = RefaccionesAPI(no_orden=no_orden, item=item, **repuesto)
            nuevo_repuesto.save()
        for mano_de_obra in data["mano_de_obra"]:
            nueva_mano_de_obra = ManoDeObraAPI(no_orden=no_orden, item=item, **mano_de_obra)
            nueva_mano_de_obra.save()

        return Response(status=status.HTTP_200_OK)


class APIEntrevista(APIView):
    def post(self, request):
        try:
            no_cita = request.data.get("no_cita")
            queryset = EntrevistaProfesionalAPI.objects.get(no_cita=no_cita)
            serializer = EntrevistaProfesionalSerializer(queryset, many=False)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response(status=status.HTTP_404_NOT_FOUND)
