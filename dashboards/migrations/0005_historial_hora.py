# Generated by Django 4.2.2 on 2023-11-25 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0004_remove_historial_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='historial',
            name='hora',
            field=models.TimeField(null=True),
        ),
    ]
