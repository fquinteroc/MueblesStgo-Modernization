from src.database import db
from datetime import datetime

class Employee(db.Model):
    """
    Modelo de empleado basado en la entidad EmpleadoEntity del sistema monolítico
    """
    __tablename__ = 'employees'
    
    # Campos principales
    rut = db.Column(db.String(12), primary_key=True, nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.String(10), nullable=False)  # formato yyyy/MM/dd
    categoria = db.Column(db.String(1), nullable=False)  # A, B, C
    fecha_ingreso = db.Column(db.String(10), nullable=False)  # formato yyyy/MM/dd
    
    # Campos de control
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Employee {self.rut} - {self.nombres} {self.apellidos}>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario para serialización"""
        return {
            'rut': self.rut,
            'apellidos': self.apellidos,
            'nombres': self.nombres,
            'fecha_nacimiento': self.fecha_nacimiento,
            'categoria': self.categoria,
            'fecha_ingreso': self.fecha_ingreso,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    @property
    def nombre_completo(self):
        """Devuelve el nombre completo del empleado"""
        return f"{self.nombres} {self.apellidos}"
    
    def soft_delete(self):
        """Marca el empleado como inactivo (soft delete)"""
        self.activo = False
        self.fecha_actualizacion = datetime.utcnow()
    
    def activate(self):
        """Reactiva un empleado marcado como inactivo"""
        self.activo = True
        self.fecha_actualizacion = datetime.utcnow()
