import os
import logging
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text
from src.database import db, migrate
from src.blueprints.employee_controller import bp as employee_bp
from src.errors.errors import APIError, BadRequest, NotFound, Forbidden
from src.config import config

def create_app(config_name=None):
    """Factory para crear la aplicación Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)
    
    setup_logging(app)
    
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(employee_bp)
    
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Tablas de base de datos creadas/verificadas")
        except Exception as e:
            app.logger.error(f"Error creando tablas: {str(e)}")
    
    register_error_handlers(app)
    
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
        app.logger.info('MueblesStgo Employee Management Service startup')

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
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            'success': False,
            'error': 'Método no permitido',
            'code': 405
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        app.logger.error(f"Internal Server Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'code': 500
        }), 500

def register_additional_routes(app):
    """Registrar rutas adicionales de la aplicación"""
    
    @app.route('/')
    def index():
        """Ruta raíz con información del microservicio"""
        return jsonify({
            'service': 'MueblesStgo Employee Management Service',
            'version': '1.0.0',
            'status': 'running',
            'description': 'Microservicio para gestión completa de empleados',
            'endpoints': {
                'employees': {
                    'create': 'POST /api/employees',
                    'get_all': 'GET /api/employees',
                    'get_by_rut': 'GET /api/employees/{rut}',
                    'update': 'PUT /api/employees/{rut}',
                    'delete': 'DELETE /api/employees/{rut}',
                    'activate': 'PATCH /api/employees/{rut}/activate',
                    'by_category': 'GET /api/employees/category/{category}',
                    'search': 'GET /api/employees/search?name={name}',
                    'get_category': 'GET /api/employees/{rut}/category',
                    'by_date_range': 'GET /api/employees/date-range?start_date={start}&end_date={end}',
                    'statistics': 'GET /api/employees/stats'
                },
                'health': {
                    'ping': 'GET /api/ping',
                    'health_detailed': 'GET /health'
                }
            },
            'features': [
                'CRUD completo de empleados',
                'Validación de RUT chileno',
                'Soft delete de empleados',
                'Búsqueda por nombre y categoría',
                'Filtros por fecha de ingreso',
                'Estadísticas de empleados',
                'Paginación de resultados'
            ]
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
            'service': 'employee-management-service',
            'status': 'healthy',
            'database': db_status,
            'environment': app.config.get('ENV', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'features': {
                'employees_management': 'active',
                'data_validation': 'active',
                'soft_delete': 'active',
                'search_capabilities': 'active'
            }
        })
    
    @app.route('/api/health')
    def api_health():
        """Health check específico para la API"""
        try:
            # Importar aquí para evitar importación circular
            from src.services.employee_service import EmployeeService
            
            service = EmployeeService()
            employee_count = service.get_active_employees_count()
            
            return jsonify({
                'api_status': 'healthy',
                'service': 'employee-management-service',
                'employee_count': employee_count,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            app.logger.error(f"API health check failed: {str(e)}")
            return jsonify({
                'api_status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5002))
    host = os.getenv('HOST', '0.0.0.0')
    
    app.logger.info(f"Iniciando Employee Management Service en {host}:{port}")
    app.run(host=host, port=port, debug=app.config.get('DEBUG', False))
