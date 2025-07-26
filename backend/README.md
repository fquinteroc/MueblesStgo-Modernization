# MueblesStgo Backend - Sistema de Microservicios

Este proyecto contiene los microservicios backend para el sistema MueblesStgo, implementados como una arquitectura de microservicios con Docker.

## Arquitectura

El sistema está compuesto por:

- **Data Upload Service** (Puerto 5001): Microservicio para la carga y procesamiento de datos de asistencia
- **Employee Management Service** (Puerto 5002): Microservicio para la gestión de empleados
- **MySQL Data DB** (Puerto 3306): Base de datos para el servicio de carga de datos
- **MySQL Employees DB** (Puerto 3308): Base de datos para el servicio de gestión de empleados

## Requisitos Previos

- Docker
- Docker Compose

## Ejecución del Sistema Completo

Para ejecutar todos los microservicios y sus bases de datos asociadas:

```bash
# Desde la carpeta raíz del backend
docker-compose up -d
```

Para ver los logs de todos los servicios:

```bash
docker-compose logs -f
```

Para ejecutar solo servicios específicos:

```bash
# Solo el servicio de carga de datos
docker-compose up -d mysql-data data-upload-service

# Solo el servicio de gestión de empleados
docker-compose up -d mysql-employees employee-management-service
```

## Puertos de los Servicios

- **Data Upload Service**: http://localhost:5001
- **Employee Management Service**: http://localhost:5002
- **MySQL Data DB**: localhost:3306
- **MySQL Employees DB**: localhost:3308

## Endpoints Principales

### Data Upload Service (Puerto 5001)
- `GET /ping` - Health check
- `POST /api/data/upload` - Subir archivo de datos

### Employee Management Service (Puerto 5002)
- `GET /api/ping` - Health check
- `GET /api/employees` - Listar empleados
- `POST /api/employees` - Crear empleado
- `GET /api/employees/{rut}` - Obtener empleado por RUT
- `PUT /api/employees/{rut}` - Actualizar empleado
- `DELETE /api/employees/{rut}` - Eliminar empleado



## Estructura del Proyecto

```
backend/
├── docker-compose.yml          # Orquestación de todos los servicios
├── README.md                   # Este archivo
├── data-upload-service/        # Microservicio de carga de datos
│   ├── Dockerfile
│   ├── docker-compose.yml     # Configuración individual
│   ├── init.sql               # Script de inicialización DB
│   └── src/                   # Código fuente
└── employee-management-service/  # Microservicio de gestión de empleados
    ├── Dockerfile
    ├── docker-compose.yml     # Configuración individual
    ├── init.sql               # Script de inicialización DB
    └── src/                   # Código fuente
```

## Variables de Entorno

Las variables de entorno están configuradas en el docker-compose.yml principal. Para entornos de producción, se recomienda:

1. Cambiar las contraseñas por defecto
2. Usar secretos de Docker para credenciales sensibles
3. Configurar `SECRET_KEY` con valores seguros
4. Ajustar `CORS_ORIGINS` según sea necesario
