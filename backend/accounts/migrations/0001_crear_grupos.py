# Migración de datos: creación de los grupos/roles base del sistema SGAB.
# Los roles se implementan con los Grupos nativos de Django.

from django.db import migrations


def crear_grupos(apps, schema_editor):
    """
    Crea los grupos base del sistema si todavía no existen.

    Se usa get_or_create para que la migración sea segura e idempotente:
    si el grupo ya fue creado manualmente desde el admin, no se duplica.
    """
    Group = apps.get_model("auth", "Group")

    for nombre in ("Administrador", "Repartidor", "Cliente"):
        Group.objects.get_or_create(name=nombre)


class Migration(migrations.Migration):
    """
    Depende de las migraciones de autenticación para garantizar que el
    modelo Group ya exista antes de crear los roles.
    """

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        # La reversa no elimina grupos para no borrar asignaciones existentes.
        migrations.RunPython(crear_grupos, migrations.RunPython.noop),
    ]
