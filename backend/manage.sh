#!/bin/bash

# Script de gestión del sistema MueblesStgo Backend
# Uso: ./manage.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función de ayuda
show_help() {
    echo "Script de gestión del sistema MueblesStgo Backend"
    echo ""
    echo "Uso: ./manage.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start           - Iniciar todos los servicios"
    echo "  stop            - Detener todos los servicios"
    echo "  restart         - Reiniciar todos los servicios"
    echo "  build           - Reconstruir las imágenes y iniciar"
    echo "  status          - Mostrar el estado de los servicios"
    echo "  logs            - Mostrar logs de todos los servicios"
    echo "  logs-data       - Mostrar logs del servicio de datos"
    echo "  logs-employees  - Mostrar logs del servicio de empleados"
    echo "  clean           - Limpiar contenedores y volúmenes (CUIDADO: elimina datos)"
    echo "  db-data         - Conectar a la base de datos de datos"
    echo "  db-employees    - Conectar a la base de datos de empleados"
    echo "  help            - Mostrar esta ayuda"
    echo ""
}

# Verificar que Docker está ejecutándose
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker no está ejecutándose. Por favor, inicia Docker y intenta de nuevo."
        exit 1
    fi
}

# Comandos principales
case "$1" in
    "start")
        print_message "Iniciando todos los servicios..."
        check_docker
        docker compose up -d
        print_message "Servicios iniciados. Use './manage.sh status' para verificar el estado."
        ;;
    
    "stop")
        print_message "Deteniendo todos los servicios..."
        check_docker
        docker compose down
        print_message "Servicios detenidos."
        ;;
    
    "restart")
        print_message "Reiniciando todos los servicios..."
        check_docker
        docker compose down
        docker compose up -d
        print_message "Servicios reiniciados."
        ;;
    
    "build")
        print_message "Reconstruyendo imágenes e iniciando servicios..."
        check_docker
        print_message "Eliminando imágenes antiguas..."
        docker compose down
        print_message "Reconstruyendo imágenes..."
        docker compose build --no-cache
        print_message "Iniciando servicios..."
        docker compose up -d
        print_message "Servicios reconstruidos e iniciados."
        ;;

    "status")
        print_message "Estado de los servicios:"
        check_docker
        docker compose ps
        ;;
    
    "logs")
        print_message "Mostrando logs de todos los servicios (Ctrl+C para salir):"
        check_docker
        docker compose logs -f
        ;;
    
    "logs-data")
        print_message "Mostrando logs del servicio de datos (Ctrl+C para salir):"
        check_docker
        docker compose logs -f data-upload-service mysql-data
        ;;
    
    "logs-employees")
        print_message "Mostrando logs del servicio de empleados (Ctrl+C para salir):"
        check_docker
        docker compose logs -f employee-management-service mysql-employees
        ;;
    
    "clean")
        print_warning "¡CUIDADO! Esto eliminará todos los contenedores y volúmenes."
        print_warning "Se perderán todos los datos almacenados."
        read -p "¿Estás seguro? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_message "Limpiando sistema..."
            check_docker
            docker compose down -v
            docker system prune -f
            print_message "Sistema limpiado."
        else
            print_message "Operación cancelada."
        fi
        ;;
    
    "db-data")
        print_message "Conectando a la base de datos de datos..."
        check_docker
        docker exec -it mueblesstgo_mysql_data mysql -u appuser -papppassword mueblesstgo_data
        ;;
    
    "db-employees")
        print_message "Conectando a la base de datos de empleados..."
        check_docker
        docker exec -it mueblesstgo_mysql_employees mysql -u appuser -papppassword mueblesstgo_employees
        ;;
    
    "help"|"")
        show_help
        ;;
    
    *)
        print_error "Comando desconocido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
