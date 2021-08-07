from django.urls import path

from ohfandugfmanager import views

urlpatterns = [
    path('', views.ohfandugf, name='ohfandugf'),
    path('g/', views.ohfandugf_g, name='ohfandugf_g'),
    path('t/', views.ohfandugf_t, name='ohfandugf_t'),
    path('add/', views.addohfandugf, name='addohfandugf'),
    path('<int:eoauid>/edit', views.editohfandugf, name='editohfandugf'),
    path('fiberdetails/', views.fiberdetails, name='fiberdetails'),
    path('fiberdetails/<int:aoaufid>/add', views.addohfandugffiber, name='addohfandugffiber'),
    path('fiberdetails/<int:eoaufid>/edit', views.editohfandugffiber, name='editohfandugffiber'),
    path('fiberdetails/<int:roaufid>/reject', views.rejohfandugffiber, name='rejohfandugffiber'),
    path('billingdetails/', views.billingdetails, name='billingdetails'),
    path('billingdetails/<int:aoaubid>/add', views.addohfandugfbilling, name='addohfandugfbilling'),
    path('billingdetails/<int:eoaubid>/edit', views.editohfandugfbilling, name='editohfandugfbilling'),
    path('billingdetails/<int:reoaubid>/renew', views.renewohfandugfbilling, name='renewohfandugfbilling'),
    path('billingdetails/<int:roaubid>/reject', views.rejohfandugfbilling, name='rejohfandugfbilling'),
    path('historybillingdetails/<str:hioaubid>/edit', views.historyohfandugfbilling, name='historyohfandugfbilling'),

]