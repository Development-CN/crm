# Generated by Django 4.2.2 on 2023-11-10 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, null=True)),
                ('sala', models.CharField(max_length=255, null=True)),
                ('habilitado', models.BooleanField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Asesores',
            },
        ),
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('clasificacion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Catalogos',
            },
        ),
        migrations.CreateModel(
            name='CatalogoModelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'CatalogoModelo',
            },
        ),
        migrations.CreateModel(
            name='CatalogoRespuestasByEtapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=50)),
                ('etapa', models.CharField(choices=[('No contactado', 'No contactado'), ('Interaccion', 'Interaccion'), ('Oportunidad', 'Oportunidad'), ('Pedido', 'Pedido'), ('Desistido', 'Desistido')], max_length=50)),
                ('estado', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo', models.CharField(blank=True, choices=[('normal', 'normal'), ('compra', 'compra'), ('peritaje', 'peritaje')], max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Catalogo Respuestas By Etapa',
            },
        ),
        migrations.CreateModel(
            name='CatalogoStockVehiculos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=50)),
                ('marca', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Catalogo Stock Vehiculos',
            },
        ),
        migrations.CreateModel(
            name='HistorialCompleto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingreso', models.DateTimeField(null=True)),
                ('respuesta', models.CharField(max_length=255, null=True)),
                ('etapa', models.CharField(max_length=255, null=True)),
                ('origen', models.CharField(max_length=255, null=True)),
                ('nombres', models.CharField(max_length=255, null=True)),
                ('apellidos', models.CharField(max_length=255, null=True)),
                ('anfitrion', models.CharField(max_length=255, null=True)),
                ('sala', models.CharField(max_length=255, null=True)),
                ('asesor', models.CharField(max_length=255, null=True)),
                ('telefonos', models.CharField(max_length=255, null=True)),
                ('correos', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialProspectos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingreso', models.DateTimeField(null=True)),
                ('estado', models.CharField(max_length=255, null=True)),
                ('etapa', models.CharField(max_length=255, null=True)),
                ('medio', models.CharField(max_length=255, null=True)),
                ('fuente', models.CharField(max_length=255, null=True)),
                ('nombres', models.CharField(max_length=255, null=True)),
                ('apellidos', models.CharField(max_length=255, null=True)),
                ('tipo_modulo', models.CharField(max_length=255, null=True)),
                ('modulo', models.CharField(max_length=255, null=True)),
                ('actividad', models.CharField(max_length=255, null=True)),
                ('documento', models.CharField(max_length=255, null=True)),
                ('telefonos', models.CharField(max_length=255, null=True)),
                ('correos', models.CharField(max_length=255, null=True)),
                ('ciudad_nacimiento', models.CharField(max_length=255, null=True)),
                ('ciudad_vive', models.CharField(max_length=255, null=True)),
                ('total_gestiones', models.CharField(max_length=255, null=True)),
                ('usuario', models.CharField(max_length=255, null=True)),
                ('vinculos', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'HistorialProspectos',
            },
        ),
        migrations.CreateModel(
            name='InteresesDesistidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_vehiculo_interes', models.IntegerField()),
                ('comentario', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'InteresesDesistidos',
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen_lead', models.CharField(max_length=50)),
                ('marcas_interes', models.CharField(blank=True, max_length=3000, null=True)),
                ('forma_pago', models.CharField(blank=True, max_length=50, null=True)),
                ('sala', models.CharField(max_length=50, null=True)),
                ('etapa', models.CharField(max_length=100, null=True)),
                ('respuesta', models.CharField(max_length=100, null=True)),
                ('fecha_hora_reasignacion', models.DateTimeField(blank=True, null=True)),
                ('fecha_hora_accion_siguiente', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('fecha_apertura', models.DateTimeField(null=True)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('fecha_cambio_de_etapa', models.DateTimeField(blank=True, null=True)),
                ('tiempo_cambio_de_etapa', models.IntegerField(blank=True, null=True)),
                ('fecha_ultima_accion', models.DateField(blank=True, null=True)),
                ('fecha_primer_contacto', models.DateTimeField(blank=True, null=True)),
                ('tiempo_primer_contacto', models.IntegerField(blank=True, null=True)),
                ('fecha_contacto_asesor', models.DateTimeField(blank=True, null=True)),
                ('fecha_cita', models.DateField(blank=True, null=True)),
                ('fecha_aprobacion_credito', models.DateField(blank=True, null=True)),
                ('fecha_recepcion_documentos', models.DateField(blank=True, null=True)),
                ('fecha_aprobacion_documentos', models.DateField(blank=True, null=True)),
                ('activo', models.BooleanField()),
                ('interes', models.CharField(max_length=50, null=True)),
                ('estado_llamada_verificacion', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo_solicitud_verificacion', models.CharField(blank=True, max_length=100, null=True)),
                ('plazo_pago', models.CharField(blank=True, max_length=100, null=True)),
                ('comentario', models.CharField(blank=True, max_length=100, null=True)),
                ('campania', models.CharField(max_length=100, null=True)),
                ('tipo_documento', models.CharField(max_length=60, null=True)),
                ('documento', models.CharField(max_length=60, null=True)),
                ('test_drive', models.BooleanField()),
                ('nombre_asesor', models.CharField(max_length=100, null=True)),
                ('fecha_hora_asignacion_asesor', models.DateTimeField(null=True)),
                ('nombre_anfitrion', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeadPeritaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_nombre', models.CharField(max_length=50)),
                ('c_primer_apellido', models.CharField(max_length=50)),
                ('c_segundo_apellido', models.CharField(max_length=50)),
                ('c_correo', models.CharField(max_length=200)),
                ('c_tipo_documento', models.CharField(max_length=10)),
                ('c_cedula_nit', models.CharField(max_length=50)),
                ('c_numero_telefonico', models.CharField(max_length=13)),
                ('l_etapa', models.CharField(max_length=50)),
                ('l_respuesta', models.CharField(max_length=50)),
                ('l_estado', models.CharField(max_length=50)),
                ('l_nombre_asesor', models.CharField(max_length=100)),
                ('l_vitrina_sala', models.CharField(max_length=50)),
                ('v_marca', models.CharField(max_length=50)),
                ('v_linea', models.CharField(max_length=50)),
                ('v_caja', models.CharField(max_length=50)),
                ('v_placa', models.CharField(max_length=50)),
                ('v_ciudad_placa', models.CharField(max_length=50)),
                ('v_modelo', models.CharField(max_length=50)),
                ('v_kilometraje', models.CharField(max_length=50)),
                ('v_color', models.CharField(max_length=50)),
                ('v_lugar_mto', models.CharField(max_length=500)),
                ('v_reclamaciones_siniestros', models.BooleanField()),
                ('v_peritaje_anterior', models.BooleanField()),
                ('v_valor_revista_motor', models.FloatField()),
                ('v_valor_esperado_cliente', models.FloatField()),
                ('v_valor_aproximado', models.FloatField()),
                ('activa', models.BooleanField()),
                ('fecha_cierre', models.DateField(null=True)),
                ('l_nombre_perito', models.CharField(max_length=50, null=True)),
                ('l_origen_lead', models.CharField(max_length=50)),
                ('l_comentario_inicial', models.CharField(max_length=500, null=True)),
                ('p_version_formato', models.IntegerField(null=True)),
                ('p_fecha_hora', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name_plural': 'LeadsPeritaje',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_lead_o_compra', models.IntegerField()),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('responsable', models.CharField(max_length=100)),
                ('operacion_realizada', models.CharField(max_length=100, null=True)),
                ('comentarios', models.CharField(max_length=100, null=True)),
                ('tipo', models.CharField(choices=[('normal', 'normal'), ('compra', 'compra'), ('peritaje', 'peritaje')], max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='Prospecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('celular', models.CharField(blank=True, max_length=15, null=True)),
                ('correo', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=50, null=True)),
                ('departamento', models.CharField(blank=True, max_length=50, null=True)),
                ('localidad', models.CharField(blank=True, max_length=50, null=True)),
                ('profesion', models.CharField(blank=True, max_length=100, null=True)),
                ('ingresos', models.CharField(blank=True, max_length=50, null=True)),
                ('vehiculo_actual', models.CharField(blank=True, max_length=100, null=True)),
                ('interes_deporte', models.CharField(blank=True, max_length=50, null=True)),
                ('interes_mascotas', models.CharField(blank=True, max_length=50, null=True)),
                ('contacto_nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('contacto_telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_captura', models.DateTimeField()),
                ('nombre_asesor', models.CharField(max_length=100, null=True)),
                ('correo_asesor', models.CharField(blank=True, max_length=100, null=True)),
                ('anfitrion', models.CharField(max_length=50)),
                ('fecha_hora_asignacion_asesor', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.BooleanField(null=True)),
                ('politica_privacidad', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Usados19_22',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=255, null=True)),
                ('origen', models.CharField(max_length=255, null=True)),
                ('fecha', models.DateTimeField()),
                ('hora_militar', models.DateTimeField()),
                ('recibida_por', models.CharField(max_length=255, null=True)),
                ('nombre_de_cliente', models.CharField(max_length=255, null=True)),
                ('celular', models.CharField(max_length=15, null=True)),
                ('correo', models.CharField(max_length=255, null=True)),
                ('interesado_en', models.CharField(max_length=255, null=True)),
                ('referencia', models.CharField(max_length=255, null=True)),
                ('enviado_a', models.CharField(max_length=255, null=True)),
                ('asesor_asignado', models.CharField(max_length=255, null=True)),
                ('hora_correo', models.DateTimeField()),
                ('observaciones', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usados2021',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=255, null=True)),
                ('origen', models.CharField(max_length=255, null=True)),
                ('reclasificacion_origen_anfitrion_digital', models.DateTimeField()),
                ('fecha', models.DateTimeField()),
                ('hora_militar', models.DateTimeField()),
                ('recibida_por', models.CharField(max_length=255, null=True)),
                ('nombre_de_cliente', models.CharField(max_length=255, null=True)),
                ('celular', models.CharField(max_length=15, null=True)),
                ('correo', models.CharField(max_length=255, null=True)),
                ('interesado_en', models.CharField(max_length=255, null=True)),
                ('referencia', models.CharField(max_length=255, null=True)),
                ('enviado_a', models.CharField(max_length=255, null=True)),
                ('asesor_asignado', models.CharField(max_length=255, null=True)),
                ('hora_correo', models.DateTimeField()),
                ('observaciones', models.CharField(max_length=255, null=True)),
                ('fecha_verificacion', models.DateTimeField()),
                ('estatus', models.CharField(max_length=255, null=True)),
                ('verificado_por', models.CharField(max_length=255, null=True)),
                ('observaciones_1', models.CharField(max_length=255, null=True)),
                ('f20', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Usados2021',
            },
        ),
        migrations.CreateModel(
            name='VehiculosInteresLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('comentario', models.CharField(blank=True, max_length=50, null=True)),
                ('peritaje', models.BooleanField(null=True)),
                ('cotizar', models.BooleanField()),
                ('aprobacion', models.BooleanField()),
                ('fecha', models.DateField(blank=True, null=True)),
                ('precio', models.FloatField(null=True)),
                ('codigo_vehiculo', models.CharField(max_length=50, null=True)),
                ('separado', models.BooleanField(null=True)),
                ('facturado', models.BooleanField(null=True)),
                ('mostrado', models.BooleanField(null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.lead')),
            ],
            options={
                'verbose_name_plural': 'VehiculosInteresLeads',
            },
        ),
        migrations.CreateModel(
            name='Retomas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=500)),
                ('valor', models.FloatField()),
                ('total', models.FloatField()),
                ('total_restante', models.FloatField()),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.lead')),
            ],
            options={
                'verbose_name_plural': 'Retomas',
            },
        ),
        migrations.AddField(
            model_name='lead',
            name='prospecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.prospecto'),
        ),
        migrations.CreateModel(
            name='HistorialVerificaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_llamada', models.CharField(max_length=50, null=True)),
                ('tipo_solicitud', models.CharField(max_length=50, null=True)),
                ('responsable', models.CharField(max_length=50, null=True)),
                ('reasignado', models.CharField(blank=True, max_length=50, null=True)),
                ('observaciones', models.CharField(max_length=50, null=True)),
                ('fecha_hora_verificacion', models.DateTimeField()),
                ('responsable_original_lead', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo', models.CharField(choices=[('venta', 'venta'), ('compra', 'compra'), ('peritaje', 'peritaje')], max_length=50)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.lead')),
            ],
            options={
                'verbose_name_plural': 'HistorialVerificaciones',
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(null=True)),
                ('responsable', models.CharField(max_length=100, null=True)),
                ('operacion', models.CharField(max_length=255, null=True)),
                ('comentarios', models.CharField(blank=True, max_length=255, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.lead')),
            ],
            options={
                'verbose_name_plural': 'Historial',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, null=True)),
                ('tipo', models.CharField(choices=[('Testdrive', 'Testdrive'), ('Peritaje', 'Peritaje'), ('Whatsapp', 'Whatsapp'), ('Llamada', 'Llamada'), ('Cita Vitrina', 'Cita Vitrina')], max_length=255, null=True)),
                ('telefono_cliente', models.CharField(max_length=255, null=True)),
                ('observaciones', models.CharField(max_length=255)),
                ('fecha_hora', models.DateTimeField()),
                ('tiempo_evento', models.CharField(max_length=255, null=True)),
                ('cumplido', models.BooleanField(default=False, null=True)),
                ('fecha_hora_cumplido', models.DateTimeField(blank=True, null=True)),
                ('asesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.asesor')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.lead')),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apertura', models.DateField()),
                ('origen_lead', models.CharField(max_length=50)),
                ('nombre_comprador', models.CharField(max_length=100, null=True)),
                ('fecha_hora_asignacion_comprador', models.DateTimeField(null=True)),
                ('nombre_anfitrion', models.CharField(max_length=100, null=True)),
                ('etapa', models.CharField(max_length=100)),
                ('respuesta', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
                ('fecha_ultimaaccion', models.DateField(null=True)),
                ('fecha_hora_accionsiguiente', models.DateTimeField(null=True)),
                ('tipo_interes', models.CharField(max_length=100, null=True)),
                ('comentario_apertura', models.CharField(max_length=100, null=True)),
                ('compania', models.CharField(max_length=100, null=True)),
                ('tipo_documento', models.CharField(max_length=60, null=True)),
                ('documento', models.CharField(max_length=60, null=True)),
                ('marca', models.CharField(max_length=50, null=True)),
                ('modelo', models.CharField(max_length=50, null=True)),
                ('anio', models.CharField(max_length=50, null=True)),
                ('version', models.CharField(max_length=50, null=True)),
                ('color', models.CharField(max_length=50, null=True)),
                ('kilometraje', models.CharField(max_length=50, null=True)),
                ('cilindraje', models.CharField(max_length=50, null=True)),
                ('unique_owner', models.CharField(max_length=2, null=True)),
                ('caja', models.CharField(max_length=50, null=True)),
                ('placa', models.CharField(max_length=7, null=True)),
                ('ciudad_placa', models.CharField(max_length=100, null=True)),
                ('peritaje_lugar_cita', models.CharField(max_length=50, null=True)),
                ('peritaje_fecha_hora_cita', models.DateTimeField(null=True)),
                ('peritaje_direccion_cita', models.CharField(max_length=100, null=True)),
                ('peritaje_ciudad_cita', models.CharField(max_length=50, null=True)),
                ('oferta_madiautos', models.FloatField(null=True)),
                ('oferta_revista', models.FloatField(null=True)),
                ('pretension_cliente', models.FloatField(null=True)),
                ('estado_vehiculo', models.CharField(max_length=100, null=True)),
                ('reclamacion_siniestros', models.CharField(max_length=100, null=True)),
                ('observacion_vehiculo', models.CharField(max_length=100, null=True)),
                ('peritaje_correo', models.CharField(max_length=100, null=True)),
                ('peritaje_carroceria', models.CharField(max_length=50, null=True)),
                ('peritaje_combustible', models.CharField(max_length=50, null=True)),
                ('fecha_primer_contacto', models.DateField(null=True)),
                ('fecha_peritaje', models.DateField(null=True)),
                ('fecha_cierre', models.DateField(null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('forma_pago', models.CharField(max_length=50, null=True)),
                ('activo', models.BooleanField(null=True)),
                ('concretada', models.BooleanField(null=True)),
                ('valor_final', models.FloatField(null=True)),
                ('prospecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboards.prospecto')),
            ],
            options={
                'verbose_name_plural': 'Compras',
            },
        ),
        migrations.CreateModel(
            name='CatalogoEmpleados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('sala', models.CharField(max_length=50)),
                ('puesto', models.CharField(max_length=50)),
                ('division', models.CharField(max_length=50, null=True)),
                ('correo', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Catalogo Empleados',
            },
        ),
    ]
