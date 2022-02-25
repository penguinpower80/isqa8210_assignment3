from django.contrib import admin

from tech.models import Part


class PartAdmin(admin.ModelAdmin):
    def fmtCost(self, obj):
        return obj.fmtCost()

    fmtCost.short_description="Cost"
    list_display = ("name", "fmtCost", "status",)


admin.site.register(Part, PartAdmin)
