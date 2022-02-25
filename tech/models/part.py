from django.db import models

from tech.models.choices import PartStatus


class Part(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    cost = models.FloatField("Cost $")
    status = models.CharField(
        max_length=1,
        choices=PartStatus.choices,
        default=PartStatus.UNKNOWN
    )
    leadtime = models.SmallIntegerField("Lead Time (In days)", null=True, blank=True)

    def fmtCost(self):
        return "${:.2f}".format(self.cost)

    def __str__(self):
        return "{} ({})".format(self.name, self.get_status_display() )
