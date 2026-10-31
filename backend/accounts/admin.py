# Configuración del Django Admin para la gestión de usuarios y roles.
# Los roles se administran mediante los Grupos nativos de Django.

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User


# Textos visibles en la cabecera del panel administrativo.
admin.site.site_header = "SGAB - Administración"
admin.site.site_title = "SGAB"
admin.site.index_title = "Panel de administración"


class UsuarioAdmin(UserAdmin):
    """
    Administración de usuarios.

    Se extiende el UserAdmin de Django para mostrar los roles (grupos)
    directamente en el listado y permitir filtrar usuarios por rol.
    """

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "get_grupos",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    @admin.display(description="Roles")
    def get_grupos(self, obj):
        """Devuelve los nombres de los grupos del usuario separados por coma."""
        return ", ".join(grupo.name for grupo in obj.groups.all()) or "Sin rol"


class GrupoAdmin(GroupAdmin):
    """
    Administración de roles.

    Muestra cuántos usuarios tiene asignado cada grupo para facilitar
    la revisión de los roles del sistema.
    """

    list_display = ("name", "cantidad_usuarios")

    @admin.display(description="Usuarios")
    def cantidad_usuarios(self, obj):
        """Cuenta los usuarios que pertenecen al grupo."""
        return obj.user_set.count()


# Reemplazar los registros por defecto por las versiones personalizadas.
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GrupoAdmin)
