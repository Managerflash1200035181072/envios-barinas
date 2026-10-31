# Importaciones estándar y de Django
from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import RegistroForm


# Vista de Registro
def registro(request):
    """
    Muestra un formulario de registro de Django. Si el formulario es válido,
    crea el usuario, lo autentica y lo redirige al home.

    Si el usuario ya tiene una sesión activa, se le redirige al home para
    evitar que vuelva a registrarse estando autenticado.
    """
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # Instanciar formulario con los datos enviados
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardar usuario en la base de datos y asignarle el rol Cliente
            user = form.save()

            # Iniciar sesión automáticamente
            login(request, user)
            return redirect("home")
    else:
        # Para petición GET: mostrar formulario vacío
        form = RegistroForm()

    return render(request, "accounts/registro.html", {"form": form})


# Vista de Inicio de Sesión
def login_view(request):
    """
    Procesa el formulario de login. Si las credenciales son válidas,
    autentica al usuario y lo redirige al home.

    Si el usuario ya está autenticado, se le redirige al home.
    """
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # Extraer credenciales del formulario
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Autenticar con el sistema de auth de Django
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {"error": "Usuario o contraseña incorrectos."},
        )

    # Si es GET, mostrar el formulario
    return render(request, "accounts/login.html")


# Vista de cierre de sesión
@require_POST
def logout_view(request):
    """
    Cierra la sesión del usuario y redirige al home público.

    Se exige POST para evitar que el cierre de sesión se ejecute desde
    un enlace GET y para aprovechar la protección CSRF de Django.
    """
    logout(request)
    return redirect("home")


# Vista de home público (Visitante y usuarios autenticados)
def home(request):
    """
    Página principal del sistema.

    Es pública: el Visitante ve una presentación con acceso a login y
    registro, mientras que el usuario autenticado ve su panel de inicio.
    La plantilla decide qué contenido mostrar con user.is_authenticated.
    """
    return render(request, "accounts/home.html")


# Funciones auxiliares para verificar roles del usuario (Grupos de Django)
def es_cliente(user):
    """Retorna True si el usuario pertenece al grupo 'Cliente'."""
    return user.groups.filter(name="Cliente").exists()


def es_repartidor(user):
    """Retorna True si el usuario pertenece al grupo 'Repartidor'."""
    return user.groups.filter(name="Repartidor").exists()


def es_administrador(user):
    """
    Retorna True si el usuario es superusuario o pertenece al grupo
    'Administrador'. Así el superusuario también puede usar el panel
    personalizado, además del Django Admin nativo.
    """
    return user.is_superuser or user.groups.filter(name="Administrador").exists()


def requiere_rol(verificar_rol):
    """
    Decorador que exige que el usuario cumpla con el rol indicado.

    Debe usarse junto a @login_required. Si el usuario está autenticado
    pero no tiene el rol requerido, se responde con un error 403.
    """

    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not verificar_rol(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorador


# Vista exclusiva para el rol Cliente
@login_required
@requiere_rol(es_cliente)
def panel_cliente(request):
    """
    Panel del cliente. Solo accesible para usuarios del grupo 'Cliente'.

    Aquí se integrarán luego la creación y consulta de envíos del cliente.
    """
    return render(request, "accounts/cliente.html")


# Vista exclusiva para el rol Repartidor
@login_required
@requiere_rol(es_repartidor)
def panel_repartidor(request):
    """
    Panel de repartidor. Solo accesible para usuarios del grupo 'Repartidor'.

    Si el usuario no pertenece al grupo, Django responde con un error 403.
    Aquí se integrarán luego los envíos asignados.
    """
    return render(request, "accounts/repartidor.html")


# Vista exclusiva para el rol Administrador
@login_required
@requiere_rol(es_administrador)
def panel_admin(request):
    """
    Panel de administración personalizado. Solo para el grupo 'Administrador'.

    El superusuario también puede acceder al Django Admin por defecto en /admin/.
    """
    return render(request, "accounts/admin.html")
