import io

from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def get_pdf_file(data):
    """Generate PDF file"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Verdana', 'verdana.ttf'))
    textobject = p.beginText()
    textobject.setTextOrigin(50, 790)

    textobject.setFont('Verdana', 30)
    textobject.textLine('Список Покупок')

    textobject.setTextOrigin(50, 700)
    textobject.setFont('Verdana', 15)

    for items in data:
        row = ('• {} ({}) -{}'.format(items['ingredients__name'],
                                      items['ingredients__measurement_unit'],
                                      items['amount'],))
        textobject.textLine(row)

    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='ShopList.pdf')
