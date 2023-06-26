from django.db import models

# Create your models here.
class ubicaciones(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=8, default=0)
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'ubicaciones'
        ordering = ['id']
        get_latest_by = 'id'

    def __str__(self):
        return str(self.id) + " | " + self.nombre