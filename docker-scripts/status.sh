#!/bin/bash
# Script para ver el estado de los contenedores

echo "📊 Estado de los contenedores:"
echo ""

# Mostrar estado de los contenedores
docker-compose ps

echo ""
echo "📋 Información adicional:"
echo "   - Ver logs: ./logs.sh"
echo "   - Acceder al shell: ./shell.sh"
echo "   - Detener: ./stop.sh"
