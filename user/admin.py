from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UsersAdmin(UserAdmin):
    # 1. Показываем карту прямо в общем списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'rfid_card')

    # 2. Добавляем поиск по номеру карты
    search_fields = ('username', 'email', 'first_name', 'last_name', 'rfid_card')

    # 3. Добавляем кастомное поле в форму РЕДАКТИРОВАНИЯ пользователя
    fieldsets = UserAdmin.fieldsets + (
        ('RFID-карта', {'fields': ('rfid_card',)}),
    )

    # 4. Добавляем кастомное поле в форму СОЗДАНИЯ пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('RFID-карта', {'fields': ('rfid_card',)}),
    )