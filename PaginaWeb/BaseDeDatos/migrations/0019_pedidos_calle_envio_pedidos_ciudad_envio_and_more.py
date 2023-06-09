# Generated by Django 4.0.3 on 2022-04-30 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseDeDatos', '0018_alter_clientes_promocionados_promocion'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='calle_envio',
            field=models.CharField(default='nulo', max_length=100, verbose_name='Calle de Envio'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='ciudad_envio',
            field=models.CharField(default='nulo', max_length=100, verbose_name='Ciudad de Envio'),
        ),
        migrations.AddField(
            model_name='pedidos',
            name='comuna_envio',
            field=models.CharField(default='nulo', max_length=100, verbose_name='Comuna de Envio'),
        ),
    ]
