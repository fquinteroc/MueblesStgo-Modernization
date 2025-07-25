import re
from datetime import datetime
from src.errors.errors import ValidationError

class EmployeeValidator:
    """Validador para datos de empleados"""
    
    # Categorías válidas
    VALID_CATEGORIES = ['A', 'B', 'C']
    
    @staticmethod
    def validate_rut(rut):
        """
        Valida que el RUT esté en formato chileno abreviado (xxxxxxxx-x)
        """
        if not rut or not isinstance(rut, str) or rut.strip() == '':
            raise ValidationError('RUT no puede estar vacío')
        
        rut = rut.strip()
        
        # Formato: números-dígito verificador
        pattern = r'^\d{1,8}-[0-9Kk]$'
        if not re.match(pattern, rut):
            raise ValidationError(f'RUT inválido: {rut}. Debe estar en formato xxxxxxxx-x')
        
        return True
    
    @staticmethod
    def validate_fecha(fecha, campo_nombre="fecha"):
        """
        Valida que la fecha esté en formato yyyy/MM/dd
        """
        if not fecha or not isinstance(fecha, str):
            raise ValidationError(f'{campo_nombre} inválida: debe estar en formato yyyy/MM/dd')
        
        fecha = fecha.strip()
        if fecha == '':
            raise ValidationError(f'{campo_nombre} no puede estar vacía')
        
        # Validar formato exacto con regex
        pattern = r'^\d{4}/\d{2}/\d{2}$'
        if not re.match(pattern, fecha):
            raise ValidationError(f'{campo_nombre} inválida: {fecha}. Debe estar en formato yyyy/MM/dd')
        
        try:
            datetime.strptime(fecha, '%Y/%m/%d')
            return True
        except ValueError:
            raise ValidationError(f'{campo_nombre} inválida: {fecha}. Debe ser una fecha válida')
    
    @staticmethod
    def validate_categoria(categoria):
        """
        Valida que la categoría sea A, B o C
        """
        if not categoria or not isinstance(categoria, str):
            raise ValidationError('Categoría no puede estar vacía')
        
        categoria = categoria.strip().upper()
        
        if categoria not in EmployeeValidator.VALID_CATEGORIES:
            raise ValidationError(f'Categoría inválida: {categoria}. Debe ser A, B o C')
        
        return True
    
    @staticmethod
    def validate_nombres(nombres):
        """
        Valida que los nombres no estén vacíos
        """
        if not nombres or not isinstance(nombres, str) or nombres.strip() == '':
            raise ValidationError('Nombres no pueden estar vacíos')
        
        nombres = nombres.strip()
        if len(nombres) < 2:
            raise ValidationError('Nombres deben tener al menos 2 caracteres')
        
        if len(nombres) > 100:
            raise ValidationError('Nombres no pueden exceder 100 caracteres')
        
        return True
    
    @staticmethod
    def validate_apellidos(apellidos):
        """
        Valida que los apellidos no estén vacíos
        """
        if not apellidos or not isinstance(apellidos, str) or apellidos.strip() == '':
            raise ValidationError('Apellidos no pueden estar vacíos')
        
        apellidos = apellidos.strip()
        if len(apellidos) < 2:
            raise ValidationError('Apellidos deben tener al menos 2 caracteres')
        
        if len(apellidos) > 100:
            raise ValidationError('Apellidos no pueden exceder 100 caracteres')
        
        return True
    
    @staticmethod
    def validate_fecha_nacimiento_logica(fecha_nacimiento):
        """
        Valida que la fecha de nacimiento sea lógica (no futura, no muy antigua)
        """
        try:
            fecha_dt = datetime.strptime(fecha_nacimiento, '%Y/%m/%d')
            hoy = datetime.now()
            
            # No puede ser fecha futura
            if fecha_dt > hoy:
                raise ValidationError('Fecha de nacimiento no puede ser futura')
            
            # No puede ser más de 100 años atrás
            if (hoy - fecha_dt).days > 36500:
                raise ValidationError('Fecha de nacimiento no puede ser más de 100 años atrás')
            
            # Debe tener al menos 18 años
            if (hoy - fecha_dt).days < 6570:
                raise ValidationError('El empleado debe tener al menos 18 años')
            
            return True
        except ValueError:
            raise ValidationError('Fecha de nacimiento inválida')
    
    @staticmethod
    def validate_fecha_ingreso_logica(fecha_ingreso, fecha_nacimiento=None):
        """
        Valida que la fecha de ingreso sea lógica
        """
        try:
            fecha_ingreso_dt = datetime.strptime(fecha_ingreso, '%Y/%m/%d')
            hoy = datetime.now()
            
            # No puede ser fecha futura
            if fecha_ingreso_dt > hoy:
                raise ValidationError('Fecha de ingreso no puede ser futura')
            
            # No puede ser más de 50 años atrás
            if (hoy - fecha_ingreso_dt).days > 18250:
                raise ValidationError('Fecha de ingreso no puede ser más de 50 años atrás')
            
            # Si se proporciona fecha de nacimiento, validar coherencia
            if fecha_nacimiento:
                fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%Y/%m/%d')
                if fecha_ingreso_dt < fecha_nacimiento_dt:
                    raise ValidationError('Fecha de ingreso no puede ser anterior a fecha de nacimiento')
                
                # Debe haber al menos 16 años entre nacimiento e ingreso
                if (fecha_ingreso_dt - fecha_nacimiento_dt).days < 5840:
                    raise ValidationError('Debe haber al menos 16 años entre fecha de nacimiento y fecha de ingreso')
            
            return True
        except ValueError:
            raise ValidationError('Fecha de ingreso inválida')
    
    @classmethod
    def validate_employee_data(cls, data):
        """
        Valida todos los datos de un empleado
        """
        # Validaciones básicas
        cls.validate_rut(data.get('rut'))
        cls.validate_nombres(data.get('nombres'))
        cls.validate_apellidos(data.get('apellidos'))
        cls.validate_fecha(data.get('fecha_nacimiento'), 'Fecha de nacimiento')
        cls.validate_fecha(data.get('fecha_ingreso'), 'Fecha de ingreso')
        cls.validate_categoria(data.get('categoria'))
        
        # Validaciones lógicas
        cls.validate_fecha_nacimiento_logica(data.get('fecha_nacimiento'))
        cls.validate_fecha_ingreso_logica(data.get('fecha_ingreso'), data.get('fecha_nacimiento'))
        
        return True
