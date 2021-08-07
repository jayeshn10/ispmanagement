from django.contrib import admin

# Register your models here.
from threesaillthroughvendors.models import TTVIllSalesDetails, TTVIllNocDetails, TTVIllFieldEngineerDetails, \
    TTVIllBillingDetails, TTVIllDoneConnectionsDetails

admin.site.register(TTVIllSalesDetails)
admin.site.register(TTVIllNocDetails)
admin.site.register(TTVIllFieldEngineerDetails)
admin.site.register(TTVIllBillingDetails)
admin.site.register(TTVIllDoneConnectionsDetails)