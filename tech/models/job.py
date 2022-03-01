import calendar
import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from tech.helpers.helpers import getDateTimeFormat, roundFifteen
from tech.models.choices import JobStatus, JobLevel, PartLocation
from tech.models.technician import Technician
from tech.models.user import User


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
    description = models.TextField(help_text="Describe what the problem is.")
    appointment = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.appointment and self.technician:
            dow = calendar.day_name[self.appointment.weekday()]
            hasDay = self.technician.days.filter(day=dow).count() > 0
            if not hasDay:
                raise ValidationError("Tech doesn't work this day!")

    def fmtAppt(self):
        if self.appointment:
            return self.appointment.strftime(getDateTimeFormat())
        else:
            return ''

    def totalCost(self):
        # Hours cost
        # parts cost
        totalcost = 0
        partscost = self.jobpart_set.filter(status=PartLocation.INSTALLED).aggregate(Sum('cost'))
        if partscost['cost__sum']:
            totalcost += partscost['cost__sum']
        time_per_user = {}
        for t in self.jobtime_set.all():
            if not t.end:
                continue
            diff = t.end - t.start
            if t.technician_id in time_per_user:
                time_per_user[t.technician_id]['seconds'] += diff.seconds
            else:
                time_per_user[t.technician_id] = {}
                time_per_user[t.technician_id]['seconds'] = diff.seconds
                time_per_user[t.technician_id]['tech'] = t.technician

        if len(time_per_user) > 0:
            for t in time_per_user:
                minutes = time_per_user[t]['seconds'] / 60 # minutes
                hours = roundFifteen(minutes) / 60
                totalcost += hours * time_per_user[t]['tech'].level.payrate;
        return totalcost

    def __str__(self):
        return "Job " + str(self.id)
