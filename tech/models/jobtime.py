from django.db import models

from tech.models.job import Job
from tech.models.technician import Technician


class JobTime(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        total_diff = self.end - self.start
        days = total_diff.days
        hours, leftover = divmod(days.seconds, 3600)
        minutes, seconds = divmod(leftover, 60)
        time_string = []
        if days > 0:
            time_string.append( days + ' day(s)')
        if hours > 0:
            time_string.append( hours + ' hour(s)')
        if minutes > 0:
            time_string.append( minutes + ' minute(s)')

        return ", " . join(time_string)