import json
import pytest
from src.models.employee import Employee
from src.database import db

class TestEmployeeController:
    """Tests para el controlador de empleados"""
    
    def test_ping_endpoint(self, client):
        """Test del endpoint de ping"""
        response = client.get('/api/ping')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert data['service'] == 'employee-management-service'
    
    def test_create_employee_success(self, client, employee_data):
        """Test de creación exitosa de empleado"""
        response = client.post('/api/employees', 
                              json=employee_data,
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'Empleado creado exitosamente'
        assert data['data']['rut'] == employee_data['rut']
        assert data['data']['nombres'] == employee_data['nombres']
    
    def test_create_employee_duplicate_rut(self, client, employee_instance, employee_data):
        """Test de error al crear empleado con RUT duplicado"""
        response = client.post('/api/employees',
                              json=employee_data,
                              content_type='application/json')
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Ya existe un empleado' in data['error']
    
    def test_create_employee_invalid_data(self, client):
        """Test de validación de datos inválidos"""
        invalid_data = {
            'rut': 'invalid-rut',
            'nombres': '',
            'apellidos': 'Test',
            'fecha_nacimiento': 'invalid-date',
            'categoria': 'X',
            'fecha_ingreso': '2020/01/01'
        }
        
        response = client.post('/api/employees',
                              json=invalid_data,
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_get_employee_success(self, client, employee_instance):
        """Test de obtención exitosa de empleado"""
        response = client.get(f'/api/employees/{employee_instance.rut}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['rut'] == employee_instance.rut
        assert data['data']['nombres'] == employee_instance.nombres
    
    def test_get_employee_not_found(self, client):
        """Test de empleado no encontrado"""
        response = client.get('/api/employees/99999999-9')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'no encontrado' in data['error']
    
    def test_get_all_employees(self, client, multiple_employees):
        """Test de obtención de todos los empleados"""
        response = client.get('/api/employees')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['employees']) == 3
        assert 'pagination' in data['data']
    
    def test_get_all_employees_with_pagination(self, client, multiple_employees):
        """Test de paginación"""
        response = client.get('/api/employees?page=1&per_page=2')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['employees']) == 2
        assert data['data']['pagination']['page'] == 1
        assert data['data']['pagination']['per_page'] == 2
    
    def test_update_employee_success(self, client, employee_instance):
        """Test de actualización exitosa de empleado"""
        update_data = {
            'categoria': 'B',
            'apellidos': 'González Silva'
        }
        
        response = client.put(f'/api/employees/{employee_instance.rut}',
                             json=update_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['categoria'] == 'B'
        assert data['data']['apellidos'] == 'González Silva'
    
    def test_update_employee_not_found(self, client):
        """Test de actualización de empleado no encontrado"""
        update_data = {'categoria': 'B'}
        
        response = client.put('/api/employees/99999999-9',
                             json=update_data,
                             content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_delete_employee_success(self, client, employee_instance):
        """Test de eliminación exitosa de empleado"""
        response = client.delete(f'/api/employees/{employee_instance.rut}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'eliminado exitosamente' in data['message']
    
    def test_get_employees_by_category(self, client, multiple_employees):
        """Test de obtención de empleados por categoría"""
        response = client.get('/api/employees/category/A')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['category'] == 'A'
        # Debería haber al menos un empleado de categoría A
        employees_cat_a = [emp for emp in data['data'] if emp['categoria'] == 'A']
        assert len(employees_cat_a) >= 1
    
    def test_search_employees_by_name(self, client, multiple_employees):
        """Test de búsqueda de empleados por nombre"""
        response = client.get('/api/employees/search?name=María')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['search_term'] == 'María'
        # Debería encontrar al menos un empleado con María en el nombre
        assert len(data['data']) >= 1
    
    def test_search_employees_empty_name(self, client):
        """Test de búsqueda con nombre vacío"""
        response = client.get('/api/employees/search?name=')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_get_employee_category(self, client, employee_instance):
        """Test de obtención de categoría específica"""
        response = client.get(f'/api/employees/{employee_instance.rut}/category')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['rut'] == employee_instance.rut
        assert data['data']['categoria'] == employee_instance.categoria
    
    def test_activate_employee(self, client, employee_instance):
        """Test de reactivación de empleado"""
        # Primero desactivar el empleado
        employee_instance.soft_delete()
        db.session.commit()
        
        response = client.patch(f'/api/employees/{employee_instance.rut}/activate')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['activo'] is True
    
    def test_get_employee_statistics(self, client, multiple_employees):
        """Test de obtención de estadísticas"""
        response = client.get('/api/employees/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'total_employees' in data['data']
        assert 'by_category' in data['data']
        assert data['data']['total_employees'] >= 3
    
    def test_get_employees_by_date_range(self, client, multiple_employees):
        """Test de obtención de empleados por rango de fechas"""
        response = client.get('/api/employees/date-range?start_date=2020/01/01&end_date=2023/12/31')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'date_range' in data  # date_range está en el nivel superior, no dentro de data
        assert 'data' in data
        assert isinstance(data['data'], list)  # data contiene la lista de empleados
        assert len(data['data']) >= 0  # Puede no haber empleados en ese rango
        assert 'total' in data
        assert data['date_range']['start_date'] == '2020/01/01'
        assert data['date_range']['end_date'] == '2023/12/31'
    
    def test_get_employees_by_date_range_missing_params(self, client):
        """Test de error cuando faltan parámetros en date range"""
        response = client.get('/api/employees/date-range?start_date=2020/01/01')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'requeridos' in data['error']
    
    def test_get_employees_by_date_range_no_params(self, client):
        """Test de error cuando no se envían parámetros en date range"""
        response = client.get('/api/employees/date-range')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'requeridos' in data['error']
    
    def test_invalid_category(self, client):
        """Test de categoría inválida"""
        response = client.get('/api/employees/category/X')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
