import pytest
import json
from src.services.employee_service import EmployeeService
from src.errors.errors import EmployeeNotFound, EmployeeAlreadyExists, ValidationError
from tests.conftest import employee_data


class TestEmployeeService:
    """Tests para EmployeeService"""
    
    def test_create_employee_already_exists(self, app, employee_instance):
        """Test crear empleado que ya existe"""
        with app.app_context():
            service = EmployeeService()
            duplicate_data = {
                'rut': employee_instance.rut,
                'nombres': 'Otro Nombre',
                'apellidos': 'Otro Apellido',
                'fecha_nacimiento': '1990/01/01',
                'categoria': 'B',
                'fecha_ingreso': '2023/01/01'
            }
            
            with pytest.raises(EmployeeAlreadyExists):
                service.create_employee(duplicate_data)
    
    def test_get_employee_not_found(self, app):
        """Test obtener empleado que no existe"""
        with app.app_context():
            service = EmployeeService()
            
            with pytest.raises(EmployeeNotFound):
                service.get_employee_by_rut('99999999-9')
    
    def test_update_employee_not_found(self, app):
        """Test actualizar empleado que no existe"""
        with app.app_context():
            service = EmployeeService()
            update_data = {'categoria': 'B'}
            
            with pytest.raises(EmployeeNotFound):
                service.update_employee('99999999-9', update_data)
    
    def test_delete_employee_not_found(self, app):
        """Test eliminar empleado que no existe"""
        with app.app_context():
            service = EmployeeService()
            
            with pytest.raises(EmployeeNotFound):
                service.delete_employee('99999999-9')
    
    def test_get_employees_by_category_invalid(self, app):
        """Test obtener empleados por categoría inválida debe lanzar error"""
        with app.app_context():
            service = EmployeeService()
            
            with pytest.raises(ValidationError):
                service.get_employees_by_category('Z')
    
    def test_search_employees_empty_result(self, app):
        """Test buscar empleados sin resultados"""
        with app.app_context():
            service = EmployeeService()
            result = service.search_employees_by_name('NoExiste')
            
            assert len(result) == 0
    
    def test_get_employees_by_date_range_empty(self, app):
        """Test obtener empleados por rango de fechas sin resultados"""
        with app.app_context():
            service = EmployeeService()
            result = service.get_employees_by_date_range('1900/01/01', '1900/12/31')
            
            assert len(result) == 0
    
    def test_activate_employee_not_found(self, app):
        """Test activar empleado que no existe"""
        with app.app_context():
            service = EmployeeService()
            
            with pytest.raises(EmployeeNotFound):
                service.activate_employee('99999999-9')
