from django.contrib import admin
from django.utils.html import format_html
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Producto.
    
    Proporciona una interfaz completa para gestionar productos
    con funcionalidades avanzadas de búsqueda, filtrado y visualización.
    """
    
    # Campos a mostrar en la lista
    list_display = [
        'id',
        'nombre',
        'categoria',
        'marca',
        'precio_formateado',
        'cantidad',
        'tiene_stock_display',
        'fecha_creacion'
    ]
    
    # Campos editables en la lista (para edición rápida)
    list_editable = ['cantidad']
    
    # Campos de búsqueda
    search_fields = ['nombre', 'categoria', 'marca']
    
    # Filtros laterales
    list_filter = [
        'categoria',
        'marca',
        'fecha_creacion',
        'fecha_actualizacion'
    ]
    
    # Campos a mostrar en el formulario de edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'categoria', 'marca')
        }),
        ('Precio y Stock', {
            'fields': ('precio', 'cantidad')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    # Campos de solo lectura
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    # Ordenamiento por defecto
    ordering = ['-fecha_creacion']
    
    # Número de elementos por página
    list_per_page = 25
    
    # Acciones personalizadas
    actions = ['marcar_sin_stock', 'duplicar_productos']
    
    def precio_formateado(self, obj):
        """Muestra el precio formateado como moneda"""
        return obj.get_precio_formateado()
    precio_formateado.short_description = 'Precio'
    precio_formateado.admin_order_field = 'precio'
    
    def tiene_stock_display(self, obj):
        """Muestra el estado del stock con colores"""
        if obj.tiene_stock():
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Con Stock</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Sin Stock</span>'
            )
    tiene_stock_display.short_description = 'Stock'
    tiene_stock_display.admin_order_field = 'cantidad'
    
    def marcar_sin_stock(self, request, queryset):
        """Acción para marcar productos como sin stock"""
        updated = queryset.update(cantidad=0)
        self.message_user(
            request,
            f'{updated} producto(s) marcado(s) como sin stock.'
        )
    marcar_sin_stock.short_description = "Marcar como sin stock"
    
    def duplicar_productos(self, request, queryset):
        """Acción para duplicar productos seleccionados"""
        duplicados = 0
        for producto in queryset:
            # Crear copia del producto
            nuevo_producto = Producto(
                nombre=f"{producto.nombre} (Copia)",
                categoria=producto.categoria,
                marca=producto.marca,
                precio=producto.precio,
                cantidad=0  # Stock inicial en 0
            )
            nuevo_producto.save()
            duplicados += 1
        
        self.message_user(
            request,
            f'{duplicados} producto(s) duplicado(s) exitosamente.'
        )
    duplicar_productos.short_description = "Duplicar productos seleccionados"
    
    def get_queryset(self, request):
        """Optimizar consultas con select_related si fuera necesario"""
        return super().get_queryset(request)
    
    def save_model(self, request, obj, form, change):
        """Personalizar el guardado del modelo"""
        super().save_model(request, obj, form, change)
        
        # Log de la acción
        if change:
            self.message_user(request, f'Producto "{obj.nombre}" actualizado exitosamente.')
        else:
            self.message_user(request, f'Producto "{obj.nombre}" creado exitosamente.')
