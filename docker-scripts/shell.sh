#!/bin/bash
# Script para acceder al shell del contenedor Django

echo "🐚 Accediendo al shell del contenedor Django..."

# Acceder al shell del contenedor web
docker-compose exec web bash
