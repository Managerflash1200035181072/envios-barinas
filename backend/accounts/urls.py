# Importaciones de Django para enrutamiento
from django.urls import path

from . import views

urlpatterns = [
    # Página principal pública (Visitante y usuarios autenticados)
    path("", views.home, name="home"),
    # Página de registro para nuevos usuarios
    path("registro/", views.registro, name="registro"),
    # Inicio de sesión
    path("login/", views.login_view, name="login"),
    # Cierre de sesión (solo POST)
    path("logout/", views.logout_view, name="logout"),
    # Panel exclusivo del rol Cliente
    path("cliente/", views.panel_cliente, name="panel_cliente"),
    # Panel exclusivo del rol Repartidor
    path("repartidor/", views.panel_repartidor, name="panel_repartidor"),
    # Panel exclusivo del rol Administrador
    path("admin-panel/", views.panel_admin, name="panel_admin"),
]
