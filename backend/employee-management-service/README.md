# 👥 Employee Management Service - MueblesStgo

Microservicio Flask para la gestión completa de empleados del sistema MueblesStgo. Proporciona operaciones CRUD, búsquedas avanzadas y validaciones de negocio para el manejo de información de empleados.

**🎯 Microservicio Backend Puro - Solo API REST**

## 🚀 Características

### Funcionalidades Principales

✅ **CRUD Completo**: Crear, leer, actualizar y eliminar empleados  
✅ **Validación Integral**: RUT chileno, fechas, categorías laborales  
✅ **Búsqueda Avanzada**: Por nombre, categoría, fechas de ingreso  
✅ **Soft Delete**: Eliminación lógica de empleados  
✅ **Paginación**: Resultados paginados para mejor rendimiento  
✅ **Estadísticas**: Métricas y reportes de empleados  

### Endpoints API Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información del microservicio |
| `GET` | `/health` | Verificación completa de salud |
| `GET` | `/api/ping` | Health check básico |
| **Gestión de Empleados** |
| `POST` | `/api/employees` | **Principal**: Crear empleado |
| `GET` | `/api/employees` | Listar empleados (paginado) |
| `GET` | `/api/employees/{rut}` | Obtener empleado por RUT |
| `PUT` | `/api/employees/{rut}` | Actualizar empleado |
| `DELETE` | `/api/employees/{rut}` | Eliminar empleado (soft delete) |
| `PATCH` | `/api/employees/{rut}/activate` | Reactivar empleado |
| **Consultas Especializadas** |
| `GET` | `/api/employees/category/{category}` | Empleados por categoría |
| `GET` | `/api/employees/search?name={name}` | Búsqueda por nombre |
| `GET` | `/api/employees/{rut}/category` | Solo obtener categoría |
| `GET` | `/api/employees/date-range` | Por rango de fechas |
| `GET` | `/api/employees/stats` | Estadísticas generales |

## 📋 Modelo de Datos

### Estructura del Empleado

```json
{
  "rut": "12345678-9",
  "nombres": "Juan Carlos",
  "apellidos": "Pérez González",
  "fecha_nacimiento": "1990/05/15",
  "categoria": "A",
  "fecha_ingreso": "2022/01/10",
  "activo": true,
  "fecha_creacion": "2023-07-25T10:30:00",
  "fecha_actualizacion": "2023-07-25T10:30:00"
}
```

### Categorías Válidas
- **A**: Categoría A
- **B**: Categoría B  
- **C**: Categoría C

### Validaciones de Negocio

#### RUT
- Formato chileno abreviado: `12345678-9`
- Dígito verificador válido (0-9, K, k)
- Unicidad en el sistema

#### Fechas
- Formato: `yyyy/MM/dd`
- Fecha de nacimiento: No futura, mínimo 18 años
- Fecha de ingreso: No futura, coherente con nacimiento

#### Nombres y Apellidos
- Mínimo 2 caracteres
- Máximo 100 caracteres
- No pueden estar vacíos

## 🔧 Instalación y Configuración

### Prerrequisitos

- Python 3.12+
- MySQL 8.0+
- Pipenv

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd employee-management-service

# Instalar dependencias
pipenv install

# Activar entorno virtual
pipenv shell

# Configurar variables de entorno
export FLASK_ENV=development
export DATABASE_URL=mysql+pymysql://user:password@localhost:3306/mueblesstgo_employees

# Ejecutar migraciones
flask db upgrade

# Iniciar el servidor
python src/main.py
```

### Variables de Entorno

```bash
# Base de datos
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/mueblesstgo_employees

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key
PORT=5002

# CORS
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# Paginación
EMPLOYEES_PER_PAGE=50
MAX_EMPLOYEES_PER_PAGE=200

# Logging
LOG_LEVEL=INFO
```

## 🐳 Docker

### Docker Compose

```yaml
services:
  employee-service:
    build: .
    ports:
      - "5002:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://appuser:apppassword@mysql:3306/mueblesstgo_employees
      - FLASK_ENV=production
    depends_on:
      - mysql
```

### Comandos Docker

```bash
# Construir imagen
docker build -t employee-management-service .

# Ejecutar con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs employee-service
```

## 📊 Ejemplos de Uso

### Crear Empleado

```bash
curl -X POST http://localhost:5002/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "rut": "12345678-9",
    "nombres": "Juan Carlos",
    "apellidos": "Pérez González",
    "fecha_nacimiento": "1990/05/15",
    "categoria": "A",
    "fecha_ingreso": "2022/01/10"
  }'
```

### Buscar Empleados

```bash
# Por categoría
curl http://localhost:5002/api/employees/category/A

# Por nombre
curl "http://localhost:5002/api/employees/search?name=Juan"

# Con paginación
curl "http://localhost:5002/api/employees?page=1&per_page=10"

# Por rango de fechas
curl "http://localhost:5002/api/employees/date-range?start_date=2020/01/01&end_date=2023/12/31"
```

### Actualizar Empleado

```bash
curl -X PUT http://localhost:5002/api/employees/12345678-9 \
  -H "Content-Type: application/json" \
  -d '{
    "categoria": "B",
    "apellidos": "Pérez Silva"
  }'
```

### Obtener Estadísticas

```bash
curl http://localhost:5002/api/employees/stats
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=src

# Tests específicos
pytest tests/test_employee_service.py
```

### Estructura de Tests

```
tests/
├── conftest.py                 # Configuración de pytest
├── test_employee_controller.py # Tests de endpoints
├── test_employee_service.py    # Tests de lógica de negocio
├── test_employee_repository.py # Tests de acceso a datos
├── test_employee_validator.py  # Tests de validación
├── test_employee_schema.py     # Tests de serialización
└── test_integration.py         # Tests de integración
```

## 🏗️ Arquitectura

### Patrón de Capas

```
┌─────────────────────────┐
│     Controllers         │ ← Flask Blueprints (HTTP)
├─────────────────────────┤
│     Services           │ ← Lógica de negocio
├─────────────────────────┤
│     Repositories       │ ← Acceso a datos
├─────────────────────────┤
│     Models/Schemas     │ ← Estructura de datos
└─────────────────────────┘
```

### Componentes Principales

- **Controllers**: Manejo de requests HTTP y respuestas
- **Services**: Lógica de negocio y orquestación
- **Repositories**: Abstracción de acceso a datos
- **Validators**: Validaciones de dominio
- **Schemas**: Serialización y validación de entrada
- **Models**: Definición de entidades de base de datos

## 🔧 Configuración Avanzada

### Base de Datos

El servicio soporta MySQL para producción y SQLite para desarrollo/testing:

```python
# Producción
DATABASE_URL=mysql+pymysql://user:pass@host:3306/db

# Desarrollo
DATABASE_URL=sqlite:///employees.db

# Testing
DATABASE_URL=sqlite:///:memory:
```

### Logging

Configuración de logs estructurados:

```python
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

### Paginación

Límites configurables para consultas:

```python
EMPLOYEES_PER_PAGE=50      # Por defecto
MAX_EMPLOYEES_PER_PAGE=200 # Máximo permitido
```

## 🚀 Producción

### Consideraciones

- Usar variables de entorno para configuración
- Configurar SSL/TLS en el proxy reverso
- Implementar rate limiting
- Configurar monitoring y alertas
- Usar un web server como Gunicorn

### Comando de Producción

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 "src.main:create_app()"
```

## 📈 Monitoreo

### Health Checks

- `GET /health` - Estado completo del servicio
- `GET /api/ping` - Health check básico
- `GET /api/health` - Estado específico de la API

### Métricas Disponibles

- Total de empleados activos/inactivos
- Distribución por categorías
- Estadísticas de fechas de ingreso
- Rendimiento de consultas

## 🤝 Contribución

1. Fork del proyecto
2. Crear feature branch (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push al branch (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es parte del sistema MueblesStgo y está bajo licencia MIT.

---

**Desarrollado para MueblesStgo - Sistema de Gestión de Empleados**
