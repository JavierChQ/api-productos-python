@echo off
REM Script para detener la aplicación Django en Docker (Windows)

echo 🛑 Deteniendo API de Productos...

REM Detener contenedores
docker-compose down

echo ✅ Aplicación detenida exitosamente!
echo.
echo 📋 Comandos útiles:
echo    - Eliminar volúmenes: docker-compose down -v
echo    - Eliminar imágenes: docker-compose down --rmi all
echo    - Ver contenedores: docker ps -a

pause
