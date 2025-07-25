import pytest
from src.main import create_app
from src.database import db
from src.models.employee import Employee

@pytest.fixture
def app():
    """Crear aplicación de prueba"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()

@pytest.fixture
def employee_data():
    """Datos de empleado para pruebas"""
    return {
        'rut': '12345678-9',
        'apellidos': 'González Pérez',
        'nombres': 'Juan Carlos',
        'fecha_nacimiento': '1985/03/15',
        'categoria': 'A',
        'fecha_ingreso': '2020/01/15'
    }

@pytest.fixture
def employee_instance(app, employee_data):
    """Instancia de empleado en base de datos"""
    with app.app_context():
        employee = Employee(**employee_data)
        db.session.add(employee)
        db.session.commit()
        # Refrescar el objeto para evitar DetachedInstanceError
        db.session.refresh(employee)
        # Acceder a todos los atributos para cargarlos en memoria
        _ = employee.rut, employee.nombres, employee.apellidos
        _ = employee.categoria, employee.fecha_nacimiento, employee.fecha_ingreso
        _ = employee.activo, employee.fecha_creacion, employee.fecha_actualizacion
        return employee

@pytest.fixture
def multiple_employees(app):
    """Múltiples empleados para pruebas"""
    with app.app_context():
        employees_data = [
            {
                'rut': '11111111-1',
                'apellidos': 'Pérez López',
                'nombres': 'María Elena',
                'fecha_nacimiento': '1990/05/20',
                'categoria': 'A',
                'fecha_ingreso': '2021/01/10'
            },
            {
                'rut': '22222222-2',
                'apellidos': 'Silva Martínez',
                'nombres': 'Carlos Eduardo',
                'fecha_nacimiento': '1988/08/15',
                'categoria': 'B',
                'fecha_ingreso': '2020/06/20'
            },
            {
                'rut': '33333333-3',
                'apellidos': 'Torres Rodríguez',
                'nombres': 'Ana Isabel',
                'fecha_nacimiento': '1992/12/10',
                'categoria': 'C',
                'fecha_ingreso': '2022/03/15'
            }
        ]
        
        employees = []
        for emp_data in employees_data:
            employee = Employee(**emp_data)
            db.session.add(employee)
            employees.append(employee)
        
        db.session.commit()
        
        # Refrescar todos los empleados para evitar DetachedInstanceError
        for employee in employees:
            db.session.refresh(employee)
            # Acceder a todos los atributos para cargarlos en memoria
            _ = employee.rut, employee.nombres, employee.apellidos
            _ = employee.categoria, employee.fecha_nacimiento, employee.fecha_ingreso
            _ = employee.activo, employee.fecha_creacion, employee.fecha_actualizacion
            
        return employees
