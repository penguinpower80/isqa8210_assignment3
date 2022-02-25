import logging

from django.contrib import admin
from django.db.models import Q

from tech.models import Job, JobPart, JobTime, PartLocation


class JobPartInline(admin.TabularInline):
    model = JobPart
    extra = 1

class JobTimeInline(admin.StackedInline):
    model = JobTime
    extra = 1

class JobAdmin(admin.ModelAdmin):
    inlines = [
        JobTimeInline,
        JobPartInline,
    ]

    def customer(self):
        return self.customer.get_full_name()

    def appt(self, obj):
        return obj.fmtAppt()

    def parts(self, obj):
        parts = JobPart.objects.filter(job_id = obj.id).filter( Q(status=PartLocation.PENDING) | Q(status=PartLocation.ORDERED)).all()
        return str( len(parts) )


    parts.short_description="Pending or Ordered Parts"

    list_display = ("customer", "status", "level", "appt", "parts")


admin.site.register(Job, JobAdmin)

