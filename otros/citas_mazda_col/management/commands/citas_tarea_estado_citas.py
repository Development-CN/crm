from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date_time = datetime.now()

        # ACTUALIZACIÓN DE ESTADO DE LAS CITAS
        # La proxima hora de ejecución de la tarea programada
        update_state_next_run = current_date_time.replace(hour=1, minute=0, second=0, microsecond=0)

        # Si la hora ya pasó, establecer la ejecución para el dia de mañana
        if not current_date_time.hour <= 1:
            update_state_next_run = update_state_next_run + timedelta(days=1)

        # Se crea o actualiza la tarea
        task, update_state_created = Schedule.objects.update_or_create(
            name="Actualización de estado de las citas",
            defaults={
                "func": "citas_mazda_col.tasks.actualizacion_estado_citas",
                "args": "",
                "next_run": update_state_next_run,
                "schedule_type": Schedule.DAILY,
                "cron": None,
                "repeats": -1,
            },
        )

        if update_state_created:
            message = "creó"
        else:
            message = "actualizó"

        self.stdout.write(self.style.SUCCESS(f'Se {message} la tarea programada: "Actualización de estado de citas"'))
        self.stdout.write(self.style.SUCCESS(f"La proxima ejecución sera: {update_state_next_run}"))

        self.stdout.write(self.style.WARNING("REINICIAR EL SERVICIO DE TAREAS PROGRAMADAS"))
