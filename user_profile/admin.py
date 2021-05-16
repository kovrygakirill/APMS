from django.contrib import admin
from .models import UserProfile
from project.admin import BaseModelAdmin
from project.admin import TaskInstanceInline


class TaskInstanceInlineProxy(TaskInstanceInline):
    fields = ['get_task_link', 'get_start_datetime', 'get_finish_datetime', 'get_total_time', 'type', 'status', ]
    readonly_fields = ['get_task_link', 'get_start_datetime', 'get_finish_datetime', 'get_total_time', 'type', 'status']


class UserProfileAdmin(BaseModelAdmin):
    inlines = [TaskInstanceInlineProxy]
    fields = ('username', 'email', 'first_name', 'last_name')
    list_display = ['username', 'email', 'first_name', 'last_name', 'default_actions']
    list_filter = ['is_superuser', ]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    BaseModelAdmin.default_actions.short_description = 'actions'


admin.site.register(UserProfile, UserProfileAdmin)
