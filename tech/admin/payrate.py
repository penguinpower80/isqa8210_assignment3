from django.contrib import admin

from tech.models import PayRate


class PayrateAdmin(admin.ModelAdmin):
    list_display = ("level", "fmtpayrate")


admin.site.register(PayRate, PayrateAdmin)
