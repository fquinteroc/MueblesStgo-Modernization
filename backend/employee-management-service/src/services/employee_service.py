from typing import List, Optional, Dict, Any, Tuple
from src.repositories.employee_repository import EmployeeRepository
from src.validators.employee_validator import EmployeeValidator
from src.schemas.employee_schema import EmployeeSchema, EmployeeUpdateSchema
from src.errors.errors import EmployeeAlreadyExists, EmployeeNotFound, ValidationError
from src.models.employee import Employee

class EmployeeService:
    """Servicio de lógica de negocio para empleados"""
    
    def __init__(self):
        self.repository = EmployeeRepository()
        self.schema = EmployeeSchema()
        self.update_schema = EmployeeUpdateSchema()
    
    def create_employee(self, employee_data: dict) -> Employee:
        """
        Crea un nuevo empleado después de validar los datos
        """
        try:
            # Validar datos
            validated_data = self.schema.load(employee_data)
            
            # Verificar que no exista ya un empleado con este RUT
            if self.repository.exists(validated_data['rut']):
                raise EmployeeAlreadyExists(validated_data['rut'])
            
            # Crear empleado
            employee = self.repository.create(validated_data)
            
            return employee
            
        except Exception as e:
            self.repository.rollback()
            raise e
    
    def get_employee_by_rut(self, rut: str) -> Employee:
        """
        Obtiene un empleado por RUT
        """
        return self.repository.find_by_rut_or_raise(rut)
    
    def get_all_employees(self, page: int = 1, per_page: int = 50, 
                         active_only: bool = True) -> Tuple[List[Employee], int, int]:
        """
        Obtiene todos los empleados con paginación
        Retorna (empleados, total, páginas)
        """
        return self.repository.find_all(page, per_page, active_only)
    
    def update_employee(self, rut: str, update_data: dict) -> Employee:
        """
        Actualiza un empleado existente
        """
        try:
            # Validar datos de actualización
            validated_data = self.update_schema.load(update_data)
            
            # Actualizar empleado
            employee = self.repository.update(rut, validated_data)
            
            return employee
            
        except Exception as e:
            self.repository.rollback()
            raise e
    
    def delete_employee(self, rut: str) -> Employee:
        """
        Elimina un empleado (soft delete)
        """
        return self.repository.delete(rut)
    
    def activate_employee(self, rut: str) -> Employee:
        """
        Reactiva un empleado inactivo
        """
        return self.repository.activate(rut)
    
    def get_employees_by_category(self, category: str, active_only: bool = True) -> List[Employee]:
        """
        Obtiene empleados por categoría
        """
        # Validar categoría
        EmployeeValidator.validate_categoria(category)
        
        return self.repository.find_by_category(category, active_only)
    
    def search_employees_by_name(self, search_term: str, active_only: bool = True) -> List[Employee]:
        """
        Busca empleados por nombre
        """
        if not search_term or search_term.strip() == '':
            raise ValidationError('Término de búsqueda no puede estar vacío')
        
        search_term = search_term.strip()
        if len(search_term) < 2:
            raise ValidationError('Término de búsqueda debe tener al menos 2 caracteres')
        
        return self.repository.search_by_name(search_term, active_only)
    
    def get_employee_category(self, rut: str) -> dict:
        """
        Obtiene solo la categoría de un empleado
        """
        employee = self.repository.find_by_rut_or_raise(rut)
        return {
            'rut': employee.rut,
            'categoria': employee.categoria,
            'nombres': employee.nombres,
            'apellidos': employee.apellidos
        }
    
    def get_employees_by_date_range(self, start_date: str, end_date: str, 
                                   active_only: bool = True) -> List[Employee]:
        """
        Obtiene empleados por rango de fechas de ingreso
        """
        # Validar fechas
        EmployeeValidator.validate_fecha(start_date, 'Fecha inicio')
        EmployeeValidator.validate_fecha(end_date, 'Fecha fin')
        
        return self.repository.find_by_date_range(start_date, end_date, active_only)
    
    def get_employee_statistics(self) -> dict:
        """
        Obtiene estadísticas de empleados
        """
        total_employees = self.repository.count_all(active_only=True)
        total_inactive = self.repository.count_all(active_only=False) - total_employees
        categories_count = self.repository.count_by_category(active_only=True)
        all_categories = self.repository.get_all_categories()
        
        return {
            'total_employees': total_employees,
            'total_inactive': total_inactive,
            'total_all': total_employees + total_inactive,
            'by_category': categories_count,
            'available_categories': all_categories
        }
    
    def validate_employee_data(self, data: dict) -> dict:
        """
        Valida datos de empleado sin crear
        """
        return self.schema.load(data)
    
    def get_employees_summary(self) -> dict:
        """
        Obtiene un resumen de empleados para dashboards
        """
        stats = self.get_employee_statistics()
        recent_employees = self.repository.find_all(page=1, per_page=5, active_only=True)[0]
        
        return {
            'statistics': stats,
            'recent_employees': [emp.to_dict() for emp in recent_employees]
        }
    
    def bulk_update_category(self, ruts: List[str], new_category: str) -> dict:
        """
        Actualiza la categoría de múltiples empleados
        """
        # Validar categoría
        EmployeeValidator.validate_categoria(new_category)
        
        updated_count = 0
        errors = []
        
        for rut in ruts:
            try:
                self.repository.update(rut, {'categoria': new_category.upper()})
                updated_count += 1
            except EmployeeNotFound:
                errors.append(f'Empleado con RUT {rut} no encontrado')
            except Exception as e:
                errors.append(f'Error actualizando {rut}: {str(e)}')
        
        return {
            'updated_count': updated_count,
            'total_requested': len(ruts),
            'errors': errors
        }
    
    def get_active_employees_count(self) -> int:
        """
        Obtiene el número de empleados activos
        """
        return self.repository.count_all(active_only=True)
    
    def check_employee_exists(self, rut: str) -> bool:
        """
        Verifica si existe un empleado con el RUT dado
        """
        return self.repository.exists(rut)
