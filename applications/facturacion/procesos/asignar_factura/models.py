from django.db import models

from applications.facturacion.procesos.elaborar_remision.models import FletesRemisiones
from datetime import date

# Create your models here.
class FletesFacturas(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    remisiones = models.ManyToManyField(FletesRemisiones, through='FletesFacturasRemisiones')
    fecha = models.DateField(default=date.today())

    class Meta:
        db_table = 'fle_facturas'
        ordering = ['id']
        get_latest_by = 'id'


class FletesFacturasRemisiones(models.Model):
    id = models.AutoField(primary_key=True)
    remision = models.ForeignKey(FletesRemisiones, on_delete=models.CASCADE, db_column='id_remision')
    factura = models.ForeignKey(FletesFacturas, on_delete=models.CASCADE, db_column='id_factura')

    class Meta:
        db_table = 'fle_facturas_remision'
        ordering = ['id']
        get_latest_by = 'id'
    