# 👥 Employee Management Service - MueblesStgo

Microservicio Flask para la gestión completa de empleados del sistema MueblesStgo. Proporciona operaciones CRUD, búsquedas avanzadas y validaciones de negocio para el manejo de información de empleados.


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