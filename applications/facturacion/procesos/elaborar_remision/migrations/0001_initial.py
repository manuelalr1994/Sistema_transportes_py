# Generated by Django 4.0 on 2022-09-28 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nom_campos', '0001_initial'),
        ('procesar_maquila', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FletesAbonos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tipo', models.CharField(max_length=1)),
                ('campo_agricola', models.ForeignKey(db_column='id_campo_agricola', on_delete=django.db.models.deletion.CASCADE, to='nom_campos.nomcampos')),
                ('maquila', models.ForeignKey(db_column='id_maquila', on_delete=django.db.models.deletion.CASCADE, to='procesar_maquila.fletesmaquilas')),
            ],
        ),
        migrations.CreateModel(
            name='FletesRemisiones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=10, unique=True)),
                ('fecha', models.DateField()),
                ('importe', models.DecimalField(decimal_places=2, max_digits=12)),
                ('facturada', models.BooleanField(default=False)),
                ('campo_agricola', models.ForeignKey(db_column='id_campo_agricola', on_delete=django.db.models.deletion.CASCADE, to='nom_campos.nomcampos')),
                ('maquilas_afectadas', models.ManyToManyField(through='elaborar_remision.FletesAbonos', to='procesar_maquila.FletesMaquilas')),
            ],
            options={
                'db_table': 'fle_remisiones',
                'ordering': ['id'],
                'get_latest_by': 'id',
            },
        ),
        migrations.AddField(
            model_name='fletesabonos',
            name='remision',
            field=models.ForeignKey(db_column='id_remision', on_delete=django.db.models.deletion.CASCADE, to='elaborar_remision.fletesremisiones'),
        ),
    ]