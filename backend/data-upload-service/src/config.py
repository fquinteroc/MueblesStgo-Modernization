import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'mysql+pymysql://root:password@localhost:3306/mueblesstgo_data'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    
    # Configuración de Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'txt'}
    ALLOWED_FILENAME = 'DATA.TXT'
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # CORS (para el frontend de Angular)
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4200').split(',')
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False
    
    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self):
        """Engine options adaptados al tipo de base de datos"""
        db_uri = self.SQLALCHEMY_DATABASE_URI
        if db_uri and 'sqlite' in db_uri:
            # SQLite no soporta pool_timeout ni max_overflow
            return {
                'pool_pre_ping': True,
                'pool_recycle': 300
            }
        return super().SQLALCHEMY_ENGINE_OPTIONS

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_url = os.getenv('DATABASE_URL')
        if not db_url and os.getenv('FLASK_ENV') == 'production':
            raise ValueError("DATABASE_URL environment variable is required in production")
        return db_url or super().SQLALCHEMY_DATABASE_URI
    
    @property
    def SECRET_KEY(self):
        secret = os.getenv('SECRET_KEY')
        if (not secret or secret == 'dev-secret-key-change-in-production') and os.getenv('FLASK_ENV') == 'production':
            raise ValueError("SECRET_KEY environment variable is required in production")
        return secret or super().SECRET_KEY

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    # SQLite no soporta estas opciones del motor
    SQLALCHEMY_ENGINE_OPTIONS = {}

# Configuración según el entorno
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
