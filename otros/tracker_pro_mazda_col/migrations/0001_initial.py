from django.conf import settings
from django.db import migrations

TABLERO_DB = settings.TABLERO_DB


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            f""" 
            CREATE VIEW  [dbo].[v_informacion_historica] as 
            select * from {TABLERO_DB}.dbo.tb_citas_header_nw    
            """
        ),
        migrations.RunSQL(
            f"""
            CREATE view [dbo].[v_tracker] as 

            select distinct
                
                id_hd= a.id_hd,
                no_orden = b.noorden,
                placas= b.noplacas,
                fecha =cast(b.fecha as date),
                telefono_agencia = '320',
                tecnico = t.NOMBRE_EMPLEADO,
                asesor = case when a.idasesor = '' then 'Sin asesor registrado'

                else (select top 1 nombre from {TABLERO_DB}.dbo.SccUsuarios where cveAsesor=a.idAsesor) end,

                vehiculo = b.vehiculo,
                hora_llegada = b.horallegada,
                hora_inicio_asesor = b.horairecepcion,
                hora_fin_asesor = b.horafrecepcion,
                hora_promesa = d.Fecha_Entrega,
                hora_grabado=a.horarampa,

                inicio_tecnico = a.fecha_hora_ini_oper,
                fin_tecnico = (case when a.fecha_hora_paro is null then a.Fecha_Hora_Fin_Oper else a.fecha_hora_paro end),
                detenido = (case when a.fecha_hora_paro is not null then 'True' else 'False' end ), 
                
                servicio_capturado = (case 

                when a.serviciocapturado like '%Servicio%' then 'Servicio'
                when a.servicioCapturado like '%Diagnostico%' then 'Diagnostico'
                when a.servicioCapturado like '%Reparacion%' then 'Reparacion'
                else a.servicioCapturado end),

                inicio_tecnico_lavado = c.fecha_hora_ini_oper,
                fin_tecnico_lavado = c.fecha_hora_fin_oper,
                ultima_actualizacion = (case

                when b.horairecepcion is null then DATEDIFF(minute , b.horallegada, getdate()) 
                when b.horaFrecepcion is null then DATEDIFF(minute,  b.horairecepcion, getdate())
                when a.fecha_hora_ini_oper is null then DATEDIFF(minute, b.horaFrecepcion, getdate())
                when a.fecha_hora_fin_oper is null then DATEDIFF(minute, a.fecha_hora_ini_oper, getdate())
                when c.fecha_hora_ini_oper is null then DATEDIFF(minute, a.fecha_hora_fin_oper, getdate())
                when c.fecha_hora_fin_oper is null then DATEDIFF(minute, c.fecha_hora_ini_oper, getdate())
                else  DATEDIFF(minute, c.fecha_hora_fin_oper, getdate())
                end),

                motivo_paro=(case 
                when a.id_motivo_paro='2' then 'Refacciones' 
                when a.id_motivo_paro='3' then 'Autorización'
                when a.id_motivo_paro='4' then 'Proceso'
                when a.id_motivo_paro='7' then 'Trabajo en otro taller'

                    end)

                
            from {TABLERO_DB}.dbo.tb_citas as a with(nolock) 

                inner join {TABLERO_DB}.dbo.Tb_CITAS_HEADER_NW  as b with (nolock) on a.id_hd = b.id_hd
                left join {TABLERO_DB}.dbo.tb_tecnicos as t with(nolock) on a.idTecnico = t.id_empleado
                left join {TABLERO_DB}.dbo.tb_citas  as c with(nolock) on c.id_hd=a.id_hd and c.servicioCapturado = 'lavado'
                LEFT JOIN {TABLERO_DB}.dbo. TB_Confirmacion_Entregas as d with(nolock) on b.id_hd=d.id_hd AND d.status='Confirmado'

                where t.NOMBRE_EMPLEADO<> 'NO SHOW'
                and b.HoraRetiro is null
                and b.Horallegada is not null
                and b.noOrden <> 0
                and b.fecha > '20190101'
                and a.servicioCapturado <> 'Lavado'
            """
        ),
    ]
