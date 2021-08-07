from django.contrib import admin

# Register your models here.
from vendorsillthroughthreesa.models import VTTIllDoneConnectionsDetails, VTTIllSalesDetails, VTTIllFiberTeam, \
    VTTIllNocDetails, VTTIllFieldEngineerDetails, VTTIllBillingDetails

admin.site.register(VTTIllDoneConnectionsDetails)
admin.site.register(VTTIllSalesDetails)
admin.site.register(VTTIllFiberTeam)
admin.site.register(VTTIllNocDetails)
admin.site.register(VTTIllFieldEngineerDetails)
admin.site.register(VTTIllBillingDetails)