import pytest
from src.models.data import Data

class TestDataModel:
    """Pruebas para el modelo Data"""
    
    def test_create_data_instance(self):
        """Test de creación de instancia del modelo Data"""
        data = Data(
            fecha='2023/10/15',
            hora='08:00',
            rut='12345678-9'
        )
        
        assert data.fecha == '2023/10/15'
        assert data.hora == '08:00'
        assert data.rut == '12345678-9'
        assert data.id is None  # ID se asigna al guardar en BD
    
    def test_data_repr(self):
        """Test de representación string del modelo"""
        data = Data(
            fecha='2023/10/15',
            hora='08:00',
            rut='12345678-9'
        )
        
        expected = "<Data 2023/10/15 08:00 12345678-9>"
        assert repr(data) == expected
    
    def test_data_tablename(self):
        """Test del nombre de tabla"""
        assert Data.__tablename__ == 'data'
    
    def test_data_columns(self):
        """Test de las columnas del modelo"""
        # Verificar que las columnas existen
        assert hasattr(Data, 'id')
        assert hasattr(Data, 'fecha')
        assert hasattr(Data, 'hora')
        assert hasattr(Data, 'rut')
        
        # Verificar propiedades de las columnas
        assert Data.id.primary_key is True
        assert Data.fecha.nullable is False
        assert Data.hora.nullable is False
        assert Data.rut.nullable is False
    
    def test_data_persistence(self, app):
        """Test de persistencia del modelo en base de datos"""
        with app.app_context():
            from src.database import db
            
            # Crear y guardar registro
            data = Data(
                fecha='2023/10/15',
                hora='08:00',
                rut='12345678-9'
            )
            db.session.add(data)
            db.session.commit()
            
            # Verificar que se guardó
            assert data.id is not None
            
            # Recuperar de la base de datos
            retrieved = Data.query.filter_by(id=data.id).first()
            assert retrieved is not None
            assert retrieved.fecha == '2023/10/15'
            assert retrieved.hora == '08:00'
            assert retrieved.rut == '12345678-9'
    
    def test_data_query_operations(self, app, sample_data_records):
        """Test de operaciones de consulta del modelo"""
        with app.app_context():
            from src.database import db
            
            # Agregar registros de prueba
            for record in sample_data_records:
                db.session.add(record)
            db.session.commit()
            
            # Test de consultas
            all_data = Data.query.all()
            assert len(all_data) == len(sample_data_records)
            
            # Query por RUT
            rut_data = Data.query.filter_by(rut='12345678-9').all()
            assert len(rut_data) == 4  # Según sample_data_records
            
            # Query por fecha
            fecha_data = Data.query.filter_by(fecha='2023/10/15').all()
            assert len(fecha_data) == 4  # Según sample_data_records
            
            # Query por fecha y RUT
            specific_data = Data.query.filter_by(
                fecha='2023/10/15', 
                rut='12345678-9'
            ).all()
            assert len(specific_data) == 2
    
    def test_data_field_lengths(self):
        """Test de longitudes de campos"""
        # Verificar longitudes máximas de los campos String
        assert Data.fecha.type.length == 10  # yyyy/MM/dd
        assert Data.hora.type.length == 5   # HH:mm
        assert Data.rut.type.length == 12   # xxxxxxxx-x
    
    def test_data_with_different_rut_formats(self, app):
        """Test con diferentes formatos válidos de RUT"""
        with app.app_context():
            from src.database import db
            
            ruts = [
                '12345678-9',
                '1234567-8', 
                '12345-6',
                '1-9',
                '87654321-K'
            ]
            
            for i, rut in enumerate(ruts):
                data = Data(
                    fecha='2023/10/15',
                    hora=f'0{8+i}:00',
                    rut=rut
                )
                db.session.add(data)
            
            db.session.commit()
            
            # Verificar que todos se guardaron correctamente
            saved_data = Data.query.all()
            assert len(saved_data) == len(ruts)
            
            saved_ruts = [record.rut for record in saved_data]
            for rut in ruts:
                assert rut in saved_ruts
    
    def test_data_equality(self):
        """Test de igualdad de instancias (por id)"""
        data1 = Data(
            fecha='2023/10/15',
            hora='08:00',
            rut='12345678-9'
        )
        data1.id = 1
        
        data2 = Data(
            fecha='2023/10/15',
            hora='08:00',
            rut='12345678-9'
        )
        data2.id = 1
        
        data3 = Data(
            fecha='2023/10/15',
            hora='08:00',
            rut='12345678-9'
        )
        data3.id = 2
        
        # Objetos con mismo ID son iguales
        assert data1.id == data2.id
        # Objetos con diferente ID son diferentes
        assert data1.id != data3.id
