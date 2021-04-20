from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from payment.models import Payment
from admin_numeric_filter.admin import RangeNumericFilter
from client.admin import BaseModelAdmin


class PaymentAdmin(BaseModelAdmin):
    fields = ['comment', 'price', 'project']
    search_fields = ['project__title']
    ordering = ['project']
    list_display = ['comment', 'get_price_in_dollar', 'get_projects', 'default_actions']
    list_filter = ('project', ('price', RangeNumericFilter), )

    def get_price_in_dollar(self, obj):
        return f'{obj.price} $'

    get_price_in_dollar.short_description = 'price'

    def get_projects(self, obj):
        app_label = self.get_app_label_obj(obj.project)
        model_name = self.get_model_name_obj(obj.project)
        view_name = f'admin:{app_label}_{model_name}_change'

        user_permissions = self.get_user_permissions()
        default_permissions = self.dict_default_permissions(app_label, model_name)

        result = []
        if default_permissions['change'] or default_permissions['view'] in user_permissions:
            link_url = reverse(view_name, args=[obj.project.pk])
            result.append('<a href="{}">{}</a>'.format(link_url, obj.project.title))
        else:
            result.append('{}'.format(obj.project.title))

        return format_html("<br / >".join(result))

    get_projects.short_description = 'proect'

    def default_actions(self, obj):
        html_delete_action = self.get_html_action(obj, action='delete')
        html_change_action = self.get_html_action(obj, action='change')

        return format_html('{} &nbsp; {}', html_delete_action, html_change_action)

    default_actions.short_description = 'actions'


admin.site.register(Payment, PaymentAdmin)
