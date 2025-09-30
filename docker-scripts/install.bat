@echo off
REM Script para instalar y configurar la aplicación (Windows)

echo 🚀 Instalando API de Productos con Docker...

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

REM Construir contenedores
echo 📦 Construyendo contenedores...
docker-compose build

REM Iniciar servicios
echo 🔄 Iniciando servicios...
docker-compose up -d

REM Esperar a que MySQL esté listo
echo ⏳ Esperando a que MySQL esté listo...
timeout /t 15 /nobreak >nul

REM Ejecutar migraciones
echo 🗄️ Ejecutando migraciones...
docker-compose exec web python manage.py migrate

REM Crear superusuario
echo 👤 Creando superusuario...
docker-compose exec web python manage.py createsuperuser

echo ✅ ¡Instalación completada exitosamente!
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
echo    - Estado: docker-compose ps

pause
