# Generated by Django 4.2.2 on 2023-11-25 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0003_alter_historialverificaciones_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historial',
            name='hora',
        ),
    ]
