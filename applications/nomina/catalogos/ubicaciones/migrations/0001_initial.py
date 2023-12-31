# Generated by Django 4.0 on 2022-09-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ubicaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(default=0, max_length=8)),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'ubicaciones',
                'ordering': ['id'],
                'get_latest_by': 'id',
            },
        ),
    ]
