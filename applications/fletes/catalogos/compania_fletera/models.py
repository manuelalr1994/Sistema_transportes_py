from django.db import models

# Create your models here.
class CompaniasFleteras(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, unique=True, error_messages={'unique':'Ya existe una compañia fletera con este codigo'})
    cuenta = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, null=True, blank=True)
    ciudad = models.CharField(max_length=30, null=True, blank=True)
    codigo_postal = models.CharField(max_length=5, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    tarjeta = models.CharField(max_length=16, null=True, blank=True)
    rfc = models.CharField(max_length=50, null=True, blank=True)
    colonia = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    activo = models.BooleanField(default=True)
    #ubicacion = models.ForeignKey(ubicaciones, on_delete=models.CASCADE, db_column='id_ubicacion', default='1')

    class Meta:
        get_latest_by = 'codigo'
        db_table = 'companias_fleteras'

    def __str__(self):
        return self.nombre