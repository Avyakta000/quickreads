from django.contrib import admin
from .models import User, ApplicationAPIKey
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)

@admin.register(ApplicationAPIKey)
class ApplicationAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = ('name', 'client_name', 'client_type', 'is_active', 'is_unlimited', 'usage_count', 'usage_limit')
    search_fields = ('name', 'client_name', 'application')
    list_filter = ('client_type', 'is_active', 'is_unlimited', 'created_at')

admin.site.unregister(APIKey)
