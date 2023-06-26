# Create your models here.

from django.db import models
from applications.nomina.catalogos.ubicaciones.models import ubicaciones

# Modelos de nomina
class NomEmpresas(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    direccion = models.CharField(max_length=20, blank=True, null=True)
    colonia = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    cp = models.CharField(max_length=5, blank=True, null=True)
    activo = models.BooleanField(default=True)
    #ubicacion = models.ForeignKey(ubicaciones, on_delete=models.CASCADE, db_column="id_ubicacion")

    class Meta:
        db_table = 'nom_empresas'
        get_latest_by = 'codigo'
        ordering = ['id']

    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombre)


'''
class NomAuto(models.Model):
    id_auto = models.AutoField(primary_key=True)
    nom_auto = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'nom_auto'


class NomCatalogoFleteros(models.Model):
    id_catfle = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=5, blank=True, null=True)
    nombre_fletero = models.CharField(max_length=50, blank=True, null=True)
    camion = models.CharField(max_length=40, blank=True, null=True)
    costo = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    tipo_combustible = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    precio = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    codigo_fletero = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)

    class Meta:
        db_table = 'nom_catalogo_fleteros'


class NomSueldosNoIntegrados(models.Model):
    tiempos = models.DecimalField(max_digits=3, decimal_places=1)
    equivalen = models.CharField(max_length=10, blank=True, null=True)
    costo = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    costo_domingo = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'nom_sueldos_no_integrados'


class NomSueldosIntegrados(models.Model):
    tiempos = models.DecimalField(max_digits=3, decimal_places=1)
    equivalencia = models.CharField(max_length=10, blank=True, null=True)
    costo = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    costo_domingo = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    costo_real = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'nom_sueldos_integrados'

class NomCostosVarios(models.Model):
    monto = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True)
    monto_hora = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    prestamo = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True)

    class Meta:
        db_table = 'nom_costos_varios'


class NomEjercicio(models.Model):
    anio = models.CharField(max_length=4)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'nom_ejercicio'


class NomFormaPago(models.Model):
    codigo = models.CharField(max_length=2)
    nombre = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        db_table = 'nom_forma_pago'


class NomJornada(models.Model):
    semana = models.DecimalField(max_digits=2, decimal_places=0)
    empleado = models.CharField(max_length=8)
    empresa = models.CharField(max_length=5, blank=True, null=True)
    labor = models.CharField(max_length=3, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    horas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tiempos = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dinero = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    salario_integrado = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    total_nomina = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    sueldo = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    cierre = models.BooleanField(blank=True, null=True)
    usuario = models.CharField(max_length=10, blank=True, null=True)
    temporada = models.CharField(max_length=10, blank=True, null=True)
    anio = models.CharField(max_length=4, blank=True, null=True)
    num_horas_extras = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    monto_hrs_extras = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    ahorro = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    referencia = models.CharField(max_length=35, blank=True, null=True)
    puesto = models.CharField(max_length=35, blank=True, null=True)
    salario_diario = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'nom_jornada'

'''


