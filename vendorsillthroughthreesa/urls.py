from django.conf.urls import url
from django.urls import path

from vendorsillthroughthreesa import views

urlpatterns = [
    path('', views.vttillconnections, name='vttillconnections'),
    path('threesaillconnectionsoverallleads/add/', views.addvttillcon, name='addvttillcon'),
    path('vttillsalesdetails/', views.vttillsalesdetails, name='vttillsalesdetails'),
    path('vttillsalesdetails/<int:asnid>/add', views.addvttillsales, name='addvttillsales'),
    path('vttillsalesdetails/<int:esid>/edit', views.editvttillsales, name='editvttillsales'),
    path('vttillsalesdetails/<int:rsid>/reject', views.rejectvttillsales, name='rejectvttillsales'),
    path('vttillfiberdetails/', views.vttillfiberdetails, name='vttillfiberdetails'),
    path('vttillfiberdetails/<int:afid>/add', views.addvttillfiber, name='addvttillfiber'),
    path('vttillfiberdetails/<int:efid>/edit', views.editvttillfiber, name='editvttillfiber'),
    path('vttillfiberdetails/<int:rfid>/reject', views.rejectvttillfiber, name='rejectvttillfiber'),
    path('vttillnocdetails/', views.vttillnocdetails, name='vttillnocdetails'),
    path('vttillnocdetails/<int:anid>/add', views.addvttillnoc, name='addvttillnoc'),
    path('vttillnocdetails/<int:enid>/edit', views.editvttillnoc, name='editvttillnoc'),
    path('vttillnocdetails/<int:rnid>/reject', views.rejectvttillnoc, name='rejectvttillnoc'),
    path('vttillfieldenggdetails/', views.vttillfieldenggdetails, name='vttillfieldenggdetails'),
    path('vttillfieldenggdetails/<int:afeid>/add', views.addvttillfieldengg, name='addvttillfieldengg'),
    path('vttillfieldenggdetails/<int:efeid>/edit', views.editvttillfieldengg, name='editvttillfieldengg'),
    path('vttillfieldenggdetails/<int:rfeid>/reject', views.rejectvttillfieldengg, name='rejectvttillfieldengg'),
    path('vttillbillingdetails/', views.vttillbillingdetails, name='vttillbillingdetails'),
    path('vttillbillingdetails/<int:abid>/add', views.addvttillbilling, name='addvttillbilling'),
    path('vttillbillingdetails/<int:ebid>/edit', views.editvttillbilling, name='editvttillbilling'),
    path('vttillbillingdetails/<int:rebid>/renew', views.renewvttillbilling, name='renewvttillbilling'),
    path('vttillbillingdetails/<int:rbid>/reject', views.rejectvttillbilling, name='rejectvttillbilling'),
]