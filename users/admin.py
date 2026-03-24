from django.contrib.auth import admin
from users.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
