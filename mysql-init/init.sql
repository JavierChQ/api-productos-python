-- Script de inicialización para MySQL
-- Este archivo se ejecuta automáticamente cuando se crea el contenedor

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS db_productos 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE db_productos;

-- Crear usuario si no existe
CREATE USER IF NOT EXISTS 'api_user'@'%' IDENTIFIED BY 'api_password';

-- Otorgar permisos al usuario
GRANT ALL PRIVILEGES ON db_productos.* TO 'api_user'@'%';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Mostrar información de la base de datos
SELECT 'Base de datos db_productos creada exitosamente' AS status;
