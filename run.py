from app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    # Silenciar logs de peticiones HTTP (reduce ruido de Unity WebGL)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)

    print("🏛️  UMSA Digital iniciado")
    print("📍 http://localhost:5000")
    print("🎮 Animación Unity: http://localhost:5000/animacion/")
    print("=" * 50)

    app.run(debug=False, port=5000, use_reloader=False)
