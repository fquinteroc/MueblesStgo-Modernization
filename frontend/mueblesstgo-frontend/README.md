# MueblesStgo Frontend


## 📋 Requisitos Previos

Antes de desplegar el frontend, asegúrate de tener instalado:

- **Node.js** (versión 18 o superior)
- **npm** (viene incluido con Node.js)
- **Angular CLI** (se instalará como dependencia)

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd tingeso/frontend/mueblesstgo-frontend
```

### 2. Instalar dependencias
```bash
npm install
```

## 🚀 Despliegue

### Desarrollo Local

Para ejecutar el servidor de desarrollo:

```bash
npm start
# o alternativamente
npm run ng serve
```

La aplicación estará disponible en `http://localhost:4200/`. La aplicación se recargará automáticamente si cambias algún archivo fuente.

## 🔗 Integración con Backend

Este frontend se conecta con los microservicios del backend:

- **data-upload-service** - Servicio de carga de datos
- **employee-management-service** - Servicio de gestión de empleados

Asegúrate de que los servicios del backend estén ejecutándose antes de usar la aplicación.
