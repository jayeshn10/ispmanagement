"""threesaillmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from threesaillconnections import views

urlpatterns = [
    path('', views.threesaillconnections, name='threesaillconnections'),
    path('threesaillconnectionsoverallleads/add/', views.addillcon, name='addillcon'),
    path('threesaillsalesdetails/', views.threesaillsalesdetails, name='threesaillsalesdetails'),
    path('threesaillsalesdetails/<int:nid>/add', views.addillsales, name='addillsales'),
    path('threesaillsalesdetails/<int:sid>/edit', views.editillsales, name='editillsales'),
    path('threesaillsalesdetails/<int:did>/reject', views.rejectillsales, name='rejectillsales'),
    path('threesaillfiberdetails/', views.threesaillfiberdetails, name='threesaillfiberdetails'),
    path('threesaillfiberdetails/<int:afid>/add', views.addillfiber, name='addillfiber'),
    path('threesaillfiberdetails/<int:efid>/edit', views.editillfiber, name='editillfiber'),
    path('threesaillfiberdetails/<int:rfid>/reject', views.rejectillfiber, name='rejectillfiber'),
    path('threesaillnocdetails/', views.threesaillnocdetails, name='threesaillnocdetails'),
    path('threesaillnocdetails/<int:anid>/add', views.addillnoc, name='addillnoc'),
    path('threesaillnocdetails/<int:enid>/edit', views.editillnoc, name='editillnoc'),
    path('threesaillnocdetails/<int:rnid>/reject', views.rejectillnoc, name='rejectillnoc'),
    path('threesaillfieldenggdetails/', views.threesaillfieldenggdetails, name='threesaillfieldenggdetails'),
    path('threesaillfieldenggdetails/<int:afeid>/add', views.addillfieldengg, name='addillfieldengg'),
    path('threesaillfieldenggdetails/<int:efeid>/edit', views.editillfieldengg, name='editillfieldengg'),
    path('threesaillfieldenggdetails/<int:rfeid>/reject', views.rejectillfieldengg, name='rejectillfieldengg'),
    path('threesaillbillingdetails/', views.threesaillbillingdetails, name='threesaillbillingdetails'),
    path('threesaillbillingdetails/<int:abid>/add', views.addillbilling, name='addillbilling'),
    path('threesaillbillingdetails/<int:ebid>/edit', views.editillbilling, name='editillbilling'),
    path('threesaillbillingdetails/<int:rbid>/reject', views.rejectillbilling, name='rejectillbilling'),
    path('threesaillbillingdetails/<int:rebid>/renew', views.renewillbilling, name='renewillbilling'),
]
