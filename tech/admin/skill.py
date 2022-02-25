from django.contrib import admin

from tech.models import Skill


class SkillAdmin(admin.ModelAdmin):
    pass
    # list_display = ("name", "fmtCost", "status",)


admin.site.register(Skill, SkillAdmin)
