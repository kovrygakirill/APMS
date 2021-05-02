from django.contrib import admin

from payment.models import Payment
from project.models import Project, Task, CommentTask
from payment.admin import BasePaymentAdmin
from client.admin import BaseModelAdmin
from rangefilter.filters import DateRangeFilter
from admin_numeric_filter.admin import RangeNumericFilter


class BaseTaskAdmin:
    def get_total_time(self, obj):
        return f'{obj.total_time} {"hour" if obj.total_time in [0, 1] else "hours"}'

    get_total_time.short_description = 'total time complete'

    def get_start_datetime(self, obj):
        return self.parse_datetime(obj.start_datetime)

    get_start_datetime.short_description = 'start'

    def get_finish_datetime(self, obj):
        return self.parse_datetime(obj.release_datetime)

    get_finish_datetime.short_description = 'planned finish'

    @staticmethod
    def parse_datetime(date_time):
        return date_time.strftime("%Y-%m-%d %H:%M")



class TaskInstanceInline(admin.TabularInline, BaseTaskAdmin):
    model = Task
    extra = 0

    fields = ['title', 'user', 'get_start_datetime', 'get_finish_datetime', 'get_total_time', 'type', 'status', ]
    readonly_fields = ['title', 'user', 'get_start_datetime', 'get_finish_datetime', 'get_total_time',
                       'type', 'status', ]
    list_filter = ('title', 'status')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentInstanceInline(admin.TabularInline, BasePaymentAdmin):
    model = Payment
    extra = 0
    fields = ['comment', 'get_price_in_dollar', 'project']
    readonly_fields = ['comment', 'get_price_in_dollar', 'project']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectAdmin(BaseModelAdmin):
    readonly_fields = ('get_total_time_develop_in_hours', 'get_budget')
    inlines = [TaskInstanceInline, PaymentInstanceInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'client', 'description', ('start_date', 'release_date'), 'status',)
        }),
        ('GENERAL INFO', {
            # 'classes': ('collapse',),
            'fields': ('get_total_time_develop_in_hours', 'get_budget',),
        }),
    )
    search_fields = ['title']
    ordering = ['title']
    list_display = ['get_project', 'get_client', 'start_date', 'get_finish_date', 'status',
                    'default_actions']
    list_filter = ('client', ('start_date', DateRangeFilter), ('release_date', DateRangeFilter), 'status')

    def get_project(self, obj):
        return obj.title

    get_project.short_description = 'project'

    def get_client(self, obj):
        return self.get_link_to_obj(obj.client)

    get_client.short_description = 'client'

    def get_total_time_develop_in_hours(self, obj):
        a = obj.task.all()
        sum_hours = sum([i.total_time for i in a])
        return f'{sum_hours} {"hour" if sum_hours in [0, 1] else "hours"}'

    get_total_time_develop_in_hours.short_description = 'total development time'

    def get_finish_date(self, obj):
        return obj.release_date

    get_finish_date.short_description = 'planned finish'

    def get_budget(self, obj):
        total_budget = 0
        for payment in obj.payment.all():
            total_budget += payment.price

        return f'{total_budget} $'

    get_budget.short_description = 'total budget'

    BaseModelAdmin.default_actions.short_description = 'actions'


class TaskAdmin(BaseModelAdmin, BaseTaskAdmin):
    fields = ['title', 'project', 'user', 'description', ('start_datetime', 'release_datetime'), 'total_time',
              'type', 'status', ]
    search_fields = ['title']
    ordering = ['title']
    list_display = ['title', 'get_project', 'get_user', 'get_start_datetime', 'get_finish_datetime', 'get_total_time',
                    'type', 'status', 'default_actions']
    list_filter = ('project', 'user', ('total_time', RangeNumericFilter),
                   ('start_datetime', DateRangeFilter), ('release_datetime', DateRangeFilter), 'type', 'status')

    def get_project(self, obj):
        return self.get_link_to_obj(obj.project)

    get_project.short_description = 'project'

    def get_user(self, obj):
        return self.get_link_to_obj(obj.user)

    get_user.short_description = 'appointed by'

    BaseModelAdmin.default_actions.short_description = 'actions'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(CommentTask)
