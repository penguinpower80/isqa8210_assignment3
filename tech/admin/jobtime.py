from django.contrib import admin

from tech.models import JobTime


class JobTimeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
    #list_display = ("name", "fmtCost", "status",)

admin.site.register(JobTime, JobTimeAdmin)