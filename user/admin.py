from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UsersAdmin(UserAdmin):
    # Переопределяем list_display для отображения полей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Используем стандартные наборы полей UserAdmin,
    # так как ваша модель наследуется от AbstractUser
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets