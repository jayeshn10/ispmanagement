from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from sitemanager.forms import UserAdminAddForm, UserAdminChangeForm
from sitemanager.models import User, RejectionMessage, IllVendors, IllNotification, IllConnectionShiftHistory, \
    ThreesaIllConnectionsDetails, IllBillingHistory

admin.site.register(IllConnectionShiftHistory)


@admin.register(ThreesaIllConnectionsDetails)
class ThreesaIllConnectionsDetailsAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html(
            '<a class="btn" href="/threesaillconnections/threesaillconnectionsdetails/{}/change/">Edit</a>', obj.id)

    change_button.short_description = 'Edit'
    '''def delete_button(self, obj):
        return format_html('<a class="btn" href="/threesaillconnections/threesaillconnectionsdetails/{}/delete/">Delete</a>', obj.id)

    delete_button.short_description = "Delete" '''
    ordering = ('id',)
    list_display = ['id', 'ill_custid', 'ill_cust_name', 'ill_gendate', 'ill_cust_address', 'ill_sales_person',
                    'ill_feasibility',
                    'change_button', ]
    search_fields = ['id', 'ill_cust_name', 'ill_gendate', 'ill_cust_address', 'ill_sales_person', 'ill_feasibility', ]
    list_filter = ['ill_gendate', 'ill_sales_person', 'ill_feasibility','ill_conn_type' ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_form = UserAdminChangeForm
    add_form = UserAdminAddForm

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(UserAdmin, self).get_form(request, obj, **kwargs)

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'
    ordering = ('id',)
    list_display = ['id', 'username', 'email', 'user_full_name', 'user_mobile', 'group', 'is_superuser', 'is_staff',
                    'is_active', 'last_login', 'date_joined', ]
    search_fields = ['id', 'username', 'email', 'user_full_name', 'user_mobile', ]
    list_filter = ['groups__name', 'is_staff', ]


@admin.register(IllVendors)
class IllVendorsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'v_code', 'v_name', 'v_contactno', 'v_address', 'v_gstno']
    search_fields = ['id', 'v_code', 'v_name', 'v_contactno', 'v_address', 'v_gstno']


@admin.register(RejectionMessage)
class RejectionMessageAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'msg_sender', 'msg_receiver', 'conn_code', 'rej_module_name']
    search_fields = ['id', 'msg_sender', 'msg_receiver', 'conn_code', 'rej_module_name']
    list_filter = ['msg_sender', 'msg_receiver', 'conn_code', 'rej_module_name']


@admin.register(IllNotification)
class IllNotificationAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'conn_code', 'link_code', 'ill_prev_assign_obj_id', 'ill_ntfc_sender',
                    'ill_ntfc_receiver',
                    'assign_date_time', 'accept_mod_url', 'reject_mod_url', 'get_ill_app_name_display']
    search_fields = ['id', 'conn_code', 'link_code', 'ill_prev_assign_obj_id', 'ill_ntfc_sender',
                     'ill_ntfc_receiver','get_ill_app_name_display',
                     'assign_date_time', 'accept_mod_url', 'reject_mod_url']
    list_filter = ['ill_app_name','ill_ntfc_sender','ill_ntfc_receiver']

admin.site.register(IllBillingHistory)