from django.db import models
from applications.fletes.catalogos.compania_fletera.models import CompaniasFleteras

# Create your models here.
class Camiones(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=8, unique=True, error_messages={'unique':'Ya existe un camion con este codigo'})
    nombre = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    compania_fletera = models.ForeignKey(CompaniasFleteras, on_delete=models.CASCADE, db_column='id_compania_fletera')
    costo_hra = models.DecimalField(max_digits=6, decimal_places=2)
    activo = models.BooleanField(default=True)
    
    class Meta:
        get_latest_by = 'codigo'
        db_table = 'camiones'

    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombre)
        