"""
Gestion de usuarios
Modelos para la creacion, login, cierre de session de los usuarios
"""
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class UsuarioManager(BaseUserManager):

    def create_user(self,nick,nombres,apellidos,correo,password=None):
        if not correo:
            raise ValueError("Debes proporcionar un correo valido.")
        if not nick:
            raise ValueError("Debes proporcionar un nick valido.")
        user=self.model(
            correo=self.normalize_email(correo),
            nick=nick,
            nombres=nombres,
            apellidos=apellidos
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,nick,nombres,apellidos,correo,password):
        user=self.create_user(
            correo=self.normalize_email(correo),
            nick=nick,
            nombres=nombres,
            apellidos=apellidos,
            password=password   
        )

        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superadmin=True

        user.save()
        return user


class DatosGenericos(models.Model):
    fecha_creacion=models.DateField(verbose_name="Fecha de Creacion", auto_now_add=True)
    fecha_actualizacion=models.DateField(verbose_name="Fecha de Actualizacion", auto_now=True)
    estado=models.BooleanField(verbose_name="Estado", default=True)

    class Meta:
        abstract = True


class Rol(DatosGenericos):
    nombre=models.CharField(verbose_name="Nombre", max_length=50)
    
    class Meta:
        verbose_name="Rol"
        verbose_name_plural="Roles"
        db_table="cuentas_usuario_rol"

    def __str__(self):
        return self.nombre
    

class Pais(DatosGenericos):
    nombre=models.CharField(verbose_name="Nombre", max_length=150)

    class Meta:
        verbose_name="Pais"
        verbose_name_plural="Paises"
        db_table="cuentas_usuario_pais"
    
    def __str__(self):
        return self.nombre
    

class Departamento(DatosGenericos):
    nombre=models.CharField(verbose_name="Nombre", max_length=100)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name="Departamento"
        verbose_name_plural="Departamentos"
        db_table="cuentas_usuario_departamento"

        
class Municipio(DatosGenericos):
    nombre=models.CharField(verbose_name="Nombre", max_length=100)
    departamento=models.ForeignKey(Departamento, verbose_name=("Departamento"), on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name="Municipio"
        verbose_name_plural="Municipios"
        db_table="cuentas_usuario_municipio"



class TipoIdentificacion(DatosGenericos):
    nombre=models.CharField(max_length=50)

    class Meta:
        verbose_name="Tipo de Identificacion"
        verbose_name_plural="Tipos de Identificacion"
        db_table = "cuentas_usuario_tipo_identificacion"

    def __str__(self):
        return self.nombre


class Usuario(AbstractBaseUser,DatosGenericos):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    tipo_identificacion=models.ForeignKey(TipoIdentificacion, verbose_name="Tipo de identificacion", on_delete=models.CASCADE,related_name="usuarios",null=True,blank=True)
    numero_identificacion=models.CharField(verbose_name="Numero de Identificacion", max_length=100,unique=True,null=True,blank=True)
    nick=models.CharField(verbose_name="Nick",max_length=200)
    nombres=models.CharField(verbose_name="Nombre",max_length=100)
    apellidos=models.CharField(verbose_name="Apellido",max_length=100)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    pais=models.ForeignKey(Pais,verbose_name="Pais", on_delete=models.CASCADE,related_name="usuarios",null=True,blank=True)
    departamento=models.ForeignKey(Departamento,verbose_name="Departamento", on_delete=models.CASCADE,related_name="usuarios",null=True,blank=True)
    municipio=models.ForeignKey(Municipio,verbose_name="Municipio", on_delete=models.CASCADE,related_name="usuarios",null=True,blank=True)
    rol=models.ForeignKey(Rol,verbose_name="Rol", on_delete=models.CASCADE,related_name="usuarios",null=True,blank=True)
    correo=models.EmailField(verbose_name="Correo",unique=True,null=False)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES,null=True,blank=True)
    foto=models.ImageField(upload_to='media/perfil/usuarios/', blank=True, null=True)

    is_admin=models.BooleanField(verbose_name="Admin" ,default=False)
    is_staff=models.BooleanField(verbose_name="Acceso al Dash" , default=False)
    is_active=models.BooleanField(verbose_name="Habilitado" ,default=True)
    is_superadmin=models.BooleanField(verbose_name="SuperAdmin" ,default=False)

    USERNAME_FIELD="correo"
    REQUIRED_FIELDS=["nick","nombres","apellidos"]

    objects=UsuarioManager()
    
    class Meta:
        verbose_name="Usuario"
        verbose_name_plural="Usuarios"
        db_table="cuentas_usuario_usuario"

    def __str__(self) :
        return self.correo
    
    def full_name(self):
        return f"{self.nombres} {self.apellidos}"
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True




