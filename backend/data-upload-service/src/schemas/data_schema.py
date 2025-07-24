from marshmallow import Schema, fields, validate, post_load
from datetime import datetime

class DataSchema(Schema):
    """Schema para validación y serialización de datos de marcación"""
    
    id = fields.Int(dump_only=True)
    fecha = fields.Str(
        required=True, 
        validate=validate.Regexp(
            r'^\d{4}/\d{2}/\d{2}$',
            error='Fecha debe estar en formato yyyy/MM/dd'
        )
    )
    hora = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\d{2}:\d{2}$',
            error='Hora debe estar en formato HH:mm'
        )
    )
    rut = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\d{1,8}-[0-9Kk]$',
            error='RUT debe estar en formato xxxxxxxx-x'
        )
    )
    
    @post_load
    def validate_datetime(self, data, **kwargs):
        """Validación adicional de fecha y hora"""
        try:
            datetime.strptime(data['fecha'], '%Y/%m/%d')
        except ValueError:
            raise validate.ValidationError('Fecha inválida', field_name='fecha')
        
        try:
            datetime.strptime(data['hora'], '%H:%M')
        except ValueError:
            raise validate.ValidationError('Hora inválida', field_name='hora')
        
        return data

class DataStatsSchema(Schema):
    """Schema para estadísticas de datos"""
    total_records = fields.Int()
    total_employees = fields.Int()
    date_range = fields.Dict()
    last_upload = fields.DateTime()

class FileUploadResponseSchema(Schema):
    """Schema para respuesta de carga de archivo"""
    success = fields.Bool()
    message = fields.Str()
    registros_procesados = fields.Int()
    errors = fields.List(fields.Str())