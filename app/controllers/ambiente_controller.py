from flask import Blueprint, request, jsonify, render_template, session
from app.models.ambiente import AmbienteModel
from app.utils.auth import login_required, admin_required

ambiente_bp = Blueprint('ambientes', __name__)

@ambiente_bp.route('/')
@login_required
def listar():
    model = AmbienteModel()

    # Si es estudiante, solo mostrar SUS solicitudes
    if session.get('rol') == 'estudiante':
        todas = model.get_all()
        solicitudes = [s for s in todas if s.get('estudiante_id') == session.get('user_id')]
        es_admin = False
    else:
        # Administrativo ve todas
        solicitudes = model.get_all()
        es_admin = True

    return render_template('ambientes.html', solicitudes=solicitudes, es_admin=es_admin)

@ambiente_bp.route('/api/listar', methods=['GET'])
@login_required
def api_listar():
    model = AmbienteModel()

    if session.get('rol') == 'estudiante':
        todas = model.get_all()
        return jsonify([s for s in todas if s.get('estudiante_id') == session.get('user_id')])

    return jsonify(model.get_all())

@ambiente_bp.route('/api/crear', methods=['POST'])
@login_required
def api_crear():
    data = request.get_json()
    model = AmbienteModel()

    # Estudiante solo puede crear para sí mismo
    estudiante_id = data.get('estudiante_id')
    if session.get('rol') == 'estudiante' and estudiante_id != session.get('user_id'):
        return jsonify({'success': False, 'error': 'No puedes crear solicitudes para otro estudiante'}), 403

    nueva = model.create_solicitud(
        estudiante_id=estudiante_id,
        ambiente_data={
            'ambiente_id': data.get('ambiente_id'),
            'fecha_uso': data.get('fecha_uso'),
            'hora_inicio': data.get('hora_inicio'),
            'hora_fin': data.get('hora_fin'),
            'motivo': data.get('motivo'),
            'asistentes': data.get('asistentes', 1)
        }
    )
    return jsonify({'success': True, 'data': nueva}), 201

@ambiente_bp.route('/api/actualizar/<doc_id>', methods=['PUT'])
@login_required
def api_actualizar(doc_id):
    data = request.get_json()
    model = AmbienteModel()

    # Verificar que el estudiante solo actualice sus propias solicitudes
    if session.get('rol') == 'estudiante':
        solicitud = model.get_by_id(doc_id)
        if not solicitud or solicitud.get('estudiante_id') != session.get('user_id'):
            return jsonify({'success': False, 'error': 'No autorizado'}), 403

    actualizado = model.update(doc_id, data)
    if actualizado:
        return jsonify({'success': True, 'data': actualizado})
    return jsonify({'success': False, 'error': 'No encontrado'}), 404

@ambiente_bp.route('/api/eliminar/<doc_id>', methods=['DELETE'])
@login_required
def api_eliminar(doc_id):
    model = AmbienteModel()

    # Solo admin puede eliminar cualquiera; estudiante solo las suyas
    if session.get('rol') == 'estudiante':
        solicitud = model.get_by_id(doc_id)
        if not solicitud or solicitud.get('estudiante_id') != session.get('user_id'):
            return jsonify({'success': False, 'error': 'No autorizado'}), 403

    if model.delete(doc_id):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No encontrado'}), 404
