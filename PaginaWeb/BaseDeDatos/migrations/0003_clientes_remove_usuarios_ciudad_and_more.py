# Generated by Django 4.0.3 on 2022-03-29 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseDeDatos', '0002_alter_usuarios_sexo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_unico', models.CharField(max_length=100, unique=True, verbose_name='Nombre_Unico')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=40, verbose_name='Apellido')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=100, verbose_name='Contraseña')),
                ('sexo', models.CharField(max_length=1, verbose_name='Sexo')),
                ('celular', models.CharField(max_length=9, verbose_name='Celular')),
                ('edad', models.IntegerField(verbose_name='Edad')),
                ('pais', models.CharField(max_length=50, verbose_name='País')),
                ('ciudad', models.CharField(max_length=50, verbose_name='Ciudad')),
                ('comuna', models.CharField(max_length=50, verbose_name='Comuna')),
            ],
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='pais',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='nivel_staff',
            field=models.IntegerField(default=0, null=True, verbose_name='Nivel Staff'),
        ),
    ]
