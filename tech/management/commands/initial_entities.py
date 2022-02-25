from os.path import exists

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.management.base import BaseCommand


from tech.models import WorkingDay, PayRate, Skill, Part, PartStatus


class Command(BaseCommand):
    help = "Create Initial Entities (Days of week, payrates, etc)."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")



    def handle(self, *args, **options):
        # self.stdout.write('Adding days of week...')
        # WorkingDay.objects.create(day='Monday')
        # WorkingDay.objects.create(day='Tuesday')
        # WorkingDay.objects.create(day='Wednesday')
        # WorkingDay.objects.create(day='Thursday')
        # WorkingDay.objects.create(day='Friday')
        # WorkingDay.objects.create(day='Saturday')
        # WorkingDay.objects.create(day='Sunday')
        #
        # self.stdout.write('Adding initial payrate level')
        # PayRate.objects.create(level='Entry', payrate='15.00')
        #
        # self.stdout.write('Adding initial skill')
        # Skill.objects.create(name='Windows')
        # Skill.objects.create(name='Mac')
        # Skill.objects.create(name='Linux')
        # Skill.objects.create(name='Servers')
        # Skill.objects.create(name='Printers')
        # Skill.objects.create(name='Networking')

        self.stdout.write('Adding Parts')
        self.add_dummy_part("Old Mouse", "oscar-ivan-esquivel-arteaga-ZtxED1cpB1E-unsplash.jpg", 14.99, PartStatus.DISCONTINUED)
        self.add_dummy_part("1TB Harddrive", "nick-van-der-ende-VYfxkePredI-unsplash.jpg", 100, PartStatus.WAREHOUSE)
        self.add_dummy_part("Keyboard", "martin-garrido-cVUPic1cbd4-unsplash.jpg", 25.99, PartStatus.WAREHOUSE)
        self.add_dummy_part("Laptop", "erick-cerritos-i5UV2HpITYA-unsplash.jpg", 1250, PartStatus.UNAVAILABLE, 14)
        self.add_dummy_part("Computer", "luke-hodde-Z-UuXG6iaA8-unsplash.jpg", 730, PartStatus.ORDER)

        self.stdout.write('Done setting up entities')

    def add_dummy_part(self, name, image, cost, status, leadtime=None):
        if not exists('media/' + image):
            self.stdout.write('Adding ' + name)
            f = open('tech/assets/photos/' + image, "rb")
            Part.objects.create(name=name,image=File(f, name=image), cost=cost, status=status, leadtime=leadtime)
        else:
            self.stdout.write("Image for " + name + " already exists.")