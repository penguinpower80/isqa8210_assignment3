from django.db import models

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
