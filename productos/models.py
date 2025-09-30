from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Producto(models.Model):
    """
    Modelo para representar un producto en el sistema.
    
    Campos:
    - id: Identificador único (auto-incremento)
    - nombre: Nombre del producto
    - categoria: Categoría del producto
    - marca: Marca del producto
    - precio: Precio del producto (DecimalField para precisión monetaria)
    - cantidad: Cantidad disponible en inventario
    - fecha_creacion: Fecha y hora de creación del registro
    - fecha_actualizacion: Fecha y hora de última actualización
    """
    
    # Campos del modelo
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre del producto",
        help_text="Nombre descriptivo del producto"
    )
    
    categoria = models.CharField(
        max_length=100,
        verbose_name="Categoría",
        help_text="Categoría a la que pertenece el producto"
    )
    
    marca = models.CharField(
        max_length=100,
        verbose_name="Marca",
        help_text="Marca del producto"
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio",
        help_text="Precio del producto en la moneda base"
    )
    
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad",
        help_text="Cantidad disponible en inventario"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']  # Ordenar por fecha de creación descendente
        indexes = [
            models.Index(fields=['categoria']),
            models.Index(fields=['marca']),
            models.Index(fields=['precio']),
        ]
    
    def __str__(self):
        """Representación en string del modelo"""
        return f"{self.nombre} - {self.marca} ({self.categoria})"
    
    def get_precio_formateado(self):
        """Retorna el precio formateado como moneda"""
        return f"${self.precio:,.2f}"
    
    def tiene_stock(self):
        """Verifica si el producto tiene stock disponible"""
        return self.cantidad > 0
    
    def reducir_stock(self, cantidad_a_reducir):
        """
        Reduce la cantidad de stock del producto
        
        Args:
            cantidad_a_reducir (int): Cantidad a reducir del stock
            
        Returns:
            bool: True si se pudo reducir el stock, False en caso contrario
        """
        if self.cantidad >= cantidad_a_reducir:
            self.cantidad -= cantidad_a_reducir
            self.save()
            return True
        return False
