from django.contrib import admin
from users.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('email', 'phone', 'telegram_id', 'avatar', "is_active",)