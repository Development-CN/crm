import io
import logging
import os
import textwrap
import reportlab
from datetime import datetime

from django.conf import settings
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


from .models import (
    ActividadesAsesorFirmas,
    ActividadesTecnicoCaptura,
    Informacion,
    Items,
    ListaItems,
    ListaItemsTecnicoCaptura,
    VTecnicos,
)

CWD = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
FORMATO_MULTIPUNTOS = os.path.join(THIS_FOLDER, "pdf", "hoja_multipuntos.pdf")

logger = logging.getLogger(__name__)


reportlab.rl_config.TTFSearchPath.append(str(CWD) + "/pdf")
pdfmetrics.registerFont(TTFont("Mazda", "MazdaType-Medium.ttf"))

STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(name="Mazda", fontName="Mazda", fontSize=9, leading=12))


def get_pdf_calidad(no_orden):
    buffer = io.BytesIO()

    # Información general
    info = Informacion.objects.get(no_orden=no_orden)
    tecnico = VTecnicos.objects.get(id_empleado=info.tecnico).nombre_empleado
    lista_items = ListaItems.objects.filter(revision__id=1)
    lista_items_captura = ListaItemsTecnicoCaptura.objects.all()

    # Inspección de técnico
    queryset_tecnico = Items.objects.filter(no_orden=no_orden)
    queryset_tecnico_captura = ActividadesTecnicoCaptura.objects.filter(no_orden=no_orden)

    try:
        firma = ActividadesAsesorFirmas.objects.get(no_orden=no_orden, tipo="tecnico").firma
    except Exception:
        firma = None
        logger.info("Hoja multipuntos: No hay firma de cliente")

    can = canvas.Canvas(buffer, pagesize=letter)
    can.setFont("Mazda", 9)

    caracter_default = "✔"
    caracter_no_default = "✔"
    can.setFillColorRGB(0.6,0.6,0.6)

    if queryset_tecnico.filter(item__revision__id=1).exists():
        # Escritura de la información de la orden
        
        try:
            can.drawString(138, 783, info.cliente.upper())
            can.drawString(190, 757, info.vehiculo.upper())
            can.drawString(173, 746, info.placas.upper())
            can.drawString(160, 735, info.vin.upper())
            can.drawString(172, 725, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            can.drawString(164, 714, info.no_orden)
            can.drawRightString(565, 736, "ASESOR: " + info.asesor.upper())
            can.drawRightString(565, 714, "TÉCNICO: " + tecnico.upper())
            can.drawRightString(565, 725, "TELÉFONO DE CONTACTO: " + settings.TELEFONO)
        except Exception:
            pass

        # concatenando los comentarios
        comentarios = ""
        for item_comentarios in lista_items:
            if queryset_tecnico.filter(item=item_comentarios).exists():
                item_inspeccionado = queryset_tecnico.get(item=item_comentarios)
            
                if item_inspeccionado.comentarios:

                    comentarios += str(lista_items.get(id=item_inspeccionado.item_id).descripcion) + ": " + str(item_inspeccionado.comentarios) + " || "
                
                else:
                    pass

        can.setFont("Mazda", 8)
        texto_comentarios = textwrap.fill(comentarios, 105)
        #texto_comentarios = textwrap.fill("hola", 80)
        box_comentarios = can.beginText(32, 100)
        box_comentarios.textLines(texto_comentarios.upper())
        can.drawText(box_comentarios)

    
        can.setFont("Helvetica-Bold", 11)
        # Escritura del estado de cada item de la hoja multipuntos
        for item_formato in lista_items:
            if queryset_tecnico.filter(item=item_formato).exists():
                item_inspeccionado = queryset_tecnico.get(item=item_formato)

                # Estado del item
                try:
                    if item_inspeccionado.estado == "Buen Estado":
                        can.drawString(item_formato.g_x, item_formato.g_y, caracter_default)
                    if item_inspeccionado.estado == "Recomendado":
                        try:
                            can.drawString(item_formato.y_x, item_formato.y_y, caracter_no_default)
                        except Exception:
                            can.drawString(item_formato.r_x, item_formato.r_y, caracter_no_default)
                    if item_inspeccionado.estado == "Inmediato":
                        can.drawString(item_formato.r_x, item_formato.r_y, caracter_no_default)
                    if item_inspeccionado.estado == "Corregido":
                        can.drawString(item_formato.modificado_x, item_formato.modificado_y, caracter_default)
                except Exception:
                    pass

                # Valor capturado
                try:
                    if item_inspeccionado.valor:
                        can.drawString(
                            item_formato.valor_x,
                            item_formato.valor_y,
                            item_inspeccionado.valor,
                        )
                except Exception:
                    pass

                # Item cambiado
                try:
                    if item_inspeccionado.cambiado:
                        can.drawString(
                            item_formato.modificado_x,
                            item_formato.modificado_y,
                            caracter_default,
                        )
                except Exception:
                    pass


            else:
                logger.info(f"Hoja Multipuntos: no se encuentra el item '{item_formato.descripcion}'")

        # Escritura de próximo servicio
        can.setFont("Mazda", 8)
        if queryset_tecnico_captura:
            for item_formato in lista_items_captura:
                try:
                    item_inspeccionado = queryset_tecnico_captura.filter(
                        item=item_formato.nombre, valor__isnull=False
                    ).first()

                    text = textwrap.fill(item_inspeccionado.valor, item_formato.line_size)
                    box = can.beginText(item_formato.x, item_formato.y)
                    box.textLines(text.upper())
                    can.drawText(box)
                except Exception as error:
                    logger.error(error)

        # Escritura de la firma
        '''
        if firma:
            can.drawImage(os.path.join(settings.MEDIA_ROOT, firma), 465, 20, 90, 45, mask="auto")
            can.drawString(460, 21, "__________________")
            can.drawString(465, 9, "Firma del técnico")
        '''
        
    else:
        pass

    can.showPage()
    can.save()
    buffer.seek(0)

    datos_multipuntos = PdfFileReader(buffer)
    existing_pdf = PdfFileReader(open(FORMATO_MULTIPUNTOS, "rb"))
    page = existing_pdf.getPage(0)
    page.mergePage(datos_multipuntos.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)
    buffer_pdf = io.BytesIO()
    output.write(buffer_pdf)
    buffer_pdf.seek(0)
    return buffer_pdf
