-- Inicialización de base de datos para Employee Management Service
-- MueblesStgo - Sistema de Gestión de Empleados

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS mueblesstgo_employees 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE mueblesstgo_employees;

-- Eliminar tabla si existe (para recrear)
DROP TABLE IF EXISTS employees;

-- Crear tabla de empleados
CREATE TABLE employees (
    rut VARCHAR(12) NOT NULL PRIMARY KEY COMMENT 'RUT del empleado en formato chileno (12345678-9)',
    apellidos VARCHAR(100) NOT NULL COMMENT 'Apellidos del empleado',
    nombres VARCHAR(100) NOT NULL COMMENT 'Nombres del empleado',
    fecha_nacimiento VARCHAR(10) NOT NULL COMMENT 'Fecha de nacimiento en formato yyyy/MM/dd',
    categoria ENUM('A', 'B', 'C') NOT NULL COMMENT 'Categoría laboral del empleado',
    fecha_ingreso VARCHAR(10) NOT NULL COMMENT 'Fecha de ingreso en formato yyyy/MM/dd',
    activo BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Estado del empleado (activo/inactivo)',
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro',
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última actualización'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Crear índices para optimizar consultas
CREATE INDEX idx_employees_activo ON employees(activo);
CREATE INDEX idx_employees_categoria ON employees(categoria);
CREATE INDEX idx_employees_fecha_ingreso ON employees(fecha_ingreso);
CREATE INDEX idx_employees_nombres ON employees(nombres);
CREATE INDEX idx_employees_apellidos ON employees(apellidos);
CREATE INDEX idx_employees_categoria_activo ON employees(categoria, activo);

-- Insertar datos de ejemplo para testing
INSERT INTO employees (rut, apellidos, nombres, fecha_nacimiento, categoria, fecha_ingreso) VALUES
('12345678-9', 'González Pérez', 'Juan Carlos', '1985/03/15', 'A', '2020/01/15'),
('98765432-1', 'Martínez Silva', 'María Elena', '1990/07/22', 'B', '2021/03/10'),
('11111111-1', 'López Rodríguez', 'Pedro Antonio', '1988/11/30', 'C', '2019/05/20'),
('22222222-2', 'Sánchez Torres', 'Ana Isabel', '1992/02/14', 'A', '2022/08/01'),
('33333333-3', 'Ramírez Morales', 'Carlos Eduardo', '1987/09/08', 'B', '2020/11/15'),
('44444444-4', 'Herrera Jiménez', 'Lucía Fernanda', '1991/12/03', 'C', '2021/07/22'),
('55555555-5', 'Castro Vargas', 'Miguel Ángel', '1984/05/17', 'A', '2018/12/10'),
('66666666-6', 'Rojas Mendoza', 'Patricia Alejandra', '1989/08/25', 'B', '2022/02/28'),
('77777777-7', 'Díaz Fuentes', 'Roberto Daniel', '1986/01/12', 'C', '2020/06/18'),
('88888888-8', 'Moreno Guerrero', 'Carmen Rosa', '1993/04/05', 'A', '2023/01/09')
ON DUPLICATE KEY UPDATE 
    apellidos = VALUES(apellidos),
    nombres = VALUES(nombres),
    fecha_nacimiento = VALUES(fecha_nacimiento),
    categoria = VALUES(categoria),
    fecha_ingreso = VALUES(fecha_ingreso);

-- Comentario sobre la estructura
SELECT 'Base de datos mueblesstgo_employees inicializada exitosamente' as mensaje;
SELECT COUNT(*) as 'Empleados insertados' FROM employees;
