from django.db import models

# En este caso, a cada campo se le va a especificar su cabla (codigo_cultivo), ya que si tienen los
# mismos nombres, se pisan en el POST request (se hacen lista y los forms usan el primer elemento solo)
class Cultivos(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, null=False)
    nombre = models.CharField(max_length=25, blank=True, null=False)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cultivos'

    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombre)


class Variedad(models.Model):
    id = models.AutoField(primary_key=True)
    id_cultivo = models.ForeignKey(Cultivos, on_delete=models.CASCADE, db_column='id_cultivo')
    codigo = models.CharField(max_length=3, null=False)
    nombre = models.CharField(max_length=25, blank=True, null=False)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'variedad'
        constraints = [
            models.UniqueConstraint(fields=['codigo', 'id_cultivo'], 
            name='Combinacion codigo-cultivo debe ser unica')
        ]

    def __str__(self):
        return str(self.codigo) + " | " + str(self.nombre)


'''
# Create your models here.
class NomCultivos(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=25, blank=True, null=True)
    codigo_variedad = models.CharField(max_length=3, blank=True, null=True)
    nombre_variedad = models.CharField(max_length=25, blank=True, null=True)
    codigo_seccion = models.CharField(max_length=3, blank=True, null=True)
    nombre_seccion = models.CharField(max_length=25, blank=True, null=True)
    codigo_cuadro = models.CharField(max_length=3, blank=True, null=True)
    nombre_cuadro = models.CharField(max_length=25, blank=True, null=True)
    hectareas = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    plantas = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    lineas = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    desahilitar = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)

    class Meta:
        db_table = 'nom_cultivos'

'''