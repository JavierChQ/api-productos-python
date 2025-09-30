#!/bin/bash
# Script para detener la aplicación Django en Docker

echo "🛑 Deteniendo API de Productos..."

# Detener contenedores
docker-compose down

echo "✅ Aplicación detenida exitosamente!"
echo ""
echo "📋 Comandos útiles:"
echo "   - Eliminar volúmenes: docker-compose down -v"
echo "   - Eliminar imágenes: docker-compose down --rmi all"
echo "   - Ver contenedores: docker ps -a"
