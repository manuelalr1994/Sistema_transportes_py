from django.db import models

# Create your models here.
class NomLabores(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=8, default=0)
    nombre = models.CharField(max_length=40, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'nom_labores'
        get_latest_by = 'codigo'

    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombre)