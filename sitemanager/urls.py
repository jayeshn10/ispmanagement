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
from django.urls import path, include

from sitemanager import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('user_profile/<int:pid1>/', views.user_profile, name='user_profile'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_edit_details/<int:pid1>/', views.user_edit_details, name='user_edit_details'),
    path('user_view/', views.user_view, name='user_view'),
    path('user_change_password/<int:pid1>/', views.user_change_password, name='user_change_password'),
    path('user_change_jobrole/<int:pid3>/', views.user_change_group, name='user_change_jobrole'),
    path('deletemsg/<int:msgid>/', views.deletemsg, name='deletemsg'),
    path('threesaillconnectionsoverallleads/', views.threesaillconnectionsoverallleads,
         name='threesaillconnectionsoverallleads'),
    path('threesaillconnectionsoverallleads/<int:cid>/edit', views.editillconn, name='editillconn'),
    path('illvendor/', views.illvendor, name='illvendor'),
    path('illvendor/add', views.addillvendor, name='addillvendor'),
    path('illvendor/<int:evid>/edit', views.editillvendor, name='editillvendor'),
    path('ohfandugfvendor/', views.ohfandugfvendor, name='ohfandugfvendor'),
    path('ohfandugfvendor/add', views.addohfandugfvendor, name='addohfandugfvendor'),
    path('ohfandugfvendor/<int:eoauvid>/edit', views.editiohfandugfvendor, name='editiohfandugfvendor'),
    path('shift-connection/', views.shiftconnection, name='shiftconnection'),
    path('shift-connection/<str:ccid>', views.shiftconncheck, name='shiftconncheck'),
    path('shift-connection-verify/', views.shiftconnverify, name='shiftconnverify'),
    path('shift-connection-history/', views.shiftconnhistory, name='shiftconnhistory'),
    path('3saipping/<str:pipaddress>', views.threesaipping, name='3saipping'),
    path('location/', views.threesalocation, name='location'),
    path('downloadbackupdata/', views.downloadbackupdata, name='downloadbackupdata'),
    path('showbillinghistory/<str:connid>', views.showbillinghistory, name='showbillinghistory'),

]
