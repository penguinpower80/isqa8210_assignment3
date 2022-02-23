import logging

from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
# Register your models here.
from django.utils.safestring import SafeString

from tech.models import User, PayRate, Technician


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    #form = UserChangeForm
    #add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    def type(self, obj):
        if obj.is_tech():
            return SafeString('<a href="../technician/{}/change/">Tech</a>'.format(obj.id) )
        if obj.is_customer():
            return 'Customer'
        return '-'

    list_display = ("username", "email", "first_name", "last_name", "type",)
    fieldsets = (
        (None, {
            'fields':('username','password', 'is_active',)
        }),
        ('Personal Info', {
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
            'fields': ('groups', 'last_login',),
        }),
    )
    #fieldsets = BaseUserAdmin.fieldsets


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)

class PayrateAdmin(admin.ModelAdmin):
    list_display = ("level", "fmtpayrate")

admin.site.register(PayRate, PayrateAdmin)

class TechnicianAdmin(admin.ModelAdmin):
    pass
admin.site.register(Technician, TechnicianAdmin)