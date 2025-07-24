import pytest
import json
from io import BytesIO
from werkzeug.datastructures import FileStorage
from unittest.mock import patch, MagicMock
from src.models.data import Data

class TestSubirDataController:
    """Pruebas para el controlador de subida de datos"""
    
    def test_ping_endpoint(self, client):
        """Test del endpoint de salud /ping"""
        response = client.get('/ping')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert data['service'] == 'data-upload-service'
    
    def test_upload_no_file(self, client):
        """Test de carga sin archivo"""
        response = client.post('/upload', data={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'No se ha proporcionado ningún archivo' in data['error']
    
    def test_get_data_success(self, client, populated_db):
        """Test de obtención exitosa de todos los datos"""
        with patch('src.blueprints.subir_data_controller.SubirDataService') as mock_service_class:
            mock_instance = MagicMock()
            mock_service_class.return_value = mock_instance
            
            # Crear datos mock
            mock_data = [
                Data(id=1, fecha='2023/10/15', hora='08:00', rut='12345678-9'),
                Data(id=2, fecha='2023/10/15', hora='17:30', rut='12345678-9')
            ]
            mock_instance.obtener_todos_los_datos.return_value = mock_data
            
            response = client.get('/data')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['total_records'] == 2
            assert len(data['data']) == 2
    
    def test_upload_success(self, client, sample_data_file):
        """Test de carga exitosa de archivo"""
        with patch('src.blueprints.subir_data_controller.SubirDataService') as mock_service_class:
            mock_instance = MagicMock()
            mock_service_class.return_value = mock_instance
            mock_instance.guardar.return_value = '/path/to/file.txt'
            mock_instance.leer_txt.return_value = {
                'mensaje': 'Archivo procesado exitosamente',
                'registros_procesados': 6
            }
            
            response = client.post('/upload', data={'file': sample_data_file})
            assert response.status_code == 200
            
            # Verificar que los métodos fueron llamados
            mock_instance.guardar.assert_called_once()
            mock_instance.leer_txt.assert_called_once_with('/path/to/file.txt')
    
    def test_get_data_by_rut_error(self, client):
        """Test de error al obtener datos por RUT"""
        with patch('src.blueprints.subir_data_controller.SubirDataService') as mock_service_class:
            mock_instance = MagicMock()
            mock_service_class.return_value = mock_instance
            mock_instance.obtener_datos_por_rut.side_effect = Exception('Database error')
            
            response = client.get('/data/rut/12345678-9')
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['success'] is False
            assert 'Error obteniendo datos' in data['error']
    
    def test_get_distinct_ruts_success(self, client):
        """Test de obtención exitosa de RUTs únicos"""
        with patch('src.blueprints.subir_data_controller.SubirDataService') as mock_service_class:
            mock_instance = MagicMock()
            mock_service_class.return_value = mock_instance
            mock_instance.obtener_ruts_distintos.return_value = ['12345678-9', '87654321-0']
            
            response = client.get('/ruts')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['total_ruts'] == 2
            assert '12345678-9' in data['ruts']
            assert '87654321-0' in data['ruts']
    
    def test_get_stats_success(self, client):
        """Test de obtención exitosa de estadísticas"""
        with patch('src.blueprints.subir_data_controller.SubirDataService') as mock_service_class:
            mock_instance = MagicMock()
            mock_service_class.return_value = mock_instance
            
            # Mock data
            mock_data = [Data() for _ in range(10)]  # 10 registros
            mock_ruts = ['12345678-9', '87654321-0']  # 2 empleados
            
            mock_instance.obtener_todos_los_datos.return_value = mock_data
            mock_instance.obtener_ruts_distintos.return_value = mock_ruts
            
            response = client.get('/stats')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['stats']['total_records'] == 10
            assert data['stats']['total_employees'] == 2
            assert data['stats']['service_status'] == 'active'
