#!/bin/bash
# Script para restaurar backup de la base de datos

echo "🔄 Restaurando backup de la base de datos..."

# Verificar que se proporcionó el archivo de backup
if [ -z "$1" ]; then
    echo "❌ Error: Debes proporcionar el archivo de backup"
    echo "Uso: ./restore.sh backup_20240101_120000.sql"
    exit 1
fi

# Verificar que el archivo existe
if [ ! -f "backups/$1" ]; then
    echo "❌ Error: El archivo backups/$1 no existe"
    exit 1
fi

# Restaurar backup
docker-compose exec -T db mysql -u api_user -papi_password db_productos < backups/$1

echo "✅ Backup restaurado exitosamente!"
