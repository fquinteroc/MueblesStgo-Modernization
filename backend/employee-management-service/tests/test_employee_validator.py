import pytest
from src.validators.employee_validator import EmployeeValidator
from src.errors.errors import ValidationError

class TestEmployeeValidator:
    """Tests para el validador de empleados"""
    
    def test_validate_rut_valid(self):
        """Test de validación de RUT válido"""
        valid_ruts = ['12345678-9', '1234567-8', '11111111-1', '98765432-K', '11223344-k']
        
        for rut in valid_ruts:
            assert EmployeeValidator.validate_rut(rut) is True
    
    def test_validate_rut_invalid(self):
        """Test de validación de RUT inválido"""
        invalid_ruts = ['', None, '123456789', '1234567-', '-1234567', 'abc-1', '12345678-X']
        
        for rut in invalid_ruts:
            with pytest.raises(ValidationError):
                EmployeeValidator.validate_rut(rut)
    
    def test_validate_fecha_valid(self):
        """Test de validación de fecha válida"""
        valid_dates = ['2023/01/01', '1990/12/31', '2000/06/15', '1985/02/28']
        
        for fecha in valid_dates:
            assert EmployeeValidator.validate_fecha(fecha) is True
    
    def test_validate_fecha_invalid(self):
        """Test de validación de fecha inválida"""
        invalid_dates = ['', None, '2023-01-01', '01/01/2023', '2023/13/01', '2023/01/32', 'invalid']
        
        for fecha in invalid_dates:
            with pytest.raises(ValidationError):
                EmployeeValidator.validate_fecha(fecha)
    
    def test_validate_categoria_valid(self):
        """Test de validación de categoría válida"""
        valid_categories = ['A', 'B', 'C', 'a', 'b', 'c']
        
        for categoria in valid_categories:
            assert EmployeeValidator.validate_categoria(categoria) is True
    
    def test_validate_categoria_invalid(self):
        """Test de validación de categoría inválida"""
        invalid_categories = ['', None, 'D', 'X', '1', 'AB']
        
        for categoria in invalid_categories:
            with pytest.raises(ValidationError):
                EmployeeValidator.validate_categoria(categoria)
    
    def test_validate_nombres_valid(self):
        """Test de validación de nombres válidos"""
        valid_names = ['Juan', 'María Elena', 'Carlos Eduardo', 'Ana Isabel']
        
        for nombre in valid_names:
            assert EmployeeValidator.validate_nombres(nombre) is True
    
    def test_validate_nombres_invalid(self):
        """Test de validación de nombres inválidos"""
        invalid_names = ['', None, 'A', 'A' * 101]  # Vacío, muy corto, muy largo
        
        for nombre in invalid_names:
            with pytest.raises(ValidationError):
                EmployeeValidator.validate_nombres(nombre)
    
    def test_validate_apellidos_valid(self):
        """Test de validación de apellidos válidos"""
        valid_surnames = ['González', 'Pérez López', 'Silva Martínez']
        
        for apellido in valid_surnames:
            assert EmployeeValidator.validate_apellidos(apellido) is True
    
    def test_validate_apellidos_invalid(self):
        """Test de validación de apellidos inválidos"""
        invalid_surnames = ['', None, 'A', 'A' * 101]
        
        for apellido in invalid_surnames:
            with pytest.raises(ValidationError):
                EmployeeValidator.validate_apellidos(apellido)
    
    def test_validate_fecha_nacimiento_logica_valid(self):
        """Test de validación lógica de fecha de nacimiento"""
        # Fecha válida (30 años)
        fecha_valida = '1993/01/01'
        assert EmployeeValidator.validate_fecha_nacimiento_logica(fecha_valida) is True
    
    def test_validate_fecha_nacimiento_logica_future(self):
        """Test de fecha de nacimiento futura"""
        fecha_futura = '2030/01/01'
        with pytest.raises(ValidationError) as excinfo:
            EmployeeValidator.validate_fecha_nacimiento_logica(fecha_futura)
        assert 'futura' in str(excinfo.value)
    
    def test_validate_fecha_nacimiento_logica_too_old(self):
        """Test de fecha de nacimiento muy antigua"""
        fecha_antigua = '1900/01/01'
        with pytest.raises(ValidationError) as excinfo:
            EmployeeValidator.validate_fecha_nacimiento_logica(fecha_antigua)
        assert '100 años' in str(excinfo.value)
    
    def test_validate_fecha_nacimiento_logica_too_young(self):
        """Test de fecha de nacimiento muy reciente (menor de edad)"""
        fecha_reciente = '2010/01/01'
        with pytest.raises(ValidationError) as excinfo:
            EmployeeValidator.validate_fecha_nacimiento_logica(fecha_reciente)
        assert '18 años' in str(excinfo.value)
    
    def test_validate_fecha_ingreso_logica_valid(self):
        """Test de validación lógica de fecha de ingreso"""
        fecha_valida = '2020/01/01'
        assert EmployeeValidator.validate_fecha_ingreso_logica(fecha_valida) is True
    
    def test_validate_fecha_ingreso_logica_future(self):
        """Test de fecha de ingreso futura"""
        fecha_futura = '2030/01/01'
        with pytest.raises(ValidationError) as excinfo:
            EmployeeValidator.validate_fecha_ingreso_logica(fecha_futura)
        assert 'futura' in str(excinfo.value)
    
    def test_validate_fecha_ingreso_logica_coherencia(self):
        """Test de coherencia entre fecha de nacimiento e ingreso"""
        fecha_nacimiento = '1990/01/01'
        fecha_ingreso = '2010/01/01'  # 20 años después
        
        assert EmployeeValidator.validate_fecha_ingreso_logica(fecha_ingreso, fecha_nacimiento) is True
    
    def test_validate_fecha_ingreso_logica_incoherencia(self):
        """Test de incoherencia entre fechas"""
        fecha_nacimiento = '1990/01/01'
        fecha_ingreso = '1989/01/01'  # Antes del nacimiento
        
        with pytest.raises(ValidationError) as excinfo:
            EmployeeValidator.validate_fecha_ingreso_logica(fecha_ingreso, fecha_nacimiento)
        assert 'anterior' in str(excinfo.value)
    
    def test_validate_fecha_ingreso_logica_muy_joven(self):
        """Test de ingreso muy joven"""
        fecha_nacimiento = '1990/01/01'
        fecha_ingreso = '2000/01/01'  # Solo 10 años después
        
        with pytest.raises(ValidationError) as excinfo:
            EmployeeValidator.validate_fecha_ingreso_logica(fecha_ingreso, fecha_nacimiento)
        assert '16 años' in str(excinfo.value)
    
    def test_validate_employee_data_complete_valid(self):
        """Test de validación completa de datos válidos"""
        valid_data = {
            'rut': '12345678-9',
            'nombres': 'Juan Carlos',
            'apellidos': 'González Pérez',
            'fecha_nacimiento': '1985/03/15',
            'categoria': 'A',
            'fecha_ingreso': '2020/01/15'
        }
        
        assert EmployeeValidator.validate_employee_data(valid_data) is True
    
    def test_validate_employee_data_complete_invalid(self):
        """Test de validación completa de datos inválidos"""
        invalid_data = {
            'rut': 'invalid-rut',
            'nombres': '',
            'apellidos': 'Test',
            'fecha_nacimiento': '2030/01/01',  # Futura
            'categoria': 'X',  # Inválida
            'fecha_ingreso': '2020/01/01'
        }
        
        with pytest.raises(ValidationError):
            EmployeeValidator.validate_employee_data(invalid_data)
