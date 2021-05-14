from django.contrib import admin

from payment.models import Payment
from project.models import Project, Task, CommentTask
from payment.admin import BasePaymentAdmin
from client.admin import BaseModelAdmin
from rangefilter.filters import DateRangeFilter
from admin_numeric_filter.admin import RangeNumericFilter
from client.admin import BaseTabularInlineAdmin


from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class TaskAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Task
        fields = '__all__'


class CommentTaskAdminForm(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = CommentTask
        fields = '__all__'


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


class TaskInstanceInline(BaseTabularInlineAdmin, BaseTaskAdmin):
    model = Task
    extra = 0

    fields = ['get_task_link', 'get_user_link', 'get_start_datetime', 'get_finish_datetime', 'get_total_time', 'type', 'status', ]
    readonly_fields = ['get_task_link', 'get_user_link', 'get_start_datetime', 'get_finish_datetime', 'get_total_time',
                       'type', 'status', ]
    ordering = ['start_datetime', 'release_datetime']

    def get_task_link(self, obj):
        return self.get_link_to_obj(obj)

    get_task_link.short_description = 'Name'


    def get_user_link(self, obj):
        return self.get_link_to_obj(obj.user)

    get_user_link.short_description = 'Appointed by'


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentInstanceInline(BaseTabularInlineAdmin, BasePaymentAdmin):
    model = Payment
    extra = 0
    fields = ['get_payment_link', 'get_price_in_dollar', 'project']
    readonly_fields = ['get_payment_link', 'get_price_in_dollar', 'project']

    def get_payment_link(self, obj):
        return self.get_link_to_obj(obj)

    get_payment_link.short_description = 'Comment'

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


class BaseCommentAdmin:
    def get_comment(self, obj):
        comm = obj.comment[0:30]
        return comm + " ..." if len(comm) == 30 else comm

    get_comment.short_description = 'comment'

    def get_time(self, obj):
        return f'{obj.time} {"hour" if obj.time in [0, 1] else "hours"}'

    get_time.short_description = 'time complete'


class CommentTaskAdmin(BaseModelAdmin, BaseCommentAdmin):
    form = CommentTaskAdminForm
    fields = ['task', 'comment', 'user', 'status', 'time']
    search_fields = ['comment']
    ordering = ['time']
    list_display = ['get_comment', 'get_task', 'get_user', 'status', 'get_time', 'default_actions']

    list_filter = ('task', 'user', ('time', RangeNumericFilter), 'status')

    def get_user(self, obj):
        return self.get_link_to_obj(obj.user)

    get_user.short_description = 'appointed by'

    def get_task(self, obj):
        return self.get_link_to_obj(obj.task)

    get_task.short_description = 'Task'


class CommentTaskInstanceInline(BaseTabularInlineAdmin, BaseCommentAdmin):
    form = CommentTaskAdminForm
    model = CommentTask
    extra = 1

    fields = ['task', 'comment', 'user', 'status', 'time']
    show_change_link = True

    # readonly_fields = ['task', 'comment', 'user', 'status', 'time']
    # list_filter = ('title', 'status')

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class TaskAdmin(BaseModelAdmin, BaseTaskAdmin):
    form = TaskAdminForm
    fields = ['title', 'project', 'user', 'description', ('start_datetime', 'release_datetime'), 'total_time',
              'type', 'status', ]
    inlines = [CommentTaskInstanceInline, ]
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
admin.site.register(CommentTask, CommentTaskAdmin)
