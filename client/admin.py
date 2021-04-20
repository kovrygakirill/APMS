from django.contrib import admin
from client.models import Client
from django.utils.html import format_html
from django.urls import reverse
from project.models import Project


class BaseModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(BaseModelAdmin, self).get_queryset(request)
        self.request = request
        return qs

    @staticmethod
    def dict_default_permissions(app_label, model_name):
        return {
            'view': f'{app_label}.view_{model_name}',
            'delete': f'{app_label}.delete_{model_name}',
            'create': f'{app_label}.create_{model_name}',
            'change': f'{app_label}.change_{model_name}'
        }

    @staticmethod
    def dict_default_actions(app_label, model_name):
        return {
            'view': f'admin:{app_label}_{model_name}_view',
            'delete': f'admin:{app_label}_{model_name}_delete',
            'create': f'admin:{app_label}_{model_name}_create',
            'change': f'admin:{app_label}_{model_name}_change',
        }

    def get_user_permissions(self):
        return self.request.user.get_all_permissions()

    def get_app_label_obj(self, obj):
        return obj._meta.app_label

    def get_model_name_obj(self, obj):
        return obj._meta.model_name

    def get_html_action(self, obj, action=''):
        default_permissions = self.dict_default_permissions(self.get_app_label_obj(obj), self.get_model_name_obj(obj))
        default_actions = self.dict_default_actions(self.get_app_label_obj(obj), self.get_model_name_obj(obj))

        if default_permissions[action] in self.get_user_permissions():
            result = format_html('<a href="{}" style="text-decoration: underline">{}</a>',
                                 reverse(default_actions[action], args=[obj.pk]),
                                 action.title(),
                                 )
        else:
            result = format_html('-')

        return result


class ProjectInstanceInline(admin.TabularInline):
    model = Project
    extra = 0
    readonly_fields = ['client', 'title', 'description', 'start_date', 'release_date', 'status']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ClientAdmin(BaseModelAdmin):
    fields = ['title', 'description', 'get_projects']
    inlines = [ProjectInstanceInline]
    readonly_fields = ('get_projects',)
    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'description', 'get_projects')
    #     }),
    # )
    search_fields = ['title']
    ordering = ['title', ]
    list_display = ['related_title', 'description', 'get_projects', 'default_actions']
    list_filter = ('title',)

    # exclude = ('get_projects', )

    def related_title(self, obj):
        return obj.title

    related_title.short_description = 'сompany'

    def get_projects(self, obj):
        app_label = self.get_app_label_obj(obj.project.model)
        model_name = self.get_model_name_obj(obj.project.model)
        view_name = f'admin:{app_label}_{model_name}_change'

        user_permissions = self.get_user_permissions()
        default_permissions = self.dict_default_permissions(app_label, model_name)

        result = []
        if default_permissions['change'] or default_permissions['view'] in user_permissions:
            for project in obj.project.all():
                link_url = reverse(view_name, args=[project.pk])
                result.append('<a href="{}">{}</a>'.format(link_url, project.title))
        else:
            for project in obj.project.all():
                result.append('{}'.format(project.title))

        return format_html("<br / >".join(result))

    get_projects.short_description = 'proects'

    def default_actions(self, obj):
        html_delete_action = self.get_html_action(obj, action='delete')
        html_change_action = self.get_html_action(obj, action='change')

        return format_html('{} &nbsp; {}', html_delete_action, html_change_action)

    default_actions.short_description = 'actions'


admin.site.register(Client, ClientAdmin)
