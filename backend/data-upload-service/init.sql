-- Script de inicialización de la base de datos MueblesStgo
-- Data Upload Service

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS mueblesstgo_data CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE mueblesstgo_data;

CREATE TABLE IF NOT EXISTS data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha VARCHAR(10) NOT NULL COMMENT 'Fecha en formato yyyy/MM/dd',
    hora VARCHAR(5) NOT NULL COMMENT 'Hora en formato HH:mm',
    rut VARCHAR(12) NOT NULL COMMENT 'RUT del empleado en formato chileno',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_rut (rut),
    INDEX idx_fecha (fecha),
    INDEX idx_rut_fecha (rut, fecha),
    INDEX idx_fecha_hora (fecha, hora)
) ENGINE=InnoDB COMMENT='Tabla de marcaciones de asistencia de empleados';


CREATE TABLE IF NOT EXISTS upload_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    records_processed INT DEFAULT 0,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('success', 'error') DEFAULT 'success',
    error_message TEXT,
    file_size INT,
    
    INDEX idx_upload_date (upload_date),
    INDEX idx_status (status)
) ENGINE=InnoDB COMMENT='Log de cargas de archivos';


INSERT IGNORE INTO data (fecha, hora, rut) VALUES
('2024/01/15', '08:00', '671-9'),
('2024/01/15', '18:00', '671-9'),
('2024/01/15', '08:15', '982-4'),
('2024/01/15', '17:45', '982-4'),
('2024/01/16', '08:05', '671-9'),
('2024/01/16', '18:10', '671-9');


SELECT 'Database initialized successfully' AS status;