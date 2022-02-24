from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from tech.models import WorkingDay, PayRate, Skill


class Command(BaseCommand):
    help = "Create Initial Entities (Days of week, payrates, etc)."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Adding days of week...')
        WorkingDay.objects.create(day='Monday')
        WorkingDay.objects.create(day='Tuesday')
        WorkingDay.objects.create(day='Wednesday')
        WorkingDay.objects.create(day='Thursday')
        WorkingDay.objects.create(day='Friday')
        WorkingDay.objects.create(day='Saturday')
        WorkingDay.objects.create(day='Sunday')

        self.stdout.write('Adding initial payrate level')
        PayRate.objects.create(level='Entry', payrate='15.00')

        self.stdout.write('Adding initial skill')
        Skill.objects.create(name='Windows')
        Skill.objects.create(name='Mac')
        Skill.objects.create(name='Linux')
        Skill.objects.create(name='Servers')
        Skill.objects.create(name='Printers')
        Skill.objects.create(name='Networking')


        self.stdout.write('Done setting up entities')