from django.urls import path

from threesaoperators import views

urlpatterns = [
    path('', views.netoperators, name='netoperators'),
    path('add/', views.addnetoperator, name='addnetoperator'),
    path('<int:enetopid>/edit/', views.editnetoperator, name='editnetoperator'),
    path('fiberdetails/', views.fiberdetails, name='fibernetopdetails'),
    path('fiberdetails/<int:anetopfid>/add', views.addnetopfiber, name='addnetopfiber'),
    path('fiberdetails/<int:enetopfid>/edit', views.editnetopfiber, name='editnetopfiber'),
    path('fiberdetails/<int:rnetopfid>/reject', views.rejnetopfiber, name='rejnetopfiber'),
    path('nocdetails/', views.opnocdetails, name='opnocdetails'),
    path('nocdetails/<int:anetopnid>/add', views.addnetopnoc, name='addnetopnoc'),
    path('nocdetails/<int:enetopnid>/edit', views.editnetopnoc, name='editnetopnoc'),
    path('nocdetails/<int:rnetopnid>/reject', views.rejnetopnoc, name='rejnetopnoc'),
    path('billingdetails/', views.opbilldetails, name='opbilldetails'),
    path('billingdetails/<int:anetopbid>/add', views.addnetopbill, name='addnetopbill'),
    path('billingdetails/<int:enetopbid>/edit', views.editnetopbill, name='editnetopbill'),
    path('billingdetails/<int:rnetopbid>/reject', views.rejnetopbill, name='rejnetopbill'),
    path('billingdetails/<int:rennetopbid>/renew', views.renewnetopbill, name='renewnetopbill'),
    path('showbillinghistory/<str:opid>', views.netopbillhistory, name='netopbillhistory'),

]