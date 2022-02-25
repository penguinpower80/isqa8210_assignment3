import logging

from django.db import models

from tech.helpers.helpers import timeWorked
from tech.models.job import Job
from tech.models.technician import Technician


class JobTime(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def totalTimeWorked(self):
        return self.end - self.start

    def __str__(self):
        total_diff = self.totalTimeWorked()
        return timeWorked(total_diff.seconds)