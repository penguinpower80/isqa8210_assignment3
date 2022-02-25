import logging

from django.contrib import admin
from django.db.models import Q
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from tech.helpers.helpers import timeWorked
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

    list_filter = (
        "status",
        "level",
        ("technician", RelatedDropdownFilter),
        ("customer_name", RelatedDropdownFilter),
    )
    search_fields = ("description__icontains",)

    def customer(self):
        return self.customer.get_full_name()

    def appt(self, obj):
        return obj.fmtAppt()

    def parts(self, obj):
        parts = JobPart.objects.filter(job_id=obj.id).filter(
            Q(status=PartLocation.PENDING) | Q(status=PartLocation.ORDERED)).all()
        return str(len(parts))

    def customer_name(self, obj):
        return obj.customer.get_full_name()

    list_filter = (
        "status",
        "level",
        ("technician", RelatedDropdownFilter),
        ("customer", RelatedDropdownFilter),
    )

    parts.short_description = "Pending or Ordered Parts"

    def time(self, obj):
        times = JobTime.objects.filter(job_id=obj.id).all()
        total_seconds = 0
        for time in times:
            total_seconds += time.totalTimeWorked().seconds
        return timeWorked(total_seconds)

    time.short_description = "Total Time Worked"

    list_display = ("customer_name", "status", "level", "appt", "parts", "time")


admin.site.register(Job, JobAdmin)
