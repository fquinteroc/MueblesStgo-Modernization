import pytest
import os
import tempfile
from io import BytesIO
from werkzeug.datastructures import FileStorage

# Configurar variables de entorno antes de importar la app
os.environ['FLASK_ENV'] = 'testing'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret-key'

from src.main import create_app
from src.database import db
from src.models.data import Data

@pytest.fixture
def app():
    """Crea una instancia de la aplicación para testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de prueba para realizar requests"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner de comandos CLI para testing"""
    return app.test_cli_runner()

@pytest.fixture
def sample_data_file():
    """Archivo de prueba válido DATA.TXT"""
    content = """2023/10/15;08:00;12345678-9
2023/10/15;17:30;12345678-9
2023/10/15;08:15;87654321-0
2023/10/15;17:45;87654321-0
2023/10/16;08:30;12345678-9
2023/10/16;17:00;12345678-9"""
    
    return FileStorage(
        stream=BytesIO(content.encode('utf-8')),
        filename='DATA.TXT',
        content_type='text/plain'
    )

@pytest.fixture
def invalid_data_file():
    """Archivo de prueba con formato inválido"""
    content = """2023-10-15;08:00;12345678-9
    2023/10/15;25:00;12345678-9
    2023/10/15;08:15;invalid-rut"""
    
    return FileStorage(
        stream=BytesIO(content.encode('utf-8')),
        filename='DATA.TXT',
        content_type='text/plain'
    )

@pytest.fixture
def wrong_filename_file():
    """Archivo con nombre incorrecto"""
    content = """2023/10/15;08:00;12345678-9"""
    
    return FileStorage(
        stream=BytesIO(content.encode('utf-8')),
        filename='WRONG.TXT',
        content_type='text/plain'
    )

@pytest.fixture
def empty_file():
    """Archivo vacío"""
    return FileStorage(
        stream=BytesIO(b''),
        filename='DATA.TXT',
        content_type='text/plain'
    )

@pytest.fixture
def sample_data_records():
    """Registros de datos de prueba"""
    return [
        Data(fecha='2023/10/15', hora='08:00', rut='12345678-9'),
        Data(fecha='2023/10/15', hora='17:30', rut='12345678-9'),
        Data(fecha='2023/10/15', hora='08:15', rut='87654321-0'),
        Data(fecha='2023/10/15', hora='17:45', rut='87654321-0'),
        Data(fecha='2023/10/16', hora='08:30', rut='12345678-9'),
        Data(fecha='2023/10/16', hora='17:00', rut='12345678-9')
    ]

@pytest.fixture
def populated_db(app, sample_data_records):
    """Base de datos poblada con datos de prueba"""
    with app.app_context():
        for record in sample_data_records:
            db.session.add(record)
        db.session.commit()
        yield db
        db.session.query(Data).delete()
        db.session.commit()

@pytest.fixture
def temp_upload_folder():
    """Directorio temporal para uploads"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # El directorio se limpia automáticamente
