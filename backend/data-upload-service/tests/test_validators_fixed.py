import pytest
from io import BytesIO
from werkzeug.datastructures import FileStorage
from src.validators.data_validator import DataValidator
from src.errors.errors import BadRequest

class TestDataValidator:
    """Pruebas para el validador de datos"""
    
    def test_validate_fecha_valid(self):
        """Test de validación de fecha válida"""
        valid_dates = [
            '2023/10/15',
            '2023/01/01',
            '2023/12/31',
            '2024/02/29',  # Año bisiesto
            '1999/05/20'
        ]
        
        for fecha in valid_dates:
            assert DataValidator.validate_fecha(fecha) is True
    
    def test_validate_fecha_invalid_format(self):
        """Test de validación de fecha con formato inválido"""
        invalid_dates = [
            '2023-10-15',  # Guiones en lugar de barras
            '15/10/2023',  # Formato DD/MM/YYYY
            '10/15/2023',  # Formato MM/DD/YYYY
            '23/10/15',    # Año de 2 dígitos
            '2023/1/1',    # Sin ceros a la izquierda
            'invalid_date',
            '',
        ]
        
        for fecha in invalid_dates:
            with pytest.raises(BadRequest) as exc_info:
                DataValidator.validate_fecha(fecha)
            assert 'Fecha inválida' in str(exc_info.value.description)
            assert 'yyyy/MM/dd' in str(exc_info.value.description)
    
    def test_validate_hora_valid(self):
        """Test de validación de hora válida"""
        valid_times = [
            '08:00',
            '17:30',
            '23:59',
            '00:00',
            '12:00',
            '09:15'
        ]
        
        for hora in valid_times:
            assert DataValidator.validate_hora(hora) is True
    
    def test_validate_hora_invalid_format(self):
        """Test de validación de hora con formato inválido"""
        invalid_times = [
            '8:00',     # Sin cero a la izquierda
            '08:0',     # Sin cero a la izquierda en minutos
            '08-00',    # Guiones en lugar de dos puntos
            '8am',      # Formato AM/PM
            'invalid_time',
            '',
        ]
        
        for hora in invalid_times:
            with pytest.raises(BadRequest) as exc_info:
                DataValidator.validate_hora(hora)
            assert 'Hora inválida' in str(exc_info.value.description)
            assert 'HH:mm' in str(exc_info.value.description)
    
    def test_validate_rut_valid(self):
        """Test de validación de RUT válido"""
        valid_ruts = [
            '12345678-9',
            '1234567-8',
            '12345-6',
            '1-9',
            '87654321-0',
            '11111111-K',
            '22222222-k'  # k minúscula también válida
        ]
        
        for rut in valid_ruts:
            assert DataValidator.validate_rut(rut) is True
    
    def test_validate_rut_invalid_format(self):
        """Test de validación de RUT con formato inválido"""
        invalid_ruts = [
            '12345678',      # Sin guión ni dígito verificador
            '12345678-',     # Sin dígito verificador
            '-9',            # Sin número
            '12345678-99',   # Dígito verificador de más de 1 carácter
            '12345678_9',    # Guión bajo en lugar de guión
            '12345678.9',    # Punto en lugar de guión
            '123456789-9',   # Más de 8 dígitos
            'abcdefgh-9',    # Letras en lugar de números
            '12345678-A',    # Dígito verificador inválido (no K ni número)
        ]
        
        for rut in invalid_ruts:
            with pytest.raises(BadRequest) as exc_info:
                DataValidator.validate_rut(rut)
            if rut is None or rut == '':
                assert 'RUT no puede estar vacío' in str(exc_info.value.description)
            else:
                assert 'RUT inválido' in str(exc_info.value.description)
                assert 'xxxxxxxx-x' in str(exc_info.value.description)
    
    def test_validate_rut_none_or_empty(self):
        """Test de validación de RUT nulo o vacío"""
        invalid_ruts = [None, '', '   ']
        
        for rut in invalid_ruts:
            with pytest.raises(BadRequest) as exc_info:
                DataValidator.validate_rut(rut)
            assert 'RUT no puede estar vacío' in str(exc_info.value.description)
    
    def test_validate_line_format_valid(self):
        """Test de validación de línea con formato válido"""
        valid_lines = [
            '2023/10/15;08:00;12345678-9',
            '2023/12/31;23:59;87654321-0',
            '2024/01/01;00:00;1234567-K'
        ]
        
        for i, line in enumerate(valid_lines, 1):
            fecha, hora, rut = DataValidator.validate_line_format(line, i)
            parts = line.split(';')
            assert fecha == parts[0]
            assert hora == parts[1]
            assert rut == parts[2]
    
    def test_validate_line_format_wrong_number_of_fields(self):
        """Test de validación de línea con número incorrecto de campos"""
        invalid_lines = [
            '2023/10/15;08:00',              # Solo 2 campos
            '2023/10/15;08:00;12345678-9;extra',  # 4 campos
            '2023/10/15',                    # 1 campo
            '',                              # Línea vacía
            ';;;'                            # Solo separadores
        ]
        
        for i, line in enumerate(invalid_lines, 1):
            with pytest.raises(BadRequest) as exc_info:
                DataValidator.validate_line_format(line, i)
            assert f'Línea {i} mal formateada' in str(exc_info.value.description)
            assert 'exactamente 3 campos' in str(exc_info.value.description)
    
    def test_validate_line_format_invalid_data(self):
        """Test de validación de línea con datos inválidos"""
        invalid_lines = [
            ('2023-10-15;08:00;12345678-9', 'Fecha inválida'),
            ('2023/10/15;25:00;12345678-9', 'Hora inválida'),
            ('2023/10/15;08:00;invalid-rut', 'RUT inválido')
        ]
        
        for line, expected_error in invalid_lines:
            with pytest.raises(BadRequest) as exc_info:
                DataValidator.validate_line_format(line, 1)
            assert expected_error.split()[0].lower() in str(exc_info.value.description).lower()
    
    def test_validate_file_valid(self):
        """Test de validación de archivo válido"""
        valid_file = FileStorage(
            stream=BytesIO(b'test content'),
            filename='DATA.TXT',
            content_type='text/plain'
        )
        
        assert DataValidator.validate_file(valid_file) is True
    
    def test_validate_file_case_insensitive(self):
        """Test de validación de archivo con diferentes casos"""
        valid_filenames = ['DATA.TXT', 'data.txt', 'Data.Txt']
        
        for filename in valid_filenames:
            valid_file = FileStorage(
                stream=BytesIO(b'test content'),
                filename=filename,
                content_type='text/plain'
            )
            assert DataValidator.validate_file(valid_file) is True
    
    def test_validate_file_none(self):
        """Test de validación de archivo nulo"""
        with pytest.raises(BadRequest) as exc_info:
            DataValidator.validate_file(None)
        assert 'No se ha proporcionado ningún archivo' in str(exc_info.value.description)
    
    
    def test_validate_file_wrong_filename(self):
        """Test de validación de archivo con nombre incorrecto"""
        wrong_filenames = [
            'WRONG.TXT',
            'data.csv',
            'marcaciones.txt',
            'DATA'
        ]
        
        for filename in wrong_filenames:
            wrong_file = FileStorage(
                stream=BytesIO(b'test content'),
                filename=filename,
                content_type='text/plain'
            )
            
            with pytest.raises(BadRequest) as exc_info:
                DataValidator.validate_file(wrong_file)
            assert 'El nombre del archivo debe ser exactamente "DATA.TXT"' in str(exc_info.value.description)
