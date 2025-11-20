from django.contrib import admin
from .models import UserStyleProfile

# Register your models here.

@admin.register(UserStyleProfile)
class UserStyleProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skin_tone', 'body_type', 'gender', 'created_at']
    list_filter = ['skin_tone', 'body_type', 'gender', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
