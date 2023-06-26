from django.db import models
from applications.fletes.catalogos.camiones.models import Camiones
from applications.fletes.catalogos.compania_fletera.models import CompaniasFleteras
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.cuadrilleros.models import NomCuadrilleros
from applications.nomina.catalogos.cultivos.models import Cultivos, Variedad
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.labores.models import NomLabores
from applications.nomina.catalogos.semanas.models import NomSemanas, NomTipoSemanas


# Create your models here.
class FleJornada(models.Model):

    campo_agricola = models.ForeignKey(NomCampos, on_delete=models.CASCADE, db_column='id_campo_agricola')
    tipo_semana = models.ForeignKey(NomTipoSemanas, on_delete=models.CASCADE, db_column='id_tipo_semana')
    semana = models.ForeignKey(NomSemanas, on_delete=models.CASCADE, db_column='id_semana')
    cuadrillero = models.ForeignKey(NomCuadrilleros, on_delete=models.CASCADE, db_column='id_cuadrillero')
    cultivo = models.ForeignKey(Cultivos, on_delete=models.CASCADE, db_column='id_cultivo')
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, db_column='id_variedad')
    labor = models.ForeignKey(NomLabores, on_delete=models.CASCADE, db_column='id_labor')
    camion = models.ForeignKey(Camiones, on_delete=models.CASCADE, db_column='id_camion')
    fecha = models.DateField()
    hora_entrada = models.DecimalField(decimal_places=2, max_digits = 4)
    hora_salida = models.DecimalField(decimal_places=2, max_digits = 4)
    costo_hra = models.DecimalField(decimal_places=2, max_digits = 8)
    total_hrs = models.DecimalField(decimal_places=2, max_digits = 4)
    importe = models.DecimalField(decimal_places=2, max_digits = 12)
    cerrada = models.BooleanField(default=False)

    class Meta:
        db_table = 'fle_jornada'