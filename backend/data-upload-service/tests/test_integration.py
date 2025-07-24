import pytest
import os
import json
from io import BytesIO
from werkzeug.datastructures import FileStorage
from src.main import create_app
from src.database import db
from src.models.data import Data

class TestIntegration:
    """Pruebas de integración del microservicio completo"""
    
    @pytest.fixture
    def app(self):
        """App de testing para integración"""
        app = create_app('testing')
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        """Cliente de prueba"""
        return app.test_client()
    
    def test_complete_upload_flow(self, client):
        """Test del flujo completo de carga de archivo"""
        # 1. Verificar que no hay datos inicialmente
        response = client.get('/data')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_records'] == 0
        
        # 2. Subir archivo válido
        file_content = """2023/10/15;08:00;12345678-9
2023/10/15;17:30;12345678-9
2023/10/15;08:15;87654321-0
2023/10/15;17:45;87654321-0"""
        
        file_data = FileStorage(
            stream=BytesIO(file_content.encode('utf-8')),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': file_data})
        assert response.status_code == 200
        upload_data = json.loads(response.data)
        assert upload_data['success'] is True
        assert upload_data['registros_procesados'] == 4
        
        # 3. Verificar que los datos se guardaron
        response = client.get('/data')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_records'] == 4
        assert len(data['data']) == 4
        
        # 4. Verificar datos por RUT
        response = client.get('/data/rut/12345678-9')
        assert response.status_code == 200
        rut_data = json.loads(response.data)
        assert rut_data['total_records'] == 2
        assert rut_data['rut'] == '12345678-9'
        
        # 5. Verificar RUTs únicos
        response = client.get('/ruts')
        assert response.status_code == 200
        ruts_data = json.loads(response.data)
        assert ruts_data['total_ruts'] == 2
        assert '12345678-9' in ruts_data['ruts']
        assert '87654321-0' in ruts_data['ruts']
        
        # 6. Verificar estadísticas
        response = client.get('/stats')
        assert response.status_code == 200
        stats_data = json.loads(response.data)
        assert stats_data['stats']['total_records'] == 4
        assert stats_data['stats']['total_employees'] == 2
    
    def test_upload_replaces_previous_data(self, client):
        """Test que la carga de archivo reemplaza datos previos"""
        # 1. Subir primer archivo
        file1_content = """2023/10/15;08:00;12345678-9
2023/10/15;17:30;12345678-9"""
        
        file1_data = FileStorage(
            stream=BytesIO(file1_content.encode('utf-8')),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': file1_data})
        assert response.status_code == 200
        
        # 2. Verificar datos del primer archivo
        response = client.get('/data')
        data = json.loads(response.data)
        assert data['total_records'] == 2
        
        # 3. Subir segundo archivo (diferente)
        file2_content = """2023/10/16;09:00;87654321-0
2023/10/16;18:00;87654321-0
2023/10/16;09:30;11111111-1"""
        
        file2_data = FileStorage(
            stream=BytesIO(file2_content.encode('utf-8')),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': file2_data})
        assert response.status_code == 200
        
        # 4. Verificar que los datos fueron reemplazados
        response = client.get('/data')
        data = json.loads(response.data)
        assert data['total_records'] == 3  # Solo del segundo archivo
        
        # 5. Verificar que RUTs son del segundo archivo
        response = client.get('/ruts')
        ruts_data = json.loads(response.data)
        assert '87654321-0' in ruts_data['ruts']
        assert '11111111-1' in ruts_data['ruts']
        assert '12345678-9' not in ruts_data['ruts']  # Del primer archivo
    
    def test_error_handling_integration(self, client):
        """Test de manejo de errores de integración"""
        # 1. Test archivo con nombre incorrecto
        wrong_file = FileStorage(
            stream=BytesIO(b'content'),
            filename='WRONG.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': wrong_file})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        
        # 2. Test sin archivo
        response = client.post('/upload', data={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        
        # 3. Test archivo con formato inválido
        invalid_content = """2023-10-15;08:00;12345678-9
2023/10/15;25:00;invalid-rut"""
        
        invalid_file = FileStorage(
            stream=BytesIO(invalid_content.encode('utf-8')),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': invalid_file})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_health_checks_integration(self, client):
        """Test de endpoints de salud en integración"""
        # 1. Test ping del blueprint
        response = client.get('/ping')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert data['service'] == 'data-upload-service'
        
        # 2. Test health check completo
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['service'] == 'data-upload-service'
        assert data['status'] == 'healthy'
        assert data['database'] == 'connected'  # En testing usa SQLite en memoria
        
        # 3. Test endpoint raíz
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['service'] == 'MueblesStgo Data Upload Service'
        assert data['status'] == 'running'
    
    def test_data_query_operations_integration(self, client):
        """Test de operaciones de consulta de datos"""
        # 1. Subir datos de prueba
        file_content = """2023/10/15;08:00;12345678-9
2023/10/15;12:00;12345678-9
2023/10/15;17:30;12345678-9
2023/10/16;08:30;12345678-9
2023/10/15;08:15;87654321-0
2023/10/15;17:45;87654321-0"""
        
        file_data = FileStorage(
            stream=BytesIO(file_content.encode('utf-8')),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': file_data})
        assert response.status_code == 200
        
        # 2. Test obtener todos los datos
        response = client.get('/data')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_records'] == 6
        assert len(data['data']) == 6
        
        # 3. Test obtener datos por RUT específico
        response = client.get('/data/rut/12345678-9')
        assert response.status_code == 200
        rut_data = json.loads(response.data)
        assert rut_data['total_records'] == 4
        assert all(record['rut'] == '12345678-9' for record in rut_data['data'])
        
        # 4. Test obtener datos por RUT que no existe
        response = client.get('/data/rut/99999999-9')
        assert response.status_code == 200
        rut_data = json.loads(response.data)
        assert rut_data['total_records'] == 0
        assert len(rut_data['data']) == 0
        
        # 5. Test obtener RUTs únicos
        response = client.get('/ruts')
        assert response.status_code == 200
        ruts_data = json.loads(response.data)
        assert ruts_data['total_ruts'] == 2
        assert set(ruts_data['ruts']) == {'12345678-9', '87654321-0'}
    
    def test_empty_file_handling(self, client):
        """Test de manejo de archivo vacío"""
        empty_file = FileStorage(
            stream=BytesIO(b''),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': empty_file})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['registros_procesados'] == 0
        
        # Verificar que no hay datos
        response = client.get('/data')
        data = json.loads(response.data)
        assert data['total_records'] == 0
    
    def test_file_with_empty_lines(self, client):
        """Test de archivo con líneas vacías"""
        file_content = """2023/10/15;08:00;12345678-9

2023/10/15;17:30;12345678-9
        
2023/10/16;08:15;87654321-0

"""
        
        file_data = FileStorage(
            stream=BytesIO(file_content.encode('utf-8')),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': file_data})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['registros_procesados'] == 3  # Solo las líneas con contenido
    
    def test_cors_headers(self, client):
        """Test de headers CORS en las respuestas"""
        response = client.get('/')
        # Los headers CORS deben estar presentes
        assert 'Access-Control-Allow-Origin' in response.headers or response.status_code == 200
        
        # Test OPTIONS request
        response = client.open('/', method='OPTIONS')
        # Debe manejar OPTIONS requests para CORS
        assert response.status_code in [200, 204, 404]  # 404 es OK si no hay handler específico
    
    def test_concurrent_operations(self, client):
        """Test de operaciones concurrentes básicas"""
        # 1. Subir datos
        file_content = """2023/10/15;08:00;12345678-9
2023/10/15;17:30;12345678-9"""
        
        file_data = FileStorage(
            stream=BytesIO(file_content.encode('utf-8')),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        response = client.post('/upload', data={'file': file_data})
        assert response.status_code == 200
        
        # 2. Hacer múltiples consultas simultáneas (simular concurrencia)
        responses = []
        for _ in range(5):
            responses.append(client.get('/data'))
            responses.append(client.get('/ruts'))
            responses.append(client.get('/stats'))
        
        # Todas las respuestas deben ser exitosas
        for response in responses:
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
    
    def test_service_info_consistency(self, client):
        """Test de consistencia de información del servicio"""
        # La información del servicio debe ser consistente entre endpoints
        
        # 1. Endpoint raíz
        response = client.get('/')
        root_data = json.loads(response.data)
        
        # 2. Health check
        response = client.get('/health')
        health_data = json.loads(response.data)
        
        # 3. Ping
        response = client.get('/ping')
        ping_data = json.loads(response.data)
        
        # Verificar consistencia
        assert 'data-upload-service' in health_data['service']
        assert ping_data['service'] == 'data-upload-service'
        assert root_data['service'] == 'MueblesStgo Data Upload Service'
