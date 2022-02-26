from django.contrib import admin
from django.utils.safestring import SafeString

from tech.models import Part


class PartAdmin(admin.ModelAdmin):
    def fmtCost(self, obj):
        return obj.fmtCost()

    fmtCost.short_description="Cost"

    def picture(self, obj):
        return SafeString("<img src='{}' height='100px' />".format( obj.image.url))

    list_display = ("picture","name", "fmtCost", "status",)
    list_display_links = ("picture", "name",)


admin.site.register(Part, PartAdmin)
