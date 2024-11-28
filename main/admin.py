# crm/admin.py
from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AlreadyRegistered

from .models import *
from .admin_forms import EventAdminForm


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация',
         {'fields': ('firstName', 'lastName', 'fatherName', 'email', 'stack', 'portfolio', 'contacts', 'picture')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'firstName', 'lastName', 'fatherName', 'email', 'stack', 'portfolio',
            'contacts', 'picture', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'start_date', 'end_date', 'leader', 'curator', 'participant_count')
    list_filter = ('type', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    filter_horizontal = ('participants',)

    def participant_count(self, obj):
        return obj.participants.count()

    participant_count.short_description = "Количество участников"


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event, EventAdmin)

app = apps.get_app_config('main')

for model_name, model in app.models.items():
    try:
        if model not in admin.site._registry:
            admin.site.register(model)
    except AlreadyRegistered:
        pass
