from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
import tempfile
from datetime import datetime
import qrcode
from io import BytesIO

def generar_record_academico(estudiante_data, output_path):
    """
    Genera un PDF del récord académico estilo UMSA con QR del sello digital.

    Args:
        estudiante_data: dict con datos del estudiante, materias y sello digital
        output_path: ruta donde guardar el PDF
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=2*cm
    )

    elements = []
    styles = getSampleStyleSheet()

    # Colores UMSA
    umsa_blue = HexColor('#1a365d')
    umsa_gold = HexColor('#c9a227')
    light_gray = HexColor('#f7fafc')

    # === ENCABEZADO INSTITUCIONAL ===
    header_data = [
        ['UNIVERSIDAD MAYOR DE SAN ANDRÉS', '', ''],
        ['FACULTAD DE CIENCIAS PURAS Y NATURALES', '', ''],
        ['CARRERA INFORMÁTICA', '', ''],
    ]

    header_table = Table(header_data, colWidths=[13*cm, 2*cm, 2*cm])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 14),
        ('TEXTCOLOR', (0, 0), (0, 0), umsa_blue),
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (0, 1), 11),
        ('TEXTCOLOR', (0, 1), (0, 1), umsa_blue),
        ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 2), (0, 2), 10),
        ('TEXTCOLOR', (0, 2), (0, 2), umsa_blue),
        ('ALIGN', (0, 0), (0, 2), 'CENTER'),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 1), (2, 1)),
        ('SPAN', (0, 2), (2, 2)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.3*cm))

    # === TÍTULO ===
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=umsa_blue,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph('HISTORIAL ACADÉMICO', title_style))
    elements.append(Spacer(1, 0.2*cm))

    # === DATOS DEL ESTUDIANTE ===
    nombre = estudiante_data.get('nombre', 'N/A')
    ci = estudiante_data.get('ci', 'N/A')
    reg_univ = estudiante_data.get('id', 'N/A')
    carrera = estudiante_data.get('carrera', 'INFORMÁTICA')
    fecha = datetime.now().strftime('La Paz, %d de %B de %Y')

    info_data = [
        ['Nombre(s):', nombre, 'Fecha:', fecha],
        ['Cédula:', ci, 'Reg. Univ.:', reg_univ],
        ['Carrera:', carrera, '', ''],
    ]

    info_table = Table(info_data, colWidths=[2.5*cm, 7*cm, 2.5*cm, 3.5*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, light_gray),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*cm))

    # === MATERIAS POR GESTIÓN ===
    gestiones = estudiante_data.get('gestiones', [])

    if not gestiones:
        materias = estudiante_data.get('materias', [])
        if materias:
            gestiones = [{'gestion': '2023-1', 'materias': materias}]

    total_inscritas = 0
    total_aprobadas = 0
    total_reprobadas = 0
    total_abandonadas = 0
    suma_notas_aprobadas = 0
    suma_notas_todas = 0

    for gestion_data in gestiones:
        gestion_nombre = gestion_data.get('gestion', 'SIN GESTIÓN')
        materias = gestion_data.get('materias', [])

        if not materias:
            continue

        # Título de gestión
        gestion_style = ParagraphStyle(
            'GestionTitle',
            parent=styles['Heading2'],
            fontSize=10,
            textColor=white,
            alignment=TA_CENTER,
            backColor=umsa_blue,
            spaceAfter=2,
            spaceBefore=4,
            fontName='Helvetica-Bold'
        )
        elements.append(Paragraph(f'{gestion_nombre}', gestion_style))

        # Tabla de materias
        materias_data = [['No.', 'Sigla', 'Materia', 'Par.', 'Nota', 'Folio', 'Libro', 'Observación', 'Docente']]

        g_inscritas = len(materias)
        g_aprobadas = 0
        g_reprobadas = 0
        g_abandonadas = 0
        g_suma_aprobadas = 0
        g_suma_todas = 0

        for i, mat in enumerate(materias, 1):
            nota = mat.get('nota', 0)
            observacion = mat.get('observacion', '')

            if not observacion:
                if nota >= 51:
                    observacion = 'APROBADO'
                    g_aprobadas += 1
                    g_suma_aprobadas += nota
                elif nota == 0:
                    observacion = 'ABANDONO'
                    g_abandonadas += 1
                else:
                    observacion = 'REPROBADO'
                    g_reprobadas += 1
            else:
                if 'APROB' in observacion.upper():
                    g_aprobadas += 1
                    g_suma_aprobadas += nota
                elif 'ABAND' in observacion.upper() or 'ABAN' in observacion.upper():
                    g_abandonadas += 1
                else:
                    g_reprobadas += 1

            g_suma_todas += nota

            materias_data.append([
                str(i),
                mat.get('sigla', ''),
                mat.get('materia', ''),
                str(mat.get('paralelo', mat.get('par', ''))),
                str(nota) if nota > 0 else '-',
                str(mat.get('folio', '')),
                str(mat.get('libro', '')),
                observacion,
                mat.get('docente', '')
            ])

        # Totales de gestión
        prom_gral = round(g_suma_todas / g_inscritas, 2) if g_inscritas > 0 else 0
        prom_aprob = round(g_suma_aprobadas / g_aprobadas, 2) if g_aprobadas > 0 else 0

        materias_data.append([
            str(g_inscritas), str(g_aprobadas), str(g_reprobadas), str(g_abandonadas),
            str(prom_gral), str(prom_aprob), '', '', ''
        ])

        col_widths = [0.8*cm, 1.8*cm, 5*cm, 0.8*cm, 1*cm, 1*cm, 0.8*cm, 1.8*cm, 4.5*cm]

        materias_table = Table(materias_data, colWidths=col_widths, repeatRows=1)
        materias_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), umsa_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 7),
            ('ALIGN', (0, 1), (0, -2), 'CENTER'),
            ('ALIGN', (3, 1), (5, -2), 'CENTER'),
            ('ALIGN', (7, 1), (7, -2), 'CENTER'),
            ('BACKGROUND', (0, -1), (-1, -1), light_gray),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 0.5, umsa_blue),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]))
        elements.append(materias_table)
        elements.append(Spacer(1, 0.3*cm))

        total_inscritas += g_inscritas
        total_aprobadas += g_aprobadas
        total_reprobadas += g_reprobadas
        total_abandonadas += g_abandonadas
        suma_notas_aprobadas += g_suma_aprobadas
        suma_notas_todas += g_suma_todas

    # === RESUMEN FINAL ===
    elements.append(Spacer(1, 0.5*cm))

    prom_gral_total = round(suma_notas_todas / total_inscritas, 2) if total_inscritas > 0 else 0
    prom_aprob_total = round(suma_notas_aprobadas / total_aprobadas, 2) if total_aprobadas > 0 else 0

    resumen_data = [
        ['RESUMEN ACADÉMICO'],
        [f'INSCRITAS: {total_inscritas}   APROBADAS: {total_aprobadas}   REPROBADAS: {total_reprobadas}   ABANDONOS: {total_abandonadas}'],
        [f'PROM. GRAL.: {prom_gral_total}   PROM. APROB.: {prom_aprob_total}'],
    ]

    resumen_table = Table(resumen_data, colWidths=[17*cm])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), umsa_gold),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), light_gray),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, umsa_blue),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(resumen_table)

    # === SECCIÓN SELLO DIGITAL CON QR ===
    elements.append(Spacer(1, 0.8*cm))

    sello_hash = estudiante_data.get('sello_hash', 'N/A')
    sello_qr_url = estudiante_data.get('sello_qr_url', '')
    cert_id = estudiante_data.get('cert_id', '')

    # Generar imagen QR del sello
    qr_img = None
    if sello_qr_url:
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(f'http://localhost:5000{sello_qr_url}')
            qr.make(fit=True)
            qr_img_buffer = BytesIO()
            qr.make_image(fill_color="#1a365d", back_color="white").save(qr_img_buffer, format='PNG')
            qr_img_buffer.seek(0)
            qr_img = Image(qr_img_buffer, width=2.5*cm, height=2.5*cm)
        except Exception:
            pass

    # Tabla con QR y datos del sello
    sello_data = []
    if qr_img:
        sello_data = [
            [qr_img, 
             f'<b>DOCUMENTO DIGITAL VALIDADO POR UMSA</b><br/>'
             f'ID: {cert_id}<br/>'
             f'Hash: {sello_hash[:40]}...<br/>'
             f'Fecha emisión: {datetime.now().strftime("%d/%m/%Y %H:%M")}<br/>'
             f'<i>Escanee el QR para verificar autenticidad</i>']
        ]
    else:
        sello_data = [
            ['', f'<b>DOCUMENTO DIGITAL VALIDADO POR UMSA</b><br/>'
             f'ID: {cert_id}<br/>'
             f'Hash: {sello_hash[:40]}...<br/>'
             f'Fecha emisión: {datetime.now().strftime("%d/%m/%Y %H:%M")}']
        ]

    sello_table = Table(sello_data, colWidths=[3*cm, 14*cm])
    sello_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (1, 0), (1, 0), 8),
        ('TEXTCOLOR', (1, 0), (1, 0), HexColor('#718096')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f7fafc')),
    ]))
    elements.append(sello_table)

    # Generar PDF
    doc.build(elements)
    return output_path
