import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock, mock_open
from io import BytesIO
from werkzeug.datastructures import FileStorage
from src.services.subir_data_service import SubirDataService
from src.errors.errors import BadRequest
from src.models.data import Data

class TestSubirDataService:
    """Pruebas para el servicio de subida de datos"""
    
    @pytest.fixture
    def service(self):
        """Instancia del servicio para testing"""
        return SubirDataService()
    
    @pytest.fixture
    def valid_file(self):
        """Archivo válido para testing"""
        return FileStorage(
            stream=BytesIO(b'test content'),
            filename='DATA.TXT',
            content_type='text/plain'
        )
    
    @pytest.fixture
    def invalid_filename_file(self):
        """Archivo con nombre inválido"""
        return FileStorage(
            stream=BytesIO(b'test content'),
            filename='WRONG.TXT',
            content_type='text/plain'
        )
    
    def test_guardar_success(self, service, valid_file):
        """Test de guardado exitoso de archivo"""
        with patch('src.services.subir_data_service.os.makedirs') as mock_makedirs, \
             patch('src.services.subir_data_service.secure_filename') as mock_secure, \
             patch.object(valid_file, 'save') as mock_save:
            
            mock_secure.return_value = 'DATA.TXT'
            
            result = service.guardar(valid_file)
            
            mock_makedirs.assert_called_once_with('uploads', exist_ok=True)
            mock_secure.assert_called_once_with('DATA.TXT')
            mock_save.assert_called_once()
            assert result == 'uploads/DATA.TXT'
    
    def test_guardar_invalid_file(self, service, invalid_filename_file):
        """Test de guardado con archivo inválido"""
        with patch.object(service.validator, 'validate_file') as mock_validate:
            mock_validate.side_effect = BadRequest('Archivo inválido')
            
            with pytest.raises(BadRequest):
                service.guardar(invalid_filename_file)
    
    def test_leer_txt_success(self, service, app):
        """Test de lectura exitosa de archivo TXT"""
        with app.app_context():
            file_content = """2023/10/15;08:00;12345678-9
2023/10/15;17:30;12345678-9
2023/10/16;08:15;87654321-0"""
            
            with patch('builtins.open', mock_open(read_data=file_content)), \
                 patch.object(service, '_limpiar_datos_previos') as mock_limpiar, \
                 patch.object(service.data_repository, 'add') as mock_add, \
                 patch.object(service.validator, 'validate_line_format') as mock_validate:
                
                # Configurar mock del validador
                mock_validate.side_effect = [
                    ('2023/10/15', '08:00', '12345678-9'),
                    ('2023/10/15', '17:30', '12345678-9'),
                    ('2023/10/16', '08:15', '87654321-0')
                ]
                
                result = service.leer_txt('/fake/path/DATA.TXT')
                
                # Verificaciones
                mock_limpiar.assert_called_once()
                assert mock_add.call_count == 3
                assert result['registros_procesados'] == 3
                assert 'exitosamente' in result['mensaje']
    
    def test_leer_txt_empty_file(self, service, app):
        """Test de lectura de archivo vacío"""
        with app.app_context():
            with patch('builtins.open', mock_open(read_data="")), \
                 patch.object(service, '_limpiar_datos_previos') as mock_limpiar, \
                 patch.object(service.data_repository, 'add') as mock_add:
                
                result = service.leer_txt('/fake/path/DATA.TXT')
                
                mock_limpiar.assert_called_once()
                mock_add.assert_not_called()
                assert result['registros_procesados'] == 0
    
    def test_leer_txt_with_empty_lines(self, service, app):
        """Test de lectura de archivo con líneas vacías"""
        with app.app_context():
            file_content = """2023/10/15;08:00;12345678-9

2023/10/15;17:30;12345678-9
            
2023/10/16;08:15;87654321-0"""
            
            with patch('builtins.open', mock_open(read_data=file_content)), \
                 patch.object(service, '_limpiar_datos_previos'), \
                 patch.object(service.data_repository, 'add') as mock_add, \
                 patch.object(service.validator, 'validate_line_format') as mock_validate:
                
                mock_validate.side_effect = [
                    ('2023/10/15', '08:00', '12345678-9'),
                    ('2023/10/15', '17:30', '12345678-9'),
                    ('2023/10/16', '08:15', '87654321-0')
                ]
                
                result = service.leer_txt('/fake/path/DATA.TXT')
                
                # Solo debe procesar 3 líneas (ignorando las vacías)
                assert mock_add.call_count == 3
                assert result['registros_procesados'] == 3
    
    def test_leer_txt_validation_error(self, service, app):
        """Test de lectura con error de validación"""
        with app.app_context():
            file_content = """2023/10/15;08:00;12345678-9
invalid;line;format"""
            
            with patch('builtins.open', mock_open(read_data=file_content)), \
                 patch.object(service, '_limpiar_datos_previos'), \
                 patch.object(service.data_repository, 'rollback') as mock_rollback, \
                 patch.object(service.validator, 'validate_line_format') as mock_validate:
                
                # Primera línea válida, segunda inválida
                mock_validate.side_effect = [
                    ('2023/10/15', '08:00', '12345678-9'),
                    BadRequest('Formato inválido en línea 2')
                ]
                
                with pytest.raises(BadRequest) as exc_info:
                    service.leer_txt('/fake/path/DATA.TXT')
                
                assert 'Formato inválido en línea 2' in str(exc_info.value)
                mock_rollback.assert_called_once()
    
    def test_leer_txt_general_error(self, service, app):
        """Test de lectura con error general"""
        with app.app_context():
            with patch('builtins.open', side_effect=IOError('File not found')), \
                 patch.object(service.data_repository, 'rollback') as mock_rollback:
                
                with pytest.raises(BadRequest) as exc_info:
                    service.leer_txt('/fake/path/DATA.TXT')
                
                assert 'Error procesando archivo' in str(exc_info.value)
                mock_rollback.assert_called_once()
    
    def test_limpiar_datos_previos(self, service):
        """Test de limpieza de datos previos"""
        with patch.object(service.data_repository, 'delete_all') as mock_delete:
            service._limpiar_datos_previos()
            mock_delete.assert_called_once()
    
    def test_obtener_todos_los_datos(self, service):
        """Test de obtención de todos los datos"""
        mock_data = [Data(), Data(), Data()]
        with patch.object(service.data_repository, 'find_all', return_value=mock_data) as mock_find:
            result = service.obtener_todos_los_datos()
            
            mock_find.assert_called_once()
            assert result == mock_data
            assert len(result) == 3
    
    def test_obtener_datos_por_rut(self, service):
        """Test de obtención de datos por RUT"""
        rut = '12345678-9'
        mock_data = [Data(rut=rut), Data(rut=rut)]
        
        with patch.object(service.data_repository, 'find_by_rut', return_value=mock_data) as mock_find:
            result = service.obtener_datos_por_rut(rut)
            
            mock_find.assert_called_once_with(rut)
            assert result == mock_data
            assert len(result) == 2
    
    def test_obtener_ruts_distintos(self, service):
        """Test de obtención de RUTs únicos"""
        mock_ruts = ['12345678-9', '87654321-0', '11111111-1']
        
        with patch.object(service.data_repository, 'find_distinct_rut', return_value=mock_ruts) as mock_find:
            result = service.obtener_ruts_distintos()
            
            mock_find.assert_called_once()
            assert result == mock_ruts
            assert len(result) == 3
    
    def test_constants(self):
        """Test de las constantes del servicio"""
        from src.services.subir_data_service import ALLOWED_NAME, UPLOAD_FOLDER
        
        assert ALLOWED_NAME == 'DATA.TXT'
        assert UPLOAD_FOLDER == 'uploads'
