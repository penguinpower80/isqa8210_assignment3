from django.db import models

from tech.models.job import Job


class ClientSchedule(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    time = models.TimeField()