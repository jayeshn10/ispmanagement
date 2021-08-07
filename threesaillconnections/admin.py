from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from threesaillconnections.models import ThreesaIllSalesDetails, ThreesaIllFiberTeam, \
    ThreesaIllNocDetails, ThreesaIllFieldEngineerDetails, ThreesaIllBillingDetails, ThreesaIllDoneConnectionsDetails

admin.site.site_header = "Threesa ILL Management System"

@admin.register(ThreesaIllSalesDetails)
class ThreesaIllSalesDetailsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'conn_code', 'po_img', 'location_pin', 'purchase_order_no', 'kyc_details', 'gst_no',
                    'cust_cpn_name',
                    'cust_cpn_num', 'assign_fiber_engg']
    search_fields = ['id', ]

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


@admin.register(ThreesaIllFiberTeam)
class ThreesaIllFiberTeamAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'conn_code', 'media_img', 'switch_img',  'port_media_type', 'fiber_core',
                    'pop_name', 'assign_noc']
    search_fields = ['id', ]


@admin.register(ThreesaIllNocDetails)
class ThreesaIllNocDetailsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'conn_code', 'ill_ip', 'ill_subnet', 'ill_gateway', 'ill_dns', 'ill_dns2', 'ill_switch_ip',
                    'ill_switch_port_no', 'ill_bandwidth', 'ill_vland', 'ill_mac_add', 'ill_routing_status']
    search_fields = ['id', 'ill_ip', 'ill_subnet', 'ill_gateway', 'ill_dns', 'ill_dns2', 'ill_switch_ip',
                     'ill_switch_port_no', 'ill_bandwidth', 'ill_vland', 'ill_mac_add', 'ill_routing_status']


@admin.register(ThreesaIllFieldEngineerDetails)
class ThreesaIllFieldEngineerDetailsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'conn_code', 'link_status', 'cust_cpn_name', 'cust_cpn_num']
    search_fields = ['id', 'link_status', 'cust_cpn_name', 'cust_cpn_num']


@admin.register(ThreesaIllBillingDetails)
class ThreesaIllBillingDetailsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ['id', 'conn_code', 'payment_status']
    search_fields = ['id', 'payment_status']


admin.site.register(ThreesaIllDoneConnectionsDetails)
