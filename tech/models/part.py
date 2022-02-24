from django.db import models

from tech.models.choices import PartStatus


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