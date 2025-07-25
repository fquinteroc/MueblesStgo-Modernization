from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError as MarshmallowValidationError, post_load
from src.validators.employee_validator import EmployeeValidator
from src.errors.errors import ValidationError

class EmployeeSchema(Schema):
    """Schema para serialización y validación de empleados"""
    
    rut = fields.Str(required=True, validate=validate.Length(min=3, max=12))
    apellidos = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    nombres = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    fecha_nacimiento = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    categoria = fields.Str(required=True, validate=validate.OneOf(['A', 'B', 'C']))
    fecha_ingreso = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    activo = fields.Bool(load_default=True, dump_default=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    fecha_actualizacion = fields.DateTime(dump_only=True)
    
    @validates('rut')
    def validate_rut(self, value, **kwargs):
        """Validación personalizada para RUT"""
        try:
            EmployeeValidator.validate_rut(value)
        except ValidationError as e:
            raise MarshmallowValidationError(str(e))
    
    @validates('fecha_nacimiento')
    def validate_fecha_nacimiento(self, value, **kwargs):
        """Validación personalizada para fecha de nacimiento"""
        try:
            EmployeeValidator.validate_fecha(value, 'Fecha de nacimiento')
            EmployeeValidator.validate_fecha_nacimiento_logica(value)
        except ValidationError as e:
            raise MarshmallowValidationError(str(e))
    
    @validates('fecha_ingreso')
    def validate_fecha_ingreso(self, value, **kwargs):
        """Validación personalizada para fecha de ingreso"""
        try:
            EmployeeValidator.validate_fecha(value, 'Fecha de ingreso')
        except ValidationError as e:
            raise MarshmallowValidationError(str(e))
    
    @validates('nombres')
    def validate_nombres(self, value, **kwargs):
        """Validación personalizada para nombres"""
        try:
            EmployeeValidator.validate_nombres(value)
        except ValidationError as e:
            raise MarshmallowValidationError(str(e))
    
    @validates('apellidos')
    def validate_apellidos(self, value, **kwargs):
        """Validación personalizada para apellidos"""
        try:
            EmployeeValidator.validate_apellidos(value)
        except ValidationError as e:
            raise MarshmallowValidationError(str(e))
    
    @validates_schema
    def validate_fechas_coherencia(self, data, **kwargs):
        """Validación de coherencia entre fechas"""
        if 'fecha_nacimiento' in data and 'fecha_ingreso' in data:
            try:
                EmployeeValidator.validate_fecha_ingreso_logica(
                    data['fecha_ingreso'], 
                    data['fecha_nacimiento']
                )
            except ValidationError as e:
                raise MarshmallowValidationError({'fecha_ingreso': str(e)})
    
    @post_load
    def normalize_data(self, data, **kwargs):
        """Normaliza los datos después de la validación"""
        # Normalizar RUT y categoría a mayúsculas
        if 'rut' in data:
            data['rut'] = data['rut'].strip()
        if 'categoria' in data:
            data['categoria'] = data['categoria'].strip().upper()
        if 'nombres' in data:
            data['nombres'] = data['nombres'].strip()
        if 'apellidos' in data:
            data['apellidos'] = data['apellidos'].strip()
        
        return data

class EmployeeUpdateSchema(EmployeeSchema):
    """Schema para actualización de empleados (campos opcionales excepto RUT)"""
    
    rut = fields.Str(dump_only=True)
    apellidos = fields.Str(validate=validate.Length(min=2, max=100))
    nombres = fields.Str(validate=validate.Length(min=2, max=100))
    fecha_nacimiento = fields.Str(validate=validate.Length(min=10, max=10))
    categoria = fields.Str(validate=validate.OneOf(['A', 'B', 'C']))
    fecha_ingreso = fields.Str(validate=validate.Length(min=10, max=10))
    activo = fields.Bool()

class EmployeeCategoryResponseSchema(Schema):
    """Schema simplificado para respuesta de categoría"""
    
    rut = fields.Str(required=True)
    categoria = fields.Str(required=True)
    nombres = fields.Str(required=True)
    apellidos = fields.Str(required=True)

class EmployeeListResponseSchema(Schema):
    """Schema para respuestas de lista de empleados con metadata"""
    
    employees = fields.List(fields.Nested(EmployeeSchema))
    total = fields.Int()
    page = fields.Int()
    per_page = fields.Int()
    pages = fields.Int()

class EmployeeSearchResponseSchema(Schema):
    """Schema para respuestas de búsqueda"""
    
    employees = fields.List(fields.Nested(EmployeeSchema))
    total = fields.Int()
    search_term = fields.Str()

class APIResponseSchema(Schema):
    """Schema genérico para respuestas de la API"""
    
    success = fields.Bool(load_default=True)
    message = fields.Str()
    data = fields.Raw()
    error = fields.Str()
    code = fields.Int()
