from django.db import models

# Create your models here.
from django.db import models
from applications.fletes.catalogos.camiones.models import Camiones
from applications.fletes.catalogos.compania_fletera.models import CompaniasFleteras
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.cuadrilleros.models import NomCuadrilleros
from applications.nomina.catalogos.cultivos.models import Cultivos, Variedad
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.labores.models import NomLabores
from applications.nomina.catalogos.semanas.models import NomSemanas, NomTipoSemanas
from applications.nomina.catalogos.labores.models import NomLabores
from applications.nomina.catalogos.empleados.models import NomEmpleado


# Create your models here.
class NomJornales(models.Model):

    campo_agricola = models.ForeignKey(NomCampos, on_delete=models.CASCADE, db_column='id_campo_agricola')
    tipo_semana = models.ForeignKey(NomTipoSemanas, on_delete=models.CASCADE, db_column='id_tipo_semana')
    semana = models.ForeignKey(NomSemanas, on_delete=models.CASCADE, db_column='id_semana')
    cuadrillero = models.ForeignKey(NomCuadrilleros, on_delete=models.CASCADE, db_column='id_cuadrillero')
    temporada = models.CharField(max_length=2, blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField()
    labor = models.ForeignKey(NomLabores, on_delete=models.CASCADE, db_column='id_labor')
    empleado = models.ForeignKey(NomEmpleado, on_delete=models.CASCADE, db_column='id_empleado')
    total_dinero = models.DecimalField(decimal_places=2, max_digits = 12)
    total_hrs_extra = models.DecimalField(decimal_places=2, max_digits = 8)
    total_dinero_hrs_extra = models.DecimalField(decimal_places=2, max_digits = 8)
    cerrada = models.BooleanField(default=False)

    class Meta:
        db_table = 'nom_jornales'