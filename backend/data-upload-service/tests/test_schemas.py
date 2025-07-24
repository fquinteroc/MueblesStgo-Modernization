import pytest
from marshmallow import ValidationError
from src.schemas.data_schema import DataSchema, DataStatsSchema, FileUploadResponseSchema
from src.models.data import Data

class TestDataSchema:
    """Pruebas para el schema de datos"""
    
    @pytest.fixture
    def schema(self):
        """Instancia del schema para testing"""
        return DataSchema()
    
    def test_serialize_data_model(self, schema):
        """Test de serialización de modelo Data"""
        data = Data(
            id=1,
            fecha='2023/10/15',
            hora='08:00',
            rut='12345678-9'
        )
        
        result = schema.dump(data)
        
        assert result['id'] == 1
        assert result['fecha'] == '2023/10/15'
        assert result['hora'] == '08:00'
        assert result['rut'] == '12345678-9'
    
    def test_serialize_multiple_data(self, schema):
        """Test de serialización de múltiples registros"""
        data_list = [
            Data(id=1, fecha='2023/10/15', hora='08:00', rut='12345678-9'),
            Data(id=2, fecha='2023/10/15', hora='17:30', rut='12345678-9')
        ]
        
        schema_many = DataSchema(many=True)
        result = schema_many.dump(data_list)
        
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['id'] == 2
    
    def test_deserialize_valid_data(self, schema):
        """Test de deserialización de datos válidos"""
        valid_data = {
            'fecha': '2023/10/15',
            'hora': '08:00',
            'rut': '12345678-9'
        }
        
        result = schema.load(valid_data)
        
        assert result['fecha'] == '2023/10/15'
        assert result['hora'] == '08:00'
        assert result['rut'] == '12345678-9'
    
    def test_validate_fecha_format(self, schema):
        """Test de validación del formato de fecha"""
        # Fechas válidas
        valid_dates = [
            '2023/10/15',
            '2023/01/01',
            '2023/12/31'
        ]
        
        for fecha in valid_dates:
            data = {'fecha': fecha, 'hora': '08:00', 'rut': '12345678-9'}
            result = schema.load(data)
            assert result['fecha'] == fecha
        
        # Fechas inválidas
        invalid_dates = [
            '2023-10-15',   # Guiones
            '15/10/2023',   # Formato DD/MM/YYYY
            '2023/10/32',   # Día inválido
            'invalid',      # Texto
            '23/10/15'      # Año corto
        ]
        
        for fecha in invalid_dates:
            data = {'fecha': fecha, 'hora': '08:00', 'rut': '12345678-9'}
            with pytest.raises(ValidationError):
                schema.load(data)
    
    def test_validate_hora_format(self, schema):
        """Test de validación del formato de hora"""
        # Horas válidas
        valid_times = [
            '08:00',
            '23:59',
            '00:00',
            '12:30'
        ]
        
        for hora in valid_times:
            data = {'fecha': '2023/10/15', 'hora': hora, 'rut': '12345678-9'}
            result = schema.load(data)
            assert result['hora'] == hora
        
        # Horas inválidas
        invalid_times = [
            '8:00',      # Sin cero
            '24:00',     # Hora inválida
            '23:60',     # Minutos inválidos
            '08-00',     # Guiones
            'invalid'    # Texto
        ]
        
        for hora in invalid_times:
            data = {'fecha': '2023/10/15', 'hora': hora, 'rut': '12345678-9'}
            with pytest.raises(ValidationError):
                schema.load(data)
    
    def test_validate_rut_format(self, schema):
        """Test de validación del formato de RUT"""
        # RUTs válidos
        valid_ruts = [
            '12345678-9',
            '1234567-8',
            '12345-6',
            '1-9',
            '87654321-K',
            '11111111-k'
        ]
        
        for rut in valid_ruts:
            data = {'fecha': '2023/10/15', 'hora': '08:00', 'rut': rut}
            result = schema.load(data)
            assert result['rut'] == rut
        
        # RUTs inválidos
        invalid_ruts = [
            '12345678',      # Sin guión
            '12345678-',     # Sin dígito verificador
            '123456789-9',   # Muy largo
            'abcdefgh-9',    # Letras
            '12345678-99',   # DV muy largo
            '12345678_9'     # Guión bajo
        ]
        
        for rut in invalid_ruts:
            data = {'fecha': '2023/10/15', 'hora': '08:00', 'rut': rut}
            with pytest.raises(ValidationError):
                schema.load(data)
    
    def test_required_fields(self, schema):
        """Test de campos requeridos"""
        required_fields = ['fecha', 'hora', 'rut']
        
        for field in required_fields:
            data = {'fecha': '2023/10/15', 'hora': '08:00', 'rut': '12345678-9'}
            del data[field]
            
            with pytest.raises(ValidationError) as exc_info:
                schema.load(data)
            assert field in exc_info.value.messages
    
    def test_post_load_validation(self, schema):
        """Test de validación adicional en post_load"""
        # Datos válidos
        valid_data = {
            'fecha': '2023/10/15',
            'hora': '08:00',
            'rut': '12345678-9'
        }
        
        result = schema.load(valid_data)
        assert result is not None
        
        # Fecha inválida para datetime
        invalid_data = {
            'fecha': '2023/02/30',  # 30 de febrero no existe
            'hora': '08:00',
            'rut': '12345678-9'
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_data)
        assert 'fecha' in exc_info.value.messages

class TestDataStatsSchema:
    """Pruebas para el schema de estadísticas"""
    
    @pytest.fixture
    def schema(self):
        return DataStatsSchema()
    
class TestFileUploadResponseSchema:
    """Pruebas para el schema de respuesta de carga de archivos"""
    
    @pytest.fixture
    def schema(self):
        return FileUploadResponseSchema()
    
    def test_serialize_success_response(self, schema):
        """Test de serialización de respuesta exitosa"""
        response_data = {
            'success': True,
            'message': 'Archivo procesado exitosamente',
            'registros_procesados': 50,
            'errors': []
        }
        
        result = schema.dump(response_data)
        
        assert result['success'] is True
        assert result['message'] == 'Archivo procesado exitosamente'
        assert result['registros_procesados'] == 50
        assert result['errors'] == []
    
    def test_serialize_error_response(self, schema):
        """Test de serialización de respuesta con errores"""
        response_data = {
            'success': False,
            'message': 'Error procesando archivo',
            'registros_procesados': 0,
            'errors': ['Línea 5: formato inválido', 'Línea 10: RUT inválido']
        }
        
        result = schema.dump(response_data)
        
        assert result['success'] is False
        assert result['message'] == 'Error procesando archivo'
        assert result['registros_procesados'] == 0
        assert len(result['errors']) == 2
