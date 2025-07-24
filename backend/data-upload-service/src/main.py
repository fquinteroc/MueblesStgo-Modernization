import os
import logging
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text
from src.database import db, migrate
from src.blueprints.subir_data_controller import bp as subir_bp
from src.errors.errors import APIError, BadRequest, NotFound, Forbidden
from src.config import config

def create_app(config_name=None):
    """Factory para crear la aplicación Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    app.config.from_object(config.get(config_name, config['default']))
    
    setup_logging(app)
    
    # Configurar CORS para Angular
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Crear directorio de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Registrar blueprints
    app.register_blueprint(subir_bp)
    
    # Crear tablas si no existen
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Tablas de base de datos creadas/verificadas")
        except Exception as e:
            app.logger.error(f"Error creando tablas: {str(e)}")
    
    # Manejadores de errores
    register_error_handlers(app)
    
    # Endpoints adicionales
    register_additional_routes(app)
    
    return app

def setup_logging(app):
    """Configurar logging de la aplicación"""
    if not app.debug and not app.testing:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('MueblesStgo Data Upload Service startup')

def register_error_handlers(app):
    """Registrar manejadores de errores personalizados"""
    
    @app.errorhandler(APIError)
    def handle_api_error(e):
        app.logger.error(f"API Error: {e.description}")
        return jsonify({
            'success': False,
            'error': e.description,
            'code': e.code
        }), e.code
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            'success': False,
            'error': 'Endpoint no encontrado',
            'code': 404
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        app.logger.error(f"Internal Server Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'code': 500
        }), 500
    
    @app.errorhandler(413)
    def handle_file_too_large(e):
        return jsonify({
            'success': False,
            'error': 'Archivo demasiado grande. Máximo 16MB.',
            'code': 413
        }), 413

def register_additional_routes(app):
    """Registrar rutas adicionales de la aplicación"""
    
    @app.route('/')
    def index():
        """Ruta raíz con información del microservicio"""
        return jsonify({
            'service': 'MueblesStgo Data Upload Service',
            'version': '1.0.0',
            'status': 'running',
            'description': 'Microservicio para carga y procesamiento de archivos de marcaciones',
            'endpoints': {
                'upload': 'POST /upload',
                'get_data': 'GET /data',
                'get_data_by_rut': 'GET /data/rut/<rut>',
                'get_ruts': 'GET /ruts',
                'get_stats': 'GET /stats',
                'health': 'GET /ping',
                'health_detailed': 'GET /health'
            }
        })
    
    @app.route('/health')
    def health_check():
        """Endpoint de verificación de salud del servicio"""
        try:
            db.session.execute(text('SELECT 1'))
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'
            app.logger.error(f"Database health check failed: {str(e)}")
        
        return jsonify({
            'service': 'data-upload-service',
            'status': 'healthy',
            'database': db_status,
            'environment': app.config.get('ENV', 'unknown'),
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    app.logger.info(f"Iniciando servidor en {host}:{port}")
    app.run(host=host, port=port, debug=app.config.get('DEBUG', False))