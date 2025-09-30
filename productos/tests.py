from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Producto


class ProductoModelTest(TestCase):
    """
    Pruebas para el modelo Producto.
    
    Verifica la funcionalidad básica del modelo,
    validaciones y métodos personalizados.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.producto = Producto.objects.create(
            nombre="Laptop Dell XPS 13",
            categoria="Electrónicos",
            marca="Dell",
            precio=Decimal('1299.99'),
            cantidad=10
        )
    
    def test_crear_producto(self):
        """Prueba la creación de un producto"""
        self.assertEqual(self.producto.nombre, "Laptop Dell XPS 13")
        self.assertEqual(self.producto.categoria, "Electrónicos")
        self.assertEqual(self.producto.marca, "Dell")
        self.assertEqual(self.producto.precio, Decimal('1299.99'))
        self.assertEqual(self.producto.cantidad, 10)
        self.assertTrue(self.producto.tiene_stock())
    
    def test_str_representation(self):
        """Prueba la representación en string del modelo"""
        expected = "Laptop Dell XPS 13 - Dell (Electrónicos)"
        self.assertEqual(str(self.producto), expected)
    
    def test_precio_formateado(self):
        """Prueba el método get_precio_formateado"""
        precio_formateado = self.producto.get_precio_formateado()
        self.assertEqual(precio_formateado, "$1,299.99")
    
    def test_tiene_stock(self):
        """Prueba el método tiene_stock"""
        # Producto con stock
        self.assertTrue(self.producto.tiene_stock())
        
        # Producto sin stock
        self.producto.cantidad = 0
        self.assertFalse(self.producto.tiene_stock())
    
    def test_reducir_stock_exitoso(self):
        """Prueba la reducción exitosa de stock"""
        cantidad_inicial = self.producto.cantidad
        cantidad_a_reducir = 3
        
        resultado = self.producto.reducir_stock(cantidad_a_reducir)
        
        self.assertTrue(resultado)
        self.assertEqual(self.producto.cantidad, cantidad_inicial - cantidad_a_reducir)
    
    def test_reducir_stock_insuficiente(self):
        """Prueba la reducción de stock cuando no hay suficiente"""
        cantidad_inicial = self.producto.cantidad
        cantidad_a_reducir = cantidad_inicial + 5  # Más de lo disponible
        
        resultado = self.producto.reducir_stock(cantidad_a_reducir)
        
        self.assertFalse(resultado)
        self.assertEqual(self.producto.cantidad, cantidad_inicial)  # No debe cambiar
    
    def test_meta_ordering(self):
        """Prueba el ordenamiento por defecto del modelo"""
        # Crear otro producto
        Producto.objects.create(
            nombre="Mouse Logitech",
            categoria="Accesorios",
            marca="Logitech",
            precio=Decimal('29.99'),
            cantidad=50
        )
        
        productos = Producto.objects.all()
        self.assertEqual(productos[0], self.producto)  # El más reciente primero


class ProductoAPITest(APITestCase):
    """
    Pruebas para la API REST de productos.
    
    Verifica todos los endpoints CRUD y funcionalidades adicionales.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas de API"""
        self.producto = Producto.objects.create(
            nombre="Smartphone Samsung Galaxy",
            categoria="Electrónicos",
            marca="Samsung",
            precio=Decimal('899.99'),
            cantidad=15
        )
        
        self.producto_data = {
            'nombre': 'Tablet iPad Pro',
            'categoria': 'Electrónicos',
            'marca': 'Apple',
            'precio': '1099.99',
            'cantidad': 8
        }
    
    def test_listar_productos(self):
        """Prueba el endpoint para listar productos"""
        url = reverse('producto-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('productos', response.data)
        self.assertIn('paginacion', response.data)
        self.assertEqual(len(response.data['productos']), 1)
    
    def test_crear_producto(self):
        """Prueba el endpoint para crear un producto"""
        url = reverse('producto-list')
        response = self.client.post(url, self.producto_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 2)
        self.assertEqual(Producto.objects.get(nombre='Tablet iPad Pro').marca, 'Apple')
    
    def test_obtener_producto(self):
        """Prueba el endpoint para obtener un producto específico"""
        url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.producto.nombre)
        self.assertEqual(response.data['marca'], self.producto.marca)
    
    def test_actualizar_producto(self):
        """Prueba el endpoint para actualizar un producto"""
        url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        datos_actualizacion = {
            'nombre': 'Smartphone Samsung Galaxy S21',
            'precio': '999.99',
            'cantidad': 20
        }
        response = self.client.patch(url, datos_actualizacion, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Smartphone Samsung Galaxy S21')
        self.assertEqual(self.producto.precio, Decimal('999.99'))
    
    def test_eliminar_producto(self):
        """Prueba el endpoint para eliminar un producto"""
        url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Producto.objects.count(), 0)
    
    def test_buscar_productos(self):
        """Prueba el endpoint de búsqueda de productos"""
        url = reverse('producto-buscar')
        response = self.client.get(url, {'q': 'Samsung'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('resultados', response.data)
        self.assertEqual(len(response.data['resultados']), 1)
        self.assertEqual(response.data['termino_busqueda'], 'Samsung')
    
    def test_buscar_sin_termino(self):
        """Prueba la búsqueda sin término de búsqueda"""
        url = reverse('producto-buscar')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_filtrar_por_categoria(self):
        """Prueba el filtrado por categoría"""
        url = reverse('producto-por-categoria', kwargs={'categoria': 'Electrónicos'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('productos', response.data)
        self.assertEqual(len(response.data['productos']), 1)
        self.assertEqual(response.data['categoria'], 'Electrónicos')
    
    def test_filtrar_por_marca(self):
        """Prueba el filtrado por marca"""
        url = reverse('producto-por-marca', kwargs={'marca': 'Samsung'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('productos', response.data)
        self.assertEqual(len(response.data['productos']), 1)
        self.assertEqual(response.data['marca'], 'Samsung')
    
    def test_productos_sin_stock(self):
        """Prueba el endpoint para productos sin stock"""
        # Crear un producto sin stock
        Producto.objects.create(
            nombre="Producto Agotado",
            categoria="Test",
            marca="Test",
            precio=Decimal('10.00'),
            cantidad=0
        )
        
        url = reverse('producto-sin-stock')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('productos_sin_stock', response.data)
        self.assertEqual(len(response.data['productos_sin_stock']), 1)
    
    def test_reducir_stock(self):
        """Prueba el endpoint para reducir stock"""
        url = reverse('producto-reducir-stock', kwargs={'pk': self.producto.pk})
        datos = {'cantidad': 5}
        response = self.client.post(url, datos, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('mensaje', response.data)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 10)  # 15 - 5 = 10
    
    def test_reducir_stock_insuficiente(self):
        """Prueba la reducción de stock cuando no hay suficiente"""
        url = reverse('producto-reducir-stock', kwargs={'pk': self.producto.pk})
        datos = {'cantidad': 20}  # Más de lo disponible (15)
        response = self.client.post(url, datos, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_validacion_precio_negativo(self):
        """Prueba la validación de precio negativo"""
        url = reverse('producto-list')
        datos_invalidos = {
            'nombre': 'Producto Test',
            'categoria': 'Test',
            'marca': 'Test',
            'precio': '-10.00',
            'cantidad': 5
        }
        response = self.client.post(url, datos_invalidos, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_validacion_cantidad_negativa(self):
        """Prueba la validación de cantidad negativa"""
        url = reverse('producto-list')
        datos_invalidos = {
            'nombre': 'Producto Test',
            'categoria': 'Test',
            'marca': 'Test',
            'precio': '10.00',
            'cantidad': -5
        }
        response = self.client.post(url, datos_invalidos, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_paginacion(self):
        """Prueba la paginación de productos"""
        # Crear más productos para probar paginación
        for i in range(25):
            Producto.objects.create(
                nombre=f'Producto {i}',
                categoria='Test',
                marca='Test',
                precio=Decimal('10.00'),
                cantidad=5
            )
        
        url = reverse('producto-list')
        response = self.client.get(url, {'page': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('paginacion', response.data)
        self.assertEqual(response.data['paginacion']['total_productos'], 26)  # 25 + 1 original
        self.assertEqual(response.data['paginacion']['pagina_actual'], 1)