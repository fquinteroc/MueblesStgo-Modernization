from flask import Blueprint, request, jsonify
from src.services.subir_data_service import SubirDataService
from src.schemas.data_schema import DataSchema
from src.errors.errors import BadRequest, APIError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('subir_data', __name__)

@bp.route('/ping', methods=['GET'])
def ping():
    """Endpoint de salud del microservicio"""
    return jsonify({'status': 'ok', 'service': 'data-upload-service'}), 200

@bp.route('/upload', methods=['POST'])
def upload():
    """
    API para procesar la carga y procesamiento del archivo DATA.txt
    POST /upload - Procesamiento del archivo
    Content-Type: multipart/form-data
    """
    try:
        # Obtener archivo del request
        file = request.files.get('file')
        
        if not file:
            raise BadRequest('No se ha proporcionado ningún archivo')
        
        # Instanciar servicio
        service = SubirDataService()
        
        # Guardar archivo
        logger.info(f"Guardando archivo: {file.filename}")
        path = service.guardar(file)
        
        logger.info(f"Procesando archivo: {path}")
        resultado = service.leer_txt(path)
        
        logger.info(f"Archivo procesado exitosamente: {resultado['registros_procesados']} registros")
        
        return jsonify({
            'success': True,
            'message': resultado['mensaje'],
            'registros_procesados': resultado['registros_procesados']
        }), 200
        
    except BadRequest as e:
        logger.error(f"Error de validación: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error interno: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/data', methods=['GET'])
def get_data():
    """
    API endpoint para obtener todos los datos de marcaciones
    GET /data - Obtener todos los registros cargados
    """
    try:
        service = SubirDataService()
        all_data = service.obtener_todos_los_datos()
        
        schema = DataSchema(many=True)
        data_serialized = schema.dump(all_data)
        
        return jsonify({
            'success': True,
            'data': data_serialized,
            'total_records': len(data_serialized)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo datos: {str(e)}")
        return jsonify({'success': False, 'error': 'Error obteniendo datos'}), 500

@bp.route('/data/rut/<rut>', methods=['GET'])
def get_data_by_rut(rut):
    """
    API endpoint para obtener datos por RUT específico
    GET /data/rut/<rut> - Obtener registros por RUT
    """
    try:
        service = SubirDataService()
        data = service.obtener_datos_por_rut(rut)
        
        schema = DataSchema(many=True)
        data_serialized = schema.dump(data)
        
        return jsonify({
            'success': True,
            'data': data_serialized,
            'rut': rut,
            'total_records': len(data_serialized)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo datos por RUT: {str(e)}")
        return jsonify({'success': False, 'error': 'Error obteniendo datos'}), 500

@bp.route('/ruts', methods=['GET'])
def get_distinct_ruts():
    """
    API endpoint para obtener todos los RUTs únicos
    GET /ruts - Obtener lista de RUTs únicos
    """
    try:
        service = SubirDataService()
        ruts = service.obtener_ruts_distintos()
        
        return jsonify({
            'success': True,
            'ruts': ruts,
            'total_ruts': len(ruts)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo RUTs: {str(e)}")
        return jsonify({'success': False, 'error': 'Error obteniendo RUTs'}), 500

@bp.route('/stats', methods=['GET'])
def get_stats():
    """
    API endpoint para obtener estadísticas de los datos cargados
    GET /stats - Obtener estadísticas generales
    """
    try:
        service = SubirDataService()
        
        # Obtener estadísticas
        total_records = len(service.obtener_todos_los_datos())
        total_employees = len(service.obtener_ruts_distintos())
        
        return jsonify({
            'success': True,
            'stats': {
                'total_records': total_records,
                'total_employees': total_employees,
                'service_status': 'active'
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        return jsonify({'success': False, 'error': 'Error obteniendo estadísticas'}), 500

@bp.errorhandler(APIError)
def handle_api_error(e):
    """Manejo de errores específicos de la API"""
    return jsonify({'success': False, 'error': e.description}), e.code