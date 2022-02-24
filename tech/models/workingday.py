from django.db import models

class WorkingDay(models.Model):
    day = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return self.day
