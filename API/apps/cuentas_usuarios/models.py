"""
Gestión de usuarios
Modelos para la creación, login, cierre de sesión de los usuarios
"""
# pylint: disable=E0401
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UsuarioManager(BaseUserManager):
    """
    Clase encargada de sobrescribir los métodos
    para crear usuario y superusuario
    """

    def create_user(self, nick, nombres, apellidos, correo, password=None):
        """
        Sobreescritura al método para
        crear usuario

        :param nick: Nick del usuario
        :param nombres: Nombres del usuario
        :param apellidos: Apellidos del usuario
        :param correo: Correo electrónico del usuario
        :param password: Contraseña del usuario

        :return: Usuario creado
        """
        # pylint: disable=R0913
        if not correo:
            raise ValueError("Debes proporcionar un correo válido.")
        if not nick:
            raise ValueError("Debes proporcionar un nick válido.")
        user = self.model(
            correo=self.normalize_email(correo),
            nick=nick,
            nombres=nombres,
            apellidos=apellidos
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nick, nombres, apellidos, correo, password):
        """
        Sobreescritura al método para
        crear superusuario

        :param nick: Nick del superusuario
        :param nombres: Nombres del superusuario
        :param apellidos: Apellidos del superusuario
        :param correo: Correo electrónico del superusuario
        :param password: Contraseña del superusuario

        :return: Superusuario creado
        """
        # pylint: disable=R0913
        user = self.create_user(
            correo=self.normalize_email(correo),
            nick=nick,
            nombres=nombres,
            apellidos=apellidos,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save()
        return user


class DatosGenericos(models.Model):
    """
    Modelo abstracto para datos genéricos
    """
    fecha_creacion = models.DateField(verbose_name="Fecha de Creación", auto_now_add=True)
    fecha_actualizacion = models.DateField(verbose_name="Fecha de Actualización", auto_now=True)
    estado = models.BooleanField(verbose_name="Estado", default=True)

    # pylint: disable=R0903
    class Meta:
        """
        Hacemos que la clase sea abstracta para
        que no se creen los campos en la base
        de datos
        """
        abstract = True
    # pylint: disable=R0903
    def activar(self):
        """
        Activa la instancia cambiando el estado a True.
        """
        self.estado = True
        self.save()

    def desactivar(self):
        """
        Desactiva la instancia cambiando el estado a False.
        """
        self.estado = False
        self.save()


class Rol(DatosGenericos):
    """
    Modelo para representar roles de usuario
    """
    nombre = models.CharField(verbose_name="Nombre", max_length=50)

    # pylint: disable=R0903
    class Meta:
        """
        Clase metadatos para configurar los nombres
        de la clase en la base de datos y como se
        mostrara en el dash de django admin
        """
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "cuentas_usuario_rol"

    def __str__(self):
        return str(self.nombre)


class Pais(DatosGenericos):
    """
    Modelo para representar países
    """
    nombre = models.CharField(verbose_name="Nombre", max_length=150)

    # pylint: disable=R0903
    class Meta:
        """
        Clase metadatos para configurar los nombres
        de la clase en la base de datos y como se
        mostrara en el dash de django admin
        """
        verbose_name = "Pais"
        verbose_name_plural = "Paises"
        db_table = "cuentas_usuario_pais"

    def __str__(self):
        return str(self.nombre)


class Departamento(DatosGenericos):
    """
    Modelo para representar departamentos
    """
    nombre = models.CharField(verbose_name="Nombre", max_length=100)

    def __str__(self):
        return str(self.nombre)

    # pylint: disable=R0903
    class Meta:
        """
        Clase metadatos para configurar los nombres
        de la clase en la base de datos y como se
        mostrara en el dash de django admin
        """
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        db_table = "cuentas_usuario_departamento"


class Municipio(DatosGenericos):
    """
    Modelo para representar municipios
    """
    nombre = models.CharField(verbose_name="Nombre", max_length=100)
    departamento = models.ForeignKey(Departamento,
                                     verbose_name=("Departamento"),
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True)

    def __str__(self):
        return str(self.nombre)

    # pylint: disable=R0903
    class Meta:
        """
        Clase metadatos para configurar los nombres
        de la clase en la base de datos y como se
        mostrara en el dash de django admin
        """
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        db_table = "cuentas_usuario_municipio"


class TipoIdentificacion(DatosGenericos):
    """
    Modelo para representar tipos de identificación
    """
    nombre = models.CharField(max_length=50)

    # pylint: disable=R0903
    class Meta:
        """
        Clase metadatos para configurar los nombres
        de la clase en la base de datos y como se
        mostrara en el dash de django admin
        """
        verbose_name = "Tipo de Identificación"
        verbose_name_plural = "Tipos de Identificación"
        db_table = "cuentas_usuario_tipo_identificacion"

    # pylint: disable=R0903
    def __str__(self):
        return str(self.nombre)


class Usuario(AbstractBaseUser, DatosGenericos):
    """
    Modelo personalizado de usuario
    """
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    tipo_identificacion = models.ForeignKey(
        TipoIdentificacion,
        verbose_name="Tipo de identificación",
        on_delete=models.CASCADE,
        related_name="usuarios",
        null=True, blank=True)
    numero_identificacion = models.CharField(
        verbose_name="Numero de Identificación",
        max_length=100, unique=True, null=True, blank=True)
    nick = models.CharField(verbose_name="Nick", max_length=200)
    nombres = models.CharField(verbose_name="Nombre", max_length=100)
    apellidos = models.CharField(
        verbose_name="Apellido",
        max_length=100)
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de Nacimiento",
        null=True, blank=True)
    pais = models.ForeignKey(
        Pais, verbose_name="Pais",
        on_delete=models.CASCADE,
        related_name="usuarios",
        null=True, blank=True)
    departamento = models.ForeignKey(
        Departamento, verbose_name="Departamento",
        on_delete=models.CASCADE, related_name="usuarios",
        null=True, blank=True)
    municipio = models.ForeignKey(
        Municipio, verbose_name="Municipio",
        on_delete=models.CASCADE,
        related_name="usuarios",
        null=True,
        blank=True)
    rol = models.ForeignKey(
        Rol,
        verbose_name="Rol",
        on_delete=models.CASCADE,
        related_name="usuarios",
        null=True,
        blank=True)
    correo = models.EmailField(
        verbose_name="Correo",
        unique=True, null=False)
    genero = models.CharField(
        max_length=1,
        choices=GENERO_CHOICES,
        null=True,
        blank=True)
    foto = models.ImageField(
        upload_to='media/perfil/usuarios/',
        blank=True,
        null=True)

    is_admin = models.BooleanField(
        verbose_name="Admin",
        default=False)
    is_staff = models.BooleanField(
        verbose_name="Acceso al Dash",
        default=False)
    is_active = models.BooleanField(
        verbose_name="Habilitado",
        default=True)
    is_superadmin = models.BooleanField(
        verbose_name="SuperAdmin",
        default=False)

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nick", "nombres", "apellidos"]

    objects = UsuarioManager()

    # pylint: disable=R0903
    class Meta:
        """
        Clase metadatos para configurar los nombres
        de la clase en la base de datos y como se
        mostrara en el dash de django admin
        """
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "cuentas_usuario_usuario"
    def __str__(self):
        return str(self.correo)

    def full_name(self):
        """
        funcion para poner el nombr completo
        """
        return f"{self.nombres} {self.apellidos}"

    def has_perm(self):
        """
        proporcionar una verificación personalizada de permisosen el modelo de usuario personalizado 
        """
        return self.is_admin

    def has_module_perms(self):
        """
         Este método se utiliza para determinar si el usuario
         tiene permisos para acceder a un módulo específico
         dentro de la aplicación.
        """
        return True

    def cambiar_contrasena(self, nueva_contrasena):
        """
        Cambia la contraseña del usuario.

        :param nueva_contrasena: Nueva contraseña a establecer
        """
        self.set_password(nueva_contrasena)
        self.save()

    def desactivar_cuenta(self):
        """
        Desactiva la cuenta del usuario.
        """
        self.is_active = False
        self.save()

    def activar_cuenta(self):
        """
        Activa la cuenta del usuario.
        """
        self.is_active = True
        self.save()
