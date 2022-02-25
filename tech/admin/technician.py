import logging

from django.contrib import admin
from django.utils.safestring import SafeString

from tech.models import Technician


class TechnicianAdmin(admin.ModelAdmin):
    def ulink(self, obj):
            return SafeString('<a href="../user/{}/change/">User Account</a>'.format(obj.user.id) )

    ulink.short_description = "Profile"
    def name(self,obj):
        if obj.user.first_name:
            return obj.user.first_name + ' ' + obj.user.last_name
        else:
            return obj.user.username

    def tskills(self,obj):
        return ", ".join( skill.name for skill in obj.skills.all() )

    def tdays(self,obj):
        return ", ".join( day.day for day in obj.days.all() )

    list_display = ("name","ulink", "tskills", "tdays")


admin.site.register(Technician, TechnicianAdmin)