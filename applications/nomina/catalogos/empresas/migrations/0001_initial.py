# Generated by Django 4.0 on 2022-09-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NomEmpresas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=3)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('rfc', models.CharField(blank=True, max_length=13, null=True)),
                ('direccion', models.CharField(blank=True, max_length=20, null=True)),
                ('colonia', models.CharField(blank=True, max_length=20, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=20, null=True)),
                ('estado', models.CharField(blank=True, max_length=20, null=True)),
                ('cp', models.CharField(blank=True, max_length=5, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'nom_empresas',
                'ordering': ['id'],
                'get_latest_by': 'codigo',
            },
        ),
    ]