from django.conf import settings
from django.db import migrations

TABLERO_DB = settings.TABLERO_DB


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            f""" 
            CREATE view [dbo].[v_usuarios] as
            select a.*,
            id = row_number() over (order by a.pass desc),
            last_login='',
            Is_superuser= case when a.cvePerfil=1 then 1 else 0 end,
            last_name= getdate(),
            is_staff= 1,
            is_active= 1,
            date_joined= cast('20190101' as datetime)
            from {TABLERO_DB}.dbo.sccusuarios as a
            """
        ),
        migrations.RunSQL(
            f"""
            create view [dbo].[v_tecnicos] as 
            select * from [{TABLERO_DB}].dbo.tb_tecnicos
            """
        ),
        migrations.RunSQL(
            f"""
            create view [dbo].[v_informacion_citas] as
            select 
            id_hd = a.id_hd,
            no_cita= a.NUMCITA, 
            no_orden= a.NOORDEN, 
            cliente = a.Cliente, 
            hora_llegada = a.Horallegada, 
            hora_retiro= a.HoraRetiro, 
            placas = a.noPlacas, 
            vin = a.vin, 
            vehiculo = a.Vehiculo, 
            color = a.Color 

            from {TABLERO_DB}.dbo.Tb_CITAS_HEADER_NW as a with (nolock)
            where a.Horallegada is not null
            """
        ),
    ]
