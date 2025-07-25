class APIError(Exception):
    """Excepción base para errores de la API"""
    
    def __init__(self, description, code=500):
        super().__init__(description)
        self.description = description
        self.code = code

class BadRequest(APIError):
    """Error 400 - Solicitud incorrecta"""
    
    def __init__(self, description="Solicitud incorrecta"):
        super().__init__(description, 400)

class NotFound(APIError):
    """Error 404 - Recurso no encontrado"""
    
    def __init__(self, description="Recurso no encontrado"):
        super().__init__(description, 404)

class Conflict(APIError):
    """Error 409 - Conflicto en la solicitud"""
    
    def __init__(self, description="Conflicto en la solicitud"):
        super().__init__(description, 409)

class Forbidden(APIError):
    """Error 403 - Acceso prohibido"""
    
    def __init__(self, description="Acceso prohibido"):
        super().__init__(description, 403)

class ValidationError(BadRequest):
    """Error de validación de datos"""
    
    def __init__(self, description="Error de validación"):
        super().__init__(description)

class EmployeeNotFound(NotFound):
    """Error específico cuando no se encuentra un empleado"""
    
    def __init__(self, rut=None):
        if rut:
            description = f"Empleado con RUT {rut} no encontrado"
        else:
            description = "Empleado no encontrado"
        super().__init__(description)

class EmployeeAlreadyExists(Conflict):
    """Error cuando se intenta crear un empleado que ya existe"""
    
    def __init__(self, rut):
        description = f"Ya existe un empleado con RUT {rut}"
        super().__init__(description)
