from django.urls import path

from threesaillthroughvendors import views

urlpatterns = [
    path('', views.ttvillconnections, name='ttvillconnections'),
    path('threesaillconnectionsoverallleads/add/', views.addttvillcon, name='addttvillcon'),
    path('ttvillsalesdetails/', views.ttvillsalesdetails, name='ttvillsalesdetails'),
    path('ttvillsalesdetails/<int:asnid>/add', views.addttvillsales, name='addttvillsales'),
    path('ttvillsalesdetails/<int:esid>/edit', views.editttvillsales, name='editttvillsales'),
    path('ttvillsalesdetails/<int:rsid>/reject', views.rejectttvillsales, name='rejectttvillsales'),
    path('ttvillnocdetails/', views.ttvillnocdetails, name='ttvillnocdetails'),
    path('ttvillnocdetails/<int:anid>/add', views.addttvillnoc, name='addttvillnoc'),
    path('ttvillnocdetails/<int:enid>/edit', views.editttvillnoc, name='editttvillnoc'),
    path('ttvillnocdetails/<int:rnid>/reject', views.rejectttvillnoc, name='rejectttvillnoc'),
    path('ttvillfieldenggdetails/', views.ttvillfieldenggdetails, name='ttvillfieldenggdetails'),
    path('ttvillfieldenggdetails/<int:afeid>/add', views.addttvillfieldengg, name='addttvillfieldengg'),
    path('ttvillfieldenggdetails/<int:efeid>/edit', views.editttvillfieldengg, name='editttvillfieldengg'),
    path('ttvillfieldenggdetails/<int:rfeid>/reject', views.rejectttvillfieldengg, name='rejectttvillfieldengg'),
    path('ttvillbillingdetails/', views.ttvillbillingdetails, name='ttvillbillingdetails'),
    path('ttvillbillingdetails/<int:abid>/add', views.addttvillbilling, name='addttvillbilling'),
    path('ttvillbillingdetails/<int:ebid>/edit', views.editttvillbilling, name='editttvillbilling'),
    path('ttvillbillingdetails/<int:rebid>/renew', views.renewttvillbilling, name='renewttvillbilling'),
    path('ttvillbillingdetails/<int:rbid>/reject', views.rejectttvillbilling, name='rejectttvillbilling'),
]