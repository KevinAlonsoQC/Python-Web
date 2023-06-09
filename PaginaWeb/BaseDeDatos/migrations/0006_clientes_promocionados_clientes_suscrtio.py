# Generated by Django 4.0.3 on 2022-03-29 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseDeDatos', '0005_pedidos_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes_Promocionados',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cliente', models.CharField(max_length=100, verbose_name='Nombre_Unico')),
                ('vencimiento', models.DateTimeField(verbose_name='Vencimiento')),
                ('porcentaje_descuento', models.IntegerField(default=0, verbose_name='Porcentaje de Descuento')),
                ('promocion', models.TextField(null=True, verbose_name='Nombre de Promoción')),
            ],
        ),
        migrations.AddField(
            model_name='clientes',
            name='suscrtio',
            field=models.BooleanField(default=False, verbose_name='Suscrito'),
        ),
    ]
