#!/bin/bash
# Script para hacer backup de la base de datos

echo "💾 Creando backup de la base de datos..."

# Crear directorio de backups si no existe
mkdir -p backups

# Crear backup de la base de datos
docker-compose exec db mysqldump -u api_user -papi_password db_productos > backups/backup_$(date +%Y%m%d_%H%M%S).sql

echo "✅ Backup creado exitosamente en la carpeta backups/"
