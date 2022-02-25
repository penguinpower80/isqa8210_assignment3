from django.db import models


class PayRate(models.Model):
    level = models.CharField(max_length=25)
    payrate = models.FloatField()

    def fmtpayrate(self):
        return "${:,.2f}".format(self.payrate)
    fmtpayrate.short_description = "Payrate"

    def __str__(self):
        return '{}'.format(self.level)

    class Meta:
        verbose_name = "Pay Rate"
        verbose_name_plural = "Pay Rates"
