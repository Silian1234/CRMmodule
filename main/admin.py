# crm/admin.py
from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AlreadyRegistered

from .models import Event, CustomUser
from .admin_forms import EventAdminForm

# Кастомный класс админки для CustomUser
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

# Кастомный класс админки для Event
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm  # Используем кастомную форму для фильтрации пользователей по группам
    list_display = ('name', 'type', 'start_date', 'end_date', 'leader', 'curator')  # Отображаем нужные поля
    list_filter = ('type', 'start_date', 'end_date')

# Регистрируем модели с кастомными классами
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event, EventAdmin)

# Автоматическая регистрация всех остальных моделей
app = apps.get_app_config('main')  # Замените 'crm' на имя вашего приложения

for model_name, model in app.models.items():
    try:
        if model not in admin.site._registry:  # Проверяем, зарегистрирована ли модель
            admin.site.register(model)
    except AlreadyRegistered:
        pass
