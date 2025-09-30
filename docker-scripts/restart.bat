@echo off
REM Script para reiniciar la aplicación Django en Docker (Windows)

echo 🔄 Reiniciando API de Productos...

REM Detener contenedores
docker-compose down

REM Iniciar contenedores
docker-compose up -d

echo ✅ Aplicación reiniciada exitosamente!
echo.
echo 🌐 URLs disponibles:
echo    - API: http://localhost:8000/api/productos/
echo    - Documentación: http://localhost:8000/api/docs/
echo    - Admin: http://localhost:8000/admin/
echo    - phpMyAdmin: http://localhost:8080/

pause
