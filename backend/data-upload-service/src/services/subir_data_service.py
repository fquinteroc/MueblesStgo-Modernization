import os
from werkzeug.utils import secure_filename
from src.repositories.data_repository import DataRepository
from src.models.data import Data
from src.validators.data_validator import DataValidator
from src.errors.errors import BadRequest

ALLOWED_NAME = 'DATA.TXT'
UPLOAD_FOLDER = 'uploads'

class SubirDataService:
    
    def __init__(self):
        self.data_repository = DataRepository()
        self.validator = DataValidator()
    
    def guardar(self, file):
        """
        Guarda el archivo subido después de validarlo.
        
        Validaciones:
        - Archivo no puede estar vacío
        - Nombre debe ser exactamente "DATA.TXT" (case insensitive)
        - Debe ser un archivo válido
        """
        self.validator.validate_file(file)
        
        # Crear directorio si no existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Guardar archivo
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        
        return path

    def leer_txt(self, path):
        """
        Lee y procesa el archivo TXT línea por línea.
        
        Proceso:
        1. Limpieza de datos previos
        2. Lectura línea por línea
        3. Parsing de formato: fecha;hora;rut
        4. Validación de cada campo
        5. Almacenamiento en BD
        """
        try:
            self._limpiar_datos_previos()
            
            # 2. Lectura y procesamiento del archivo
            registros_procesados = 0
            
            with open(path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    fecha, hora, rut = self.validator.validate_line_format(line, line_number)
                    
                    data_record = Data(fecha=fecha, hora=hora, rut=rut)
                    self.data_repository.add(data_record)
                    registros_procesados += 1
            
            return {
                'mensaje': f'Archivo procesado exitosamente. {registros_procesados} registros importados.',
                'registros_procesados': registros_procesados
            }
            
        except Exception as e:
            self.data_repository.rollback()
            if isinstance(e, BadRequest):
                raise e
            else:
                raise BadRequest(f'Error procesando archivo: {str(e)}')
    
    def _limpiar_datos_previos(self):
        """
        Elimina todos los registros previos de marcación.
        
        Nota: En un sistema completo, aquí también se eliminarían:
        - Justificativos relacionados
        - Autorizaciones relacionadas
        """
        self.data_repository.delete_all()
    
    def obtener_todos_los_datos(self):
        """Obtiene todos los registros de marcación"""
        return self.data_repository.find_all()
    
    def obtener_datos_por_rut(self, rut):
        """Obtiene todos los registros de un RUT específico"""
        return self.data_repository.find_by_rut(rut)
    
    def obtener_ruts_distintos(self):
        """Obtiene todos los RUTs únicos en el sistema"""
        return self.data_repository.find_distinct_rut()