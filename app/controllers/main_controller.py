from flask import Blueprint, render_template, jsonify
from app.models.ambiente import AmbienteModel
from app.models.certificado import CertificadoModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    ambiente_model = AmbienteModel()
    cert_model = CertificadoModel()

    all_ambientes = ambiente_model.get_all()
    all_certificados = cert_model.get_all()

    stats = {
        'total_ambientes': len(all_ambientes),
        'total_certificados': len(all_certificados),
        'pendientes': len([a for a in all_ambientes if a.get('estado') == 'pendiente']),
        'aprobados': len([a for a in all_ambientes if a.get('estado') == 'aprobada'])
    }
    return render_template('index.html', stats=stats)

@main_bp.route('/verificar/<doc_id>')
def verificar(doc_id):
    """Verificación pública de documentos via QR"""
    ambiente_model = AmbienteModel()
    cert_model = CertificadoModel()

    doc = ambiente_model.get_by_id(doc_id)
    if not doc:
        doc = cert_model.get_by_id(doc_id)

    return render_template('verificar.html', documento=doc, doc_id=doc_id)
