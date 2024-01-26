from django.contrib import admin
from .models import Usuario,Rol,Pais,Departamento,Municipio,TipoIdentificacion

from .forms import CustomPasswordChangeForm



class UsuarioAdmin(admin.ModelAdmin):


    fieldsets=[
        ('Datos Personales',{'fields':['genero','tipo_identificacion','numero_identificacion','nombres','apellidos','fecha_nacimiento']}),
        ('Ubicacion',{'fields':['pais','departamento','municipio']}),
        ('Registro',{'fields':['nick','correo','password','rol']}),
        ('perfil',{'fields':['foto']})
    ]
    list_display=("tipo_identificacion","numero_identificacion","nick","nombres","apellidos","correo","rol","estado","is_staff","is_admin")
    list_filter=("tipo_identificacion","estado","is_admin","is_staff","is_active","is_superadmin")
    search_fields=("numero_identificacion","correo")
    ordering=("tipo_identificacion","nombres","apellidos","correo","rol")

    

admin.site.register(Usuario,UsuarioAdmin)

class RolAdmin(admin.ModelAdmin):
    list_display=("nombre","estado")
    ordering=("nombre",)

admin.site.register(Rol,RolAdmin)

class PaisAdmin(admin.ModelAdmin):
    list_display=("nombre","estado")
    ordering=("nombre",)

admin.site.register(Pais,PaisAdmin)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display=("nombre","estado")
    ordering=("nombre",)

admin.site.register(Departamento,DepartamentoAdmin)

class MunicipioAdmin(admin.ModelAdmin):
    list_display=("nombre","estado")
    ordering=("nombre",)

admin.site.register(Municipio,MunicipioAdmin)

class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display=("nombre","estado")
    ordering=("nombre",)

admin.site.register(TipoIdentificacion,TipoIdentificacionAdmin)