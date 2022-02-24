import logging

from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.core.exceptions import ValidationError
# Register your models here.
from django.utils.safestring import SafeString

from tech.models import User, PayRate, Technician

class UserAdmin(BaseUserAdmin):

    def utype(self, obj):
        if obj.is_tech():
            return SafeString('<a href="../technician/{}/change/">Tech</a>'.format(obj.id) )
        if obj.is_customer():
            return 'Customer'
        return '-'

    list_display = ("username", "email", "first_name", "last_name", "utype",)
    fieldsets = (
        (None, {
            'fields':('username','password', 'is_active','type')
        }),
        ('Personal Info', {
            'classes': ('collapse',),
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone'
            )
        }),
        ('Address', {
           'classes': ('collapse',),
           'fields': (
               'street1','street2', 'city', 'state', 'zip',
           )
        }),
        ('comment', {
            'classes': ('collapse',),
            'fields': (
                'comments',
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('last_login',),
        }),
    )

    add_fieldsets = fieldsets





admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class PayrateAdmin(admin.ModelAdmin):
    list_display = ("level", "fmtpayrate")

admin.site.register(PayRate, PayrateAdmin)

class TechnicianAdmin(admin.ModelAdmin):
    pass
admin.site.register(Technician, TechnicianAdmin)


def tech_get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    ordering = {
        "Users": 1,
        "Technicians": 2,
        "Pay rates": 3
    }
    app_dict = self._build_app_dict(request)
    # a.sort(key=lambda x: b.index(x[0]))
    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list

admin.AdminSite.get_app_list = tech_get_app_list
