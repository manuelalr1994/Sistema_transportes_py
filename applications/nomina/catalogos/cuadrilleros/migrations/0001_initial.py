# Generated by Django 4.0 on 2022-09-28 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nom_campos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NomCuadrilleros',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(default=0, max_length=8)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('campo_agricola', models.ForeignKey(db_column='id_campo_agricola', on_delete=django.db.models.deletion.CASCADE, to='nom_campos.nomcampos')),
            ],
            options={
                'db_table': 'nom_cuadrilleros',
                'ordering': ['codigo'],
                'get_latest_by': 'codigo',
            },
        ),
    ]