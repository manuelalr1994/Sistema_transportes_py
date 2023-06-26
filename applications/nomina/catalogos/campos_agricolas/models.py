from unicodedata import decimal
from django.db import models
#from ..ubicaciones.models import ubicaciones
from applications.nomina.catalogos.semanas.models import NomTipoSemanas

# Create your models here.
class NomCampos(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=8, default=0)
    costo_hra_extra = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)
    descuento_sindical = models.BooleanField()
    tipos_semana = models.ManyToManyField(NomTipoSemanas)
    activo = models.BooleanField(default=True)
    #ubicacion = models.ForeignKey(ubicaciones, on_delete=models.CASCADE, db_column='id_ubicacion')

    class Meta:
        db_table = 'nom_campos'
        get_latest_by = 'codigo'

    def __str__(self):
        return str(self.codigo) + " | " + self.nombre