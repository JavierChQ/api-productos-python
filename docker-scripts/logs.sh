#!/bin/bash
# Script para ver logs de la aplicación Django en Docker

echo "📋 Mostrando logs de la aplicación..."

# Mostrar logs de todos los servicios
docker-compose logs -f
