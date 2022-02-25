import datetime
import logging
import random

import pytz
from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Q
from django_seed import Seed

import tech.models
from tech.models import UserTypes, PayRate, Technician, WorkingDay, Skill, Job, JobStatus, JobLevel


class Command(BaseCommand):
    help = "Seed database using Django Seed for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Seeding Tech Tracking Data data...')

        seeder = Seed.seeder()
        userModel = tech.models.User
        # add some techs
        tech_user_count = int(input('How many techs to add [0]?') or "0")
        self.stdout.write("Adding {} customers".format(tech_user_count))

        if tech_user_count > 0:
            for x in range(0, tech_user_count):
                fname = seeder.faker.unique.first_name()
                lname = seeder.faker.unique.last_name()
                username = fname[0].lower() + lname.lower()
                email = username + "@techtrack.org"
                seeder.add_entity(userModel, 1, {
                    'username': username,
                    'password': seeder.faker.password(length=15),
                    'first_name': fname,
                    'last_name': lname,
                    'is_staff': 0,
                    'is_superuser': 0,
                    'type': UserTypes.TECHNICIAN,
                    'last_login': None,
                    'street1': seeder.faker.street_address(),
                    'street2': None,
                    'zip': seeder.faker.postcode(),
                    'email': email
                })

            seed_idx = seeder.execute()


            skills = list( Skill.objects.all() )
            weekdays = WorkingDay.objects.filter(~Q(day="Saturday") & ~Q(day="Sunday")).all()

            for idx, id in enumerate(seed_idx[userModel]):
                this_tech = Technician(id)
                this_tech.user = userModel(id)
                self.stdout.write("Setting user to {} level".format(this_tech.user.id))
                level = PayRate.objects.all().order_by('?')[:1].get()
                this_tech.level = level
                self.stdout.write("Setting standard work week")
                for d in weekdays:
                    this_tech.days.add(d)

                number_of_skills = random.randint(0, len(skills) - 1)
                if number_of_skills > 0:
                    my_skills = random.sample( skills, number_of_skills)
                    self.stdout.write("Adding {} skills".format(number_of_skills))

                    for d in my_skills:
                        this_tech.skills.add(d)

                this_tech.save()


        # add some customers
        customer_user_count = int(input('How many customers to add [1]?') or "1")
        self.stdout.write("Adding {} customers".format(customer_user_count))

        if customer_user_count > 0:
            for x in range(0, customer_user_count):
                fname = seeder.faker.unique.first_name()
                lname = seeder.faker.unique.last_name()
                username = fname[0].lower() + lname.lower()
                email = username + "@techtrack.org"
                seeder.add_entity(userModel, 1, {
                    'username': username,
                    'password': seeder.faker.password(length=15),
                    'first_name': fname,
                    'last_name': lname,
                    'is_staff': 0,
                    'is_superuser': 0,
                    'type': UserTypes.CUSTOMER,
                    'last_login': None,
                    'street1': seeder.faker.street_address(),
                    'street2': None,
                    'zip': seeder.faker.postcode(),
                    'email': email
                })

            seed_idx = seeder.execute()
            tz = pytz.timezone(settings.TIME_ZONE)
            for idx, id in enumerate(seed_idx[userModel]):
                this_user = userModel(id)
                this_tech = Technician.objects.order_by('?')[:1].get()
                job = Job()
                job.customer = this_user
                job.technician = this_tech
                job.status = random.choice( random.choice(list(JobStatus)) )
                job.level = random.choice( random.choice(list(JobLevel)) )
                job.description = seeder.faker.paragraph()
                job.appointment = seeder.faker.future_datetime(tzinfo=tz)
                job.save()

