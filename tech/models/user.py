from django.contrib.auth.models import AbstractUser
from django.db import models

from tech.models import UserTypes


class User(AbstractUser):
    phone = models.CharField(max_length=25)
    street1 = models.CharField(max_length=80)
    street2 = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=15)
    comments = models.TextField(blank=True, null=True)
    type = models.TextField(max_length=10,choices=UserTypes.choices, default='T')
    email = models.EmailField('Email Address', blank=False)
    first_name = models.CharField('First Name', blank=False, max_length=25)
    last_name = models.CharField('Last Name', blank=False, max_length=25)

    def is_customer(self):
        return self.type == UserTypes.CUSTOMER

    def is_tech(self):
        return self.type == UserTypes.TECHNICIAN

