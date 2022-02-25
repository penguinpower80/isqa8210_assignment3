from django.contrib import admin

from tech.models import JobTime, JobPart


class JobPartAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
    #list_display = ("name", "fmtCost", "status",)

admin.site.register(JobPart, JobPartAdmin)