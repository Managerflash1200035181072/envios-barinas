# Importaciones de Django para enrutamiento
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Panel de Admin Django
    path('', include('accounts.urls')), # Incluir todas las rutas de la app accounts
]
