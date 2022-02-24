from django.db import models

from tech.models.job import Job
from tech.models.technician import Technician


class JobTimes(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    rate = models.FloatField()