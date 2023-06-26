from django.db import models
from applications.nomina.catalogos.campos_agricolas.models import NomCampos

# Create your models here.
class NomCuadrilleros(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=8, default=0)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    campo_agricola = models.ForeignKey(NomCampos, on_delete=models.CASCADE, db_column="id_campo_agricola")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'nom_cuadrilleros'
        ordering = ['codigo']
        get_latest_by = 'codigo'

    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombre)
