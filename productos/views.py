from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Producto
from .serializers import (
    ProductoSerializer, 
    ProductoListSerializer, 
    ProductoCreateUpdateSerializer
)


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos.
    
    Proporciona operaciones CRUD completas:
    - GET /productos/ - Listar productos (con paginación y filtros)
    - POST /productos/ - Crear nuevo producto
    - GET /productos/{id}/ - Obtener producto específico
    - PUT/PATCH /productos/{id}/ - Actualizar producto
    - DELETE /productos/{id}/ - Eliminar producto
    
    Acciones adicionales:
    - GET /productos/buscar/ - Buscar productos por nombre, categoría o marca
    - GET /productos/categoria/{categoria}/ - Filtrar por categoría
    - GET /productos/marca/{marca}/ - Filtrar por marca
    - GET /productos/sin-stock/ - Productos sin stock
    - POST /productos/{id}/reducir-stock/ - Reducir stock de un producto
    """
    
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]  # Para desarrollo, en producción usar autenticación
    
    def get_serializer_class(self):
        """
        Retorna el serializador apropiado según la acción.
        
        Returns:
            Serializer: Serializador correspondiente a la acción
        """
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductoCreateUpdateSerializer
        return ProductoSerializer
    
    def get_queryset(self):
        """
        Filtra el queryset según los parámetros de consulta.
        
        Returns:
            QuerySet: Queryset filtrado según los parámetros
        """
        queryset = Producto.objects.all()
        
        # Filtro por categoría
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria__icontains=categoria)
        
        # Filtro por marca
        marca = self.request.query_params.get('marca', None)
        if marca:
            queryset = queryset.filter(marca__icontains=marca)
        
        # Filtro por rango de precio
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)
        
        # Filtro por stock disponible
        solo_con_stock = self.request.query_params.get('solo_con_stock', None)
        if solo_con_stock and solo_con_stock.lower() == 'true':
            queryset = queryset.filter(cantidad__gt=0)
        
        # Ordenamiento
        orden = self.request.query_params.get('orden', None)
        if orden == 'precio_asc':
            queryset = queryset.order_by('precio')
        elif orden == 'precio_desc':
            queryset = queryset.order_by('-precio')
        elif orden == 'nombre':
            queryset = queryset.order_by('nombre')
        elif orden == 'fecha_desc':
            queryset = queryset.order_by('-fecha_creacion')
        else:
            queryset = queryset.order_by('-fecha_creacion')  # Orden por defecto
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """
        Buscar productos por nombre, categoría o marca.
        
        Parámetros:
        - q: Término de búsqueda
        - limit: Límite de resultados (por defecto: 20)
        
        Returns:
            Response: Lista de productos que coinciden con la búsqueda
        """
        termino = request.query_params.get('q', '')
        limite = int(request.query_params.get('limit', 20))
        
        if not termino:
            return Response(
                {'error': 'Parámetro de búsqueda "q" es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Búsqueda en nombre, categoría y marca
        productos = Producto.objects.filter(
            Q(nombre__icontains=termino) |
            Q(categoria__icontains=termino) |
            Q(marca__icontains=termino)
        )[:limite]
        
        serializer = ProductoListSerializer(productos, many=True)
        
        return Response({
            'resultados': serializer.data,
            'total': len(serializer.data),
            'termino_busqueda': termino
        })
    
    @action(detail=False, methods=['get'], url_path='categoria/(?P<categoria>[^/.]+)')
    def por_categoria(self, request, categoria=None):
        """
        Filtrar productos por categoría específica.
        
        Args:
            categoria: Nombre de la categoría
            
        Returns:
            Response: Lista de productos de la categoría
        """
        productos = Producto.objects.filter(categoria__icontains=categoria)
        serializer = ProductoListSerializer(productos, many=True)
        
        return Response({
            'categoria': categoria,
            'productos': serializer.data,
            'total': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'], url_path='marca/(?P<marca>[^/.]+)')
    def por_marca(self, request, marca=None):
        """
        Filtrar productos por marca específica.
        
        Args:
            marca: Nombre de la marca
            
        Returns:
            Response: Lista de productos de la marca
        """
        productos = Producto.objects.filter(marca__icontains=marca)
        serializer = ProductoListSerializer(productos, many=True)
        
        return Response({
            'marca': marca,
            'productos': serializer.data,
            'total': len(serializer.data)
        })
    
    @action(detail=False, methods=['get'])
    def sin_stock(self, request):
        """
        Obtener productos sin stock disponible.
        
        Returns:
            Response: Lista de productos con cantidad = 0
        """
        productos = Producto.objects.filter(cantidad=0)
        serializer = ProductoListSerializer(productos, many=True)
        
        return Response({
            'productos_sin_stock': serializer.data,
            'total': len(serializer.data)
        })
    
    @action(detail=True, methods=['post'])
    def reducir_stock(self, request, pk=None):
        """
        Reducir el stock de un producto específico.
        
        Body:
        {
            "cantidad": 5
        }
        
        Returns:
            Response: Resultado de la operación
        """
        producto = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        
        if not isinstance(cantidad, int) or cantidad <= 0:
            return Response(
                {'error': 'La cantidad debe ser un número entero positivo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if producto.reducir_stock(cantidad):
            serializer = ProductoSerializer(producto)
            return Response({
                'mensaje': f'Stock reducido exitosamente. Stock actual: {producto.cantidad}',
                'producto': serializer.data
            })
        else:
            return Response(
                {'error': 'No hay suficiente stock disponible'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def list(self, request, *args, **kwargs):
        """
        Lista productos con paginación y filtros.
        
        Parámetros de consulta:
        - page: Número de página
        - categoria: Filtrar por categoría
        - marca: Filtrar por marca
        - precio_min: Precio mínimo
        - precio_max: Precio máximo
        - solo_con_stock: Solo productos con stock
        - orden: Ordenamiento (precio_asc, precio_desc, nombre, fecha_desc)
        
        Returns:
            Response: Lista paginada de productos
        """
        queryset = self.get_queryset()
        
        # Paginación manual para mayor control
        page_size = 20
        page_number = request.query_params.get('page', 1)
        
        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            page_number = 1
        
        paginator = Paginator(queryset, page_size)
        
        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)
        
        serializer = self.get_serializer(page_obj.object_list, many=True)
        
        return Response({
            'productos': serializer.data,
            'paginacion': {
                'pagina_actual': page_obj.number,
                'total_paginas': paginator.num_pages,
                'total_productos': paginator.count,
                'productos_por_pagina': page_size,
                'tiene_siguiente': page_obj.has_next(),
                'tiene_anterior': page_obj.has_previous(),
            }
        })