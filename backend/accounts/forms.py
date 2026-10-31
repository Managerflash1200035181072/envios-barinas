from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User


class RegistroForm(UserCreationForm):
    """Formulario de registro que asigna el rol Cliente al crear la cuenta."""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambiar labels a español
        self.fields["username"].label = "Nombre de usuario"
        self.fields["first_name"].label = "Nombres"
        self.fields["last_name"].label = "Apellidos"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"

        # Los datos personales son obligatorios para identificar al cliente
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

        # Colocar textos de ayuda en español (debajo de cada campo)
        self.fields["username"].help_text = "Requerido. Máximo 150 caracteres. Letras, números y @/./+/-/_ solamente."
        self.fields["password1"].help_text = "Tu contraseña debe tener al menos 8 caracteres y no puede ser completamente numérica."
        self.fields["password2"].help_text = "Introduce la misma contraseña para verificarla."

        # Asegurar el orden deseado
        self.field_order = ["username", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        """
        Guarda el usuario y le asigna el rol Cliente por defecto.

        El rol se representa mediante el grupo "Cliente". Se usa
        get_or_create para que el registro no falle si el grupo aún no
        existe en una base de datos recién inicializada.
        """
        user = super().save(commit=commit)

        if commit:
            grupo_cliente, _ = Group.objects.get_or_create(name="Cliente")
            user.groups.add(grupo_cliente)

        return user
