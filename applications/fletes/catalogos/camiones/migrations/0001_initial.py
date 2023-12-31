# Generated by Django 4.0 on 2022-09-28 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fle_compania_fletera', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camiones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(error_messages={'unique': 'Ya existe un camion con este codigo'}, max_length=8, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('alias', models.CharField(max_length=50)),
                ('costo_hra', models.DecimalField(decimal_places=2, max_digits=6)),
                ('activo', models.BooleanField(default=True)),
                ('compania_fletera', models.ForeignKey(db_column='id_compania_fletera', on_delete=django.db.models.deletion.CASCADE, to='fle_compania_fletera.companiasfleteras')),
            ],
            options={
                'db_table': 'camiones',
                'get_latest_by': 'codigo',
            },
        ),
    ]
