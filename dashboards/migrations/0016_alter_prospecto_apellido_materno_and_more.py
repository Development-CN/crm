# Generated by Django 4.2.7 on 2024-10-22 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0015_alter_historial_operacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prospecto',
            name='apellido_materno',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='prospecto',
            name='apellido_paterno',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
