from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

from tech.models.payrate import PayRate
from tech.models.skill import Skill
from tech.models.user import User
from tech.models.workingday import WorkingDay


class Technician(models.Model):
    days = models.ManyToManyField(WorkingDay, verbose_name = "Working Days", blank=True)
    level = models.ForeignKey(PayRate, on_delete=models.CASCADE, verbose_name = "Experience Level",  null=True)
    skills = models.ManyToManyField(Skill, verbose_name="Technician Skills", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Related System User")

    class Meta:
        verbose_name = "Extra Tech Info"
        verbose_name_plural = "Extra Tech Info"

    def __str__(self):
        if self.user.first_name:
            return '{}'.format(self.user.get_full_name())
        else:
            return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_tech():
            Technician.objects.create(user=instance)