from django.db import models
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.semanas.models import NomSemanas, NomTipoSemanas


# Create your models here.
class FletesMaquilas(models.Model):
    id = models.AutoField(primary_key=True)
    campo_agricola = models.ForeignKey(NomCampos, on_delete=models.CASCADE, db_column='id_campo_agricola')
    semana = models.ForeignKey(NomSemanas, on_delete=models.CASCADE, db_column='id_semana')
    tipo_semana = models.ForeignKey(NomTipoSemanas, on_delete=models.CASCADE, db_column='id_tipo_semana')
    cant_carros = models.IntegerField()
    hrs_fletes = models.DecimalField(max_digits=9, decimal_places=2)
    costo_maquila = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    importe_maquila = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    procesada = models.BooleanField(default=False)

    class Meta:
        db_table = 'fle_maquilas'
        ordering = ['id']
        get_latest_by = 'id'

    def __str__(self):
        return str(self.id) + " | " + self.campo_agricola.nombre