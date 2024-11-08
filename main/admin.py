from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('firstName', 'lastName', 'fatherName', 'stack', 'portfolio', 'contacts', 'role', 'picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('firstName', 'lastName', 'fatherName', 'stack', 'portfolio', 'contacts', 'role', 'picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
