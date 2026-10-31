import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def versioned_static(path):
    """Devuelve la URL del estático con una versión basada en su fecha de modificación."""
    # Se parte de la URL estática normal generada por Django.
    url = static(path)
    # finders localiza el archivo real para poder leer su fecha de modificación.
    absolute_path = finders.find(path)

    if not absolute_path:
        # Si el archivo no se encuentra, se devuelve la URL sin versión.
        return url

    # El mtime cambia al editar el archivo y fuerza al navegador a recargarlo.
    return f"{url}?v={int(os.path.getmtime(absolute_path))}"
