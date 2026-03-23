from django.contrib.auth import admin
from user.models import Users


@admin.register(Users)
class UsersAdmin(admin.modelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
