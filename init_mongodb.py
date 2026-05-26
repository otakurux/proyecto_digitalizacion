#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialización de MongoDB para UMSA Digital.
Carga datos de ejemplo en las colecciones:
  - usuarios (login/registro)
  - estudiantes (con gestiones completas tipo UMSA)
  - ambientes_disponibles
  - ambientes (solicitudes)
  - certificados

Requisitos: MongoDB corriendo en localhost:27017
  o definir variable de entorno MONGO_URI

Ejecutar: python init_mongodb.py
"""

import os
import hashlib
import json
from datetime import datetime
from pymongo import MongoClient

def generate_hash(data_dict):
    content = json.dumps(data_dict, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(content.encode()).hexdigest()

def hash_password(password):
    """Genera hash seguro de contraseña usando bcrypt si está disponible, sino sha256"""
    try:
        import bcrypt
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    except ImportError:
        return hashlib.sha256(password.encode()).hexdigest()

def init_mongodb():
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["umsa_digital"]

    print(f"🔗 Conectando a MongoDB: {mongo_uri}")
    print(f"📂 Base de datos: umsa_digital")

    # 1. Colección: usuarios (sistema de login)
    usuarios = db["usuarios"]
    usuarios.drop()
    usuarios_data = [
        {
            "id": "2000001",
            "nombre": "MAMANI TRUJILLO DEIVID ENRIQUE",
            "password_hash": hash_password("estudiante123"),
            "rol": "estudiante",
            "carrera": "Informática",
            "ci": "7235715-1V",
            "activo": True,
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "2000002",
            "nombre": "JUAN CARLOS MAMANI LÓPEZ",
            "password_hash": hash_password("estudiante123"),
            "rol": "estudiante",
            "carrera": "Derecho",
            "ci": "8123456-2L",
            "activo": True,
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "3000001",
            "nombre": "Lic. Rosa María Quispe Callisaya",
            "password_hash": hash_password("admin123"),
            "rol": "administrativo",
            "carrera": "Administración",
            "ci": "6543210-1K",
            "activo": True,
            "created_at": datetime.now().isoformat()
        }
    ]
    usuarios.insert_many(usuarios_data)
    print(f"✅ Colección 'usuarios' → {usuarios.count_documents({})} documentos")
    print("   Usuarios de prueba:")
    print("   • 2000001 / estudiante123 (Estudiante - Informática)")
    print("   • 2000002 / estudiante123 (Estudiante - Derecho)")
    print("   • 3000001 / admin123 (Administrativo)")

    # 2. Colección: estudiantes (MISMO id y nombre que en usuarios)
    estudiantes = db["estudiantes"]
    estudiantes.drop()
    estudiantes_data = [
        {
            "id": "2000001",
            "nombre": "MAMANI TRUJILLO DEIVID ENRIQUE",
            "carrera": "INFORMÁTICA",
            "ci": "7235715-1V",
            "reg_univ": "1845286",
            "gestiones": [
                {
                    "gestion": "2023 PRIMERO",
                    "materias": [
                        {"sigla": "INF-111", "materia": "PROGRAMACIÓN I", "paralelo": "54", "nota": 54, "folio": "1", "libro": "C", "observacion": "APROBADO", "docente": "M.Sc. JORGE HUMBERTO TERAN POMIER"},
                        {"sigla": "INF-112", "materia": "FUNDAMENTOS DIGITALES", "paralelo": "71", "nota": 71, "folio": "2", "libro": "E", "observacion": "APROBADO", "docente": "Ph.D. MARISOL TELLEZ RAMIREZ"},
                        {"sigla": "INF-113", "materia": "PROGRAMACIÓN WEB I", "paralelo": "52", "nota": 52, "folio": "3", "libro": "C", "observacion": "APROBADO", "docente": "Lic. JUAN MARCOS MIRANDA NINA"},
                        {"sigla": "INF-114", "materia": "ÁLGEBRA", "paralelo": "51", "nota": 51, "folio": "4", "libro": "A", "observacion": "APROBADO", "docente": "M.Sc. HUGO PAREDES BARRA"},
                        {"sigla": "INF-115", "materia": "CÁLCULO I", "paralelo": "51", "nota": 51, "folio": "5", "libro": "A", "observacion": "APROBADO", "docente": "Mg.Sc. RUDY WILFREDO MAYTA CALLISAYA"},
                        {"sigla": "INF-116", "materia": "FÍSICA", "paralelo": "52", "nota": 52, "folio": "6", "libro": "B", "observacion": "APROBADO", "docente": "Ph.D. EVARISTO MAMANI CARLO"}
                    ]
                },
                {
                    "gestion": "2023 SEGUNDO",
                    "materias": [
                        {"sigla": "INF-121", "materia": "PROGRAMACIÓN II", "paralelo": "54", "nota": 54, "folio": "1", "libro": "A", "observacion": "APROBADO", "docente": "Lic. CELIA ELENA TARQUINO PERALTA"},
                        {"sigla": "INF-122", "materia": "PROGRAMACIÓN WEB II", "paralelo": "28", "nota": 28, "folio": "2", "libro": "C", "observacion": "REPROBADO", "docente": "Ph.D. MIGUEL DE SEVILLA CHAVEZ GORDILLO"},
                        {"sigla": "INF-123", "materia": "ELECTRÓNICA GENERAL I", "paralelo": "61", "nota": 61, "folio": "3", "libro": "A", "observacion": "APROBADO", "docente": "Dr. ROGER APAZA VASQUEZ"},
                        {"sigla": "INF-124", "materia": "ESTADÍSTICA I", "paralelo": "0", "nota": 0, "folio": "4", "libro": "A", "observacion": "ABANDONO", "docente": "Lic. MARÍA DE LOS ÁNGELES RAMOS BOUTIER"},
                        {"sigla": "INF-125", "materia": "ÁLGEBRA LINEAL", "paralelo": "25", "nota": 25, "folio": "5", "libro": "A", "observacion": "REPROBADO", "docente": "Lic. ZENON CONDORI GONZALES"},
                        {"sigla": "INF-126", "materia": "CÁLCULO II", "paralelo": "14", "nota": 14, "folio": "6", "libro": "A", "observacion": "REPROBADO", "docente": "M.Sc. HERNAN LAIME ZANGA"},
                        {"sigla": "TRA-136", "materia": "METODOLOGÍA DE LA INVESTIGACIÓN", "paralelo": "51", "nota": 51, "folio": "7", "libro": "B", "observacion": "APROBADO", "docente": "Lic. RAYSA CAROLINA PANIAGUA SIÑANI"}
                    ]
                },
                {
                    "gestion": "2023 VERANO",
                    "materias": [
                        {"sigla": "INF-122", "materia": "PROGRAMACIÓN WEB II", "paralelo": "53", "nota": 53, "folio": "1", "libro": "A", "observacion": "APROBADO", "docente": "Lic. TATIANA ANDREA DELGADILLO GARZOFINO"},
                        {"sigla": "INF-124", "materia": "ESTADÍSTICA I", "paralelo": "45", "nota": 45, "folio": "2", "libro": "A", "observacion": "REPROBADO", "docente": "M.Sc. VERONICA CUENCA RAMALLO"}
                    ]
                },
                {
                    "gestion": "2024 INVIERNO",
                    "materias": [
                        {"sigla": "INF-124", "materia": "ESTADÍSTICA I", "paralelo": "75", "nota": 75, "folio": "1", "libro": "A", "observacion": "APROBADO", "docente": "M.Sc. VERONICA CUENCA RAMALLO"},
                        {"sigla": "INF-132", "materia": "BASE DE DATOS I", "paralelo": "64", "nota": 64, "folio": "2", "libro": "A", "observacion": "APROBADO", "docente": "Lic. ROSALIA LOPEZ MONTALVO"}
                    ]
                }
            ]
        },
        {
            "id": "2000002",
            "nombre": "JUAN CARLOS MAMANI LÓPEZ",
            "carrera": "DERECHO",
            "ci": "8123456-2L",
            "reg_univ": "2023045",
            "gestiones": [
                {
                    "gestion": "2023-1",
                    "materias": [
                        {"sigla": "DER-101", "materia": "INTRODUCCIÓN AL DERECHO", "paralelo": "A", "nota": 90, "folio": "1", "libro": "A", "observacion": "APROBADO", "docente": "Dr. CARLOS MENDOZA"},
                        {"sigla": "DER-102", "materia": "DERECHO CIVIL I", "paralelo": "B", "nota": 85, "folio": "2", "libro": "A", "observacion": "APROBADO", "docente": "Dra. MARÍA SÁNCHEZ"}
                    ]
                },
                {
                    "gestion": "2023-2",
                    "materias": [
                        {"sigla": "DER-201", "materia": "DERECHO PENAL", "paralelo": "A", "nota": 88, "folio": "1", "libro": "B", "observacion": "APROBADO", "docente": "Dr. PEDRO RAMÍREZ"},
                        {"sigla": "DER-202", "materia": "DERECHO CONSTITUCIONAL", "paralelo": "A", "nota": 91, "folio": "2", "libro": "B", "observacion": "APROBADO", "docente": "Dra. LUISA VARGAS"}
                    ]
                }
            ]
        }
    ]
    estudiantes.insert_many(estudiantes_data)
    print(f"✅ Colección 'estudiantes' → {estudiantes.count_documents({})} documentos")

    # 3. Colección: ambientes_disponibles
    ambientes_disp = db["ambientes_disponibles"]
    ambientes_disp.drop()
    ambientes_disp_data = [
        {"id": "AUD-CENTRAL-01", "nombre": "Auditorio Central", "capacidad": 300, "ubicacion": "Planta Baja, Monoblock Central"},
        {"id": "AULA-A-105", "nombre": "Aula A-105", "capacidad": 50, "ubicacion": "Edificio Académico, Primer Piso"},
        {"id": "LAB-INF-03", "nombre": "Laboratorio de Informática 3", "capacidad": 30, "ubicacion": "Edificio Nuevo, Segundo Piso"},
        {"id": "SAL-JUNT-02", "nombre": "Sala de Juntas Decanato", "capacidad": 20, "ubicacion": "Decanato, Tercer Piso"}
    ]
    ambientes_disp.insert_many(ambientes_disp_data)
    print(f"✅ Colección 'ambientes_disponibles' → {ambientes_disp.count_documents({})} documentos")

    # 4. Colección: ambientes (solicitudes)
    ambientes = db["ambientes"]
    ambientes.drop()
    ambientes_data = [
        {
            "id": "AMB-2026-00001",
            "estudiante_id": "2000001",
            "tipo": "solicitud_ambiente",
            "ambiente_id": "AUD-CENTRAL-01",
            "fecha_uso": "2026-06-15",
            "hora_inicio": "09:00",
            "hora_fin": "12:00",
            "motivo": "Defensa de trabajo de grado - Carrera de Informática",
            "asistentes": 45,
            "estado": "aprobada",
            "sello_digital": {
                "hash": generate_hash({"id": "AMB-2026-00001", "estudiante_id": "2000001", "ambiente_id": "AUD-CENTRAL-01"}),
                "timestamp": "2026-05-20T10:30:00",
                "qr_url": "/verificar/AMB-2026-00001"
            },
            "uso_confirmado": False,
            "created_at": "2026-05-20T10:30:00",
            "updated_at": "2026-05-20T14:15:00"
        },
        {
            "id": "AMB-2026-00002",
            "estudiante_id": "2000002",
            "tipo": "solicitud_ambiente",
            "ambiente_id": "SAL-JUNT-02",
            "fecha_uso": "2026-06-20",
            "hora_inicio": "15:00",
            "hora_fin": "17:00",
            "motivo": "Reunión de comité de tesis - Facultad de Derecho",
            "asistentes": 12,
            "estado": "pendiente",
            "sello_digital": {
                "hash": generate_hash({"id": "AMB-2026-00002", "estudiante_id": "2000002", "ambiente_id": "SAL-JUNT-02"}),
                "timestamp": "2026-05-22T09:00:00",
                "qr_url": "/verificar/AMB-2026-00002"
            },
            "uso_confirmado": False,
            "created_at": "2026-05-22T09:00:00"
        },
        {
            "id": "AMB-2026-00003",
            "estudiante_id": "2000001",
            "tipo": "solicitud_ambiente",
            "ambiente_id": "LAB-INF-03",
            "fecha_uso": "2026-05-28",
            "hora_inicio": "08:00",
            "hora_fin": "10:00",
            "motivo": "Taller de programación avanzada - Grupo de estudio",
            "asistentes": 25,
            "estado": "aprobada",
            "sello_digital": {
                "hash": generate_hash({"id": "AMB-2026-00003", "estudiante_id": "2000001", "ambiente_id": "LAB-INF-03"}),
                "timestamp": "2026-05-23T11:00:00",
                "qr_url": "/verificar/AMB-2026-00003"
            },
            "uso_confirmado": True,
            "created_at": "2026-05-23T11:00:00",
            "updated_at": "2026-05-23T16:30:00"
        }
    ]
    ambientes.insert_many(ambientes_data)
    print(f"✅ Colección 'ambientes' → {ambientes.count_documents({})} documentos")

    # 5. Colección: certificados
    certificados = db["certificados"]
    certificados.drop()
    certificados_data = [
        {
            "id": "CERT-2026-00001",
            "estudiante_id": "2000001",
            "tipo": "record_academico",
            "motivo_solicitud": "Postulación a beca de excelencia académica",
            "fecha_emision": "2026-05-15T10:00:00",
            "materias": [
                {"sigla": "INF-111", "materia": "PROGRAMACIÓN I", "nota": 54, "gestion": "2023 PRIMERO"},
                {"sigla": "INF-112", "materia": "FUNDAMENTOS DIGITALES", "nota": 71, "gestion": "2023 PRIMERO"},
                {"sigla": "INF-121", "materia": "PROGRAMACIÓN II", "nota": 54, "gestion": "2023 SEGUNDO"},
                {"sigla": "INF-122", "materia": "PROGRAMACIÓN WEB II", "nota": 53, "gestion": "2023 VERANO"},
                {"sigla": "INF-124", "materia": "ESTADÍSTICA I", "nota": 75, "gestion": "2024 INVIERNO"},
                {"sigla": "INF-132", "materia": "BASE DE DATOS I", "nota": 64, "gestion": "2024 INVIERNO"}
            ],
            "promedio_general": 61.83,
            "sello_digital": {
                "hash": "a3f5c8e7d2b1a9f4e6d8c7b5a3f1e9d7c5b3a1f8e6d4c2b0a8f6e4d2c0b8a6",
                "firma_institucional": "UMSA-FIRMA-DIGITAL-INSTITUCIONAL",
                "timestamp": "2026-05-15T10:00:00",
                "qr_url": "/verificar/CERT-2026-00001"
            },
            "estado": "emitido",
            "descargas": 3,
            "created_at": "2026-05-15T10:00:00"
        },
        {
            "id": "CERT-2026-00002",
            "estudiante_id": "2000002",
            "tipo": "record_academico",
            "motivo_solicitud": "Postulación a auxiliatura de cátedra",
            "fecha_emision": "2026-05-18T14:30:00",
            "materias": [
                {"sigla": "DER-101", "materia": "INTRODUCCIÓN AL DERECHO", "nota": 90, "gestion": "2023-1"},
                {"sigla": "DER-102", "materia": "DERECHO CIVIL I", "nota": 85, "gestion": "2023-1"},
                {"sigla": "DER-201", "materia": "DERECHO PENAL", "nota": 88, "gestion": "2023-2"},
                {"sigla": "DER-202", "materia": "DERECHO CONSTITUCIONAL", "nota": 91, "gestion": "2023-2"}
            ],
            "promedio_general": 88.5,
            "sello_digital": {
                "hash": "b7e2d9f4c1a8e5b2d9f6c3a0e7d4b1f8e5c2a9f6d3b0e7c4a1f8e5d2b9c6a3f0",
                "firma_institucional": "UMSA-FIRMA-DIGITAL-INSTITUCIONAL",
                "timestamp": "2026-05-18T14:30:00",
                "qr_url": "/verificar/CERT-2026-00002"
            },
            "estado": "emitido",
            "descargas": 1,
            "created_at": "2026-05-18T14:30:00"
        }
    ]
    certificados.insert_many(certificados_data)
    print(f"✅ Colección 'certificados' → {certificados.count_documents({})} documentos")

    print("\n🎉 MongoDB inicializado exitosamente")
    print("   Base de datos: umsa_digital")
    print("   Colecciones: usuarios, estudiantes, ambientes_disponibles, ambientes, certificados")
    print("\n🚀 Ahora ejecuta: python run.py")

    client.close()

if __name__ == "__main__":
    init_mongodb()
