# Generated by Django 4.0 on 2022-09-28 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fle_camiones', '0001_initial'),
        ('nom_campos', '0001_initial'),
        ('semanas', '0001_initial'),
        ('nom_cuadrilleros', '0001_initial'),
        ('nom_labores', '0001_initial'),
        ('nom_cultivos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleJornada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_entrada', models.DecimalField(decimal_places=2, max_digits=4)),
                ('hora_salida', models.DecimalField(decimal_places=2, max_digits=4)),
                ('costo_hra', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total_hrs', models.DecimalField(decimal_places=2, max_digits=4)),
                ('importe', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cerrada', models.BooleanField(default=False)),
                ('camion', models.ForeignKey(db_column='id_camion', on_delete=django.db.models.deletion.CASCADE, to='fle_camiones.camiones')),
                ('campo_agricola', models.ForeignKey(db_column='id_campo_agricola', on_delete=django.db.models.deletion.CASCADE, to='nom_campos.nomcampos')),
                ('cuadrillero', models.ForeignKey(db_column='id_cuadrillero', on_delete=django.db.models.deletion.CASCADE, to='nom_cuadrilleros.nomcuadrilleros')),
                ('cultivo', models.ForeignKey(db_column='id_cultivo', on_delete=django.db.models.deletion.CASCADE, to='nom_cultivos.cultivos')),
                ('labor', models.ForeignKey(db_column='id_labor', on_delete=django.db.models.deletion.CASCADE, to='nom_labores.nomlabores')),
                ('semana', models.ForeignKey(db_column='id_semana', on_delete=django.db.models.deletion.CASCADE, to='semanas.nomsemanas')),
                ('tipo_semana', models.ForeignKey(db_column='id_tipo_semana', on_delete=django.db.models.deletion.CASCADE, to='semanas.nomtiposemanas')),
                ('variedad', models.ForeignKey(db_column='id_variedad', on_delete=django.db.models.deletion.CASCADE, to='nom_cultivos.variedad')),
            ],
            options={
                'db_table': 'fle_jornada',
            },
        ),
    ]
