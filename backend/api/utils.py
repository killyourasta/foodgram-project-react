import io

from django.conf import settings
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def create_pdf(data):
    shoping_list = []
    shoping_list.append('СПИСОК ПОКУПОК:')
    shoping_list.append('---------')
    for item in data:
        shoping_list.append(
            f"{item['ingredient__name']} – "
            f"{item['sum_amount']}"
            f"({item['ingredient__measurement_unit']})"
        )
    pdfmetrics.registerFont(TTFont('Ubuntu', './api/fonts/Ubuntu-C.ttf'))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    font_size = 15
    p.setFont('Ubuntu', font_size)
    start_x = 50
    start_y = 800
    for string_line in shoping_list:
        p.drawString(start_x, start_y, string_line)
        start_y -= 15
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True,
        filename=settings.SHOPPING_LIST_FILE_NAME
    )
