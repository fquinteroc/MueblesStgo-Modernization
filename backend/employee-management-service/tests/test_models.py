import pytest
from src.models.employee import Employee


class TestEmployeeModel:
    """Tests para modelo Employee"""
    
    def test_employee_repr(self, app, employee_data):
        """Test representación string del empleado"""
        with app.app_context():
            employee = Employee(**employee_data)
            expected_repr = f"<Employee {employee_data['rut']} - {employee_data['nombres']} {employee_data['apellidos']}>"
            assert str(employee) == expected_repr
    
    def test_employee_activate(self, app, employee_data):
        """Test activar empleado"""
        with app.app_context():
            employee = Employee(**employee_data)
            employee.activo = False
            employee.activate()
            assert employee.activo is True
    
    def test_employee_to_dict(self, app, employee_data):
        """Test conversión a diccionario"""
        with app.app_context():
            employee = Employee(**employee_data)
            result = employee.to_dict()
            
            assert result['rut'] == employee_data['rut']
            assert result['nombres'] == employee_data['nombres']
            assert result['apellidos'] == employee_data['apellidos']
            assert 'fecha_creacion' in result
            assert 'fecha_actualizacion' in result
