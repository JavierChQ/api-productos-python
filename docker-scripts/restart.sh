#!/bin/bash
# Script para reiniciar la aplicación Django en Docker

echo "🔄 Reiniciando API de Productos..."

# Detener contenedores
docker-compose down

# Iniciar contenedores
docker-compose up -d

echo "✅ Aplicación reiniciada exitosamente!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - API: http://localhost:8000/api/productos/"
echo "   - Documentación: http://localhost:8000/api/docs/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - phpMyAdmin: http://localhost:8080/"
