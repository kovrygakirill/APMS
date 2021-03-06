from django.contrib import admin
from django.shortcuts import redirect

from client.models import Client
from django.utils.html import format_html
from django.urls import reverse
from project.models import Project

from django.forms import TextInput, Textarea
from django.db import models
from abc import *


class BaseAdminClass:

    @abstractmethod
    def get_queryset(self, request):
        raise NotImplementedError()

    @staticmethod
    def dict_default_permissions(app_label, model_name):
        return {
            'view': f'{app_label}.view_{model_name}',
            'delete': f'{app_label}.delete_{model_name}',
            'add': f'{app_label}.add_{model_name}',
            'change': f'{app_label}.change_{model_name}'
        }

    @staticmethod
    def dict_default_actions(app_label, model_name):
        return {
            'view': f'admin:{app_label}_{model_name}_view',
            'delete': f'admin:{app_label}_{model_name}_delete',
            'add': f'admin:{app_label}_{model_name}_add',
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

    def default_actions(self, obj):
        html_delete_action = self.get_html_action(obj, action='delete')
        html_change_action = self.get_html_action(obj, action='change')

        return format_html('{} &nbsp; {}', html_delete_action, html_change_action)

    def get_link_to_obj(self, obj):
        app_label = self.get_app_label_obj(obj)
        model_name = self.get_model_name_obj(obj)
        view_name = f'admin:{app_label}_{model_name}_change'

        user_permissions = self.get_user_permissions()
        default_permissions = self.dict_default_permissions(app_label, model_name)

        result = []
        if default_permissions['change'] or default_permissions['view'] in user_permissions:
            link_url = reverse(view_name, args=[obj.pk])
            result.append('<a href="{}">{}</a>'.format(link_url, obj))
        else:
            result.append('{}'.format(obj))

        return format_html("<br / >".join(result))


class BaseModelAdmin(admin.ModelAdmin, BaseAdminClass):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 55})},
    }

    # def response_change(self, request, obj):
    #     msg_dict = {
    #         'name': obj._meta.verbose_name,
    #         'obj': str(obj),
    #     }
    #
    #     if "_saveasnew" in request.POST:
    #         msg = format_html(
    #             ('The {name} ???{obj}??? was added successfully. You may edit it again below.'),
    #             **msg_dict
    #         )
    #     elif "_addanother" in request.POST:
    #         msg = format_html(
    #             ('The {name} ???{obj}??? was changed successfully. You may add another {name} below.'),
    #             **msg_dict
    #         )
    #     else:
    #         msg = format_html(
    #             ('The {name} ???{obj}??? was changed successfully.'),
    #             **msg_dict
    #         )
    #
    #     self.message_user(request, msg, 25)
    #
    #     return redirect(request.path)

    def get_queryset(self, request):
        qs = super(BaseModelAdmin, self).get_queryset(request)
        self.request = request
        return qs


class BaseTabularInlineAdmin(admin.TabularInline, BaseAdminClass):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 55})},
    }

    def get_queryset(self, request):
        qs = super(BaseTabularInlineAdmin, self).get_queryset(request)
        self.request = request
        return qs


class ProjectInstanceInline(BaseTabularInlineAdmin):
    model = Project
    extra = 0
    fields = ['get_project_link', 'get_description', 'start_date', 'release_date', 'status']
    readonly_fields = ['get_project_link', 'get_description', 'start_date', 'release_date', 'status']
    ordering = ['start_date', 'release_date']

    def get_project_link(self, obj):
        return self.get_link_to_obj(obj)

    get_project_link.short_description = 'proect'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ClientAdmin(BaseModelAdmin):
    fields = ['title', 'description', ]
    inlines = [ProjectInstanceInline]
    readonly_fields = ('get_projects',)
    search_fields = ['title']
    ordering = ['title', ]
    list_display = ['related_title', 'get_description', 'get_projects', 'default_actions']
    list_filter = ('title',)

    def related_title(self, obj):
        return obj.title

    related_title.short_description = '??ompany'

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

    BaseModelAdmin.default_actions.short_description = 'actions'


admin.site.register(Client, ClientAdmin)
