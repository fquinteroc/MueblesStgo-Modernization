import re
from datetime import datetime
from src.errors.errors import BadRequest

class DataValidator:
    
    @staticmethod
    def validate_fecha(fecha):
        """Valida que la fecha esté en formato yyyy/MM/dd"""
        try:
            datetime.strptime(fecha, '%Y/%m/%d')
            return True
        except ValueError:
            raise BadRequest(f'Fecha inválida: {fecha}. Debe estar en formato yyyy/MM/dd')
    
    @staticmethod
    def validate_hora(hora):
        """Valida que la hora esté en formato HH:mm"""
        try:
            datetime.strptime(hora, '%H:%M')
            return True
        except ValueError:
            raise BadRequest(f'Hora inválida: {hora}. Debe estar en formato HH:mm')
    
    @staticmethod
    def validate_rut(rut):
        """Valida que el RUT esté en formato chileno abreviado (xxxxxxxx-x)"""
        if not rut or not isinstance(rut, str):
            raise BadRequest('RUT no puede estar vacío')
        
        # Formato: números-dígito verificador
        pattern = r'^\d{1,8}-[0-9Kk]$'
        if not re.match(pattern, rut):
            raise BadRequest(f'RUT inválido: {rut}. Debe estar en formato xxxxxxxx-x')
        
        return True
    
    @staticmethod
    def validate_line_format(line, line_number):
        """Valida que una línea tenga exactamente 3 campos separados por punto y coma"""
        parts = line.strip().split(';')
        if len(parts) != 3:
            raise BadRequest(f'Línea {line_number} mal formateada. Debe tener exactamente 3 campos separados por ";"')
        
        fecha, hora, rut = parts
        
        DataValidator.validate_fecha(fecha)
        DataValidator.validate_hora(hora)
        DataValidator.validate_rut(rut)
        
        return fecha, hora, rut
    
    @staticmethod
    def validate_file(file):
        """Valida que el archivo sea válido"""
        if not file:
            raise BadRequest('No se ha proporcionado ningún archivo')
        
        if file.filename == '':
            raise BadRequest('No se ha seleccionado ningún archivo')
        
        if file.filename.upper() != 'DATA.TXT':
            raise BadRequest('El nombre del archivo debe ser exactamente "DATA.TXT"')
        
        return True