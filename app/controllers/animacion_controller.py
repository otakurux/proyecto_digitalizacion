from flask import Blueprint, send_from_directory
import os

animacion_bp = Blueprint('animacion', __name__)

# Ruta absoluta a la carpeta animacion_webGL (está en la raíz del proyecto)
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../animacion_webGL"
    )
)

@animacion_bp.route('/')
def index():
    """Sirve la página principal de Unity WebGL."""
    return send_from_directory(BASE_DIR, 'index.html')

@animacion_bp.route('/Build/<path:filename>')
def build_files(filename):
    """Sirve los archivos de compilación: .data, .framework.js, .loader.js, .wasm"""
    return send_from_directory(os.path.join(BASE_DIR, 'Build'), filename)

@animacion_bp.route('/TemplateData/<path:filename>')
def template_data(filename):
    """Sirve los recursos estáticos: CSS, imágenes, favicon de Unity."""
    return send_from_directory(os.path.join(BASE_DIR, 'TemplateData'), filename)