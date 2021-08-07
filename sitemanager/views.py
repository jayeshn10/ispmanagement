import io
import os
import sqlite3
import zipfile
import xlwt
from datetime import datetime
from io import BytesIO
from pythonping import ping
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from ohfandugfmanager.models import OhfAndUgfVendors, OhfAndUgfDetails
from sitemanager.decorators import editdetails_authentication
from sitemanager.filters import UserFilter, IllConnDetailsFilter, IllVendorFilter, OhfAndUgfVendorFilter
from sitemanager.forms import CreateUserForm, EditUserDetailsForm, UserChangePasswordCustom, EditUserGroupForm, \
    AddIllVendorForm, EditIllVendorForm, EditIllConForm, \
    AddOhfAndUgfVendorForm, EditOhfAndUgfVendorForm, Num_Item_Per_Page
from sitemanager.models import User, RejectionMessage, ThreesaIllConnectionsDetails, IllVendors, \
    IllNotification, IllConnectionShiftHistory, IllBillingHistory
from threesaillconnections.models import ThreesaIllDoneConnectionsDetails, ThreesaIllBillingDetails, \
    ThreesaIllFieldEngineerDetails, ThreesaIllNocDetails, ThreesaIllFiberTeam, ThreesaIllSalesDetails
from threesaillmanager.settings import BASE_DIR
from threesaillthroughvendors.models import TTVIllDoneConnectionsDetails, TTVIllSalesDetails, TTVIllNocDetails, \
    TTVIllFieldEngineerDetails, TTVIllBillingDetails
from threesaoperators.models import NetOperatorsDetails
from vendorsillthroughthreesa.models import VTTIllDoneConnectionsDetails, VTTIllSalesDetails, VTTIllFiberTeam, \
    VTTIllNocDetails, VTTIllFieldEngineerDetails, VTTIllBillingDetails


@login_required(login_url='login')
def index(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    count_threesa_ill = ThreesaIllConnectionsDetails.objects.filter(ill_conn_type='1').count()
    count_threesa_f_ill = ThreesaIllConnectionsDetails.objects.filter(ill_conn_type='1', ill_feasibility=True).count()
    count_threesa_d_ill = ThreesaIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                          fiber_code__isnull=False,
                                                                          noc_code__isnull=False,
                                                                          fe_code__isnull=False,
                                                                          billing_code__isnull=False).count()
    count_threesa_d_a_ill = ThreesaIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                            fiber_code__isnull=False,
                                                                            noc_code__isnull=False,
                                                                            fe_code__isnull=False,
                                                                            billing_code__isnull=False,
                                                                            active_status=True).count()
    count_threesa_d_d_ill = ThreesaIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                            fiber_code__isnull=False,
                                                                            noc_code__isnull=False,
                                                                            fe_code__isnull=False,
                                                                            billing_code__isnull=False,
                                                                            active_status=False).count()

    count_ttv_ill = ThreesaIllConnectionsDetails.objects.filter(ill_conn_type='2').count()
    count_ttv_f_ill = ThreesaIllConnectionsDetails.objects.filter(ill_conn_type='2', ill_feasibility=True).count()
    count_ttv_d_ill = TTVIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                  noc_code__isnull=False,
                                                                  fe_code__isnull=False,
                                                                  billing_code__isnull=False).count()
    count_ttv_d_a_ill = TTVIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                    noc_code__isnull=False,
                                                                    fe_code__isnull=False,
                                                                    billing_code__isnull=False,
                                                                    active_status=True).count()
    count_ttv_d_d_ill = TTVIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                    noc_code__isnull=False,
                                                                    fe_code__isnull=False,
                                                                    billing_code__isnull=False,
                                                                    active_status=False).count()

    count_vtt_ill = ThreesaIllConnectionsDetails.objects.filter(ill_conn_type='3').count()
    count_vtt_f_ill = ThreesaIllConnectionsDetails.objects.filter(ill_conn_type='3', ill_feasibility=True).count()
    count_vtt_d_ill = VTTIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                  fiber_code__isnull=False,
                                                                  noc_code__isnull=False,
                                                                  fe_code__isnull=False,
                                                                  billing_code__isnull=False).count()
    count_vtt_d_a_ill = VTTIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                    fiber_code__isnull=False,
                                                                    noc_code__isnull=False,
                                                                    fe_code__isnull=False,
                                                                    billing_code__isnull=False,
                                                                    active_status=True).count()
    count_vtt_d_d_ill = VTTIllDoneConnectionsDetails.objects.filter(sale_code__isnull=False,
                                                                    fiber_code__isnull=False,
                                                                    noc_code__isnull=False,
                                                                    fe_code__isnull=False,
                                                                    billing_code__isnull=False,
                                                                    active_status=False).count()

    count_onu_links = OhfAndUgfDetails.objects.all().count()
    count_ohf_links = OhfAndUgfDetails.objects.filter(link_type='1').count()
    count_ohf_g_links = OhfAndUgfDetails.objects.filter(link_type='1', link_type_g_t='2').count()
    count_ohf_g_a_links = OhfAndUgfDetails.objects.filter(link_type='1', link_type_g_t='2', link_status=True).count()
    count_ohf_g_d_links = OhfAndUgfDetails.objects.filter(link_type='1', link_type_g_t='2', link_status=False).count()
    count_ohf_t_links = OhfAndUgfDetails.objects.filter(link_type='1', link_type_g_t='1').count()
    count_ohf_t_a_links = OhfAndUgfDetails.objects.filter(link_type='1', link_type_g_t='1', link_status=True).count()
    count_ohf_t_d_links = OhfAndUgfDetails.objects.filter(link_type='1', link_type_g_t='1', link_status=False).count()

    count_ugf_links = OhfAndUgfDetails.objects.filter(link_type='2').count()
    count_ugf_g_links = OhfAndUgfDetails.objects.filter(link_type='2', link_type_g_t='2').count()
    count_ugf_g_a_links = OhfAndUgfDetails.objects.filter(link_type='2', link_type_g_t='2', link_status=True).count()
    count_ugf_g_d_links = OhfAndUgfDetails.objects.filter(link_type='2', link_type_g_t='2', link_status=False).count()
    count_ugf_t_links = OhfAndUgfDetails.objects.filter(link_type='2', link_type_g_t='1').count()
    count_ugf_t_a_links = OhfAndUgfDetails.objects.filter(link_type='2', link_type_g_t='1', link_status=True).count()
    count_ugf_t_d_links = OhfAndUgfDetails.objects.filter(link_type='2', link_type_g_t='1', link_status=False).count()

    count_netop = NetOperatorsDetails.objects.all().count()
    count_netop_a = NetOperatorsDetails.objects.filter(active_status=True).count()
    count_netop_d = NetOperatorsDetails.objects.filter(active_status=False).count()

    context = {'objntfc_all': objntfc_all,
               'objmsgs': objmsg,
               'count_threesa_ill': count_threesa_ill,
               'count_threesa_f_ill': count_threesa_f_ill,
               'count_threesa_d_ill': count_threesa_d_ill,
               'count_threesa_d_a_ill': count_threesa_d_a_ill,
               'count_threesa_d_d_ill': count_threesa_d_d_ill,
               'count_ttv_ill': count_ttv_ill,
               'count_ttv_f_ill': count_ttv_f_ill,
               'count_ttv_d_ill': count_ttv_d_ill,
               'count_ttv_d_a_ill': count_ttv_d_a_ill,
               'count_ttv_d_d_ill': count_ttv_d_d_ill,
               'count_vtt_ill': count_vtt_ill,
               'count_vtt_f_ill': count_vtt_f_ill,
               'count_vtt_d_ill': count_vtt_d_ill,
               'count_vtt_d_a_ill': count_vtt_d_a_ill,
               'count_vtt_d_d_ill': count_vtt_d_d_ill,
               'count_onu_links': count_onu_links,
               'count_ohf_links': count_ohf_links,
               'count_ohf_g_links': count_ohf_g_links,
               'count_ohf_g_a_links': count_ohf_g_a_links,
               'count_ohf_g_d_links': count_ohf_g_d_links,
               'count_ohf_t_links': count_ohf_t_links,
               'count_ohf_t_a_links': count_ohf_t_a_links,
               'count_ohf_t_d_links': count_ohf_t_d_links,
               'count_ugf_links': count_ugf_links,
               'count_ugf_g_links': count_ugf_g_links,
               'count_ugf_g_a_links': count_ugf_g_a_links,
               'count_ugf_g_d_links': count_ugf_g_d_links,
               'count_ugf_t_links': count_ugf_t_links,
               'count_ugf_t_a_links': count_ugf_t_a_links,
               'count_ugf_t_d_links': count_ugf_t_d_links,
               'count_netop': count_netop,
               'count_netop_a': count_netop_a,
               'count_netop_d': count_netop_d,
               }
    return render(request, 'index.html', context)


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:

        if request.method == 'POST':
            loginusername = request.POST.get('loginUsername')
            loginpassword = request.POST.get('loginPassword')

            user = authenticate(request, username=loginusername, password=loginpassword)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'username or password is incorrect')

        return render(request, 'login.html')


@login_required(login_url='login')
@editdetails_authentication
def user_profile(request, pid1):
    user = User.objects.get(id=pid1)
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    context = {'user': user, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}
    return render(request, 'user_profile.html', context)


@login_required(login_url='login')
@staff_member_required(login_url='login')
def user_create(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            grps = form.cleaned_data['groups']
            for grp_name in grps:
                my_group = Group.objects.get(name=grp_name)
                my_group.user_set.add(user)

            return redirect('user_view')
    context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}
    return render(request, 'user_create.html', context)


@login_required(login_url='login')
@staff_member_required(login_url='login')
def user_view(request):
    user_data = User.objects.all()
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    filterform = UserFilter(request.GET, queryset=user_data)
    user_data = filterform.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        user_data = User.objects.filter(Q(username__icontains=searchguery) |
                                        Q(user_full_name__icontains=searchguery) |
                                        Q(email__icontains=searchguery) |
                                        Q(user_mobile__icontains=searchguery) |
                                        Q(groups__name__icontains=searchguery)
                                        )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Username', 'user full name', 'email', 'user_mobile', 'job role']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        # rows = user_data.values_list('username', 'user_full_name', 'email', 'user_mobile', 'groups__name')
        rows = []
        for user in user_data:
            grp = ''
            for x in user.groups.all():
                if grp == '':
                    grp = x.name
                else:
                    grp = grp + "," + x.name
            rows.append([user.username, user.user_full_name, user.email, user.user_mobile, grp])
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response

    page = request.GET.get('page', 1)
    itemperform = Num_Item_Per_Page()

    num_page = request.GET.get('num_page')
    if not num_page:
        num_page = 10
    num_page = int(num_page)

    paginator = Paginator(user_data, num_page)
    try:
        user_data = paginator.page(page)
    except PageNotAnInteger:
        user_data = paginator.page(1)
    except EmptyPage:
        user_data = paginator.page(paginator.num_pages)

    context = {'user_data': user_data, 'objntfc_all': objntfc_all, 'filterform': filterform, 'objmsgs': objmsg,
               'itemperform': itemperform, "rowcount": str(num_page)}
    return render(request, 'user_view.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


@editdetails_authentication
def user_edit_details(request, pid1):
    user = User.objects.get(id=pid1)
    form = EditUserDetailsForm(instance=user)
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    if request.method == 'POST':
        form = EditUserDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            user_new_info = form.save(commit=False)

            user.user_full_name = user_new_info.user_full_name
            user.email = user_new_info.email
            user.user_mobile = user_new_info.user_mobile
            if not user_new_info.user_image == '':
                user.user_image = user_new_info.user_image

            user.save()
            return redirect('user_profile', pid1)
    context = {'form': form, 'user': user, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}
    return render(request, 'user_edit_details.html', context)


@editdetails_authentication
def user_change_password(request, pid1):
    pid1 = pid1
    user = User.objects.get(id=pid1)
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    form = UserChangePasswordCustom(user)
    if request.method == 'POST':
        form = UserChangePasswordCustom(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pid1)
    context = {'form': form, 'user': user, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}
    return render(request, 'user_change_password.html', context)


@staff_member_required(login_url='login')
def user_change_group(request, pid3):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    user = User.objects.get(id=pid3)
    form = EditUserGroupForm(instance=user)

    if request.method == 'POST':
        form = EditUserGroupForm(request.POST)
        if form.is_valid():
            grps = form.cleaned_data['groups']
            user.groups.clear()
            for grp_name in grps:
                my_group = Group.objects.get(name=grp_name)
                my_group.user_set.add(user)
            form.save(commit=False)
            return redirect('user_profile', pid3)

    context = {'form': form, 'user': user, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}
    return render(request, 'user_change_group.html', context)


@login_required(login_url='login')
def deletemsg(request, msgid):
    objmsg = RejectionMessage.objects.get(id=msgid)
    objmsg.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def threesaillconnectionsoverallleads(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    tlcobj = ThreesaIllConnectionsDetails.objects.all()
    connfilter = IllConnDetailsFilter(request.GET, queryset=tlcobj)
    tlcobj = connfilter.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')

        tlcobj = ThreesaIllConnectionsDetails.objects.filter(Q(ill_custid__icontains=searchguery)
                                                             | Q(ill_cust_name__icontains=searchguery)
                                                             | Q(ill_cust_address__icontains=searchguery)
                                                             | Q(ill_gendate__icontains=searchguery)
                                                             | Q(ill_feasibility__icontains=searchguery)
                                                             | Q(ill_sales_person__username__icontains=searchguery)
                                                             )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="illconnections.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('ILL Connections')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Connection ID', 'Lead Generation Date', 'Customer Name', 'Customer Address', 'Feasibility Status',
                   'Sales Person ID', 'Assign Status', 'Sign Verification Id', 'Sign Verification Time']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = tlcobj.values_list('ill_custid', 'ill_gendate', 'ill_cust_name', 'ill_cust_address', 'ill_feasibility',
                                  'ill_sales_person__username', 'assign_status', 'ill_sign_id', 'ill_sign_time')
        for row in rows:
            row = list(row)
            row[1] = str(row[1].strftime("%d/%m/%Y %I:%M %p"))
            row[8] = str(row[8].strftime("%d/%m/%Y %I:%M %p"))
            if row[4]:
                row[4] = 'Possible'
            else:
                row[4] = 'Possible'
            if row[6]:
                row[6] = 'Assigned'
            else:
                row[6] = 'Not Assigned'
            row = tuple(row)
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response

    page = request.GET.get('page', 1)
    itemperform = Num_Item_Per_Page()

    num_page = request.GET.get('num_page')
    if not num_page:
        num_page = 10
    num_page = int(num_page)

    paginator = Paginator(tlcobj, num_page)
    try:
        tlcobj = paginator.page(page)
    except PageNotAnInteger:
        tlcobj = paginator.page(1)
    except EmptyPage:
        tlcobj = paginator.page(paginator.num_pages)

    context = {'tlcobjs': tlcobj, 'objntfc_all': objntfc_all, 'connfilter': connfilter, 'objmsgs': objmsg,
               "rowcount": str(num_page), 'itemperform': itemperform}
    return render(request, 'ill_conn_details_moduletemp.html', context)


@login_required(login_url='login')
def editillconn(request, cid):
    etlobj = ThreesaIllConnectionsDetails.objects.get(id=cid)
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    if request.user.username == etlobj.ill_sales_person.username or request.user.is_staff:
        EditPer = True
        form = EditIllConForm(instance=etlobj)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditIllConForm(request.POST)
            if form.is_valid():
                newform = form.save(commit=False)
                etlobj.ill_cust_address = newform.ill_cust_address
                etlobj.ill_cust_address_lat = newform.ill_cust_address_lat
                etlobj.ill_cust_address_long = newform.ill_cust_address_long
                etlobj.ill_sign_id = request.user.username
                etlobj.ill_sign_time = datetime.now()
                if not etlobj.ill_feasibility:
                    if newform.ill_feasibility:
                        if etlobj.ill_conn_type == '1':
                            etlobj.ill_feasibility = newform.ill_feasibility
                            doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.create(conn_code=etlobj, )
                            doneconn_obj.save()
                            if not etlobj.assign_status:
                                if newform.assign_status:
                                    etlobj.assign_status = newform.assign_status
                                    salenotification_obj = IllNotification.objects.create(
                                        conn_code=etlobj, ill_ntfc_sender=request.user.username,
                                        ill_prev_assign_obj_id=etlobj.id,
                                        ill_ntfc_receiver=etlobj.ill_sales_person.username,
                                        assign_date_time=etlobj.ill_sign_time,
                                        accept_mod_url="addillsales", reject_mod_url="rejectillsales", ill_app_name="1")
                                    salenotification_obj.save()
                        elif etlobj.ill_conn_type == '2':
                            if newform.ill_feasibility:
                                doneconn_obj = TTVIllDoneConnectionsDetails.objects.create(conn_code=etlobj, )
                                doneconn_obj.save()
                                if newform.assign_status:
                                    etlobj.assign_status = newform.assign_status
                                    salenotification_obj = IllNotification.objects.create(
                                        conn_code=etlobj, ill_ntfc_sender=request.user.username,
                                        ill_prev_assign_obj_id=etlobj.id,
                                        ill_ntfc_receiver=etlobj.ill_sales_person.username,
                                        assign_date_time=etlobj.ill_sign_time,
                                        accept_mod_url="addttvillsales", reject_mod_url="rejectttvillsales",
                                        ill_app_name="2")
                                    salenotification_obj.save()
                        elif etlobj.ill_conn_type == '3':
                            if newform.ill_feasibility:
                                etlobj.ill_feasibility = newform.ill_feasibility
                                doneconn_obj = VTTIllDoneConnectionsDetails.objects.create(conn_code=etlobj, )
                                doneconn_obj.save()
                                if newform.assign_status:
                                    etlobj.assign_status = newform.assign_status
                                    salenotification_obj = IllNotification.objects.create(
                                        conn_code=etlobj, ill_ntfc_sender=request.user.username,
                                        ill_prev_assign_obj_id=etlobj.id,
                                        ill_ntfc_receiver=etlobj.ill_sales_person.username,
                                        assign_date_time=etlobj.ill_sign_time,
                                        accept_mod_url="addvttillsales", reject_mod_url="rejectvttillsales",
                                        ill_app_name="3")
                                    salenotification_obj.save()
                else:
                    if etlobj.ill_conn_type == '1':
                        if not etlobj.assign_status:
                            if newform.assign_status:
                                etlobj.assign_status = newform.assign_status
                                salenotification_obj = IllNotification.objects.create(
                                    conn_code=etlobj, ill_ntfc_sender=request.user.username,
                                    ill_prev_assign_obj_id=etlobj.id,
                                    ill_ntfc_receiver=etlobj.ill_sales_person.username,
                                    assign_date_time=etlobj.ill_sign_time,
                                    accept_mod_url="addillsales", reject_mod_url="rejectillsales", ill_app_name="1")
                                salenotification_obj.save()
                    elif etlobj.ill_conn_type == '2':
                        if newform.assign_status:
                            etlobj.assign_status = newform.assign_status
                            salenotification_obj = IllNotification.objects.create(
                                conn_code=etlobj, ill_ntfc_sender=request.user.username,
                                ill_prev_assign_obj_id=etlobj.id,
                                ill_ntfc_receiver=etlobj.ill_sales_person.username,
                                assign_date_time=etlobj.ill_sign_time,
                                accept_mod_url="addttvillsales", reject_mod_url="rejectttvillsales",
                                ill_app_name="2")
                            salenotification_obj.save()
                    elif etlobj.ill_conn_type == '3':
                        if newform.assign_status:
                            etlobj.assign_status = newform.assign_status
                            salenotification_obj = IllNotification.objects.create(
                                conn_code=etlobj, ill_ntfc_sender=request.user.username,
                                ill_prev_assign_obj_id=etlobj.id,
                                ill_ntfc_receiver=etlobj.ill_sales_person.username,
                                assign_date_time=etlobj.ill_sign_time,
                                accept_mod_url="addvttillsales", reject_mod_url="rejectvttillsales",
                                ill_app_name="3")
                            salenotification_obj.save()

                etlobj.save()
                return redirect(prevurl)
        context = {'form': form, 'etlobj': etlobj, 'objntfc_all': objntfc_all, 'EditPer': EditPer, 'objmsgs': objmsg}

    else:
        EditPer = False
        context = {'etlobj': etlobj,
                   'objntfc_all': objntfc_all,
                   'objmsgs': objmsg,
                   'EditPer': EditPer
                   }

    return render(request, 'edit_ill_connection.html', context)


@login_required(login_url='login')
def illvendor(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    illvendorall = IllVendors.objects.all()

    filterform = IllVendorFilter(request.GET, queryset=illvendorall)
    illvendorall = filterform.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        illvendorall = IllVendors.objects.filter(Q(v_code__icontains=searchguery) |
                                                 Q(v_name__icontains=searchguery) |
                                                 Q(v_contactno__icontains=searchguery) |
                                                 Q(v_address__icontains=searchguery) |
                                                 Q(v_gstno__icontains=searchguery)
                                                 )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="vendors.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Vendors Data')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Vendor Code', 'Vendor Name', 'Contact Number', 'Vendor Address', 'GST Number']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = illvendorall.values_list('v_code', 'v_name', 'v_contactno', 'v_address', 'v_gstno')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response

    page = request.GET.get('page', 1)
    itemperform = Num_Item_Per_Page()

    num_page = request.GET.get('num_page')
    if not num_page:
        num_page = 10
    num_page = int(num_page)

    paginator = Paginator(illvendorall, num_page)
    try:
        illvendorall = paginator.page(page)
    except PageNotAnInteger:
        illvendorall = paginator.page(1)
    except EmptyPage:
        illvendorall = paginator.page(paginator.num_pages)

    context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'illvendorall': illvendorall, 'filterform': filterform,
               'itemperform': itemperform,
               'rowcount': str(num_page)}

    return render(request, 'ill_vendor.html', context)


@login_required(login_url='login')
def addillvendor(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    form = AddIllVendorForm()

    if request.method == 'POST':
        form = AddIllVendorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('illvendor')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}

    return render(request, 'add_ill_vendor.html', context)


@login_required(login_url='login')
def editillvendor(request, evid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    illvendorobj = IllVendors.objects.get(id=evid)

    if request.user.is_staff or request.user.groups.filter(name='salesperson').exists():

        form = EditIllVendorForm(instance=illvendorobj)

        if request.method == 'POST':
            # if editble:
            form = EditIllVendorForm(request.POST, instance=illvendorobj)
            if form.is_valid():
                newform = form.save(commit=False)
                if not newform.v_kyc == 'emptyfile':
                    illvendorobj.v_kyc = newform.v_kyc

                newform.save()

                return redirect('illvendor')
        editper = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'editper': editper,
                   'illvendorobj': illvendorobj}
    else:
        editper = False
        context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'illvendorobj': illvendorobj, 'editper': editper}

    return render(request, 'edit_ill_vendor.html', context)


@login_required(login_url='login')
def ohfandugfvendor(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    oauvendorobj_all = OhfAndUgfVendors.objects.all()

    filterform = OhfAndUgfVendorFilter(request.GET, queryset=oauvendorobj_all)
    oauvendorobj_all = filterform.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        oauvendorobj_all = OhfAndUgfVendors.objects.filter(Q(v_code__icontains=searchguery) |
                                                           Q(v_name__icontains=searchguery) |
                                                           Q(v_address__icontains=searchguery) |
                                                           Q(v_contact_person_name__icontains=searchguery) |
                                                           Q(v_contact_person_no__icontains=searchguery)
                                                           )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ohf-and-ugf-vendors.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Vendors Data')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Vendor Code', 'Vendor Name', 'Vendor Address', 'Contact Person Name', 'Contact Person Number']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = oauvendorobj_all.values_list('v_code', 'v_name', 'v_address', 'v_contact_person_name',
                                            'v_contact_person_no')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response
    page = request.GET.get('page', 1)
    itemperform = Num_Item_Per_Page()

    num_page = request.GET.get('num_page')
    if not num_page:
        num_page = 10
    num_page = int(num_page)

    paginator = Paginator(oauvendorobj_all, num_page)
    try:
        oauvendorobj_all = paginator.page(page)
    except PageNotAnInteger:
        oauvendorobj_all = paginator.page(1)
    except EmptyPage:
        oauvendorobj_all = paginator.page(paginator.num_pages)

    context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'oauvendorobj_all': oauvendorobj_all,
               'filterform': filterform, 'itemperform': itemperform, 'rowcount': str(num_page)}
    return render(request, 'ohfandugf/oau_vendor.html', context)


@login_required(login_url='login')
def addohfandugfvendor(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    form = AddOhfAndUgfVendorForm()

    if request.method == 'POST':
        form = AddOhfAndUgfVendorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ohfandugfvendor')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}

    return render(request, 'ohfandugf/add_oau_vendor.html', context)


@login_required(login_url='login')
def editiohfandugfvendor(request, eoauvid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    oauvendorobj = OhfAndUgfVendors.objects.get(id=eoauvid)

    if request.user.is_staff or request.user.groups.filter(name='OhfAndUgfManager').exists():

        form = EditOhfAndUgfVendorForm(instance=oauvendorobj)

        if request.method == 'POST':
            # if editble:
            form = EditOhfAndUgfVendorForm(request.POST, instance=oauvendorobj)
            if form.is_valid():
                form.save()
                return redirect('ohfandugfvendor')
        editper = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'editper': editper,
                   'oauvendorobj': oauvendorobj}
    else:
        editper = False
        context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'oauvendorobj': oauvendorobj, 'editper': editper}

    return render(request, 'ohfandugf/edit_oau_vendor.html', context)


def shift_threesa_to_ttv(connid, conntype):
    ill_vendor_codes = IllVendors.objects.all()
    ttottv = True
    objpossible = True
    context = {'ttottv': ttottv, 'connid': connid, 'conntype': conntype, 'objpossible': objpossible,
               'ill_vendor_codes': ill_vendor_codes}
    return context


def shift_threesa_to_vtt(connid, conntype):
    ill_vendor_codes = IllVendors.objects.all()
    ttovtt = True
    objpossible = True
    context = {'connid': connid, 'conntype': conntype, 'ttovtt': ttovtt, 'objpossible': objpossible,
               'ill_vendor_codes': ill_vendor_codes}
    return context


def shift_ttv_to_threesa(connid, conntype):
    fiber_engg_all = User.objects.filter(groups__name__in=['fiberengineer', ])
    ttvtot = True
    objpossible = True
    context = {'connid': connid, 'conntype': conntype, 'ttvtot': ttvtot,
               'fiber_engg_all': fiber_engg_all, 'objpossible': objpossible}
    return context


def shift_ttv_to_vtt(connid, conntype):
    ill_vendor_codes = IllVendors.objects.all()
    fiber_engg_all = User.objects.filter(groups__name__in=['fiberengineer', ])
    ttvtovtt = True
    objpossible = True
    context = {'connid': connid, 'conntype': conntype, 'ttvtovtt': ttvtovtt, 'fiber_engg_all': fiber_engg_all,
               'objpossible': objpossible, 'ill_vendor_codes': ill_vendor_codes}
    return context


def shift_vtt_to_threesa(connid, conntype):
    vtttot = True
    objpossible = True
    context = {'connid': connid, 'conntype': conntype, 'vtttot': vtttot, 'objpossible': objpossible}
    return context


def shift_vtt_to_ttv(connid, conntype):
    ill_vendor_codes = IllVendors.objects.all()
    vtttottv = True
    objpossible = True
    context = {'connid': connid, 'conntype': conntype, 'vtttottv': vtttottv, 'objpossible': objpossible,
               'ill_vendor_codes': ill_vendor_codes}
    return context


@login_required(login_url='login')
def shiftconnection(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    if request.method == 'POST':
        tlcobj = ''
        connid = request.POST.get('conn_id')
        conntype = request.POST.get('ill_conn_type')
        objpossible = False
        try:
            tlcobj = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
            if not tlcobj.ill_conn_type == conntype:
                if tlcobj.ill_conn_type == '1':
                    obj_t_d_conn = ThreesaIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
                    if obj_t_d_conn.sale_code and obj_t_d_conn.fiber_code and obj_t_d_conn.noc_code and obj_t_d_conn.fe_code and obj_t_d_conn.billing_code:
                        objpossible = True
                elif tlcobj.ill_conn_type == '2':
                    obj_ttv_d_conn = TTVIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
                    if obj_ttv_d_conn.sale_code and obj_ttv_d_conn.noc_code and obj_ttv_d_conn.fe_code and obj_ttv_d_conn.billing_code:
                        objpossible = True
                elif tlcobj.ill_conn_type == '3':
                    obj_vtt_d_conn = VTTIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
                    if obj_vtt_d_conn.sale_code and obj_vtt_d_conn.fiber_code and obj_vtt_d_conn.noc_code and obj_vtt_d_conn.fe_code and obj_vtt_d_conn.billing_code:
                        objpossible = True
        except:
            objpossible = False

        if objpossible:
            if conntype == '1':
                if tlcobj.ill_conn_type == '2':
                    context = shift_ttv_to_threesa(connid, conntype)
                    return render(request, 'shiftconnection/shift_conn_shiftpost.html', context)
                elif tlcobj.ill_conn_type == '3':
                    context = shift_vtt_to_threesa(connid, conntype)
                    return render(request, 'shiftconnection/shift_conn_shiftpost.html', context)
            elif conntype == '2':
                if tlcobj.ill_conn_type == '1':
                    context = shift_threesa_to_ttv(connid, conntype)
                    return render(request, 'shiftconnection/shift_conn_shiftpost.html', context)
                elif tlcobj.ill_conn_type == '3':
                    context = shift_vtt_to_ttv(connid, conntype)
                    return render(request, 'shiftconnection/shift_conn_shiftpost.html', context)
            elif conntype == '3':
                if tlcobj.ill_conn_type == '1':
                    context = shift_threesa_to_vtt(connid, conntype)
                    return render(request, 'shiftconnection/shift_conn_shiftpost.html', context)
                elif tlcobj.ill_conn_type == '2':
                    context = shift_ttv_to_vtt(connid, conntype)
                    return render(request, 'shiftconnection/shift_conn_shiftpost.html', context)
        else:
            context = {'objpossible': objpossible}
            return render(request, 'shiftconnection/shift_conn_shiftpost.html', context)

    context = {'objntfc_all': objntfc_all, 'objmsg': objmsg}
    return render(request, 'shiftconnection/shift_conn.html', context)


@login_required(login_url='login')
def shiftconncheck(request, ccid):
    ccid = str(ccid)
    try:
        tlcobj = ThreesaIllConnectionsDetails.objects.get(ill_custid=ccid)
        objfound = True
        context = {'objfound': objfound, 'tlcobj': tlcobj}
    except:
        objfound = False
        context = {'objfound': objfound}

    return render(request, 'shiftconnection/shift_conn_checkid.html', context)


def shifting_threesa_to_ttv(connid, conntype, ill_vendor_code):
    ill_vendor_code = int(ill_vendor_code)
    ill_vendor = IllVendors.objects.get(id=ill_vendor_code)
    obj_conn = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
    obj_t_d_conn = ThreesaIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
    obj_ttv_sale = TTVIllSalesDetails.objects.create(conn_code=obj_conn,
                                                     location_pin=obj_t_d_conn.sale_code.location_pin,
                                                     purchase_order_no=obj_t_d_conn.sale_code.purchase_order_no,
                                                     po_img=obj_t_d_conn.sale_code.po_img,
                                                     kyc_details=obj_t_d_conn.sale_code.kyc_details,
                                                     gst_no=obj_t_d_conn.sale_code.gst_no,
                                                     cust_cpn_name=obj_t_d_conn.sale_code.cust_cpn_name,
                                                     cust_cpn_num=obj_t_d_conn.sale_code.cust_cpn_num,
                                                     assign_noc=obj_t_d_conn.fiber_code.assign_noc,
                                                     assign_date_time=obj_t_d_conn.sale_code.assign_date_time,
                                                     ill_sales_receiver=obj_t_d_conn.sale_code.ill_sales_receiver,
                                                     ill_sign_id=obj_t_d_conn.sale_code.ill_sign_id,
                                                     ill_sign_time=obj_t_d_conn.sale_code.ill_sign_time,
                                                     assign_status=obj_t_d_conn.sale_code.assign_status, )
    obj_ttv_sale.save()

    obj_ttv_noc = TTVIllNocDetails.objects.create(conn_code=obj_conn,
                                                  ill_ip=obj_t_d_conn.noc_code.ill_ip,
                                                  ill_subnet=obj_t_d_conn.noc_code.ill_subnet,
                                                  ill_gateway=obj_t_d_conn.noc_code.ill_gateway,
                                                  ill_dns=obj_t_d_conn.noc_code.ill_dns,
                                                  ill_dns2=obj_t_d_conn.noc_code.ill_dns2,
                                                  ill_bandwidth=obj_t_d_conn.noc_code.ill_bandwidth,
                                                  ill_vland=obj_t_d_conn.noc_code.ill_vland,
                                                  ill_mac_add=obj_t_d_conn.noc_code.ill_mac_add,
                                                  ill_routing_status=obj_t_d_conn.noc_code.ill_routing_status,
                                                  assign_field_engg=obj_t_d_conn.noc_code.assign_field_engg,
                                                  assign_date_time=obj_t_d_conn.noc_code.assign_date_time,
                                                  ill_noc_receiver=obj_t_d_conn.noc_code.ill_noc_receiver,
                                                  ill_sign_id=obj_t_d_conn.noc_code.ill_sign_id,
                                                  ill_sign_time=obj_t_d_conn.noc_code.ill_sign_time,
                                                  assign_status=obj_t_d_conn.noc_code.assign_status,
                                                  )
    obj_ttv_noc.save()

    obj_ttv_fe = TTVIllFieldEngineerDetails.objects.create(conn_code=obj_conn,
                                                           link_status=obj_t_d_conn.fe_code.link_status,
                                                           cust_cpn_name=obj_t_d_conn.fe_code.cust_cpn_name,
                                                           cust_cpn_num=obj_t_d_conn.fe_code.cust_cpn_num,
                                                           connectivity_img=obj_t_d_conn.fe_code.connectivity_img,
                                                           assign_billing=obj_t_d_conn.fe_code.assign_billing,
                                                           assign_date_time=obj_t_d_conn.fe_code.assign_date_time,
                                                           ill_field_engg_receiver=obj_t_d_conn.fe_code.ill_field_engg_receiver,
                                                           ill_sign_id=obj_t_d_conn.fe_code.ill_sign_id,
                                                           ill_sign_time=obj_t_d_conn.fe_code.ill_sign_time,
                                                           assign_status=obj_t_d_conn.fe_code.assign_status,
                                                           )
    obj_ttv_fe.save()

    obj_ttv_bill = TTVIllBillingDetails.objects.create(conn_code=obj_conn,
                                                       assign_date_time=obj_t_d_conn.billing_code.assign_date_time,
                                                       conn_start_date=obj_t_d_conn.billing_code.conn_start_date,
                                                       conn_end_date=obj_t_d_conn.billing_code.conn_end_date,
                                                       bandwidth=obj_t_d_conn.billing_code.bandwidth,
                                                       link_validity=obj_t_d_conn.billing_code.link_validity,
                                                       payment_status=obj_t_d_conn.billing_code.payment_status,
                                                       amount=obj_t_d_conn.billing_code.amount,
                                                       payment_method=obj_t_d_conn.billing_code.payment_method,
                                                       netbanking_type=obj_t_d_conn.billing_code.netbanking_type,
                                                       transaction_id=obj_t_d_conn.billing_code.transaction_id,
                                                       transaction_receipt=obj_t_d_conn.billing_code.transaction_receipt,
                                                       billing_img=obj_t_d_conn.billing_code.billing_img,
                                                       ill_billing_receiver=obj_t_d_conn.billing_code.ill_billing_receiver,
                                                       ill_sign_id=obj_t_d_conn.billing_code.ill_sign_id,
                                                       ill_sign_time=obj_t_d_conn.billing_code.ill_sign_time,
                                                       )
    obj_ttv_bill.save()

    obj_ttv_d_conn = TTVIllDoneConnectionsDetails.objects.create(conn_code=obj_conn,
                                                                 active_status=obj_t_d_conn.active_status,
                                                                 sale_code=obj_ttv_sale,
                                                                 noc_code=obj_ttv_noc,
                                                                 fe_code=obj_ttv_fe,
                                                                 billing_code=obj_ttv_bill,
                                                                 )

    obj_ttv_d_conn.save()
    # change ill connection type
    obj_conn.ill_conn_type = conntype
    obj_conn.ill_vendor_code = ill_vendor
    obj_conn.save()

    # delete obj
    obj_t_bill = ThreesaIllBillingDetails.objects.get(id=obj_t_d_conn.billing_code.id)
    obj_t_bill.delete()

    obj_t_fe = ThreesaIllFieldEngineerDetails.objects.get(id=obj_t_d_conn.fe_code.id)
    obj_t_fe.delete()

    obj_t_noc = ThreesaIllNocDetails.objects.get(id=obj_t_d_conn.noc_code.id)
    obj_t_noc.delete()

    obj_t_fiber = ThreesaIllFiberTeam.objects.get(id=obj_t_d_conn.fiber_code.id)
    obj_t_fiber.delete()

    obj_t_sale = ThreesaIllSalesDetails.objects.get(id=obj_t_d_conn.sale_code.id)
    obj_t_sale.delete()

    # delete prev done connection obj
    obj_t_d_conn.delete()



def shifting_ttv_to_threesa(connid, conntype, assign_fiber, media_img, switch_img, port_media_type, fiber_core,
                            pop_name,
                            ill_switch_ip, ill_switch_port_no, ill_sign_id):
    assign_fiber_i = User.objects.get(id=assign_fiber)
    obj_conn = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
    obj_ttv_d_conn = TTVIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
    obj_t_sale = ThreesaIllSalesDetails.objects.create(conn_code=obj_conn,
                                                       location_pin=obj_ttv_d_conn.sale_code.location_pin,
                                                       purchase_order_no=obj_ttv_d_conn.sale_code.purchase_order_no,
                                                       po_img=obj_ttv_d_conn.sale_code.po_img,
                                                       kyc_details=obj_ttv_d_conn.sale_code.kyc_details,
                                                       gst_no=obj_ttv_d_conn.sale_code.gst_no,
                                                       cust_cpn_name=obj_ttv_d_conn.sale_code.cust_cpn_name,
                                                       cust_cpn_num=obj_ttv_d_conn.sale_code.cust_cpn_num,
                                                       assign_fiber_engg=assign_fiber_i,
                                                       assign_date_time=obj_ttv_d_conn.sale_code.assign_date_time,
                                                       ill_sales_receiver=obj_ttv_d_conn.sale_code.ill_sales_receiver,
                                                       ill_sign_id=obj_ttv_d_conn.sale_code.ill_sign_id,
                                                       ill_sign_time=obj_ttv_d_conn.sale_code.ill_sign_time,
                                                       assign_status=obj_ttv_d_conn.sale_code.assign_status, )
    obj_t_sale.save()

    obj_t_fiber = ThreesaIllFiberTeam.objects.create(conn_code=obj_conn,
                                                     media_img=media_img,
                                                     switch_img=switch_img,
                                                     port_media_type=port_media_type,
                                                     fiber_core=fiber_core,
                                                     pop_name=pop_name,
                                                     assign_noc=obj_ttv_d_conn.sale_code.assign_noc,
                                                     assign_date_time=datetime.now(),
                                                     ill_fiber_receiver=assign_fiber,
                                                     ill_sign_id=ill_sign_id,
                                                     ill_sign_time=datetime.now(),
                                                     assign_status=True, )
    obj_t_fiber.save()
    obj_t_noc = ThreesaIllNocDetails.objects.create(conn_code=obj_conn,
                                                    ill_ip=obj_ttv_d_conn.noc_code.ill_ip,
                                                    ill_subnet=obj_ttv_d_conn.noc_code.ill_subnet,
                                                    ill_gateway=obj_ttv_d_conn.noc_code.ill_gateway,
                                                    ill_dns=obj_ttv_d_conn.noc_code.ill_dns,
                                                    ill_dns2=obj_ttv_d_conn.noc_code.ill_dns2,
                                                    ill_switch_ip=ill_switch_ip,
                                                    ill_switch_port_no=ill_switch_port_no,
                                                    ill_bandwidth=obj_ttv_d_conn.noc_code.ill_bandwidth,
                                                    ill_vland=obj_ttv_d_conn.noc_code.ill_vland,
                                                    ill_mac_add=obj_ttv_d_conn.noc_code.ill_mac_add,
                                                    ill_routing_status=obj_ttv_d_conn.noc_code.ill_routing_status,
                                                    assign_field_engg=obj_ttv_d_conn.noc_code.assign_field_engg,
                                                    assign_date_time=obj_ttv_d_conn.noc_code.assign_date_time,
                                                    ill_noc_receiver=obj_ttv_d_conn.noc_code.ill_noc_receiver,
                                                    ill_sign_id=obj_ttv_d_conn.noc_code.ill_sign_id,
                                                    ill_sign_time=obj_ttv_d_conn.noc_code.ill_sign_time,
                                                    assign_status=obj_ttv_d_conn.noc_code.assign_status, )
    obj_t_noc.save()
    obj_t_fe = ThreesaIllFieldEngineerDetails.objects.create(conn_code=obj_conn,
                                                             link_status=obj_ttv_d_conn.fe_code.link_status,
                                                             cust_cpn_name=obj_ttv_d_conn.fe_code.cust_cpn_name,
                                                             cust_cpn_num=obj_ttv_d_conn.fe_code.cust_cpn_num,
                                                             connectivity_img=obj_ttv_d_conn.fe_code.connectivity_img,
                                                             assign_billing=obj_ttv_d_conn.fe_code.assign_billing,
                                                             assign_date_time=obj_ttv_d_conn.fe_code.assign_date_time,
                                                             ill_field_engg_receiver=obj_ttv_d_conn.fe_code.ill_field_engg_receiver,
                                                             ill_sign_id=obj_ttv_d_conn.fe_code.ill_sign_id,
                                                             ill_sign_time=obj_ttv_d_conn.fe_code.ill_sign_time,
                                                             assign_status=obj_ttv_d_conn.fe_code.assign_status, )
    obj_t_fe.save()
    obj_t_bill = ThreesaIllBillingDetails.objects.create(
        conn_code=obj_conn,
        assign_date_time=obj_ttv_d_conn.billing_code.assign_date_time,
        conn_start_date=obj_ttv_d_conn.billing_code.conn_start_date,
        conn_end_date=obj_ttv_d_conn.billing_code.conn_end_date,
        bandwidth=obj_ttv_d_conn.billing_code.bandwidth,
        link_validity=obj_ttv_d_conn.billing_code.link_validity,
        payment_status=obj_ttv_d_conn.billing_code.payment_status,
        amount=obj_ttv_d_conn.billing_code.amount,
        payment_method=obj_ttv_d_conn.billing_code.payment_method,
        netbanking_type=obj_ttv_d_conn.billing_code.netbanking_type,
        transaction_id=obj_ttv_d_conn.billing_code.transaction_id,
        transaction_receipt=obj_ttv_d_conn.billing_code.transaction_receipt,
        billing_img=obj_ttv_d_conn.billing_code.billing_img,
        ill_billing_receiver=obj_ttv_d_conn.billing_code.ill_billing_receiver,
        ill_sign_id=obj_ttv_d_conn.billing_code.ill_sign_id,
        ill_sign_time=obj_ttv_d_conn.billing_code.ill_sign_time,
    )
    obj_t_bill.save()

    obj_t_d_conn = ThreesaIllDoneConnectionsDetails.objects.create(conn_code=obj_conn,
                                                                   active_status=obj_ttv_d_conn.active_status,
                                                                   sale_code=obj_t_sale,
                                                                   fiber_code=obj_t_fiber,
                                                                   noc_code=obj_t_noc,
                                                                   fe_code=obj_t_fe,
                                                                   billing_code=obj_t_bill,
                                                                   )
    obj_t_d_conn.save()
    # change ill connection type
    obj_conn.ill_conn_type = conntype
    obj_conn.ill_vendor_code = None
    obj_conn.save()

    # delete obj
    obj_ttv_bill = TTVIllBillingDetails.objects.get(id=obj_ttv_d_conn.billing_code.id)
    obj_ttv_bill.delete()

    obj_ttv_fe = TTVIllFieldEngineerDetails.objects.get(id=obj_ttv_d_conn.fe_code.id)
    obj_ttv_fe.delete()

    obj_ttv_noc = TTVIllNocDetails.objects.get(id=obj_ttv_d_conn.noc_code.id)
    obj_ttv_noc.delete()

    obj_ttv_sale = TTVIllSalesDetails.objects.get(id=obj_ttv_d_conn.sale_code.id)
    obj_ttv_sale.delete()

    # delete prev done connection obj
    obj_ttv_d_conn.delete()



def shifting_threesa_to_vtt(connid, conntype, ill_vendor_code):
    ill_vendor_code = int(ill_vendor_code)
    ill_vendor = IllVendors.objects.get(id=ill_vendor_code)
    obj_conn = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
    obj_t_d_conn = ThreesaIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
    obj_vtt_sale = VTTIllSalesDetails.objects.create(conn_code=obj_conn,
                                                     location_pin=obj_t_d_conn.sale_code.location_pin,
                                                     purchase_order_no=obj_t_d_conn.sale_code.purchase_order_no,
                                                     po_img=obj_t_d_conn.sale_code.po_img,
                                                     kyc_details=obj_t_d_conn.sale_code.kyc_details,
                                                     gst_no=obj_t_d_conn.sale_code.gst_no,
                                                     cust_cpn_name=obj_t_d_conn.sale_code.cust_cpn_name,
                                                     cust_cpn_num=obj_t_d_conn.sale_code.cust_cpn_num,
                                                     assign_fiber_engg=obj_t_d_conn.sale_code.assign_fiber_engg,
                                                     assign_date_time=obj_t_d_conn.sale_code.assign_date_time,
                                                     ill_sales_receiver=obj_t_d_conn.sale_code.ill_sales_receiver,
                                                     ill_sign_id=obj_t_d_conn.sale_code.ill_sign_id,
                                                     ill_sign_time=obj_t_d_conn.sale_code.ill_sign_time,
                                                     assign_status=obj_t_d_conn.sale_code.assign_status, )
    obj_vtt_sale.save()

    obj_vtt_fiber = VTTIllFiberTeam.objects.create(conn_code=obj_conn,
                                                   media_img=obj_t_d_conn.fiber_code.media_img,
                                                   switch_img=obj_t_d_conn.fiber_code.switch_img,
                                                   port_media_type=obj_t_d_conn.fiber_code.port_media_type,
                                                   fiber_core=obj_t_d_conn.fiber_code.fiber_core,
                                                   pop_name=obj_t_d_conn.fiber_code.pop_name,
                                                   assign_noc=obj_t_d_conn.fiber_code.assign_noc,
                                                   assign_date_time=obj_t_d_conn.fiber_code.assign_date_time,
                                                   ill_fiber_receiver=obj_t_d_conn.fiber_code.ill_fiber_receiver,
                                                   ill_sign_id=obj_t_d_conn.fiber_code.ill_sign_id,
                                                   ill_sign_time=obj_t_d_conn.fiber_code.ill_sign_time,
                                                   assign_status=obj_t_d_conn.fiber_code.assign_status, )
    obj_vtt_fiber.save()
    obj_vtt_noc = VTTIllNocDetails.objects.create(conn_code=obj_conn,
                                                  ill_ip=obj_t_d_conn.noc_code.ill_ip,
                                                  ill_subnet=obj_t_d_conn.noc_code.ill_subnet,
                                                  ill_gateway=obj_t_d_conn.noc_code.ill_gateway,
                                                  ill_dns=obj_t_d_conn.noc_code.ill_dns,
                                                  ill_dns2=obj_t_d_conn.noc_code.ill_dns2,
                                                  ill_switch_ip=obj_t_d_conn.noc_code.ill_switch_ip,
                                                  ill_switch_port_no=obj_t_d_conn.noc_code.ill_switch_port_no,
                                                  ill_bandwidth=obj_t_d_conn.noc_code.ill_bandwidth,
                                                  ill_vland=obj_t_d_conn.noc_code.ill_vland,
                                                  ill_mac_add=obj_t_d_conn.noc_code.ill_mac_add,
                                                  ill_routing_status=obj_t_d_conn.noc_code.ill_routing_status,
                                                  assign_field_engg=obj_t_d_conn.noc_code.assign_field_engg,
                                                  assign_date_time=obj_t_d_conn.noc_code.assign_date_time,
                                                  ill_noc_receiver=obj_t_d_conn.noc_code.ill_noc_receiver,
                                                  ill_sign_id=obj_t_d_conn.noc_code.ill_sign_id,
                                                  ill_sign_time=obj_t_d_conn.noc_code.ill_sign_time,
                                                  assign_status=obj_t_d_conn.noc_code.assign_status, )
    obj_vtt_noc.save()
    obj_vtt_fe = VTTIllFieldEngineerDetails.objects.create(conn_code=obj_conn,
                                                           link_status=obj_t_d_conn.fe_code.link_status,
                                                           cust_cpn_name=obj_t_d_conn.fe_code.cust_cpn_name,
                                                           cust_cpn_num=obj_t_d_conn.fe_code.cust_cpn_num,
                                                           connectivity_img=obj_t_d_conn.fe_code.connectivity_img,
                                                           assign_billing=obj_t_d_conn.fe_code.assign_billing,
                                                           assign_date_time=obj_t_d_conn.fe_code.assign_date_time,
                                                           ill_field_engg_receiver=obj_t_d_conn.fe_code.ill_field_engg_receiver,
                                                           ill_sign_id=obj_t_d_conn.fe_code.ill_sign_id,
                                                           ill_sign_time=obj_t_d_conn.fe_code.ill_sign_time,
                                                           assign_status=obj_t_d_conn.fe_code.assign_status, )
    obj_vtt_fe.save()
    obj_vtt_bill = VTTIllBillingDetails.objects.create(conn_code=obj_conn,
                                                       assign_date_time=obj_t_d_conn.billing_code.assign_date_time,
                                                       conn_start_date=obj_t_d_conn.billing_code.conn_start_date,
                                                       conn_end_date=obj_t_d_conn.billing_code.conn_end_date,
                                                       bandwidth=obj_t_d_conn.billing_code.bandwidth,
                                                       link_validity=obj_t_d_conn.billing_code.link_validity,
                                                       payment_status=obj_t_d_conn.billing_code.payment_status,
                                                       amount=obj_t_d_conn.billing_code.amount,
                                                       payment_method=obj_t_d_conn.billing_code.payment_method,
                                                       netbanking_type=obj_t_d_conn.billing_code.netbanking_type,
                                                       transaction_id=obj_t_d_conn.billing_code.transaction_id,
                                                       transaction_receipt=obj_t_d_conn.billing_code.transaction_receipt,
                                                       billing_img=obj_t_d_conn.billing_code.billing_img,
                                                       ill_billing_receiver=obj_t_d_conn.billing_code.ill_billing_receiver,
                                                       ill_sign_id=obj_t_d_conn.billing_code.ill_sign_id,
                                                       ill_sign_time=obj_t_d_conn.billing_code.ill_sign_time,
                                                       )
    obj_vtt_bill.save()

    obj_vtt_d_conn = VTTIllDoneConnectionsDetails.objects.create(conn_code=obj_conn,
                                                                 active_status=obj_t_d_conn.active_status,
                                                                 sale_code=obj_vtt_sale,
                                                                 fiber_code=obj_vtt_fiber,
                                                                 noc_code=obj_vtt_noc,
                                                                 fe_code=obj_vtt_fe,
                                                                 billing_code=obj_vtt_bill,
                                                                 )
    obj_vtt_d_conn.save()
    # change ill connection type
    obj_conn.ill_conn_type = conntype
    obj_conn.ill_vendor_code = ill_vendor
    obj_conn.save()

    # delete obj
    obj_t_bill = ThreesaIllBillingDetails.objects.get(id=obj_t_d_conn.billing_code.id)
    obj_t_bill.delete()

    obj_t_fe = ThreesaIllFieldEngineerDetails.objects.get(id=obj_t_d_conn.fe_code.id)
    obj_t_fe.delete()

    obj_t_noc = ThreesaIllNocDetails.objects.get(id=obj_t_d_conn.noc_code.id)
    obj_t_noc.delete()

    obj_t_fiber = ThreesaIllFiberTeam.objects.get(id=obj_t_d_conn.fiber_code.id)
    obj_t_fiber.delete()

    obj_t_sale = ThreesaIllSalesDetails.objects.get(id=obj_t_d_conn.sale_code.id)
    obj_t_sale.delete()

    # delete prev done connection obj
    obj_t_d_conn.delete()



def shifting_vtt_to_threesa(connid, conntype):
    obj_conn = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
    obj_vtt_d_conn = VTTIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
    obj_t_sale = ThreesaIllSalesDetails.objects.create(conn_code=obj_conn,
                                                       location_pin=obj_vtt_d_conn.sale_code.location_pin,
                                                       purchase_order_no=obj_vtt_d_conn.sale_code.purchase_order_no,
                                                       po_img=obj_vtt_d_conn.sale_code.po_img,
                                                       kyc_details=obj_vtt_d_conn.sale_code.kyc_details,
                                                       gst_no=obj_vtt_d_conn.sale_code.gst_no,
                                                       cust_cpn_name=obj_vtt_d_conn.sale_code.cust_cpn_name,
                                                       cust_cpn_num=obj_vtt_d_conn.sale_code.cust_cpn_num,
                                                       assign_fiber_engg=obj_vtt_d_conn.sale_code.assign_fiber_engg,
                                                       assign_date_time=obj_vtt_d_conn.sale_code.assign_date_time,
                                                       ill_sales_receiver=obj_vtt_d_conn.sale_code.ill_sales_receiver,
                                                       ill_sign_id=obj_vtt_d_conn.sale_code.ill_sign_id,
                                                       ill_sign_time=obj_vtt_d_conn.sale_code.ill_sign_time,
                                                       assign_status=obj_vtt_d_conn.sale_code.assign_status, )
    obj_t_sale.save()

    obj_t_fiber = ThreesaIllFiberTeam.objects.create(conn_code=obj_conn,
                                                     media_img=obj_vtt_d_conn.fiber_code.media_img,
                                                     switch_img=obj_vtt_d_conn.fiber_code.switch_img,
                                                     port_media_type=obj_vtt_d_conn.fiber_code.port_media_type,
                                                     fiber_core=obj_vtt_d_conn.fiber_code.fiber_core,
                                                     pop_name=obj_vtt_d_conn.fiber_code.pop_name,
                                                     assign_noc=obj_vtt_d_conn.fiber_code.assign_noc,
                                                     assign_date_time=obj_vtt_d_conn.fiber_code.assign_date_time,
                                                     ill_fiber_receiver=obj_vtt_d_conn.fiber_code.ill_fiber_receiver,
                                                     ill_sign_id=obj_vtt_d_conn.fiber_code.ill_sign_id,
                                                     ill_sign_time=obj_vtt_d_conn.fiber_code.ill_sign_time,
                                                     assign_status=obj_vtt_d_conn.fiber_code.assign_status, )
    obj_t_fiber.save()
    obj_t_noc = ThreesaIllNocDetails.objects.create(conn_code=obj_conn,
                                                    ill_ip=obj_vtt_d_conn.noc_code.ill_ip,
                                                    ill_subnet=obj_vtt_d_conn.noc_code.ill_subnet,
                                                    ill_gateway=obj_vtt_d_conn.noc_code.ill_gateway,
                                                    ill_dns=obj_vtt_d_conn.noc_code.ill_dns,
                                                    ill_dns2=obj_vtt_d_conn.noc_code.ill_dns2,
                                                    ill_switch_ip=obj_vtt_d_conn.noc_code.ill_switch_ip,
                                                    ill_switch_port_no=obj_vtt_d_conn.noc_code.ill_switch_port_no,
                                                    ill_bandwidth=obj_vtt_d_conn.noc_code.ill_bandwidth,
                                                    ill_vland=obj_vtt_d_conn.noc_code.ill_vland,
                                                    ill_mac_add=obj_vtt_d_conn.noc_code.ill_mac_add,
                                                    ill_routing_status=obj_vtt_d_conn.noc_code.ill_routing_status,
                                                    assign_field_engg=obj_vtt_d_conn.noc_code.assign_field_engg,
                                                    assign_date_time=obj_vtt_d_conn.noc_code.assign_date_time,
                                                    ill_noc_receiver=obj_vtt_d_conn.noc_code.ill_noc_receiver,
                                                    ill_sign_id=obj_vtt_d_conn.noc_code.ill_sign_id,
                                                    ill_sign_time=obj_vtt_d_conn.noc_code.ill_sign_time,
                                                    assign_status=obj_vtt_d_conn.noc_code.assign_status, )
    obj_t_noc.save()
    obj_t_fe = ThreesaIllFieldEngineerDetails.objects.create(conn_code=obj_conn,
                                                             link_status=obj_vtt_d_conn.fe_code.link_status,
                                                             cust_cpn_name=obj_vtt_d_conn.fe_code.cust_cpn_name,
                                                             cust_cpn_num=obj_vtt_d_conn.fe_code.cust_cpn_num,
                                                             connectivity_img=obj_vtt_d_conn.fe_code.connectivity_img,
                                                             assign_billing=obj_vtt_d_conn.fe_code.assign_billing,
                                                             assign_date_time=obj_vtt_d_conn.fe_code.assign_date_time,
                                                             ill_field_engg_receiver=obj_vtt_d_conn.fe_code.ill_field_engg_receiver,
                                                             ill_sign_id=obj_vtt_d_conn.fe_code.ill_sign_id,
                                                             ill_sign_time=obj_vtt_d_conn.fe_code.ill_sign_time,
                                                             assign_status=obj_vtt_d_conn.fe_code.assign_status, )
    obj_t_fe.save()
    obj_t_bill = ThreesaIllBillingDetails.objects.create(conn_code=obj_conn,
                                                         assign_date_time=obj_vtt_d_conn.billing_code.assign_date_time,
                                                         conn_start_date=obj_vtt_d_conn.billing_code.conn_start_date,
                                                         conn_end_date=obj_vtt_d_conn.billing_code.conn_end_date,
                                                         bandwidth=obj_vtt_d_conn.billing_code.bandwidth,
                                                         link_validity=obj_vtt_d_conn.billing_code.link_validity,
                                                         payment_status=obj_vtt_d_conn.billing_code.payment_status,
                                                         amount=obj_vtt_d_conn.billing_code.amount,
                                                         payment_method=obj_vtt_d_conn.billing_code.payment_method,
                                                         netbanking_type=obj_vtt_d_conn.billing_code.netbanking_type,
                                                         transaction_id=obj_vtt_d_conn.billing_code.transaction_id,
                                                         transaction_receipt=obj_vtt_d_conn.billing_code.transaction_receipt,
                                                         billing_img=obj_vtt_d_conn.billing_code.billing_img,
                                                         ill_billing_receiver=obj_vtt_d_conn.billing_code.ill_billing_receiver,
                                                         ill_sign_id=obj_vtt_d_conn.billing_code.ill_sign_id,
                                                         ill_sign_time=obj_vtt_d_conn.billing_code.ill_sign_time,
                                                         )
    obj_t_bill.save()

    obj_t_d_conn = ThreesaIllDoneConnectionsDetails.objects.create(conn_code=obj_conn,
                                                                   active_status=obj_vtt_d_conn.active_status,
                                                                   sale_code=obj_t_sale,
                                                                   fiber_code=obj_t_fiber,
                                                                   noc_code=obj_t_noc,
                                                                   fe_code=obj_t_fe,
                                                                   billing_code=obj_t_bill,
                                                                   )
    obj_t_d_conn.save()
    # change ill connection type
    obj_conn.ill_conn_type = conntype
    obj_conn.ill_vendor_code = None
    obj_conn.save()

    # delete obj
    obj_vtt_bill = VTTIllBillingDetails.objects.get(id=obj_vtt_d_conn.billing_code.id)
    obj_vtt_bill.delete()

    obj_vtt_fe = VTTIllFieldEngineerDetails.objects.get(id=obj_vtt_d_conn.fe_code.id)
    obj_vtt_fe.delete()

    obj_vtt_noc = VTTIllNocDetails.objects.get(id=obj_vtt_d_conn.noc_code.id)
    obj_vtt_noc.delete()

    obj_vtt_fiber = VTTIllFiberTeam.objects.get(id=obj_vtt_d_conn.fiber_code.id)
    obj_vtt_fiber.delete()

    obj_vtt_sale = VTTIllSalesDetails.objects.get(id=obj_vtt_d_conn.sale_code.id)
    obj_vtt_sale.delete()

    # delete prev done connection obj
    obj_vtt_d_conn.delete()



def shifting_vtt_to_ttv(connid, conntype, ill_vendor_code):
    ill_vendor_code = int(ill_vendor_code)
    ill_vendor = IllVendors.objects.get(id=ill_vendor_code)
    obj_conn = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
    obj_vtt_d_conn = VTTIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
    obj_ttv_sale = TTVIllSalesDetails.objects.create(conn_code=obj_conn,
                                                     location_pin=obj_vtt_d_conn.sale_code.location_pin,
                                                     purchase_order_no=obj_vtt_d_conn.sale_code.purchase_order_no,
                                                     po_img=obj_vtt_d_conn.sale_code.po_img,
                                                     kyc_details=obj_vtt_d_conn.sale_code.kyc_details,
                                                     gst_no=obj_vtt_d_conn.sale_code.gst_no,
                                                     cust_cpn_name=obj_vtt_d_conn.sale_code.cust_cpn_name,
                                                     cust_cpn_num=obj_vtt_d_conn.sale_code.cust_cpn_num,
                                                     assign_noc=obj_vtt_d_conn.fiber_code.assign_noc,
                                                     assign_date_time=obj_vtt_d_conn.sale_code.assign_date_time,
                                                     ill_sales_receiver=obj_vtt_d_conn.sale_code.ill_sales_receiver,
                                                     ill_sign_id=obj_vtt_d_conn.sale_code.ill_sign_id,
                                                     ill_sign_time=obj_vtt_d_conn.sale_code.ill_sign_time,
                                                     assign_status=obj_vtt_d_conn.sale_code.assign_status, )
    obj_ttv_sale.save()

    obj_ttv_noc = TTVIllNocDetails.objects.create(conn_code=obj_conn,
                                                  ill_ip=obj_vtt_d_conn.noc_code.ill_ip,
                                                  ill_subnet=obj_vtt_d_conn.noc_code.ill_subnet,
                                                  ill_gateway=obj_vtt_d_conn.noc_code.ill_gateway,
                                                  ill_dns=obj_vtt_d_conn.noc_code.ill_dns,
                                                  ill_dns2=obj_vtt_d_conn.noc_code.ill_dns2,
                                                  ill_bandwidth=obj_vtt_d_conn.noc_code.ill_bandwidth,
                                                  ill_vland=obj_vtt_d_conn.noc_code.ill_vland,
                                                  ill_mac_add=obj_vtt_d_conn.noc_code.ill_mac_add,
                                                  ill_routing_status=obj_vtt_d_conn.noc_code.ill_routing_status,
                                                  assign_field_engg=obj_vtt_d_conn.noc_code.assign_field_engg,
                                                  assign_date_time=obj_vtt_d_conn.noc_code.assign_date_time,
                                                  ill_noc_receiver=obj_vtt_d_conn.noc_code.ill_noc_receiver,
                                                  ill_sign_id=obj_vtt_d_conn.noc_code.ill_sign_id,
                                                  ill_sign_time=obj_vtt_d_conn.noc_code.ill_sign_time,
                                                  assign_status=obj_vtt_d_conn.noc_code.assign_status,
                                                  )
    obj_ttv_noc.save()

    obj_ttv_fe = TTVIllFieldEngineerDetails.objects.create(conn_code=obj_conn,
                                                           link_status=obj_vtt_d_conn.fe_code.link_status,
                                                           cust_cpn_name=obj_vtt_d_conn.fe_code.cust_cpn_name,
                                                           cust_cpn_num=obj_vtt_d_conn.fe_code.cust_cpn_num,
                                                           connectivity_img=obj_vtt_d_conn.fe_code.connectivity_img,
                                                           assign_billing=obj_vtt_d_conn.fe_code.assign_billing,
                                                           assign_date_time=obj_vtt_d_conn.fe_code.assign_date_time,
                                                           ill_field_engg_receiver=obj_vtt_d_conn.fe_code.ill_field_engg_receiver,
                                                           ill_sign_id=obj_vtt_d_conn.fe_code.ill_sign_id,
                                                           ill_sign_time=obj_vtt_d_conn.fe_code.ill_sign_time,
                                                           assign_status=obj_vtt_d_conn.fe_code.assign_status,
                                                           )
    obj_ttv_fe.save()

    obj_ttv_bill = TTVIllBillingDetails.objects.create(conn_code=obj_conn,
                                                       assign_date_time=obj_vtt_d_conn.billing_code.assign_date_time,
                                                       conn_start_date=obj_vtt_d_conn.billing_code.conn_start_date,
                                                       conn_end_date=obj_vtt_d_conn.billing_code.conn_end_date,
                                                       bandwidth=obj_vtt_d_conn.billing_code.bandwidth,
                                                       link_validity=obj_vtt_d_conn.billing_code.link_validity,
                                                       payment_status=obj_vtt_d_conn.billing_code.payment_status,
                                                       amount=obj_vtt_d_conn.billing_code.amount,
                                                       payment_method=obj_vtt_d_conn.billing_code.payment_method,
                                                       netbanking_type=obj_vtt_d_conn.billing_code.netbanking_type,
                                                       transaction_id=obj_vtt_d_conn.billing_code.transaction_id,
                                                       transaction_receipt=obj_vtt_d_conn.billing_code.transaction_receipt,
                                                       billing_img=obj_vtt_d_conn.billing_code.billing_img,
                                                       ill_billing_receiver=obj_vtt_d_conn.billing_code.ill_billing_receiver,
                                                       ill_sign_id=obj_vtt_d_conn.billing_code.ill_sign_id,
                                                       ill_sign_time=obj_vtt_d_conn.billing_code.ill_sign_time,
                                                       )
    obj_ttv_bill.save()

    obj_ttv_d_conn = TTVIllDoneConnectionsDetails.objects.create(conn_code=obj_conn,
                                                                 active_status=obj_vtt_d_conn.active_status,
                                                                 sale_code=obj_ttv_sale,
                                                                 noc_code=obj_ttv_noc,
                                                                 fe_code=obj_ttv_fe,
                                                                 billing_code=obj_ttv_bill,
                                                                 )

    obj_ttv_d_conn.save()
    # change ill connection type
    obj_conn.ill_conn_type = conntype
    obj_conn.ill_vendor_code = ill_vendor
    obj_conn.save()

    # delete obj
    obj_vtt_bill = VTTIllBillingDetails.objects.get(id=obj_vtt_d_conn.billing_code.id)
    obj_vtt_bill.delete()

    obj_vtt_fe = VTTIllFieldEngineerDetails.objects.get(id=obj_vtt_d_conn.fe_code.id)
    obj_vtt_fe.delete()

    obj_vtt_noc = VTTIllNocDetails.objects.get(id=obj_vtt_d_conn.noc_code.id)
    obj_vtt_noc.delete()

    obj_vtt_fiber = VTTIllFiberTeam.objects.get(id=obj_vtt_d_conn.fiber_code.id)
    obj_vtt_fiber.delete()

    obj_vtt_sale = VTTIllSalesDetails.objects.get(id=obj_vtt_d_conn.sale_code.id)
    obj_vtt_sale.delete()

    # delete prev done connection obj
    obj_vtt_d_conn.delete()



def shifting_ttv_to_vtt(connid, conntype, ill_vendor_code, assign_fiber, media_img, switch_img, port_media_type,
                        fiber_core, pop_name,
                        ill_switch_ip, ill_switch_port_no, ill_sign_id):
    ill_vendor_code = int(ill_vendor_code)
    ill_vendor = IllVendors.objects.get(id=ill_vendor_code)
    assign_fiber_i = User.objects.get(id=assign_fiber)
    obj_conn = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
    obj_ttv_d_conn = TTVIllDoneConnectionsDetails.objects.get(conn_code__ill_custid=connid)
    obj_vtt_sale = VTTIllSalesDetails.objects.create(conn_code=obj_conn,
                                                     location_pin=obj_ttv_d_conn.sale_code.location_pin,
                                                     purchase_order_no=obj_ttv_d_conn.sale_code.purchase_order_no,
                                                     po_img=obj_ttv_d_conn.sale_code.po_img,
                                                     kyc_details=obj_ttv_d_conn.sale_code.kyc_details,
                                                     gst_no=obj_ttv_d_conn.sale_code.gst_no,
                                                     cust_cpn_name=obj_ttv_d_conn.sale_code.cust_cpn_name,
                                                     cust_cpn_num=obj_ttv_d_conn.sale_code.cust_cpn_num,
                                                     assign_fiber_engg=assign_fiber_i,
                                                     assign_date_time=obj_ttv_d_conn.sale_code.assign_date_time,
                                                     ill_sales_receiver=obj_ttv_d_conn.sale_code.ill_sales_receiver,
                                                     ill_sign_id=obj_ttv_d_conn.sale_code.ill_sign_id,
                                                     ill_sign_time=obj_ttv_d_conn.sale_code.ill_sign_time,
                                                     assign_status=obj_ttv_d_conn.sale_code.assign_status, )
    obj_vtt_sale.save()

    obj_vtt_fiber = VTTIllFiberTeam.objects.create(conn_code=obj_conn,
                                                   media_img=media_img,
                                                   switch_img=switch_img,
                                                   port_media_type=port_media_type,
                                                   fiber_core=fiber_core,
                                                   pop_name=pop_name,
                                                   assign_noc=obj_ttv_d_conn.sale_code.assign_noc,
                                                   assign_date_time=datetime.now(),
                                                   ill_fiber_receiver=assign_fiber,
                                                   ill_sign_id=ill_sign_id,
                                                   ill_sign_time=datetime.now(),
                                                   assign_status=True, )
    obj_vtt_fiber.save()
    obj_vtt_noc = VTTIllNocDetails.objects.create(conn_code=obj_conn,
                                                  ill_ip=obj_ttv_d_conn.noc_code.ill_ip,
                                                  ill_subnet=obj_ttv_d_conn.noc_code.ill_subnet,
                                                  ill_gateway=obj_ttv_d_conn.noc_code.ill_gateway,
                                                  ill_dns=obj_ttv_d_conn.noc_code.ill_dns,
                                                  ill_dns2=obj_ttv_d_conn.noc_code.ill_dns2,
                                                  ill_switch_ip=ill_switch_ip,
                                                  ill_switch_port_no=ill_switch_port_no,
                                                  ill_bandwidth=obj_ttv_d_conn.noc_code.ill_bandwidth,
                                                  ill_vland=obj_ttv_d_conn.noc_code.ill_vland,
                                                  ill_mac_add=obj_ttv_d_conn.noc_code.ill_mac_add,
                                                  ill_routing_status=obj_ttv_d_conn.noc_code.ill_routing_status,
                                                  assign_field_engg=obj_ttv_d_conn.noc_code.assign_field_engg,
                                                  assign_date_time=obj_ttv_d_conn.noc_code.assign_date_time,
                                                  ill_noc_receiver=obj_ttv_d_conn.noc_code.ill_noc_receiver,
                                                  ill_sign_id=obj_ttv_d_conn.noc_code.ill_sign_id,
                                                  ill_sign_time=obj_ttv_d_conn.noc_code.ill_sign_time,
                                                  assign_status=obj_ttv_d_conn.noc_code.assign_status, )
    obj_vtt_noc.save()
    obj_vtt_fe = VTTIllFieldEngineerDetails.objects.create(conn_code=obj_conn,
                                                           link_status=obj_ttv_d_conn.fe_code.link_status,
                                                           cust_cpn_name=obj_ttv_d_conn.fe_code.cust_cpn_name,
                                                           cust_cpn_num=obj_ttv_d_conn.fe_code.cust_cpn_num,
                                                           connectivity_img=obj_ttv_d_conn.fe_code.connectivity_img,
                                                           assign_billing=obj_ttv_d_conn.fe_code.assign_billing,
                                                           assign_date_time=obj_ttv_d_conn.fe_code.assign_date_time,
                                                           ill_field_engg_receiver=obj_ttv_d_conn.fe_code.ill_field_engg_receiver,
                                                           ill_sign_id=obj_ttv_d_conn.fe_code.ill_sign_id,
                                                           ill_sign_time=obj_ttv_d_conn.fe_code.ill_sign_time,
                                                           assign_status=obj_ttv_d_conn.fe_code.assign_status, )
    obj_vtt_fe.save()
    obj_vtt_bill = VTTIllBillingDetails.objects.create(conn_code=obj_conn,
                                                       assign_date_time=obj_ttv_d_conn.billing_code.assign_date_time,
                                                       conn_start_date=obj_ttv_d_conn.billing_code.conn_start_date,
                                                       conn_end_date=obj_ttv_d_conn.billing_code.conn_end_date,
                                                       bandwidth=obj_ttv_d_conn.billing_code.bandwidth,
                                                       link_validity=obj_ttv_d_conn.billing_code.link_validity,
                                                       payment_status=obj_ttv_d_conn.billing_code.payment_status,
                                                       amount=obj_ttv_d_conn.billing_code.amount,
                                                       payment_method=obj_ttv_d_conn.billing_code.payment_method,
                                                       netbanking_type=obj_ttv_d_conn.billing_code.netbanking_type,
                                                       transaction_id=obj_ttv_d_conn.billing_code.transaction_id,
                                                       transaction_receipt=obj_ttv_d_conn.billing_code.transaction_receipt,
                                                       billing_img=obj_ttv_d_conn.billing_code.billing_img,
                                                       ill_billing_receiver=obj_ttv_d_conn.billing_code.ill_billing_receiver,
                                                       ill_sign_id=obj_ttv_d_conn.billing_code.ill_sign_id,
                                                       ill_sign_time=obj_ttv_d_conn.billing_code.ill_sign_time,
                                                       )
    obj_vtt_bill.save()

    obj_vtt_d_conn = VTTIllDoneConnectionsDetails.objects.create(conn_code=obj_conn,
                                                                 active_status=obj_ttv_d_conn.active_status,
                                                                 sale_code=obj_vtt_sale,
                                                                 fiber_code=obj_vtt_fiber,
                                                                 noc_code=obj_vtt_noc,
                                                                 fe_code=obj_vtt_fe,
                                                                 billing_code=obj_vtt_bill,
                                                                 )
    obj_vtt_d_conn.save()
    # change ill connection type
    obj_conn.ill_conn_type = conntype
    obj_conn.ill_vendor_code = ill_vendor
    obj_conn.save()

    # delete obj
    obj_ttv_bill = TTVIllBillingDetails.objects.get(id=obj_ttv_d_conn.billing_code.id)
    obj_ttv_bill.delete()

    obj_ttv_fe = TTVIllFieldEngineerDetails.objects.get(id=obj_ttv_d_conn.fe_code.id)
    obj_ttv_fe.delete()

    obj_ttv_noc = TTVIllNocDetails.objects.get(id=obj_ttv_d_conn.noc_code.id)
    obj_ttv_noc.delete()

    obj_ttv_sale = TTVIllSalesDetails.objects.get(id=obj_ttv_d_conn.sale_code.id)
    obj_ttv_sale.delete()

    # delete prev done connection obj
    obj_ttv_d_conn.delete()



@login_required(login_url='login')
def shiftconnverify(request):
    context = {}
    if request.method == 'POST':
        tlcobj = ''
        connid = request.POST.get('conn_id_2')
        conntype = request.POST.get('ill_conn_type')
        objpossible = False
        try:
            tlcobj = ThreesaIllConnectionsDetails.objects.get(ill_custid=connid)
            if not tlcobj.ill_conn_type == conntype:
                objpossible = True
        except:
            objpossible = False
        if objpossible:
            if conntype == '1':
                if tlcobj.ill_conn_type == '2':
                    assign_fiber = request.POST.get('assign_fiber')
                    media_img = request.POST.get('media_img')
                    switch_img = request.POST.get('switch_img')
                    port_media_type = request.POST.get('port_media_type')
                    fiber_core = request.POST.get('fiber_core')
                    pop_name = request.POST.get('pop_name')
                    ill_switch_ip = request.POST.get('ill_switch_ip')
                    ill_switch_port_no = request.POST.get('ill_switch_port_no')
                    ill_sign_id = request.user.username
                    shifting_ttv_to_threesa(connid, conntype, assign_fiber, media_img, switch_img, port_media_type,
                                            fiber_core,
                                            pop_name, ill_switch_ip, ill_switch_port_no, ill_sign_id)
                elif tlcobj.ill_conn_type == '3':
                    shifting_vtt_to_threesa(connid, conntype)
            elif conntype == '2':
                if tlcobj.ill_conn_type == '1':
                    ill_vendor_code = request.POST.get('ill_vendor_code')
                    shifting_threesa_to_ttv(connid, conntype, ill_vendor_code)
                elif tlcobj.ill_conn_type == '3':
                    ill_vendor_code = request.POST.get('ill_vendor_code')
                    shifting_vtt_to_ttv(connid, conntype, ill_vendor_code)
            elif conntype == '3':
                if tlcobj.ill_conn_type == '1':
                    ill_vendor_code = request.POST.get('ill_vendor_code')
                    shifting_threesa_to_vtt(connid, conntype, ill_vendor_code)
                elif tlcobj.ill_conn_type == '2':
                    ill_vendor_code = request.POST.get('ill_vendor_code')
                    assign_fiber = request.POST.get('assign_fiber')
                    media_img = request.POST.get('media_img')
                    switch_img = request.POST.get('switch_img')
                    port_media_type = request.POST.get('port_media_type')
                    fiber_core = request.POST.get('fiber_core')
                    pop_name = request.POST.get('pop_name')
                    ill_switch_ip = request.POST.get('ill_switch_ip')
                    ill_switch_port_no = request.POST.get('ill_switch_port_no')
                    ill_sign_id = request.user.username
                    shifting_ttv_to_vtt(connid, conntype, ill_vendor_code, assign_fiber, media_img, switch_img,
                                        port_media_type,
                                        fiber_core,
                                        pop_name, ill_switch_ip, ill_switch_port_no, ill_sign_id)


            shift_from = ''
            shift_to = ''
            if tlcobj.ill_conn_type == '1':
                shift_from = 'Threesa'
            elif tlcobj.ill_conn_type == '2':
                shift_from = 'Threesa Through Vendor'
            elif tlcobj.ill_conn_type == '3':
                shift_from = 'Vendor Through Threesa'

            if conntype == '1':
                shift_to = 'Threesa'
            elif conntype == '2':
                shift_to = 'Threesa Through Vendor'
            elif conntype == '3':
                shift_to = 'Vendor Through Threesa'

            shift_his_obj = IllConnectionShiftHistory.objects.create(shifter_user=request.user.username,
                                                                     shift_conn_id=connid, shift_from=shift_from,
                                                                     shift_to=shift_to, shift_date=datetime.now())
            shift_his_obj.save()
            context = {}
        else:
            context = {}

    return render(request, 'shiftconnection/shift_conn_shiftsuccess.html', context)


@login_required(login_url='login')
def shiftconnhistory(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    obj_Shifthistoryall = IllConnectionShiftHistory.objects.all()

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        obj_Shifthistoryall = IllConnectionShiftHistory.objects.filter(Q(shifter_user__icontains=searchguery) |
                                                                       Q(shift_conn_id__icontains=searchguery) |
                                                                       Q(shift_from__icontains=searchguery) |
                                                                       Q(shift_to__icontains=searchguery) |
                                                                       Q(shift_date__icontains=searchguery)
                                                                       )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Shift-Ill-Conn-History.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Shift Ill Connection History')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['User', 'Connection Id', 'Shifted From', 'shifted To', 'Shifted Date']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = obj_Shifthistoryall.values_list('shifter_user', 'shift_conn_id', 'shift_from', 'shift_to', 'shift_date')
        for row in rows:
            row = list(row)
            row[4] = str(row[4].strftime("%d/%m/%Y %I:%M %p"))
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response

    page = request.GET.get('page', 1)
    itemperform = Num_Item_Per_Page()

    num_page = request.GET.get('num_page')
    if not num_page:
        num_page = 10
    num_page = int(num_page)

    paginator = Paginator(obj_Shifthistoryall, num_page)
    try:
        obj_Shifthistoryall = paginator.page(page)
    except PageNotAnInteger:
        obj_Shifthistoryall = paginator.page(1)
    except EmptyPage:
        obj_Shifthistoryall = paginator.page(paginator.num_pages)

    context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'obj_Shifthistoryall': obj_Shifthistoryall,
               'itemperform': itemperform,
               'rowcount': str(num_page)}
    return render(request, 'shiftconnection/shift_conn_history.html', context)


@login_required(login_url='login')
def threesaipping(request, pipaddress):
    context = {}

    if pipaddress == '':
        context['ping_output'] = 'Please enter a domain name!'

    else:
        output = ping(pipaddress, size=24, count=10)
        context['ping_output'] = output

    return render(request, 'ping.html', context)


def threesalocation(request):
    context = {'mylat': 19.20439905059907,
               'mylon': 72.98404471028572
               }
    return render(request, 'location.html', context)


@login_required(login_url='login')
def downloadbackupdata(request):
    conn = sqlite3.connect('db.sqlite3')
    with io.open('backup.sql', 'w') as f:
        for linha in conn.iterdump():
            f.write('%s\n' % linha)
    conn.close()
    folder_path = os.path.join(BASE_DIR, 'media')
    zip_path = BytesIO()
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, '/media/' + file_path[len_dir_path:])
        zipf.write(os.path.join(BASE_DIR, 'backup.sql'), '/dbsql/backup.sql')

    # my_zip_file = open(os.path.join(BASE_DIR, 'Folder.zip'))
    response = HttpResponse(zip_path.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'dbbackup.zip'
    return response


@login_required(login_url='login')
def showbillinghistory(request, connid):
    objbillinghs = IllBillingHistory.objects.filter(conn_code=connid)
    if request.method == 'POST' and request.POST.get('exportexcelbillhistory'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Ill-Conn-Billing-History.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Ill Connection Billing History')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Connection ID', 'Connection Type', 'Assigned Date and time',
                   'Connection Activation Date', 'Connection Expiry Date', 'Connection validity',
                   'Payment Status','amount','Payment Method','Net Banking Type', 'Transaction ID', 'Accountant ID']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = []

        for objbillinghs_1 in objbillinghs:
            rows.append([objbillinghs_1.conn_code if objbillinghs_1.conn_code else '',
                         objbillinghs_1.conn_type if objbillinghs_1.conn_type else '',
                         str(objbillinghs_1.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objbillinghs_1.assign_date_time else '',
                         str(objbillinghs_1.conn_start_date) if objbillinghs_1.conn_start_date else '',
                         str(objbillinghs_1.conn_end_date) if objbillinghs_1.conn_end_date else '',
                         objbillinghs_1.link_validity if objbillinghs_1.link_validity else '',
                         objbillinghs_1.get_payment_status_display() if objbillinghs_1.get_payment_status_display() else '',
                         objbillinghs_1.amount if objbillinghs_1.amount else '',
                         objbillinghs_1.get_payment_method_display() if objbillinghs_1.get_payment_method_display() else '',
                         objbillinghs_1.get_netbanking_type_display() if objbillinghs_1.get_netbanking_type_display() else '',
                         objbillinghs_1.transaction_id if objbillinghs_1.transaction_id else '',
                         objbillinghs_1.ill_billing_receiver if objbillinghs_1.ill_billing_receiver else '',
                         ])

        for row in rows:
            row_num += 1
            row = list(row)
            for col_num in range(len(row)):
                if row[col_num]:
                    row[col_num] = str(row[col_num])
                else:
                    row[col_num] = ''
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    context = {'objbillinghs': objbillinghs,'connid':connid }
    return render(request, 'threesaapptemp/thistorymodel.html', context)



