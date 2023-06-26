from django.db import models
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.cuadrilleros.models import NomCuadrilleros

# Create your models here.
class NomEmpleado(models.Model):
    id = models.AutoField(primary_key=True)
    # Datos del Empleado -->
    codigo = models.CharField(max_length=8)
    fecha_alta = models.DateField(blank=True, null=True)
    tipo_contrato = models.CharField(max_length=10, blank=True, null=True)
    num_tarjeta = models.CharField(max_length=16, blank=True, null=True)
    cuenta_banco = models.CharField(max_length=16, blank=True, null=True)
    paterno = models.CharField(max_length=20, blank=True, null=True)
    materno = models.CharField(max_length=20, blank=True, null=True)
    nombres = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tipo_periodo = models.CharField(max_length=15, blank=True, null=True)
    salario_base = models.CharField(max_length=15, blank=True, null=True)
    base_cotizacion = models.CharField(max_length=1, blank=True, null=True)
    puesto = models.CharField(max_length=30, blank=True, null=True)
    integrado = models.BooleanField(blank=True, null=True)
    comida = models.CharField(max_length=1, blank=True, null=True)
    campo_agricola = models.ForeignKey(NomCampos, on_delete=models.CASCADE, db_column='id_campo_agricola')
    estatus = models.CharField(max_length=1, blank=True, null=True)
    cuadrillero = models.ForeignKey(NomCuadrilleros, on_delete=models.CASCADE, db_column='id_cuadrillero')
    # Información General -->
    num_seguro_social = models.CharField(max_length=16, blank=True, null=True)
    num_infonavit = models.CharField(max_length=16, blank=True, null=True)
    rfc_trabajador = models.CharField(max_length=13, blank=True, null=True)
    curp = models.CharField(max_length=40, blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True, null=True)
    edo_civil = models.CharField(max_length=15, blank=True, null=True)
    nombre_madre = models.CharField(max_length=50, blank=True, null=True)
    nombre_padre = models.CharField(max_length=50, blank=True, null=True)
    domicilio = models.CharField(max_length=50, blank=True, null=True)
    codigo_postal = models.BooleanField(max_length=8, blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=30, blank=True, null=True)
    familiar_referencia_1 = models.CharField(max_length=30, blank=True, null=True)
    telefono_referencia_1 = models.CharField(max_length=20, blank=True, null=True)
    familiar_referencia_2 = models.CharField(max_length=30, blank=True, null=True)
    telefono_referencia_2 = models.CharField(max_length=20, blank=True, null=True)
    
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'nom_empleado'
    
    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombres) + " " + str(self.paterno) + " " + str(self.materno)