#!/bin/bash
# Script para ejecutar pruebas en Docker

echo "🧪 Ejecutando pruebas..."

# Ejecutar pruebas
docker-compose exec web python manage.py test

echo "✅ Pruebas completadas!"
