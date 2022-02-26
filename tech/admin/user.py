from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import SafeString
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from tech.models import User

class UserAdmin(BaseUserAdmin):

    def utype(self, obj):
        if obj.is_tech():
            return SafeString('<a href="../technician/{}/change/">Tech</a>'.format(obj.id) )
        if obj.is_customer():
            return 'Customer'
        return '-'
    utype.short_description = "USER TYPE"

    list_filter = (
        "is_active",
        "type",

    )


    list_display = ("username", "email", "first_name", "last_name", "utype",)
    fieldsets = [
        [None, { 'fields':('username','password','is_active','type') }],
        ['Personal Info', {
            'classes': ('collapse',),
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone'
            )
        }],
        ['Address', {
           'classes': ('collapse',),
           'fields': (
               'street1','street2', 'city', 'state', 'zip',
           )
        }],
        ('comment', {
            'fields': (
                'comments',
            )
        }),
        ['Advanced options', {
            'classes': ('collapse',),
            'fields': ('last_login','is_superuser', 'is_staff',),
        }]
    ]
    add_fieldsets = [
        [None, { 'fields':('username','password1', 'password2','is_active','type') }],
        ['Personal Info', {
            'classes': ('collapse',),
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone'
            )
        }],
        ['Address', {
           'classes': ('collapse',),
           'fields': (
               'street1','street2', 'city', 'state', 'zip',
           )
        }],
        ('comment', {
            'classes': ('collapse',),
            'fields': (
                'comments',
            )
        }),
        ['Advanced options', {
            'classes': ('collapse',),
            'fields': ('last_login','is_superuser', 'is_staff',),
        }]
    ]

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
