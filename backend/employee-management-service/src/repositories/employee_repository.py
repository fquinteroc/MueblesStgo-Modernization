from typing import List, Optional
from sqlalchemy import func, or_
from src.database import db
from src.models.employee import Employee
from src.errors.errors import EmployeeNotFound

class EmployeeRepository:
    """Repositorio para operaciones de base de datos de empleados"""
    
    @staticmethod
    def create(employee_data: dict) -> Employee:
        """
        Crea un nuevo empleado en la base de datos
        """
        employee = Employee(**employee_data)
        db.session.add(employee)
        db.session.commit()
        return employee
    
    @staticmethod
    def find_by_rut(rut: str) -> Optional[Employee]:
        """
        Busca un empleado por RUT
        """
        return Employee.query.filter_by(rut=rut).first()
    
    @staticmethod
    def find_by_rut_or_raise(rut: str) -> Employee:
        """
        Busca un empleado por RUT o lanza excepción si no se encuentra
        """
        employee = EmployeeRepository.find_by_rut(rut)
        if not employee:
            raise EmployeeNotFound(rut)
        return employee
    
    @staticmethod
    def find_all(page: int = 1, per_page: int = 50, active_only: bool = True) -> tuple:
        """
        Obtiene todos los empleados con paginación
        Retorna (empleados, total)
        """
        query = Employee.query
        
        if active_only:
            query = query.filter_by(activo=True)
        
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def find_by_category(category: str, active_only: bool = True) -> List[Employee]:
        """
        Busca empleados por categoría
        """
        query = Employee.query.filter_by(categoria=category.upper())
        
        if active_only:
            query = query.filter_by(activo=True)
        
        return query.all()
    
    @staticmethod
    def search_by_name(search_term: str, active_only: bool = True) -> List[Employee]:
        """
        Busca empleados por nombre o apellido (búsqueda parcial)
        """
        search_pattern = f"%{search_term}%"
        query = Employee.query.filter(
            or_(
                Employee.nombres.ilike(search_pattern),
                Employee.apellidos.ilike(search_pattern),
                func.concat(Employee.nombres, ' ', Employee.apellidos).ilike(search_pattern)
            )
        )
        
        if active_only:
            query = query.filter_by(activo=True)
        
        return query.all()
    
    @staticmethod
    def find_by_date_range(start_date: str, end_date: str, active_only: bool = True) -> List[Employee]:
        """
        Busca empleados por rango de fechas de ingreso
        """
        query = Employee.query.filter(
            Employee.fecha_ingreso >= start_date,
            Employee.fecha_ingreso <= end_date
        )
        
        if active_only:
            query = query.filter_by(activo=True)
        
        return query.all()
    
    @staticmethod
    def update(rut: str, update_data: dict) -> Employee:
        """
        Actualiza un empleado existente
        """
        employee = EmployeeRepository.find_by_rut_or_raise(rut)
        
        # Actualizar solo los campos proporcionados
        for field, value in update_data.items():
            if hasattr(employee, field):
                setattr(employee, field, value)
        
        db.session.commit()
        return employee
    
    @staticmethod
    def delete(rut: str) -> Employee:
        """
        Elimina un empleado (soft delete)
        """
        employee = EmployeeRepository.find_by_rut_or_raise(rut)
        employee.soft_delete()
        db.session.commit()
        return employee
    
    @staticmethod
    def hard_delete(rut: str) -> bool:
        """
        Elimina un empleado permanentemente de la base de datos
        """
        employee = EmployeeRepository.find_by_rut_or_raise(rut)
        db.session.delete(employee)
        db.session.commit()
        return True
    
    @staticmethod
    def activate(rut: str) -> Employee:
        """
        Reactiva un empleado marcado como inactivo
        """
        employee = EmployeeRepository.find_by_rut_or_raise(rut)
        employee.activate()
        db.session.commit()
        return employee
    
    @staticmethod
    def exists(rut: str) -> bool:
        """
        Verifica si existe un empleado con el RUT dado
        """
        return db.session.query(
            Employee.query.filter_by(rut=rut).exists()
        ).scalar()
    
    @staticmethod
    def count_all(active_only: bool = True) -> int:
        """
        Cuenta el total de empleados
        """
        query = Employee.query
        
        if active_only:
            query = query.filter_by(activo=True)
        
        return query.count()
    
    @staticmethod
    def count_by_category(active_only: bool = True) -> dict:
        """
        Cuenta empleados por categoría
        """
        query = Employee.query
        
        if active_only:
            query = query.filter_by(activo=True)
        
        result = query.with_entities(
            Employee.categoria,
            func.count(Employee.categoria)
        ).group_by(Employee.categoria).all()
        
        return {categoria: count for categoria, count in result}
    
    @staticmethod
    def get_all_categories() -> List[str]:
        """
        Obtiene todas las categorías distintas en uso
        """
        result = db.session.query(Employee.categoria.distinct()).all()
        return [r[0] for r in result]
    
    @staticmethod
    def rollback():
        """
        Hace rollback de la transacción actual
        """
        db.session.rollback()
