# API de Productos - Django REST Framework

Una API REST completa para la gestión de productos desarrollada con Django, Django REST Framework y MySQL.

## 🚀 Características

- **CRUD completo** para productos (Crear, Leer, Actualizar, Eliminar)
- **Base de datos MySQL** con configuración flexible
- **API REST** con Django REST Framework
- **Documentación automática** con Swagger/OpenAPI
- **Panel de administración** personalizado
- **Filtros y búsqueda** avanzados
- **Paginación** automática
- **Validaciones** robustas
- **Pruebas unitarias** completas

## 📋 Modelo de Datos

### Producto
- `id`: Identificador único (auto-incremento)
- `nombre`: Nombre del producto (máximo 200 caracteres)
- `categoria`: Categoría del producto (máximo 100 caracteres)
- `marca`: Marca del producto (máximo 100 caracteres)
- `precio`: Precio del producto (DecimalField con 2 decimales)
- `cantidad`: Cantidad disponible en inventario (entero positivo)
- `fecha_creacion`: Fecha y hora de creación (automática)
- `fecha_actualizacion`: Fecha y hora de última actualización (automática)

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.10+
- MySQL Server
- Git

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd api_productos_python
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**Windows:**
```bash
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos
1. Crear base de datos en MySQL:
```sql
CREATE DATABASE db_productos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configurar variables de entorno en `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_productos
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci

SECRET_KEY=tu_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Aplicar migraciones
```bash
python manage.py migrate
```

### 7. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 8. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

## 📚 Endpoints de la API

### Productos
- `GET /api/productos/` - Listar productos (con paginación y filtros)
- `POST /api/productos/` - Crear nuevo producto
- `GET /api/productos/{id}/` - Obtener producto específico
- `PUT /api/productos/{id}/` - Actualizar producto completo
- `PATCH /api/productos/{id}/` - Actualizar producto parcial
- `DELETE /api/productos/{id}/` - Eliminar producto

### Acciones Especiales
- `GET /api/productos/buscar/?q=termino` - Buscar productos
- `GET /api/productos/categoria/{categoria}/` - Filtrar por categoría
- `GET /api/productos/marca/{marca}/` - Filtrar por marca
- `GET /api/productos/sin-stock/` - Productos sin stock
- `POST /api/productos/{id}/reducir-stock/` - Reducir stock

### Parámetros de Consulta
- `page`: Número de página
- `categoria`: Filtrar por categoría
- `marca`: Filtrar por marca
- `precio_min`: Precio mínimo
- `precio_max`: Precio máximo
- `solo_con_stock`: Solo productos con stock (true/false)
- `orden`: Ordenamiento (precio_asc, precio_desc, nombre, fecha_desc)

## 📖 Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema JSON**: http://localhost:8000/api/schema/

## 🔧 Panel de Administración

Accede al panel de administración en:
http://localhost:8000/admin/

Funcionalidades del panel:
- Gestión completa de productos
- Búsqueda y filtros avanzados
- Edición en línea
- Acciones masivas (marcar sin stock, duplicar)
- Visualización de stock con colores

## 🧪 Ejecutar Pruebas

```bash
python manage.py test
```

Las pruebas incluyen:
- Pruebas del modelo Producto
- Pruebas de todos los endpoints de la API
- Pruebas de validaciones
- Pruebas de filtros y búsqueda
- Pruebas de paginación

## 📝 Ejemplos de Uso

### Crear un producto
```bash
curl -X POST http://localhost:8000/api/productos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell XPS 13",
    "categoria": "Electrónicos",
    "marca": "Dell",
    "precio": "1299.99",
    "cantidad": 10
  }'
```

### Listar productos con filtros
```bash
curl "http://localhost:8000/api/productos/?categoria=Electrónicos&precio_min=500&orden=precio_asc"
```

### Buscar productos
```bash
curl "http://localhost:8000/api/productos/buscar/?q=Dell"
```

### Reducir stock
```bash
curl -X POST http://localhost:8000/api/productos/1/reducir-stock/ \
  -H "Content-Type: application/json" \
  -d '{"cantidad": 2}'
```

## 🏗️ Estructura del Proyecto

```
api_productos_python/
├── api_productos/          # Configuración del proyecto
│   ├── settings.py        # Configuración de Django
│   ├── urls.py           # URLs principales
│   └── wsgi.py            # WSGI configuration
├── productos/              # App de productos
│   ├── models.py          # Modelo Producto
│   ├── views.py           # ViewSets y vistas
│   ├── serializers.py     # Serializadores DRF
│   ├── admin.py           # Configuración del admin
│   ├── urls.py            # URLs de la app
│   └── tests.py           # Pruebas unitarias
├── venv/                  # Entorno virtual
├── .env                   # Variables de entorno
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🔒 Seguridad

- Validaciones robustas en modelos y serializadores
- Sanitización de datos de entrada
- Configuración segura de base de datos
- Variables de entorno para datos sensibles

## 🚀 Despliegue

Para producción, considera:
- Cambiar `DEBUG=False`
- Configurar `ALLOWED_HOSTS` apropiadamente
- Usar variables de entorno para datos sensibles
- Configurar HTTPS
- Implementar autenticación y autorización
- Usar un servidor WSGI como Gunicorn
- Configurar un servidor web como Nginx

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades, crea un issue en el repositorio.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
