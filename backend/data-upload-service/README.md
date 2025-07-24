# 📁 Data Upload Service - MueblesStgo

Microservicio Flask para la carga y procesamiento de archivos de marcaciones de asistencia de empleados del sistema MueblesStgo.

**🎯 Microservicio Backend Puro - Solo API REST**



## 🚀 Características

### Funcionalidades Principales

✅ **API REST Pura**: Solo endpoints JSON para integración  
✅ **Carga de Archivos**: Acepta archivos `DATA.TXT` con formato específico  
✅ **Validación Completa**: Valida formato de fecha, hora y RUT
✅ **Procesamiento en Lote**: Procesa múltiples registros de marcación  


### Endpoints API Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información del microservicio |
| `GET` | `/ping` | Health check básico |
| `GET` | `/health` | Verificación completa de salud |
| `POST` | `/upload` | **Principal**: Procesar archivo DATA.TXT |
| `GET` | `/data` | Obtener todos los datos cargados |
| `GET` | `/data/rut/<rut>` | Datos por RUT específico |
| `GET` | `/ruts` | Lista de RUTs únicos |
| `GET` | `/stats` | Estadísticas generales |

## 📋 Formato de Archivo

### Especificaciones del archivo DATA.TXT

```
fecha;hora;rut
2022/06/01;08:00;671-9
2022/06/01;18:00;671-9
2022/06/02;07:59;982-4
2022/06/02;18:00;982-4
```


## 🔧 Instalación y Configuración

### Prerrequisitos

- Python 3.12+
- MySQL 8.0+
- Docker (opcional)

### Instalación Local

1. **Clonar el repositorio**
```bash
cd data-upload-service
```

### Instalación con Docker

1. **Ejecutar con Docker Compose**
```bash
docker-compose up -d
```

Esto levantará:
- MySQL en puerto 3306
- Data Upload Service en puerto 5000
- Adminer (opcional) en puerto 8080

## 🧪 Testing

### Ejecutar todas las pruebas
```bash
pipenv shell
pytest
```

### Ejecutar pruebas con cobertura
```bash
pytest --cov=src
```