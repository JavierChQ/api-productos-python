#!/bin/bash
# Script para instalar y configurar la aplicación

echo "🚀 Instalando API de Productos con Docker..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker Desktop."
    exit 1
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose."
    exit 1
fi

# Crear directorio para datos de MySQL si no existe
mkdir -p mysql-data

# Construir contenedores
echo "📦 Construyendo contenedores..."
docker-compose build

# Iniciar servicios
echo "🔄 Iniciando servicios..."
docker-compose up -d

# Esperar a que MySQL esté listo
echo "⏳ Esperando a que MySQL esté listo..."
sleep 15

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
docker-compose exec web python manage.py migrate

# Crear superusuario
echo "👤 Creando superusuario..."
docker-compose exec web python manage.py createsuperuser

echo "✅ ¡Instalación completada exitosamente!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - API: http://localhost:8000/api/productos/"
echo "   - Documentación: http://localhost:8000/api/docs/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - phpMyAdmin: http://localhost:8080/"
echo ""
echo "📋 Comandos útiles:"
echo "   - Ver logs: ./logs.sh"
echo "   - Detener: ./stop.sh"
echo "   - Reiniciar: ./restart.sh"
echo "   - Estado: ./status.sh"
