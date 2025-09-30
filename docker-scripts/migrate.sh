#!/bin/bash
# Script para ejecutar migraciones en Docker

echo "🗄️ Ejecutando migraciones..."

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

echo "✅ Migraciones ejecutadas exitosamente!"
