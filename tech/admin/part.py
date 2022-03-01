from django.contrib import admin
from django.utils.safestring import SafeString

from tech.models import Part


class PartAdmin(admin.ModelAdmin):
    def fmtCost(self, obj):
        return obj.fmtCost()

    fmtCost.short_description="Cost"

    def picture(self, obj):
        return SafeString("<div style='background-image: url({});width: 100px;height: 100px;background-position: center center;background-size: cover;background-repeat: no-repeat;border-radius: 50%;'></div>".format( obj.image.url if obj.image else ''))

    list_display = ("picture","name", "fmtCost", "status",)
    list_display_links = ("picture", "name",)


admin.site.register(Part, PartAdmin)
