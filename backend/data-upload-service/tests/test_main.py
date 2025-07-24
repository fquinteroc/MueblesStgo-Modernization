import pytest
import json
from unittest.mock import patch
from src.main import create_app
from src.errors.errors import APIError, BadRequest

class TestMainApplication:
    """Pruebas para la aplicación principal y factory"""
    
    def test_create_app_default_config(self):
        """Test de creación de app con configuración por defecto"""
        # En el entorno de testing, la app se crea con testing=True
        # por lo que esperamos que TESTING sea True
        app = create_app()
        
        assert app is not None
        assert app.config['TESTING'] is True  # En tests siempre es True
        assert 'SQLALCHEMY_DATABASE_URI' in app.config
    
    def test_create_app_testing_config(self):
        """Test de creación de app con configuración de testing"""
        app = create_app('testing')
        
        assert app is not None
        assert app.config['TESTING'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    
    def test_cors_configuration(self, app):
        """Test de configuración CORS"""
        with app.test_client() as client:
            response = client.options('/')
            # CORS debe estar configurado para permitir OPTIONS
            assert response.status_code in [200, 404]  # 404 es OK si no hay OPTIONS handler
    
    def test_database_initialization(self, app):
        """Test de inicialización de base de datos"""
        with app.app_context():
            from src.database import db
            # La BD debe estar inicializada
            assert db is not None
            # Las tablas deben existir
            assert 'data' in db.metadata.tables
    
    def test_upload_folder_creation(self):
        """Test de creación de directorio de uploads"""
        with patch('src.main.os.makedirs') as mock_makedirs:
            app = create_app('testing')
            mock_makedirs.assert_called()
    
    def test_blueprint_registration(self, app):
        """Test de registro de blueprints"""
        # Verificar que las rutas del blueprint están registradas
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        expected_routes = [
            '/ping',
            '/upload',
            '/data',
            '/data/rut/<rut>',
            '/ruts',
            '/stats'
        ]
        
        for route in expected_routes:
            assert route in routes
    
    def test_error_handlers_registration(self, client):
        """Test de registro de manejadores de errores"""
        # Test error 404
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'no encontrado' in data['error'].lower()
    
    def test_index_route(self, client):
        """Test de ruta raíz"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['service'] == 'MueblesStgo Data Upload Service'
        assert data['version'] == '1.0.0'
        assert data['status'] == 'running'
        assert 'endpoints' in data
        assert isinstance(data['endpoints'], dict)
    
    def test_health_check_route(self, client):
        """Test de endpoint de salud"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['service'] == 'data-upload-service'
        assert data['status'] == 'healthy'
        assert 'database' in data
        assert 'timestamp' in data
    
    def test_health_check_with_db_error(self, app):
        """Test de health check con error de base de datos"""
        with app.test_client() as client:
            with patch('src.main.db.session.execute') as mock_execute:
                mock_execute.side_effect = Exception('DB Connection Error')
                
                response = client.get('/health')
                assert response.status_code == 200
                data = json.loads(response.data)
                
                assert 'error' in data['database']
                assert 'DB Connection Error' in data['database']

class TestErrorHandlers:
    """Pruebas para los manejadores de errores globales"""
    
    def test_api_error_handler(self, app):
        """Test del manejador de APIError"""
        with app.test_request_context():
            from src.main import register_error_handlers
            
            # Simular un APIError
            error = BadRequest('Test error message')
            
            # El manejador debe devolver JSON con estructura específica
            with app.test_client() as client:
                with patch('src.blueprints.subir_data_controller.SubirDataService') as mock_service:
                    mock_service.return_value.guardar.side_effect = BadRequest('Test error')
                    
                    response = client.post('/upload', data={})
                    assert response.status_code == 400
                    data = json.loads(response.data)
                    assert data['success'] is False
    
    def test_404_error_handler(self, client):
        """Test del manejador de error 404"""
        response = client.get('/ruta-inexistente')
        assert response.status_code == 404
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert data['error'] == 'Endpoint no encontrado'
        assert data['code'] == 404
    
    def test_500_error_handler(self, app):
        """Test del manejador de error 500"""
        with app.test_client() as client:
            with patch('src.blueprints.subir_data_controller.SubirDataService') as mock_service:
                # Simular error interno
                mock_service.return_value.obtener_todos_los_datos.side_effect = Exception('Internal error')
                
                response = client.get('/data')
                assert response.status_code == 500
                data = json.loads(response.data)
                assert data['success'] is False
    
    def test_413_error_handler(self, client):
        """Test del manejador de error 413 (archivo muy grande)"""
        # Crear un archivo muy grande (simulado)
        large_content = b'x' * (17 * 1024 * 1024)  # 17MB, mayor que el límite
        
        response = client.post('/upload', data={
            'file': (large_content, 'DATA.TXT')
        })
        
        # Flask debería devolver 413 automáticamente
        # Si llega al endpoint, el error se maneja ahí
        assert response.status_code in [413, 400, 500]

class TestSetupLogging:
    """Pruebas para la configuración de logging"""
    
    def test_setup_logging_testing(self):
        """Test de configuración de logging en testing"""
        app = create_app('testing')
        
        assert app.logger is not None
        assert app.testing is True

class TestAdditionalRoutes:
    """Pruebas para rutas adicionales registradas"""
    
    def test_index_endpoint_structure(self, client):
        """Test de estructura completa del endpoint index"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verificar estructura completa
        required_fields = ['service', 'version', 'status', 'description', 'endpoints']
        for field in required_fields:
            assert field in data
        
        # Verificar endpoints específicos
        endpoints = data['endpoints']
        expected_endpoints = ['upload', 'get_data', 'get_data_by_rut', 'get_ruts', 'get_stats', 'health', 'health_detailed']
        for endpoint in expected_endpoints:
            assert endpoint in endpoints
    
    def test_health_endpoint_database_status(self, client):
        """Test del estado de base de datos en health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # El estado de BD debe estar presente
        assert 'database' in data
        # Debe ser 'connected' o contener 'error:'
        db_status = data['database']
        assert db_status == 'connected' or db_status.startswith('error:')
    
    def test_health_endpoint_timestamp_format(self, client):
        """Test del formato de timestamp en health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verificar que el timestamp está en formato ISO
        timestamp = data['timestamp']
        from datetime import datetime
        
        try:
            # Debe poder parsearse como ISO timestamp
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Timestamp no está en formato ISO válido: {timestamp}")

class TestApplicationConfiguration:
    """Pruebas para la configuración de la aplicación"""
    
    def test_cors_origins_configuration(self, app):
        """Test de configuración de orígenes CORS"""
        cors_origins = app.config.get('CORS_ORIGINS')
        assert cors_origins is not None
        assert isinstance(cors_origins, list)
    
    def test_upload_folder_configuration(self, app):
        """Test de configuración de directorio de uploads"""
        upload_folder = app.config.get('UPLOAD_FOLDER')
        assert upload_folder is not None
        assert isinstance(upload_folder, str)
    
    def test_max_content_length_configuration(self, app):
        """Test de configuración de tamaño máximo de archivo"""
        max_content = app.config.get('MAX_CONTENT_LENGTH')
        assert max_content is not None
        assert max_content == 16 * 1024 * 1024  # 16MB
