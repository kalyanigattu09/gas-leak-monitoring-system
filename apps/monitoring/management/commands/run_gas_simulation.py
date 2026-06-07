import time

from django.core.management.base import BaseCommand

from apps.monitoring.services.gas_service import GasSimulationService


class Command(BaseCommand):
    help = 'Simulate gas sensor readings every 5 seconds for all rooms.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=5,
            help='Seconds between readings (default: 5)',
        )
        parser.add_argument(
            '--once',
            action='store_true',
            help='Run a single simulation cycle and exit',
        )

    def handle(self, *args, **options):
        interval = options['interval']
        service = GasSimulationService()

        self.stdout.write(self.style.SUCCESS(
            f'Gas simulation started (interval: {interval}s). Press Ctrl+C to stop.'
        ))

        try:
            while True:
                readings = service.process_all_rooms()
                if readings:
                    for reading in readings:
                        self.stdout.write(
                            f'  {reading.room.name}: {reading.gas_level} ({reading.status})'
                        )
                else:
                    self.stdout.write(self.style.WARNING(
                        '  No rooms to simulate. Add rooms via the admin or /rooms/add/.'
                    ))

                if options['once']:
                    break
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nSimulation stopped.'))
