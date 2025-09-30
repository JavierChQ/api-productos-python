# Scripts de Docker para API de Productos

Este directorio contiene scripts útiles para gestionar la aplicación Django con Docker.

## 📋 Scripts disponibles:

### **🚀 Instalación y configuración:**
- `install.sh` / `install.bat` - Instala y configura la aplicación completa
- `start.sh` / `start.bat` - Inicia la aplicación
- `stop.sh` / `stop.bat` - Detiene la aplicación
- `restart.sh` / `restart.bat` - Reinicia la aplicación
- `update.sh` - Actualiza la aplicación

### **🔧 Gestión de la aplicación:**
- `status.sh` / `status.bat` - Muestra el estado de los contenedores
- `logs.sh` - Muestra logs en tiempo real
- `shell.sh` - Accede al shell del contenedor Django
- `migrate.sh` - Ejecuta migraciones
- `createsuperuser.sh` - Crea superusuario
- `test.sh` - Ejecuta pruebas

### **💾 Base de datos:**
- `backup.sh` - Crea backup de la base de datos
- `restore.sh` - Restaura backup de la base de datos

### **🧹 Mantenimiento:**
- `clean.sh` - Limpia contenedores e imágenes

## 🚀 Uso rápido:

### **Instalación inicial:**
```bash
# Linux/macOS
chmod +x docker-scripts/*.sh
./docker-scripts/install.sh

# Windows
docker-scripts\install.bat
```

### **Gestión diaria:**
```bash
# Linux/macOS
./docker-scripts/start.sh
./docker-scripts/logs.sh
./docker-scripts/stop.sh

# Windows
docker-scripts\start.bat
docker-scripts\stop.bat
```

### **Desarrollo:**
```bash
# Acceder al shell
./docker-scripts/shell.sh

# Ejecutar migraciones
./docker-scripts/migrate.sh

# Ejecutar pruebas
./docker-scripts/test.sh
```

## 📝 Notas:

- Todos los scripts deben ejecutarse desde el directorio raíz del proyecto
- Los scripts están configurados para funcionar en Linux/macOS y Windows
- En Windows, puedes usar Git Bash, WSL o los archivos .bat
- Asegúrate de tener Docker y Docker Compose instalados