from django.contrib import admin
from .models import UserProfile
from project.admin import BaseModelAdmin
from project.admin import TaskInstanceInline


class UserProfileAdmin(BaseModelAdmin):
    inlines = [TaskInstanceInline]
    fields = ('username', 'email', 'first_name', 'last_name')
    list_display = ['username', 'email', 'first_name', 'last_name', 'default_actions']
    list_filter = ['is_superuser', ]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    BaseModelAdmin.default_actions.short_description = 'actions'


admin.site.register(UserProfile, UserProfileAdmin)
