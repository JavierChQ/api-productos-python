#!/bin/bash
# Script para crear superusuario en Docker

echo "👤 Creando superusuario..."

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

echo "✅ Superusuario creado exitosamente!"
