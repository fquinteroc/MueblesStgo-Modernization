from src.database import db
from src.models.data import Data

class DataRepository:
    
    @staticmethod
    def delete_all():
        """Elimina todos los registros de marcación"""
        Data.query.delete()
        db.session.commit()
    
    @staticmethod
    def add(data_record):
        """Agrega un nuevo registro de marcación"""
        db.session.add(data_record)
        db.session.commit()
    
    @staticmethod
    def rollback():
        """Hace rollback de la transacción actual"""
        db.session.rollback()
    
    @staticmethod
    def find_all():
        """Obtiene todos los registros de marcación"""
        return Data.query.all()
    
    @staticmethod
    def find_by_rut(rut):
        """Obtiene todos los registros de un RUT específico"""
        return Data.query.filter_by(rut=rut).all()
    
    @staticmethod
    def find_by_rut_fecha(rut, fecha):
        """
        Buscar marcación específica por RUT y fecha (primera ocurrencia)
        Equivale a: SELECT * FROM data WHERE rut = :rut AND fecha = :fecha LIMIT 1
        """
        return Data.query.filter_by(rut=rut, fecha=fecha).first()
    
    @staticmethod
    def find_distinct_rut():
        """
        Obtener RUTs únicos
        Equivale a: SELECT DISTINCT rut FROM data
        """
        result = db.session.query(Data.rut.distinct()).all()
        return [r[0] for r in result]
    
    @staticmethod
    def find_fecha_rut(rut):
        """
        Buscar primera fecha de un empleado
        Equivale a: SELECT fecha FROM data WHERE rut = :rut LIMIT 1
        """
        result = Data.query.filter_by(rut=rut).first()
        return result.fecha if result else None
    
    @staticmethod
    def find_latest_by_rut_fecha(rut, fecha):
        """
        Buscar última marcación del día por RUT y fecha
        Equivale a: SELECT * FROM data WHERE rut = :rut AND fecha = :fecha ORDER BY hora DESC LIMIT 1
        """
        return Data.query.filter_by(rut=rut, fecha=fecha).order_by(Data.hora.desc()).first()
    
    @staticmethod
    def find_by_rut_fecha_all(rut, fecha):
        """
        Obtener todas las marcaciones de un RUT en una fecha específica
        """
        return Data.query.filter_by(rut=rut, fecha=fecha).order_by(Data.hora.asc()).all()
    
    @staticmethod
    def count_by_rut_fecha(rut, fecha):
        """
        Contar marcaciones de un RUT en una fecha específica
        """
        return Data.query.filter_by(rut=rut, fecha=fecha).count()
    
    @staticmethod
    def find_earliest_by_rut_fecha(rut, fecha):
        """
        Buscar primera marcación del día por RUT y fecha
        """
        return Data.query.filter_by(rut=rut, fecha=fecha).order_by(Data.hora.asc()).first()
    
    @staticmethod
    def find_by_date_range(fecha_inicio, fecha_fin):
        """
        Buscar marcaciones en un rango de fechas
        """
        return Data.query.filter(Data.fecha >= fecha_inicio, Data.fecha <= fecha_fin).all()
    
    @staticmethod
    def get_all_dates():
        """
        Obtener todas las fechas únicas en el sistema
        """
        result = db.session.query(Data.fecha.distinct()).order_by(Data.fecha.asc()).all()
        return [r[0] for r in result]