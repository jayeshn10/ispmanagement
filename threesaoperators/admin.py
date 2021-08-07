from django.contrib import admin

# Register your models here.
from threesaoperators.models import NetOperatorsDetails, NetOperatorsBillingDetails, NetOperatorsZones, \
    NetOperatorsNocDetails, NetOperatorsFiberDetails, OpBillingHistory

admin.site.register(NetOperatorsDetails)
admin.site.register(NetOperatorsZones)
admin.site.register(NetOperatorsBillingDetails)
admin.site.register(NetOperatorsNocDetails)
admin.site.register(NetOperatorsFiberDetails)
admin.site.register(OpBillingHistory)