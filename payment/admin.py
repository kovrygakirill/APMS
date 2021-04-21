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
    list_display = ['comment', 'get_price_in_dollar', 'get_project', 'default_actions']
    list_filter = ('project', ('price', RangeNumericFilter), )

    def get_price_in_dollar(self, obj):
        return f'{obj.price} $'

    get_price_in_dollar.short_description = 'price'

    def get_project(self, obj):
        return self.get_link_to_obj(obj.project)

    get_project.short_description = 'proect'

    BaseModelAdmin.default_actions.short_description = 'actions'


admin.site.register(Payment, PaymentAdmin)
