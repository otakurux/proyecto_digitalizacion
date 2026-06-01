from flask import Blueprint, send_from_directory
import os

modelo3d_bp = Blueprint('modelo3d', __name__)

# Carpeta donde están visor.html, visor.css, visor.js y cabeza.fbx
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../cabeza_3d"
    )
)

@modelo3d_bp.route('/')
def visor():
    """Sirve la página principal del visor 3D."""
    return send_from_directory(BASE_DIR, 'visor.html')

@modelo3d_bp.route('/visor.css')
def visor_css():
    """Sirve los estilos del visor."""
    return send_from_directory(BASE_DIR, 'visor.css')

@modelo3d_bp.route('/visor.js')
def visor_js():
    """Sirve el script del visor Three.js."""
    return send_from_directory(BASE_DIR, 'visor.js')

@modelo3d_bp.route('/cabeza.fbx')
def modelo_fbx():
    """Sirve el modelo 3D en formato FBX."""
    return send_from_directory(BASE_DIR, 'cabeza.fbx')