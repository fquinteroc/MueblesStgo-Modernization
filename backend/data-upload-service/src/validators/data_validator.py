import re
from datetime import datetime
from src.errors.errors import BadRequest

class DataValidator:
    
    @staticmethod
    def validate_fecha(fecha):
        """Valida que la fecha esté en formato yyyy/MM/dd"""
        if not fecha or not isinstance(fecha, str):
            raise BadRequest('Fecha inválida: None. Debe estar en formato yyyy/MM/dd')
        
        fecha = fecha.strip()
        if fecha == '':
            raise BadRequest('Fecha inválida: . Debe estar en formato yyyy/MM/dd')
        
        # Validar formato exacto con regex
        pattern = r'^\d{4}/\d{2}/\d{2}$'
        if not re.match(pattern, fecha):
            raise BadRequest(f'Fecha inválida: {fecha}. Debe estar en formato yyyy/MM/dd')
        
        try:
            datetime.strptime(fecha, '%Y/%m/%d')
            return True
        except ValueError:
            raise BadRequest(f'Fecha inválida: {fecha}. Debe estar en formato yyyy/MM/dd')
    
    @staticmethod
    def validate_hora(hora):
        """Valida que la hora esté en formato HH:mm"""
        if not hora or not isinstance(hora, str):
            raise BadRequest('Hora inválida: None. Debe estar en formato HH:mm')
        
        hora = hora.strip()
        if hora == '':
            raise BadRequest('Hora inválida: . Debe estar en formato HH:mm')
        
        # Validar formato exacto con regex
        pattern = r'^\d{2}:\d{2}$'
        if not re.match(pattern, hora):
            raise BadRequest(f'Hora inválida: {hora}. Debe estar en formato HH:mm')
        
        try:
            datetime.strptime(hora, '%H:%M')
            return True
        except ValueError:
            raise BadRequest(f'Hora inválida: {hora}. Debe estar en formato HH:mm')
    
    @staticmethod
    def validate_rut(rut):
        """Valida que el RUT esté en formato chileno abreviado (xxxxxxxx-x)"""
        if not rut or not isinstance(rut, str) or rut.strip() == '':
            raise BadRequest('RUT no puede estar vacío')
        
        # Formato: números-dígito verificador
        pattern = r'^\d{1,8}-[0-9Kk]$'
        if not re.match(pattern, rut.strip()):
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
        
        if not hasattr(file, 'filename') or file.filename == '':
            raise BadRequest('No se ha seleccionado ningún archivo')
        
        if file.filename.upper() != 'DATA.TXT':
            raise BadRequest('El nombre del archivo debe ser exactamente "DATA.TXT"')
        
        return True