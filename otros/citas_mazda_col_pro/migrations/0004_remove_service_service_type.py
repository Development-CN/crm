# Generated by Django 4.0.6 on 2022-07-14 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas_mazda_col_pro', '0003_alter_carmodel_options_alter_servicetype_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='service_type',
        ),
    ]
