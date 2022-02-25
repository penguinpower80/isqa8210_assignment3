import calendar
import logging

from django.core.exceptions import ValidationError
from django.db import models

from tech.helpers.helpers import getDateTimeFormat
from tech.models.choices import JobStatus, JobLevel
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

    def clean(self):
        if self.appointment and self.technician:
            dow = calendar.day_name[ self.appointment.weekday()]
            hasDay = self.technician.days.filter(day = dow).count() > 0
            if not hasDay:
                raise ValidationError("Tech doesn't work this day!")

    def fmtAppt(self):
        if self.appointment:
            return self.appointment.strftime(getDateTimeFormat())
        else:
            return ''

    def __str__(self):
        return "Job " + str(self.id)
