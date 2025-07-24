import pytest
from unittest.mock import patch, MagicMock
from src.repositories.data_repository import DataRepository
from src.models.data import Data
from src.database import db

class TestDataRepository:
    """Pruebas para el repositorio de datos"""
    
    def test_delete_all(self, app):
        """Test de eliminación de todos los registros"""
        with app.app_context():
            # Agregar algunos registros de prueba
            record1 = Data(fecha='2023/10/15', hora='08:00', rut='12345678-9')
            record2 = Data(fecha='2023/10/15', hora='17:30', rut='87654321-0')
            db.session.add(record1)
            db.session.add(record2)
            db.session.commit()
            
            # Verificar que existen registros
            assert Data.query.count() == 2
            
            # Eliminar todos
            DataRepository.delete_all()
            
            # Verificar que se eliminaron todos
            assert Data.query.count() == 0
    
    def test_add(self, app):
        """Test de adición de un registro"""
        with app.app_context():
            record = Data(fecha='2023/10/15', hora='08:00', rut='12345678-9')
            
            DataRepository.add(record)
            
            # Verificar que se agregó
            assert Data.query.count() == 1
            saved_record = Data.query.first()
            assert saved_record.fecha == '2023/10/15'
            assert saved_record.hora == '08:00'
            assert saved_record.rut == '12345678-9'
    
    def test_rollback(self, app):
        """Test de rollback de transacción"""
        with app.app_context():
            with patch.object(db.session, 'rollback') as mock_rollback:
                DataRepository.rollback()
                mock_rollback.assert_called_once()
    
    def test_find_all(self, app, sample_data_records):
        """Test de búsqueda de todos los registros"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar todos
            result = DataRepository.find_all()
            
            assert len(result) == len(sample_data_records)
            assert all(isinstance(record, Data) for record in result)
    
    def test_find_by_rut(self, app, sample_data_records):
        """Test de búsqueda por RUT"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar por RUT específico
            rut = '12345678-9'
            result = DataRepository.find_by_rut(rut)
            
            assert len(result) == 4  # Según sample_data_records
            assert all(record.rut == rut for record in result)
    
    def test_find_by_rut_fecha(self, app, sample_data_records):
        """Test de búsqueda por RUT y fecha (primera ocurrencia)"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar por RUT y fecha
            rut = '12345678-9'
            fecha = '2023/10/15'
            result = DataRepository.find_by_rut_fecha(rut, fecha)
            
            assert result is not None
            assert result.rut == rut
            assert result.fecha == fecha
            assert result.hora == '08:00'  # Primera ocurrencia
    
    def test_find_by_rut_fecha_not_found(self, app):
        """Test de búsqueda por RUT y fecha cuando no existe"""
        with app.app_context():
            result = DataRepository.find_by_rut_fecha('99999999-9', '2023/01/01')
            assert result is None
    
    def test_find_distinct_rut(self, app, sample_data_records):
        """Test de búsqueda de RUTs únicos"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            result = DataRepository.find_distinct_rut()
            
            # Debe haber 2 RUTs únicos según sample_data_records
            assert len(result) == 2
            assert '12345678-9' in result
            assert '87654321-0' in result
    
    def test_find_fecha_rut(self, app, sample_data_records):
        """Test de búsqueda de primera fecha de un empleado"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar primera fecha
            rut = '12345678-9'
            result = DataRepository.find_fecha_rut(rut)
            
            assert result == '2023/10/15'
    
    def test_find_fecha_rut_not_found(self, app):
        """Test de búsqueda de fecha cuando no existe el RUT"""
        with app.app_context():
            result = DataRepository.find_fecha_rut('99999999-9')
            assert result is None
    
    def test_find_latest_by_rut_fecha(self, app, sample_data_records):
        """Test de búsqueda de última marcación del día"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar última marcación del día
            rut = '12345678-9'
            fecha = '2023/10/15'
            result = DataRepository.find_latest_by_rut_fecha(rut, fecha)
            
            assert result is not None
            assert result.rut == rut
            assert result.fecha == fecha
            assert result.hora == '17:30'  # Última hora del día
    
    def test_find_by_rut_fecha_all(self, app, sample_data_records):
        """Test de búsqueda de todas las marcaciones de un día"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar todas las marcaciones del día
            rut = '12345678-9'
            fecha = '2023/10/15'
            result = DataRepository.find_by_rut_fecha_all(rut, fecha)
            
            assert len(result) == 2  # Entrada y salida
            assert result[0].hora == '08:00'  # Primera (ordenado por hora ASC)
            assert result[1].hora == '17:30'  # Segunda
    
    def test_count_by_rut_fecha(self, app, sample_data_records):
        """Test de conteo de marcaciones por RUT y fecha"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Contar marcaciones
            rut = '12345678-9'
            fecha = '2023/10/15'
            count = DataRepository.count_by_rut_fecha(rut, fecha)
            
            assert count == 2
    
    def test_find_earliest_by_rut_fecha(self, app, sample_data_records):
        """Test de búsqueda de primera marcación del día"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar primera marcación del día
            rut = '12345678-9'
            fecha = '2023/10/15'
            result = DataRepository.find_earliest_by_rut_fecha(rut, fecha)
            
            assert result is not None
            assert result.rut == rut
            assert result.fecha == fecha
            assert result.hora == '08:00'  # Primera hora del día
    
    def test_find_by_date_range(self, app, sample_data_records):
        """Test de búsqueda por rango de fechas"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Buscar en rango de fechas
            fecha_inicio = '2023/10/15'
            fecha_fin = '2023/10/16'
            result = DataRepository.find_by_date_range(fecha_inicio, fecha_fin)
            
            assert len(result) == 6  # Todos los registros de muestra
            assert all(fecha_inicio <= record.fecha <= fecha_fin for record in result)
    
    def test_get_all_dates(self, app, sample_data_records):
        """Test de obtención de todas las fechas únicas"""
        with app.app_context():
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            result = DataRepository.get_all_dates()
            
            # Debe haber 2 fechas únicas ordenadas
            assert len(result) == 2
            assert result == ['2023/10/15', '2023/10/16']  # Ordenadas ASC
