from app.models.mongo_model import MongoModel
import hashlib
import json

class CertificadoModel(MongoModel):
    def __init__(self):
        super().__init__('certificados')

    def generate_id(self):
        count = self.count() + 1
        return f"CERT-2026-{count:05d}"

    def generate_sello(self, data_dict):
        content = json.dumps(data_dict, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode()).hexdigest()

    def create_certificado(self, estudiante_id, motivo, record_academico, tipo_certificado='record'):
        cert_id = self.generate_id()

        # Filtrar materias según el tipo de certificado
        if tipo_certificado == 'record':
            materias_filtradas = [
                m for m in record_academico 
                if m.get('observacion', '').upper() == 'APROBADO'
            ]
        else:  # historial
            materias_filtradas = record_academico

        promedio = sum(m['nota'] for m in materias_filtradas) / len(materias_filtradas) if materias_filtradas else 0

        sello = self.generate_sello({
            'id': cert_id,
            'estudiante_id': estudiante_id,
            'tipo_certificado': tipo_certificado,
            'materias': materias_filtradas
        })

        nuevo_certificado = {
            'id': cert_id,
            'estudiante_id': estudiante_id,
            'tipo': 'record_academico',
            'tipo_certificado': tipo_certificado,  # 'record' o 'historial'
            'motivo_solicitud': motivo,
            'fecha_emision': __import__('datetime').datetime.now().isoformat(),
            'materias': materias_filtradas,
            'promedio_general': round(promedio, 2),
            'sello_digital': {
                'hash': sello,
                'firma_institucional': 'UMSA-FIRMA-DIGITAL-INSTITUCIONAL',
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'qr_url': f'/verificar/{cert_id}'
            },
            'estado': 'emitido',
            'descargas': 0
        }
        return self.create(nuevo_certificado)
