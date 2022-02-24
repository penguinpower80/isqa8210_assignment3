from django.db import models

from tech.models import Technician, Job, Part
from tech.models.choices import PartLocation


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
