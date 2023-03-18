# Generated by Django 4.0.3 on 2022-04-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseDeDatos', '0011_alter_pedidos_fecha_entrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes_promocionados',
            name='vencimiento',
            field=models.DateField(verbose_name='Vencimiento'),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='fecha_entrega',
            field=models.DateField(default=0, null=True, verbose_name='Fecha Entrega'),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='fecha_pedido',
            field=models.DateField(verbose_name='Fecha Pedido'),
        ),
        migrations.AlterField(
            model_name='promociones',
            name='fecha_fin',
            field=models.DateField(verbose_name='Fecha Fin'),
        ),
        migrations.AlterField(
            model_name='promociones',
            name='fecha_inicio',
            field=models.DateField(verbose_name='Fecha Inicio'),
        ),
    ]
