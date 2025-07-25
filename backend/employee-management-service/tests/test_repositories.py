import pytest
from src.repositories.employee_repository import EmployeeRepository
from src.errors.errors import EmployeeNotFound
from src.models.employee import Employee


class TestEmployeeRepository:
    """Tests para EmployeeRepository"""
    
    def test_find_by_rut_or_raise_not_found(self, app):
        """Test buscar empleado por RUT que no existe debe lanzar error"""
        with app.app_context():
            repo = EmployeeRepository()
            
            with pytest.raises(EmployeeNotFound):
                repo.find_by_rut_or_raise('99999999-9')
    
    def test_delete_not_found(self, app):
        """Test eliminar empleado que no existe debe lanzar error"""
        with app.app_context():
            repo = EmployeeRepository()
            
            with pytest.raises(EmployeeNotFound):
                repo.delete('99999999-9')
    
    def test_activate_not_found(self, app):
        """Test activar empleado que no existe debe lanzar error"""
        with app.app_context():
            repo = EmployeeRepository()
            
            with pytest.raises(EmployeeNotFound):
                repo.activate('99999999-9')
    
    def test_update_not_found(self, app):
        """Test actualizar empleado que no existe debe lanzar error"""
        with app.app_context():
            repo = EmployeeRepository()
            update_data = {'categoria': 'B'}
            
            with pytest.raises(EmployeeNotFound):
                repo.update('99999999-9', update_data)
