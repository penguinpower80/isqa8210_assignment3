from django.db import models

from tech.models import Technician, Job, Part
from tech.models.choices import PartLocation


class JobPart(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=PartLocation.choices,
        default=PartLocation.PENDING
    )

    def has_module_permission(self, request):
        return False

    def __str__(self):
        return self.part.name + ", for Job #" + str(self.job.id)