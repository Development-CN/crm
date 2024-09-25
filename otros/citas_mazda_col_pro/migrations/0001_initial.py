# Generated by Django 4.0.6 on 2022-07-14 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('year_start', models.IntegerField(blank=True, null=True)),
                ('year_end', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('wait', models.BooleanField(blank=True, default=False, null=True)),
                ('time', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('service_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='citas_mazda_col_pro.servicetype')),
            ],
        ),
    ]