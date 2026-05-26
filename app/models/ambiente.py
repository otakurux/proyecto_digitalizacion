from app.models.mongo_model import MongoModel
import hashlib
import json

class AmbienteModel(MongoModel):
    def __init__(self):
        super().__init__('ambientes')

    def generate_id(self):
        """Generar ID autoincremental basado en conteo de documentos"""
        count = self.count() + 1
        return f"AMB-2026-{count:05d}"

    def generate_sello(self, data_dict):
        """Genera hash SHA-256 como sello digital de validación"""
        content = json.dumps(data_dict, sort_keys=True, ensure_ascii=False)
        hash_obj = hashlib.sha256(content.encode())
        return hash_obj.hexdigest()

    def create_solicitud(self, estudiante_id, ambiente_data):
        solicitud_id = self.generate_id()
        sello = self.generate_sello({
            'id': solicitud_id,
            'estudiante_id': estudiante_id,
            **ambiente_data
        })

        nueva_solicitud = {
            'id': solicitud_id,
            'estudiante_id': estudiante_id,
            'tipo': 'solicitud_ambiente',
            'ambiente_id': ambiente_data.get('ambiente_id'),
            'fecha_uso': ambiente_data.get('fecha_uso'),
            'hora_inicio': ambiente_data.get('hora_inicio'),
            'hora_fin': ambiente_data.get('hora_fin'),
            'motivo': ambiente_data.get('motivo'),
            'asistentes': ambiente_data.get('asistentes', 1),
            'estado': 'pendiente',
            'sello_digital': {
                'hash': sello,
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'qr_url': f'/verificar/{solicitud_id}'
            },
            'uso_confirmado': False
        }
        return self.create(nueva_solicitud)
