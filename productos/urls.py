from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

# Crear router para las URLs del ViewSet
router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

# URLs de la app productos
urlpatterns = [
    path('api/', include(router.urls)),
]
