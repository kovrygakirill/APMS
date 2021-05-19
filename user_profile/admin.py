from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html

from .models import UserProfile
from project.admin import BaseModelAdmin
from project.admin import TaskInstanceInline


class TaskInstanceInlineProxy(TaskInstanceInline):
    fields = ['get_task_link', 'get_start_datetime', 'get_finish_datetime', 'get_total_time', 'type', 'status', ]
    readonly_fields = ['get_task_link', 'get_start_datetime', 'get_finish_datetime', 'get_total_time', 'type', 'status']


class UserProfileAdmin(BaseModelAdmin):
    inlines = [TaskInstanceInlineProxy]
    readonly_fields = ['get_interweaving_of_tasks', ]
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('INTERWEAVING OF TASKS', {
            # 'classes': ('collapse',),
            'fields': ('get_interweaving_of_tasks',),
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'default_actions']
    list_filter = ['is_superuser', ]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_interweaving_of_tasks(self, obj):
        tasks_of_user = obj.task.all().order_by("start_datetime")

        interweaving_task = []

        for i in range(len(tasks_of_user) - 1):
            start_task_time = datetime.timestamp(tasks_of_user[i].start_datetime)
            finish_task_time = datetime.timestamp(tasks_of_user[i].release_datetime)
            start_next_task_time = datetime.timestamp(tasks_of_user[i + 1].start_datetime)
            finish_next_task_time = datetime.timestamp(tasks_of_user[i + 1].release_datetime)

            if finish_next_task_time > start_task_time > start_next_task_time or \
                    start_task_time < start_next_task_time < finish_task_time:

                if tasks_of_user[i] and tasks_of_user[i + 1] not in interweaving_task:
                    interweaving_task.append(tasks_of_user[i])
                    interweaving_task.append(tasks_of_user[i + 1])
                    break

        return format_html((" and/or ".join([f'<u>{self.get_link_to_obj(task)}</u>' for task in interweaving_task])))

    get_interweaving_of_tasks.short_description = 'We recommend to change the time of tasks'

    BaseModelAdmin.default_actions.short_description = 'actions'


admin.site.register(UserProfile, UserProfileAdmin)
