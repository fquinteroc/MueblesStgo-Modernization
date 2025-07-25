from flask import Blueprint, request, jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from src.services.employee_service import EmployeeService
from src.schemas.employee_schema import (
    EmployeeSchema, EmployeeUpdateSchema, EmployeeCategoryResponseSchema,
    EmployeeListResponseSchema, EmployeeSearchResponseSchema
)
from src.errors.errors import (
    APIError, BadRequest, NotFound, Conflict, ValidationError,
    EmployeeNotFound, EmployeeAlreadyExists
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('employees', __name__, url_prefix='/api')

# Inicializar esquemas
employee_schema = EmployeeSchema()
employee_update_schema = EmployeeUpdateSchema()
category_schema = EmployeeCategoryResponseSchema()

@bp.route('/ping', methods=['GET'])
def ping():
    """Endpoint de salud del microservicio"""
    return jsonify({'status': 'ok', 'service': 'employee-management-service'}), 200

@bp.route('/employees', methods=['POST'])
def create_employee():
    """
    Crear nuevo empleado
    POST /api/employees
    Content-Type: application/json
    """
    try:
        if not request.json:
            raise BadRequest('Se requiere contenido JSON')
        
        service = EmployeeService()
        employee = service.create_employee(request.json)
        
        result = employee_schema.dump(employee)
        
        logger.info(f"Empleado creado exitosamente: {employee.rut}")
        
        return jsonify({
            'success': True,
            'message': 'Empleado creado exitosamente',
            'data': result
        }), 201
        
    except EmployeeAlreadyExists as e:
        logger.error(f"Error - empleado ya existe: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 409
        
    except (ValidationError, MarshmallowValidationError) as e:
        logger.error(f"Error de validación: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error interno creando empleado: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/<rut>', methods=['GET'])
def get_employee(rut):
    """
    Obtener empleado por RUT
    GET /api/employees/{rut}
    """
    try:
        service = EmployeeService()
        employee = service.get_employee_by_rut(rut)
        
        result = employee_schema.dump(employee)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except EmployeeNotFound as e:
        logger.error(f"Empleado no encontrado: {rut}")
        return jsonify({'success': False, 'error': str(e)}), 404
        
    except Exception as e:
        logger.error(f"Error obteniendo empleado {rut}: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees', methods=['GET'])
def get_all_employees():
    """
    Obtener lista de todos los empleados con paginación
    GET /api/employees?page=1&per_page=50&active_only=true
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 200)  # Máximo 200
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        service = EmployeeService()
        employees, total, pages = service.get_all_employees(page, per_page, active_only)
        
        result = employee_schema.dump(employees, many=True)
        
        response_data = {
            'success': True,
            'data': {
                'employees': result,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages,
                    'has_next': page < pages,
                    'has_prev': page > 1
                }
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo empleados: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/<rut>', methods=['PUT'])
def update_employee(rut):
    """
    Actualizar empleado existente
    PUT /api/employees/{rut}
    Content-Type: application/json
    """
    try:
        if not request.json:
            raise BadRequest('Se requiere contenido JSON')
        
        service = EmployeeService()
        employee = service.update_employee(rut, request.json)
        
        result = employee_schema.dump(employee)
        
        logger.info(f"Empleado actualizado exitosamente: {rut}")
        
        return jsonify({
            'success': True,
            'message': 'Empleado actualizado exitosamente',
            'data': result
        }), 200
        
    except EmployeeNotFound as e:
        logger.error(f"Empleado no encontrado para actualizar: {rut}")
        return jsonify({'success': False, 'error': str(e)}), 404
        
    except (ValidationError, MarshmallowValidationError) as e:
        logger.error(f"Error de validación actualizando {rut}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error interno actualizando empleado {rut}: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/<rut>', methods=['DELETE'])
def delete_employee(rut):
    """
    Eliminar empleado (soft delete)
    DELETE /api/employees/{rut}
    """
    try:
        service = EmployeeService()
        employee = service.delete_employee(rut)
        
        logger.info(f"Empleado eliminado exitosamente: {rut}")
        
        return jsonify({
            'success': True,
            'message': f'Empleado {rut} eliminado exitosamente'
        }), 200
        
    except EmployeeNotFound as e:
        logger.error(f"Empleado no encontrado para eliminar: {rut}")
        return jsonify({'success': False, 'error': str(e)}), 404
        
    except Exception as e:
        logger.error(f"Error eliminando empleado {rut}: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/category/<category>', methods=['GET'])
def get_employees_by_category(category):
    """
    Obtener empleados por categoría
    GET /api/employees/category/{category}?active_only=true
    """
    try:
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        service = EmployeeService()
        employees = service.get_employees_by_category(category, active_only)
        
        result = employee_schema.dump(employees, many=True)
        
        return jsonify({
            'success': True,
            'data': result,
            'category': category.upper(),
            'total': len(result)
        }), 200
        
    except ValidationError as e:
        logger.error(f"Categoría inválida: {category}")
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error obteniendo empleados por categoría {category}: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/search', methods=['GET'])
def search_employees():
    """
    Buscar empleados por nombre
    GET /api/employees/search?name={name}&active_only=true
    """
    try:
        search_term = request.args.get('name', '').strip()
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        if not search_term:
            raise BadRequest('Parámetro "name" es requerido')
        
        service = EmployeeService()
        employees = service.search_employees_by_name(search_term, active_only)
        
        result = employee_schema.dump(employees, many=True)
        
        return jsonify({
            'success': True,
            'data': result,
            'search_term': search_term,
            'total': len(result)
        }), 200
        
    except (ValidationError, BadRequest) as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error en búsqueda de empleados: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/<rut>/category', methods=['GET'])
def get_employee_category(rut):
    """
    Obtener solo la categoría de un empleado
    GET /api/employees/{rut}/category
    """
    try:
        service = EmployeeService()
        result = service.get_employee_category(rut)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except EmployeeNotFound as e:
        logger.error(f"Empleado no encontrado: {rut}")
        return jsonify({'success': False, 'error': str(e)}), 404
        
    except Exception as e:
        logger.error(f"Error obteniendo categoría del empleado {rut}: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/<rut>/activate', methods=['PATCH'])
def activate_employee(rut):
    """
    Reactivar empleado inactivo
    PATCH /api/employees/{rut}/activate
    """
    try:
        service = EmployeeService()
        employee = service.activate_employee(rut)
        
        result = employee_schema.dump(employee)
        
        logger.info(f"Empleado reactivado exitosamente: {rut}")
        
        return jsonify({
            'success': True,
            'message': f'Empleado {rut} reactivado exitosamente',
            'data': result
        }), 200
        
    except EmployeeNotFound as e:
        logger.error(f"Empleado no encontrado para reactivar: {rut}")
        return jsonify({'success': False, 'error': str(e)}), 404
        
    except Exception as e:
        logger.error(f"Error reactivando empleado {rut}: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/stats', methods=['GET'])
def get_employee_statistics():
    """
    Obtener estadísticas de empleados
    GET /api/employees/stats
    """
    try:
        service = EmployeeService()
        stats = service.get_employee_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/employees/date-range', methods=['GET'])
def get_employees_by_date_range():
    """
    Obtener empleados por rango de fechas de ingreso
    GET /api/employees/date-range?start_date=2020/01/01&end_date=2023/12/31&active_only=true
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        if not start_date or not end_date:
            raise BadRequest('Parámetros "start_date" y "end_date" son requeridos')
        
        service = EmployeeService()
        employees = service.get_employees_by_date_range(start_date, end_date, active_only)
        
        result = employee_schema.dump(employees, many=True)
        
        return jsonify({
            'success': True,
            'data': result,
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            },
            'total': len(result)
        }), 200
        
    except (ValidationError, BadRequest) as e:
        logger.error(f"Error en consulta por rango de fechas: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error obteniendo empleados por rango de fechas: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.errorhandler(APIError)
def handle_api_error(e):
    """Manejo de errores específicos de la API"""
    return jsonify({'success': False, 'error': e.description}), e.code
