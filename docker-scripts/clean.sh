#!/bin/bash
# Script para limpiar contenedores e imágenes

echo "🧹 Limpiando contenedores e imágenes..."

# Detener y eliminar contenedores
docker-compose down

# Eliminar imágenes
docker-compose down --rmi all

# Eliminar volúmenes
docker-compose down -v

# Limpiar sistema Docker
docker system prune -f

echo "✅ Limpieza completada exitosamente!"
