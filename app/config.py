# Configuración del sistema UMSA Digital
import os

class Config:
    SECRET_KEY = 'umsa_digital_secret_key_2026'
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    DEBUG = True

    # Configuración de sellos digitales
    SELLO_INSTITUCIONAL = 'UMSA-FIRMA-DIGITAL-INSTITUCIONAL'
    HASH_ALGORITHM = 'sha256'

    # Prefijos de IDs
    PREFIX_AMBIENTE = 'AMB-2026-'
    PREFIX_CERTIFICADO = 'CERT-2026-'
