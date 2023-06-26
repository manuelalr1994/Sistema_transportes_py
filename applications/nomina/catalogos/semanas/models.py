from django.db import models

# Create your models here.
class NomTipoSemanas(models.Model):
    tipo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'nom_tipo_semanas'
        ordering = ['tipo']
        get_latest_by = 'tipo'

    def __str__(self):
        return str(self.tipo) + ' | ' + self.nombre

class NomSemanas(models.Model):
    id = models.AutoField(primary_key=True)
    semana = models.DecimalField(max_digits=2, decimal_places=0)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    anio = models.CharField(max_length=4, blank=True, null=True)
    generado = models.BooleanField(default=False)
    tipo_semana = models.ForeignKey(NomTipoSemanas, default=0, on_delete=models.CASCADE, db_column='id_tipo_semana' ,)

    class Meta:
        db_table = 'nom_semanas'
        ordering = ['id']
        get_latest_by = 'id'
        constraints = [
            models.UniqueConstraint(fields=['anio','tipo_semana', 'semana'], name='unico anio tipo semana')
        ]

    def __str__(self):
        return str(self.semana) + ' | ' + str(self.fecha_inicial.strftime("%d/%m/%Y")) + '   a   ' + str(self.fecha_final.strftime("%d/%m/%Y"))