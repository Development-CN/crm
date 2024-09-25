from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CotizacionesSerializer


class APICotizaciones(APIView):
    def post(self, request):
        serializer_cotizaciones = CotizacionesSerializer(data=request.data)
        if not serializer_cotizaciones.is_valid():
            return Response(serializer_cotizaciones.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer_cotizaciones.save()
            return Response(serializer_cotizaciones.data, status=status.HTTP_201_CREATED)
