# Generated by Django 4.0.6 on 2022-07-21 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citas_mazda_col_pro', '0007_appointment_additional_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='ServicePrice',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('car_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='citas_mazda_col_pro.carmodel')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='citas_mazda_col_pro.service')),
            ],
            options={
                'verbose_name': 'Precio de servicio',
                'verbose_name_plural': 'Precios de servicio',
            },
        ),
    ]
