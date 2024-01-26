# GESTION PERSONAL | GPDARO

  Gestión de usuarios, cuentas, cuenta con administración de finanzas de ingresos, egresos, deudas, ahorros, lista de actividades y  estados de actividades según correspondan.
  
  Desarrollo proyectado a plataforma Web, desktop y móviles. **"En proceso"**

**Procesos:**
- API:          20%
- Web:        0%
- Desktop:  0%
- Móvil       0%

**Terminados:**
- 

## Tecnologías

MySQL
Django Rest Framework (Python)
Angular (TypeScript)
  

### Django Rest Framework


#### APPS

- cuentas_usuarios
- finanzas
- actividades
 

#### Testing

##### **Pylint**
Estilo y la calidad del código en el lenguaje de programación Python

**APPS**


- **'cuentas_usuarios'**
Se utilizo `# pylint: disable=R0903` para omitir la creación de métodos públicos innecesarios, `# pylint: disable=R0913` para omitir un argumento extra que se puso en la clase que hereda de `BaseUserManager` para personalizar los campos, `# pylint: disable=E0401` se omitio debido a que hay dos importaciones internas de Django que no las detecta validas.

1. Report Models
------------------------------------------------------------
116 statements analysed.
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

------------------------------------------------------------

  