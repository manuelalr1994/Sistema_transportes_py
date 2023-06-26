from statistics import mean
from django.db import models
from applications.facturacion.procesos.procesar_maquila.models import FletesMaquilas
from applications.nomina.catalogos.campos_agricolas.models import NomCampos

# Create your models here.
class FletesRemisiones(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length = 10, unique=True)
    campo_agricola = models.ForeignKey(NomCampos, on_delete=models.CASCADE, db_column='id_campo_agricola')
    fecha = models.DateField()
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    facturada = models.BooleanField(default=False)
    maquilas_afectadas = models.ManyToManyField(FletesMaquilas, through='FletesAbonos')

    class Meta:
        db_table = 'fle_remisiones'
        ordering = ['id']
        get_latest_by = 'id'


class FletesAbonos(models.Model):
    id = models.AutoField(primary_key=True)
    campo_agricola = models.ForeignKey(NomCampos, on_delete=models.CASCADE, db_column='id_campo_agricola')
    remision = models.ForeignKey(FletesRemisiones, on_delete=models.CASCADE, db_column='id_remision')
    maquila = models.ForeignKey(FletesMaquilas, on_delete=models.CASCADE, db_column='id_maquila')
    saldo = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=1)  # t = total_pagado   a = abono