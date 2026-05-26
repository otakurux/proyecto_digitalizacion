from flask import Blueprint, request, jsonify, render_template, send_file, session, flash, redirect, url_for
from app.models.certificado import CertificadoModel
from app.models.mongo_model import MongoModel
from app.utils.auth import login_required
from app.utils.pdf_generator import generar_record_academico
import os
import tempfile

certificado_bp = Blueprint('certificados', __name__)

# ---------- Helper ----------
def extraer_materias_estudiante(estudiante):
    """Aplana todas las materias de todas las gestiones del estudiante."""
    materias = []
    for gestion in estudiante.get('gestiones', []):
        materias.extend(gestion.get('materias', []))
    return materias

def filtrar_materias_por_tipo(materias, tipo_certificado):
    """Filtra materias según el tipo de certificado solicitado."""
    if tipo_certificado == 'record':
        return [m for m in materias if m.get('observacion', '').upper() == 'APROBADO']
    return materias  # historial: todas

@certificado_bp.route('/')
@login_required
def listar():
    model = CertificadoModel()

    if session.get('rol') == 'estudiante':
        todos = model.get_all()
        certificados = [c for c in todos if c.get('estudiante_id') == session.get('user_id')]
    else:
        certificados = model.get_all()

    return render_template('certificados.html', certificados=certificados)

@certificado_bp.route('/api/listar', methods=['GET'])
@login_required
def api_listar():
    model = CertificadoModel()

    if session.get('rol') == 'estudiante':
        todos = model.get_all()
        return jsonify([c for c in todos if c.get('estudiante_id') == session.get('user_id')])

    return jsonify(model.get_all())

@certificado_bp.route('/api/emitir', methods=['POST'])
@login_required
def api_emitir():
    data = request.get_json()
    model = CertificadoModel()

    estudiante_id = data.get('estudiante_id')
    tipo_certificado = data.get('tipo_certificado', 'record')

    # Validar tipo
    if tipo_certificado not in ('record', 'historial'):
        return jsonify({'success': False, 'error': 'Tipo de certificado inválido. Use "record" o "historial".'}), 400

    # Estudiante solo puede emitir para sí mismo
    if session.get('rol') == 'estudiante' and estudiante_id != session.get('user_id'):
        return jsonify({'success': False, 'error': 'No puedes emitir certificados para otro estudiante'}), 403

    estudiantes_model = MongoModel('estudiantes')
    estudiante = estudiantes_model.get_by_id(estudiante_id)

    if not estudiante:
        return jsonify({'success': False, 'error': 'Estudiante no encontrado'}), 404

    # Extraer materias de todas las gestiones
    todas_materias = extraer_materias_estudiante(estudiante)

    # EMISIÓN AUTOMÁTICA según tipo seleccionado
    nuevo = model.create_certificado(
        estudiante_id=estudiante_id,
        motivo=data.get('motivo'),
        record_academico=todas_materias,
        tipo_certificado=tipo_certificado
    )

    return jsonify({'success': True, 'data': nuevo}), 201

@certificado_bp.route('/api/actualizar/<doc_id>', methods=['PUT'])
@login_required
def api_actualizar(doc_id):
    data = request.get_json()
    model = CertificadoModel()

    if session.get('rol') == 'estudiante':
        cert = model.get_by_id(doc_id)
        if not cert or cert.get('estudiante_id') != session.get('user_id'):
            return jsonify({'success': False, 'error': 'No autorizado'}), 403

    actualizado = model.update(doc_id, data)
    if actualizado:
        return jsonify({'success': True, 'data': actualizado})
    return jsonify({'success': False, 'error': 'No encontrado'}), 404

@certificado_bp.route('/descargar/<cert_id>')
@login_required
def descargar_pdf(cert_id):
    model = CertificadoModel()
    certificado = model.get_by_id(cert_id)

    if not certificado:
        flash('Certificado no encontrado', 'danger')
        return redirect(url_for('certificados.listar'))

    # Estudiante solo puede descargar sus propios certificados
    if session.get('rol') == 'estudiante' and certificado.get('estudiante_id') != session.get('user_id'):
        flash('No autorizado', 'danger')
        return redirect(url_for('certificados.listar'))

    estudiantes_model = MongoModel('estudiantes')
    estudiante = estudiantes_model.get_by_id(certificado.get('estudiante_id'))

    if not estudiante:
        flash('Datos del estudiante no encontrados', 'danger')
        return redirect(url_for('certificados.listar'))

    # Determinar tipo y filtrar materias para el PDF
    tipo_certificado = certificado.get('tipo_certificado', 'record')
    todas_materias = extraer_materias_estudiante(estudiante)
    materias_pdf = filtrar_materias_por_tipo(todas_materias, tipo_certificado)

    # Preparar datos para el PDF
    sello = certificado.get('sello_digital', {})
    pdf_data = {
        'id': estudiante.get('id', ''),
        'nombre': estudiante.get('nombre', ''),
        'ci': estudiante.get('ci', ''),
        'carrera': estudiante.get('carrera', 'INFORMÁTICA'),
        'gestiones': estudiante.get('gestiones', []),
        'materias': materias_pdf,
        'tipo_certificado': tipo_certificado,
        'sello_hash': sello.get('hash', ''),
        'sello_qr_url': sello.get('qr_url', ''),
        'sello_timestamp': sello.get('timestamp', ''),
        'cert_id': cert_id
    }

    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f'RECORD_{cert_id}.pdf')

    try:
        generar_record_academico(pdf_data, pdf_path)

        # Actualizar contador de descargas
        model.update(cert_id, {'descargas': certificado.get('descargas', 0) + 1})

        return send_file(pdf_path, as_attachment=True, 
                        download_name=f'{"RECORD" if tipo_certificado == "record" else "HISTORIAL"}_ACADEMICO_{estudiante.get("id", "")}.pdf',
                        mimetype='application/pdf')
    except Exception as e:
        flash(f'Error al generar PDF: {str(e)}', 'danger')
        return redirect(url_for('certificados.listar'))