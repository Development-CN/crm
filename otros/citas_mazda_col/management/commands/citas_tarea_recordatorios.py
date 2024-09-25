from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date_time = datetime.now()

        # ENVÍO DE RECORDATORIOS DE CITAS
        # La proxima hora de ejecución de la tarea programada
        reminder_next_run = current_date_time.replace(hour=18, minute=0, second=0, microsecond=0)

        # Si la hora ya pasó, establecer la ejecución para el dia de mañana
        if not current_date_time.hour <= 20:
            reminder_next_run = reminder_next_run + timedelta(days=1)

        # Se crea o actualiza la tarea
        task, reminder_created = Schedule.objects.update_or_create(
            name="Envío de recordatorios de citas",
            defaults={
                "func": "citas_mazda_col.tasks.envio_recordatorios_citas",
                "args": "",
                "next_run": reminder_next_run,
                "schedule_type": Schedule.DAILY,
                "cron": None,
                "repeats": -1,
            },
        )

        if reminder_created:
            message = "creó"
        else:
            message = "actualizó"

        self.stdout.write(self.style.SUCCESS(f'Se {message} la tarea programada: "Envío de recordatorios de citas"'))
        self.stdout.write(self.style.SUCCESS(f"La proxima ejecución sera: {reminder_next_run}"))

        self.stdout.write(self.style.WARNING("REINICIAR EL SERVICIO DE TAREAS PROGRAMADAS"))
