import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'mysql+pymysql://root:password@localhost:3306/mueblesstgo_employees'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # CORS (para el frontend de Angular)
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4200').split(',')
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Configuración de paginación
    EMPLOYEES_PER_PAGE = int(os.getenv('EMPLOYEES_PER_PAGE', '50'))
    MAX_EMPLOYEES_PER_PAGE = int(os.getenv('MAX_EMPLOYEES_PER_PAGE', '200'))

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    
    def __init__(self):
        super().__init__()
        # Verificar y configurar DATABASE_URL
        db_url = os.getenv('DATABASE_URL')
        if not db_url and os.getenv('FLASK_ENV') == 'production':
            raise ValueError("DATABASE_URL environment variable is required in production")
        if db_url:
            self.SQLALCHEMY_DATABASE_URI = db_url
            
        # Verificar y configurar SECRET_KEY
        secret = os.getenv('SECRET_KEY')
        if (not secret or secret == 'dev-secret-key-change-in-production') and os.getenv('FLASK_ENV') == 'production':
            raise ValueError("SECRET_KEY environment variable is required in production")
        if secret:
            self.SECRET_KEY = secret

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    SQLALCHEMY_ENGINE_OPTIONS = {}

# Configuración según el entorno
config = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig(),
    'testing': TestingConfig(),
    'default': DevelopmentConfig()
}
