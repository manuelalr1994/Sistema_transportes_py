from django.db import models

# Create your models here.
class NomPuestos(models.Model):
    id = models.AutoField(primary_key=True)
    # Datos del Empleado -->
    codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'nom_puestos'
        get_latest_by = 'codigo'
        ordering = ['id']

    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombre)