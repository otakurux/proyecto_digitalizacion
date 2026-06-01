from flask import Flask, send_from_directory
import os
import logging

def create_app():
    app = Flask(__name__, 
                 template_folder='views/templates',
                 static_folder='views/static')
    app.secret_key = 'umsa_digital_secret_key_2026_seguro'

    # Silenciar logs de peticiones estáticas (reduce ruido de la animación Unity)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Solo mostrar errores, no INFO

    # Registrar blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.ambiente_controller import ambiente_bp
    from app.controllers.certificado_controller import certificado_bp
    from app.controllers.modelo3d_controller import modelo3d_bp
    from app.controllers.animacion_controller import animacion_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(ambiente_bp, url_prefix='/ambientes')
    app.register_blueprint(certificado_bp, url_prefix='/certificados')
    app.register_blueprint(modelo3d_bp, url_prefix='/visor3d')
    app.register_blueprint(animacion_bp, url_prefix='/animacion')

    return app
