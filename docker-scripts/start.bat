@echo off
REM Script para iniciar la aplicación Django en Docker (Windows)

echo 🚀 Iniciando API de Productos con Docker...

REM Verificar que Docker esté instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado. Por favor instala Docker Desktop.
    pause
    exit /b 1
)

REM Verificar que Docker Compose esté instalado
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose no está instalado. Por favor instala Docker Compose.
    pause
    exit /b 1
)

REM Crear directorio para datos de MySQL si no existe
if not exist mysql-data mkdir mysql-data

REM Construir y ejecutar contenedores
echo 📦 Construyendo contenedores...
docker-compose build

echo 🔄 Iniciando servicios...
docker-compose up -d

REM Esperar a que MySQL esté listo
echo ⏳ Esperando a que MySQL esté listo...
timeout /t 10 /nobreak >nul

REM Ejecutar migraciones
echo 🗄️ Ejecutando migraciones...
docker-compose exec web python manage.py migrate

REM Crear superusuario (opcional)
echo 👤 ¿Deseas crear un superusuario? (y/n)
set /p response=
if /i "%response%"=="y" (
    docker-compose exec web python manage.py createsuperuser
)

echo ✅ ¡Aplicación iniciada exitosamente!
echo.
echo 🌐 URLs disponibles:
echo    - API: http://localhost:8000/api/productos/
echo    - Documentación: http://localhost:8000/api/docs/
echo    - Admin: http://localhost:8000/admin/
echo    - phpMyAdmin: http://localhost:8080/
echo.
echo 📋 Comandos útiles:
echo    - Ver logs: docker-compose logs -f
echo    - Detener: docker-compose down
echo    - Reiniciar: docker-compose restart

pause
