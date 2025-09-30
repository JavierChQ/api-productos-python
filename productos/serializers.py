from rest_framework import serializers
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Producto.
    
    Proporciona serialización/deserialización de objetos Producto
    para la API REST, incluyendo validaciones personalizadas.
    """
    
    # Campos calculados (read-only)
    precio_formateado = serializers.CharField(source='get_precio_formateado', read_only=True)
    tiene_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'categoria',
            'marca',
            'precio',
            'cantidad',
            'fecha_creacion',
            'fecha_actualizacion',
            'precio_formateado',
            'tiene_stock'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_precio(self, value):
        """
        Validación personalizada para el campo precio.
        
        Args:
            value: Valor del precio a validar
            
        Returns:
            decimal.Decimal: Precio validado
            
        Raises:
            serializers.ValidationError: Si el precio no es válido
        """
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value
    
    def validate_cantidad(self, value):
        """
        Validación personalizada para el campo cantidad.
        
        Args:
            value: Valor de la cantidad a validar
            
        Returns:
            int: Cantidad validada
            
        Raises:
            serializers.ValidationError: Si la cantidad no es válida
        """
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value
    
    def validate(self, data):
        """
        Validación a nivel de objeto completo.
        
        Args:
            data: Diccionario con todos los datos del producto
            
        Returns:
            dict: Datos validados
            
        Raises:
            serializers.ValidationError: Si los datos no son válidos
        """
        # Validar que el nombre no esté vacío después de strip
        if 'nombre' in data:
            data['nombre'] = data['nombre'].strip()
            if not data['nombre']:
                raise serializers.ValidationError({
                    'nombre': 'El nombre del producto no puede estar vacío'
                })
        
        # Validar que la categoría no esté vacía después de strip
        if 'categoria' in data:
            data['categoria'] = data['categoria'].strip()
            if not data['categoria']:
                raise serializers.ValidationError({
                    'categoria': 'La categoría no puede estar vacía'
                })
        
        # Validar que la marca no esté vacía después de strip
        if 'marca' in data:
            data['marca'] = data['marca'].strip()
            if not data['marca']:
                raise serializers.ValidationError({
                    'marca': 'La marca no puede estar vacía'
                })
        
        return data


class ProductoListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listados de productos.
    
    Incluye solo los campos esenciales para optimizar
    el rendimiento en listados con muchos productos.
    """
    
    precio_formateado = serializers.CharField(source='get_precio_formateado', read_only=True)
    tiene_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'categoria',
            'marca',
            'precio',
            'cantidad',
            'precio_formateado',
            'tiene_stock'
        ]


class ProductoCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para operaciones de creación y actualización.
    
    Excluye campos de solo lectura para optimizar las operaciones
    de escritura en la base de datos.
    """
    
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria',
            'marca',
            'precio',
            'cantidad'
        ]
    
    def validate_precio(self, value):
        """Validación del precio para operaciones de escritura"""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value
    
    def validate_cantidad(self, value):
        """Validación de la cantidad para operaciones de escritura"""
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value
