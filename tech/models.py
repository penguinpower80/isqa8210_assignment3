import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

class UserTypes(models.TextChoices):
    CUSTOMER = 'C', _('Customer')
    TECHNICIAN = 'T', _('Technician')
    STAFF = 'S', _('Staff')

class User(AbstractUser):
    phone = models.CharField(max_length=25)
    street1 = models.CharField(max_length=80)
    street2 = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=15)
    comments = models.TextField(blank=True, null=True)
    type = models.TextField(max_length=10,choices=UserTypes.choices, default='T')
    email = models.EmailField(_('Email Address'), blank=False)
    first_name = models.CharField('First Name', blank=False, max_length=25)
    last_name = models.CharField(_('Last Name'), blank=False, max_length=25)

    def is_customer(self):
        return User.type == UserTypes.CUSTOMER

    def is_tech(self):
        return User.type == UserTypes.TECHNICIAN


class JobStatus(models.TextChoices):
    NEW = 'N', _('New')
    OPEN = 'O', _('Open')
    CANCEL = 'X', _('Cancelled')
    HOLD = 'H', _('Hold')
    WAITING = 'W', _('Waiting')
    COMPLETE = 'C', _('Complete')


class PartStatus(models.TextChoices):
    WAREHOUSE = 'W', _('At the warehouse')
    UNAVAILABLE = 'U', _('Not Available')
    DISCONTINUED = 'D', _('Discontinued')
    ORDER = 'O', _('Order')


class JobLevel(models.TextChoices):
    LOW = 'L', _('Low Urgency')
    NORMAL = 'N', _('Normal Urgency')
    CRITICAL = 'C', _('Critical Urgency')


class PartLocation(models.TextChoices):
    PENDING = 'P', _('Pending')
    DISPATCHED = 'D', _('Dispatched')
    TECHNICIAN = 'T', _('With the Technician')
    ORDERED = 'O', _('Ordered')
    INSTALLED = 'I', _('Installed')
    CANCELED = 'C', _('Cancelled')

class Skill(models.Model):
    name = models.CharField(max_length=100)

class PayRate(models.Model):
    level = models.CharField(max_length=25)
    payrate = models.FloatField()

    def fmtpayrate(self):
        logging.warning(self)
        return "${:,.2f}".format(self.payrate)
    fmtpayrate.short_description = "Payrate"

    def __str__(self):
        return '{}'.format(self.level)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if User.is_tech():
            Technician.objects.create(user=instance)

class WorkingDay(models.Model):
    day = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return self.day


class Technician(models.Model):
    days = models.ManyToManyField(WorkingDay, verbose_name = "Working Days")
    level = models.ForeignKey(PayRate, on_delete=models.CASCADE, verbose_name = "Experience Level")
    skills = models.ManyToManyField(Skill, verbose_name="Technician Skills")
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Related System User")
    def __str__(self):
        if self.user.first_name:
            return '{}'.format(self.user.get_full_name())
        else:
            return self.user.username


class Job(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobcustomer')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='jobtechnician')
    status = models.CharField(
        max_length=1,
        choices=JobStatus.choices,
        default=JobStatus.NEW
    )
    level = models.CharField(
        max_length=1,
        choices=JobLevel.choices,
        default=JobLevel.NORMAL
    )
    requestor = models.CharField(max_length=80)
    street1 = models.CharField(max_length=80)
    street2 = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=15)
    description = models.TextField()
    customer_comment = models.TextField(blank=True, null=True)
    dispatch_comment = models.TextField(blank=True, null=True)
    appointment = models.DateTimeField(),


class TechHistory(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned = models.DateTimeField(),
    comment = models.TextField(blank=True, null=True)


class JobTimes(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    rate = models.FloatField()


class ClientSchedule(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    time = models.TimeField()


class Part(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    cost = models.FloatField()
    status = models.CharField(
        max_length=1,
        choices=PartStatus.choices,
        default=PartStatus.WAREHOUSE
    )
    leadtime = models.SmallIntegerField()


class PartCategory(models.Model):
    name = models.CharField(max_length=100)


class JobPart(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    cost = models.FloatField()
    status = models.CharField(
        max_length=1,
        choices=PartLocation.choices,
        default=PartLocation.PENDING
    )
    eta = models.CharField(max_length=100)



