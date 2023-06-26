# Generated by Django 4.0 on 2022-09-28 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nom_campos', '0001_initial'),
        ('nom_cuadrilleros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NomEmpleado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=8)),
                ('fecha_alta', models.DateField(blank=True, null=True)),
                ('tipo_contrato', models.CharField(blank=True, max_length=10, null=True)),
                ('num_tarjeta', models.CharField(blank=True, max_length=16, null=True)),
                ('cuenta_banco', models.CharField(blank=True, max_length=16, null=True)),
                ('paterno', models.CharField(blank=True, max_length=20, null=True)),
                ('materno', models.CharField(blank=True, max_length=20, null=True)),
                ('nombres', models.CharField(blank=True, max_length=20, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('tipo_periodo', models.CharField(blank=True, max_length=15, null=True)),
                ('salario_base', models.CharField(blank=True, max_length=15, null=True)),
                ('base_cotizacion', models.CharField(blank=True, max_length=1, null=True)),
                ('puesto', models.CharField(blank=True, max_length=30, null=True)),
                ('integrado', models.BooleanField(blank=True, null=True)),
                ('comida', models.CharField(blank=True, max_length=1, null=True)),
                ('estatus', models.CharField(blank=True, max_length=1, null=True)),
                ('num_seguro_social', models.CharField(blank=True, max_length=16, null=True)),
                ('num_infonavit', models.CharField(blank=True, max_length=16, null=True)),
                ('rfc_trabajador', models.CharField(blank=True, max_length=13, null=True)),
                ('curp', models.CharField(blank=True, max_length=40, null=True)),
                ('sexo', models.CharField(blank=True, max_length=10, null=True)),
                ('edo_civil', models.CharField(blank=True, max_length=15, null=True)),
                ('nombre_madre', models.CharField(blank=True, max_length=50, null=True)),
                ('nombre_padre', models.CharField(blank=True, max_length=50, null=True)),
                ('domicilio', models.CharField(blank=True, max_length=50, null=True)),
                ('codigo_postal', models.BooleanField(blank=True, max_length=8, null=True)),
                ('lugar_nacimiento', models.CharField(blank=True, max_length=30, null=True)),
                ('familiar_referencia_1', models.CharField(blank=True, max_length=30, null=True)),
                ('telefono_referencia_1', models.CharField(blank=True, max_length=20, null=True)),
                ('familiar_referencia_2', models.CharField(blank=True, max_length=30, null=True)),
                ('telefono_referencia_2', models.CharField(blank=True, max_length=20, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('campo_agricola', models.ForeignKey(db_column='id_campo_agricola', on_delete=django.db.models.deletion.CASCADE, to='nom_campos.nomcampos')),
                ('cuadrillero', models.ForeignKey(db_column='id_cuadrillero', on_delete=django.db.models.deletion.CASCADE, to='nom_cuadrilleros.nomcuadrilleros')),
            ],
            options={
                'db_table': 'nom_empleado',
            },
        ),
    ]