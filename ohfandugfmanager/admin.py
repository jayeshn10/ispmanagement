from django.contrib import admin

# Register your models here.
from ohfandugfmanager.models import OhfAndUgfVendors, OhfAndUgfFiberTeamDetails, OhfAndUgfBillingDetails, \
    OhfAndUgfDetails, OhfAndUgfBillingHistory

admin.site.register(OhfAndUgfVendors)
admin.site.register(OhfAndUgfFiberTeamDetails)
admin.site.register(OhfAndUgfBillingDetails)
admin.site.register(OhfAndUgfDetails)
admin.site.register(OhfAndUgfBillingHistory)
