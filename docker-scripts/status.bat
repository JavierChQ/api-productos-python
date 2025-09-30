@echo off
REM Script para ver el estado de los contenedores (Windows)

echo 📊 Estado de los contenedores:
echo.

REM Mostrar estado de los contenedores
docker-compose ps

echo.
echo 📋 Información adicional:
echo    - Ver logs: docker-compose logs -f
echo    - Acceder al shell: docker-compose exec web bash
echo    - Detener: docker-compose down

pause
