from django.core.management.base import BaseCommand

from apps.rooms.models import Room


class Command(BaseCommand):
    help = 'Seed sample rooms for gas simulation testing.'

    SAMPLE_ROOMS = [
        ('Kitchen', 'Main kitchen area with gas stove'),
        ('Living Room', 'Central living area'),
        ('Bedroom 1', 'Master bedroom'),
        ('Bedroom 2', 'Guest bedroom'),
        ('Basement', 'Basement utility room with water heater'),
    ]

    def handle(self, *args, **options):
        created = 0
        for name, description in self.SAMPLE_ROOMS:
            _, was_created = Room.objects.get_or_create(
                name=name,
                defaults={'description': description},
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created room: {name}'))
            else:
                self.stdout.write(f'  Room already exists: {name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created} new room(s) created. Total rooms: {Room.objects.count()}'
        ))
