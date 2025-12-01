-- Gestor de Eventos Locales - Esquema de Base de Datos
-- Autor: Martin Peñalva Artázcoz
-- Fecha: 2024
drop database eventos_locales;

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS eventos_locales
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE eventos_locales;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de eventos
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    capacity INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'activo',
    version INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_start_datetime (start_datetime),
    CHECK (end_datetime > start_datetime),
    CHECK (capacity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de participantes
CREATE TABLE IF NOT EXISTS participants (
    participant_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone INT,
    identifier VARCHAR(50) NOT NULL UNIQUE COMMENT 'DNI/NIE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_identifier (identifier),
    INDEX idx_full_name (last_name, first_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de inscripciones (relación N:M entre eventos y participantes)
CREATE TABLE IF NOT EXISTS event_registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    participant_id INT NOT NULL,
    registered_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'confirmado',
    FOREIGN KEY (event_id) REFERENCES events(event_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    UNIQUE KEY unique_registration (event_id, participant_id),
    INDEX idx_event_id (event_id),
    INDEX idx_participant_id (participant_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de logs de auditoría
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(100) NOT NULL,
    entity_id INT NOT NULL,
    details TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_entity (entity, entity_id),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Usuario administrador por defecto (contraseña: ADMINISTRADOR)
-- Hash generado con bcrypt para 'ADMINISTRADOR'
INSERT IGNORE INTO users (username, password_hash, role) 
VALUES ('ADMIN', '$2b$12$XkHbQ5jsEJvsDfoMCs5wQ.vTEtZ.PS4pWMi9h91PnF98wjyCIAjH.', 'admin');

-- ============================================================================
-- DATOS DE EJEMPLO PARA DESARROLLO Y PRUEBAS
-- ============================================================================

-- Insertar eventos de ejemplo (solo si no existen)
INSERT IGNORE INTO events (title, description, location, start_datetime, end_datetime, capacity, status) VALUES
('Concierto de Verano', 'Concierto al aire libre con bandas locales', 'Plaza Mayor', '2025-07-15 20:00:00', '2025-07-15 23:00:00', 500, 'activo'),
('Taller de Programación', 'Taller introductorio de Python para principiantes', 'Centro Cultural', '2025-08-10 10:00:00', '2025-08-10 14:00:00', 30, 'activo'),
('Feria de Artesanía', 'Feria anual de productos artesanales locales', 'Recinto Ferial', '2025-09-01 09:00:00', '2025-09-03 20:00:00', 1000, 'planificado'),
('Charla sobre Medio Ambiente', 'Conferencia sobre sostenibilidad y cambio climático', 'Auditorio Municipal', '2025-08-20 18:00:00', '2025-08-20 20:00:00', 200, 'activo');

-- Insertar participantes de ejemplo (solo si no existen)
INSERT IGNORE INTO participants (first_name, last_name, email, phone, identifier) VALUES
('Juan', 'García Pérez', 'juan.garcia@email.com', 612345678, '12345678A'),
('María', 'López Sánchez', 'maria.lopez@email.com', 623456789, '87654321B'),
('Carlos', 'Martínez Ruiz', 'carlos.martinez@email.com', 634567890, '11223344C'),
('Ana', 'Fernández Torres', 'ana.fernandez@email.com', 645678901, '44332211D'),
('Pedro', 'González Moreno', 'pedro.gonzalez@email.com', 656789012, '55667788E');

-- Insertar inscripciones de ejemplo (solo si no existen)
-- Nota: Estos IDs dependen de que los eventos y participantes se hayan insertado correctamente
INSERT IGNORE INTO event_registrations (event_id, participant_id, status) 
SELECT e.event_id, p.participant_id, 'confirmado'
FROM events e, participants p
WHERE (e.title = 'Concierto de Verano' AND p.identifier = '12345678A')
   OR (e.title = 'Concierto de Verano' AND p.identifier = '87654321B')
   OR (e.title = 'Concierto de Verano' AND p.identifier = '11223344C')
   OR (e.title = 'Taller de Programación' AND p.identifier = '12345678A')
   OR (e.title = 'Taller de Programación' AND p.identifier = '44332211D')
   OR (e.title = 'Feria de Artesanía' AND p.identifier = '87654321B')
   OR (e.title = 'Feria de Artesanía' AND p.identifier = '11223344C')
   OR (e.title = 'Charla sobre Medio Ambiente' AND p.identifier = '12345678A')
   OR (e.title = 'Charla sobre Medio Ambiente' AND p.identifier = '87654321B')
   OR (e.title = 'Charla sobre Medio Ambiente' AND p.identifier = '55667788E');
