#!/bin/bash
# Script para actualizar la aplicación

echo "🔄 Actualizando la aplicación..."

# Detener contenedores
docker-compose down

# Construir nuevas imágenes
docker-compose build --no-cache

# Iniciar contenedores
docker-compose up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

echo "✅ Aplicación actualizada exitosamente!"
