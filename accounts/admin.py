from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet

from accounts.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("id", "username", "notify", "first_name", "last_name", 'is_active')
