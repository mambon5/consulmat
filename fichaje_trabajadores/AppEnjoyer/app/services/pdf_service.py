from reportlab.platypus import *
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime, timedelta
from io import BytesIO

def generate_pdf_report(records, user, report_type):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("INFORME DE REGISTRO HORARIO", styles['Heading1']))

    data = [['Fecha', 'Entrada', 'Salida', 'Horas']]
    total = timedelta()

    for r in records:
        if r.check_out:
            dur = r.check_out - r.check_in
            total += dur
            hours = f"{dur.seconds//3600}:{(dur.seconds//60)%60:02d}"
        else:
            hours = "-"
        data.append([
            r.check_in.strftime('%d/%m/%Y'),
            r.check_in.strftime('%H:%M'),
            r.check_out.strftime('%H:%M') if r.check_out else "-",
            hours
        ])

    table = Table(data)
    table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.black)]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
