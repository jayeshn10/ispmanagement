from datetime import datetime, date, timedelta

import xlwt
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from sitemanager.forms import Num_Item_Per_Page
from sitemanager.models import RejectionMessage, ThreesaIllConnectionsDetails, IllNotification, IllBillingHistory
from threesaillconnections.decorators import addillcon_authentication
from threesaillconnections.filters import ThreesaIllFeasibleConnDetailsFilter
from threesaillconnections.forms import AddIllConForm, AddSalesDetailsForm, EditSalesDetailsForm, \
    AddFiberDetailsForm, EditFiberDetailsForm, AddNocDetailsForm, EditNocDetailsForm, AddFieldEnggDetailsForm, \
    EditFieldEnggDetailsForm, AddBillingDetailsForm, EditBillingDetailsForm, RenewBillingDetailsForm
from threesaillconnections.models import \
    ThreesaIllSalesDetails, ThreesaIllFiberTeam, \
    ThreesaIllNocDetails, ThreesaIllFieldEngineerDetails, \
    ThreesaIllBillingDetails, ThreesaIllDoneConnectionsDetails


@login_required(login_url='login')
def threesaillconnections(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objfeasible = ThreesaIllDoneConnectionsDetails.objects.all()

    connfilter = ThreesaIllFeasibleConnDetailsFilter(request.GET, queryset=objfeasible)
    objfeasible = connfilter.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        objfeasible = ThreesaIllDoneConnectionsDetails.objects.filter(Q(conn_code__ill_custid__icontains=searchguery)
                                                                      | Q(
            conn_code__ill_cust_name__icontains=searchguery)
                                                                      | Q(
            conn_code__ill_cust_address__icontains=searchguery)
                                                                      | Q(conn_code__ill_gendate__icontains=searchguery)
                                                                      | Q(
            billing_code__conn_start_date__icontains=searchguery)
                                                                      | Q(billing_code__conn_end_date=searchguery)
                                                                      | Q(active_status__icontains=searchguery)
                                                                      )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="T-Ill-done-Connections.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Threesa Ill Done Connections')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        first_columns = ['Connection Details',
                         'Sales details',
                         'Fiber details',
                         'NOC details',
                         'Field Engineer details',
                         'Billing details',
                         ]

        ws.write_merge(0, 0, 0, 12, 'Connection Details', font_style)
        ws.write_merge(0, 0, 13, 22, 'Sales details', font_style)
        ws.write_merge(0, 0, 23, 30, 'Fiber details', font_style)
        ws.write_merge(0, 0, 31, 46, 'NOC details', font_style)
        ws.write_merge(0, 0, 47, 54, 'Field Engineer details', font_style)
        ws.write_merge(0, 0, 55, 62, 'Billing details', font_style)

        row_num = 1
        columns = ['Connection ID',
                   'Lead Generation Date',
                   'Customer Name', 'Customer Address',
                   'Feasibility Status', 'Sales Person ID',
                   'Assign Status', 'Sign Verification Id',
                   'Sign Verification Time', 'Connection Activation Date',
                   'Connection Expiry Date', 'Connection validity',
                   'Status',
                   'Assigned Date and time',
                   'Location Pin', 'Purchase Order No',
                   'GST No.', 'Customer Contact Person Name',
                   'Customer Contact Person Number', 'Assign Fiber Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assigned Date and time',
                   'Port', 'Fiber Core',
                   'POP Name', 'Assign NOC Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assigned Date and time',
                   'ILL IP', 'Ill Subnet',
                   'Ill Gateway', 'Ill DNS',
                   'ILL DNS2', 'Ill Switch IP',
                   'Ill Switch Port No', 'Ill Bandwidth',
                   'Ill VLAND', 'MAC Address',
                   'Routing Status', 'Assign Field Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assigned Date and time',
                   'Link Status',
                   'Customer Contact Person Name',
                   'Customer Contact Person Number', 'Assign Billing',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assigned Date and time',
                   'Payment Status','amount', 'Payment Method', 'Net Banking Type', 'Transaction ID',
                   'Sign Verification ID', 'Sign Verification Time'
                   ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = []

        for objfeasible_1 in objfeasible:
            rows.append([objfeasible_1.conn_code.ill_custid if objfeasible_1.conn_code else '',
                         str(objfeasible_1.conn_code.ill_gendate.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.conn_code else '',
                         objfeasible_1.conn_code.ill_cust_name if objfeasible_1.conn_code else '',
                         objfeasible_1.conn_code.ill_cust_address if objfeasible_1.conn_code else '',
                         objfeasible_1.conn_code.get_ill_feasibility_display() if objfeasible_1.conn_code else '',
                         objfeasible_1.conn_code.ill_sales_person.username if objfeasible_1.conn_code else '',
                         objfeasible_1.conn_code.get_assign_status_display() if objfeasible_1.conn_code else '',
                         objfeasible_1.conn_code.ill_sign_id if objfeasible_1.conn_code else '',
                         str(objfeasible_1.conn_code.ill_sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.conn_code.ill_sign_time else '',
                         str(objfeasible_1.billing_code.conn_start_date) if objfeasible_1.billing_code else '',
                         str(objfeasible_1.billing_code.conn_end_date) if objfeasible_1.billing_code else '',
                         objfeasible_1.billing_code.link_validity if objfeasible_1.billing_code else '',
                         objfeasible_1.get_active_status_display() if objfeasible_1.active_status else 'Deactive',
                         str(objfeasible_1.sale_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.location_pin if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.purchase_order_no if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.gst_no if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.cust_cpn_name if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.cust_cpn_num if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.assign_fiber_engg.username if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.get_assign_status_display() if objfeasible_1.sale_code else '',
                         objfeasible_1.sale_code.ill_sign_id if objfeasible_1.sale_code else '',
                         str(objfeasible_1.sale_code.ill_sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.sale_code else '',
                         str(objfeasible_1.fiber_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.fiber_code else '',
                         objfeasible_1.fiber_code.get_port_media_type_display() if objfeasible_1.fiber_code else '',
                         objfeasible_1.fiber_code.get_fiber_core_display() if objfeasible_1.fiber_code else '',
                         objfeasible_1.fiber_code.pop_name if objfeasible_1.fiber_code else '',
                         objfeasible_1.fiber_code.assign_noc.username if objfeasible_1.fiber_code else '',
                         objfeasible_1.fiber_code.get_assign_status_display() if objfeasible_1.fiber_code else '',
                         objfeasible_1.fiber_code.ill_sign_id if objfeasible_1.fiber_code else '',
                         str(objfeasible_1.fiber_code.ill_sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.fiber_code else '',
                         str(objfeasible_1.noc_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_ip if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_subnet if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_gateway if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_dns if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_dns2 if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_switch_ip if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_switch_port_no if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_bandwidth if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_vland if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_mac_add if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.get_ill_routing_status_display() if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.assign_field_engg.username if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.get_assign_status_display() if objfeasible_1.noc_code else '',
                         objfeasible_1.noc_code.ill_sign_id if objfeasible_1.noc_code else '',
                         str(objfeasible_1.noc_code.ill_sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.noc_code else '',
                         str(objfeasible_1.fe_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.fe_code else '',
                         objfeasible_1.fe_code.get_link_status_display() if objfeasible_1.fe_code else '',
                         objfeasible_1.fe_code.cust_cpn_name if objfeasible_1.fe_code else '',
                         objfeasible_1.fe_code.cust_cpn_num if objfeasible_1.fe_code else '',
                         objfeasible_1.fe_code.assign_billing.username if objfeasible_1.fe_code else '',
                         objfeasible_1.fe_code.get_assign_status_display() if objfeasible_1.fe_code else '',
                         objfeasible_1.fe_code.ill_sign_id if objfeasible_1.fe_code else '',
                         str(objfeasible_1.fe_code.ill_sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.fe_code else '',
                         str(objfeasible_1.billing_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.billing_code else '',
                         objfeasible_1.billing_code.get_payment_status_display() if objfeasible_1.billing_code else '',
                         objfeasible_1.billing_code.amount if objfeasible_1.billing_code else '',
                         objfeasible_1.billing_code.get_payment_method_display() if objfeasible_1.billing_code else '',
                         objfeasible_1.billing_code.get_netbanking_type_display() if objfeasible_1.billing_code else '',
                         objfeasible_1.billing_code.transaction_id if objfeasible_1.billing_code else '',
                         objfeasible_1.billing_code.ill_sign_id if objfeasible_1.billing_code else '',
                         str(objfeasible_1.billing_code.ill_sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objfeasible_1.billing_code else '',
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

    page = request.GET.get('page', 1)
    itemperform = Num_Item_Per_Page()

    num_page = request.GET.get('num_page')
    if not num_page:
        num_page = 10
    num_page = int(num_page)

    paginator = Paginator(objfeasible, num_page)
    try:
        objfeasible = paginator.page(page)
    except PageNotAnInteger:
        objfeasible = paginator.page(1)
    except EmptyPage:
        objfeasible = paginator.page(paginator.num_pages)

    context = {'objfeasibles': objfeasible, 'objntfc_all': objntfc_all,
               'connfilter': connfilter, 'objmsgs': objmsg, 'itemperform': itemperform, 'rowcount': str(num_page)}
    return render(request, 'threesaapptemp/threesaillconn_app_temp.html', context)


@login_required(login_url='login')
@addillcon_authentication
def addillcon(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    form = AddIllConForm()
    if request.method == 'POST':
        form = AddIllConForm(request.POST)

        if form.is_valid():
            newform = form.save(commit=False)
            newform.ill_sign_id = request.user.username
            newform.ill_sign_time = datetime.now()
            if not newform.ill_feasibility:
                newform.assign_status = False
            newform.save()
            if newform.ill_conn_type == '1':
                if newform.ill_feasibility:
                    doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.create(conn_code=newform, )
                    doneconn_obj.save()
                    if newform.assign_status:
                        salenotification_obj = IllNotification.objects.create(
                            conn_code=newform, ill_ntfc_sender=request.user.username, ill_prev_assign_obj_id=newform.id,
                            ill_ntfc_receiver=newform.ill_sales_person.username, assign_date_time=newform.ill_sign_time,
                            accept_mod_url="addillsales", reject_mod_url="rejectillsales", ill_app_name="1")
                        salenotification_obj.save()

            if newform.ill_feasibility:
                return redirect('threesaillconnections')
            else:
                return redirect('threesaillconnectionsoverallleads')
    context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg}
    return render(request, 'threesaapptemp/add_ill_connection.html', context)


@login_required(login_url='login')
def addillsales(request, nid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objsn = IllNotification.objects.get(id=nid)
    finst = {'conn_code': objsn.conn_code, }
    form = AddSalesDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddSalesDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)

            newform.conn_code = objsn.conn_code
            newform.assign_date_time = objsn.assign_date_time
            newform.ill_sales_receiver = objsn.ill_ntfc_receiver
            newform.ill_sign_id = request.user.username
            newform.ill_sign_time = datetime.now()

            newform.save()
            doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.get(conn_code=newform.conn_code)
            doneconn_obj.sale_code = newform
            doneconn_obj.save()

            if newform.assign_status:
                fibernotification_obj = IllNotification.objects.create(
                    conn_code=newform.conn_code, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_fiber_engg.username, assign_date_time=newform.ill_sign_time,
                    accept_mod_url="addillfiber", reject_mod_url="rejectillfiber", ill_app_name="1")
                fibernotification_obj.save()

            objsn.delete()

            return redirect('threesaillconnections')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objsn': objsn, 'objmsgs': objmsg}
    return render(request, 'threesaapptemp/add_ill_sales.html', context)


@login_required(login_url='login')
def threesaillsalesdetails(request):
    return redirect('threesaillconnections')


@login_required(login_url='login')
def rejectillsales(request, did):
    objsn = IllNotification.objects.get(id=did)
    objillcon = ThreesaIllConnectionsDetails.objects.get(id=objsn.ill_prev_assign_obj_id)
    objillcon.assign_status = False
    objillcon.save()
    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objsn.ill_ntfc_sender,
                                                conn_code=objillcon.ill_custid, rej_module_name='sales')
    rejmsgobj.save()
    delobj = objsn.id
    objsn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'threesaillsalesdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def editillsales(request, sid):
    etlsobj = ThreesaIllSalesDetails.objects.get(id=sid)
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    if request.user.username == etlsobj.ill_sales_receiver or request.user.is_staff:
        form = EditSalesDetailsForm(instance=etlsobj)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditSalesDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)

                etlsobj.location_pin = newform.location_pin
                etlsobj.purchase_order_no = newform.purchase_order_no
                etlsobj.gst_no = newform.gst_no
                etlsobj.cust_cpn_name = newform.cust_cpn_name
                etlsobj.cust_cpn_num = newform.cust_cpn_num
                etlsobj.ill_sign_id = request.user.username
                etlsobj.ill_sign_time = datetime.now()

                if not newform.po_img == 'emptyfile':
                    etlsobj.po_img = newform.po_img

                if not newform.kyc_details == 'emptyfile':
                    etlsobj.kyc_details = newform.kyc_details

                if not etlsobj.assign_status:
                    etlsobj.assign_fiber_engg = newform.assign_fiber_engg
                    if newform.assign_status:
                        etlsobj.assign_status = newform.assign_status

                etlsobj.save()
                if newform.assign_status:
                    fibernotification_obj = IllNotification.objects.create(
                        conn_code=etlsobj.conn_code, ill_ntfc_sender=request.user.username,
                        ill_prev_assign_obj_id=etlsobj.id,
                        ill_ntfc_receiver=etlsobj.assign_fiber_engg.username, assign_date_time=etlsobj.ill_sign_time,
                        accept_mod_url="addillfiber", reject_mod_url="rejectillfiber", ill_app_name="1")
                    fibernotification_obj.save()

                return redirect(prevurl)
        EditPer = True
        context = {
            'form': form,
            'etlsobj': etlsobj,
            'objntfc_all': objntfc_all,
            'EditPer': EditPer,
            'objmsgs': objmsg,
        }
    else:
        EditPer = False
        context = {
            'etlsobj': etlsobj,
            'objntfc_all': objntfc_all,
            'EditPer': EditPer,
            'objmsgs': objmsg,
        }

    return render(request, 'threesaapptemp/edit_ill_sales.html', context)


@login_required(login_url='login')
def threesaillfiberdetails(request):
    return redirect('threesaillconnections')


@login_required(login_url='login')
def addillfiber(request, afid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objfn = IllNotification.objects.get(id=afid)
    finst = {'conn_code': objfn.conn_code, }
    form = AddFiberDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddFiberDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.conn_code = objfn.conn_code
            newform.assign_date_time = objfn.assign_date_time
            newform.ill_fiber_receiver = objfn.ill_ntfc_receiver
            newform.ill_sign_id = request.user.username
            newform.ill_sign_time = datetime.now()

            if not newform.assign_date_time == objfn.assign_date_time:
                newform.assign_date_time = objfn.assign_date_time
            newform.save()
            doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.get(conn_code=newform.conn_code)
            doneconn_obj.fiber_code = newform
            doneconn_obj.save()

            if newform.assign_status:
                nocnotification_obj = IllNotification.objects.create(
                    conn_code=newform.conn_code, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_noc.username, assign_date_time=newform.ill_sign_time,
                    accept_mod_url="addillnoc", reject_mod_url="rejectillnoc", ill_app_name="1")
                nocnotification_obj.save()

            objfn.delete()

            return redirect('threesaillconnections')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objfn': objfn, 'objmsgs': objmsg}
    return render(request, 'threesaapptemp/add_ill_fiber.html', context)


@login_required(login_url='login')
def editillfiber(request, efid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    etlfobj = ThreesaIllFiberTeam.objects.get(id=efid)

    if request.user.username == etlfobj.ill_fiber_receiver or request.user.is_staff:
        form = EditFiberDetailsForm(instance=etlfobj)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditFiberDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                etlfobj.port_media_type = newform.port_media_type
                etlfobj.fiber_core = newform.fiber_core
                etlfobj.pop_name = newform.pop_name
                etlfobj.ill_sign_id = request.user.username
                etlfobj.ill_sign_time = datetime.now()

                if not newform.media_img == 'emptyfile':
                    etlfobj.media_img = newform.media_img

                if not newform.switch_img == 'emptyfile':
                    etlfobj.switch_img = newform.switch_img

                if not etlfobj.assign_status:
                    etlfobj.assign_noc = newform.assign_noc
                    if newform.assign_status:
                        etlfobj.assign_status = newform.assign_status
                        nocnotification_obj = IllNotification.objects.create(
                            conn_code=etlfobj.conn_code, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=etlfobj.id,
                            ill_ntfc_receiver=etlfobj.assign_noc.username, assign_date_time=etlfobj.ill_sign_time,
                            accept_mod_url="addillnoc", reject_mod_url="rejectillnoc", ill_app_name="1")
                        nocnotification_obj.save()

                etlfobj.save()
                return redirect(prevurl)

        EditPer = True
        context = {
            'form': form,
            'etlfobj': etlfobj,
            'objntfc_all': objntfc_all,
            'EditPer': EditPer,
            'objmsgs': objmsg,
        }

    else:
        EditPer = False
        context = {
            'etlfobj': etlfobj,
            'objntfc_all': objntfc_all,
            'EditPer': EditPer,
            'objmsgs': objmsg,
        }

    return render(request, 'threesaapptemp/edit_ill_fiber.html', context)


@login_required(login_url='login')
def rejectillfiber(request, rfid):
    objfn = IllNotification.objects.get(id=rfid)
    objillsale = ThreesaIllSalesDetails.objects.get(id=objfn.ill_prev_assign_obj_id)
    objillsale.assign_status = False
    objillsale.save()
    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objfn.ill_ntfc_sender,
                                                conn_code=objillsale.conn_code.ill_custid, rej_module_name='Fiber')
    rejmsgobj.save()
    delobj = objfn.id
    objfn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'threesaillfiberdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def threesaillnocdetails(request):
    return redirect('threesaillconnections')


@login_required(login_url='login')
def addillnoc(request, anid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objnn = IllNotification.objects.get(id=anid)
    finst = {'conn_code': objnn.conn_code, }
    form = AddNocDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddNocDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.conn_code = objnn.conn_code
            newform.assign_date_time = objnn.assign_date_time
            newform.ill_noc_receiver = objnn.ill_ntfc_receiver
            newform.ill_sign_id = request.user.username
            newform.ill_sign_time = datetime.now()

            if not newform.assign_date_time == objnn.assign_date_time:
                newform.assign_date_time = objnn.assign_date_time
            newform.save()

            doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.get(conn_code=newform.conn_code)
            doneconn_obj.noc_code = newform
            doneconn_obj.save()

            if newform.assign_status:
                fieldengg_notification_obj = IllNotification.objects.create(
                    conn_code=newform.conn_code, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_field_engg.username, assign_date_time=newform.ill_sign_time,
                    accept_mod_url="addillfieldengg", reject_mod_url="rejectillfieldengg", ill_app_name="1")
                fieldengg_notification_obj.save()

            objnn.delete()

            return redirect('threesaillconnections')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objnn': objnn, 'objmsgs': objmsg}
    return render(request, 'threesaapptemp/add_ill_noc.html', context)


@login_required(login_url='login')
def editillnoc(request, enid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    etlnobj = ThreesaIllNocDetails.objects.get(id=enid)

    if request.user.username == etlnobj.ill_noc_receiver or request.user.is_staff:
        form = EditNocDetailsForm(instance=etlnobj)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditNocDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                etlnobj.ill_ip = newform.ill_ip
                etlnobj.ill_subnet = newform.ill_subnet
                etlnobj.ill_gateway = newform.ill_gateway
                etlnobj.ill_dns = newform.ill_dns
                etlnobj.ill_dns2 = newform.ill_dns2
                etlnobj.ill_switch_ip = newform.ill_switch_ip
                etlnobj.ill_switch_port_no = newform.ill_switch_port_no
                etlnobj.ill_bandwidth = newform.ill_bandwidth
                etlnobj.ill_vland = newform.ill_vland
                etlnobj.ill_mac_add = newform.ill_mac_add
                etlnobj.ill_routing_status = newform.ill_routing_status
                etlnobj.ill_sign_id = request.user.username
                etlnobj.ill_sign_time = datetime.now()

                if not etlnobj.assign_status:
                    etlnobj.assign_field_engg = newform.assign_field_engg
                    if newform.assign_status:
                        etlnobj.assign_status = newform.assign_status
                        fieldengg_notification_obj = IllNotification.objects.create(
                            conn_code=etlnobj.conn_code, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=etlnobj.id,
                            ill_ntfc_receiver=etlnobj.assign_field_engg.username,
                            assign_date_time=etlnobj.ill_sign_time,
                            accept_mod_url="addillfieldengg", reject_mod_url="rejectillfieldengg", ill_app_name="1")
                        fieldengg_notification_obj.save()

                etlnobj.save()

                return redirect(prevurl)

        EditPer = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'etlnobj': etlnobj, 'EditPer': EditPer, 'objmsgs': objmsg}
    else:
        EditPer = False
        context = {'objntfc_all': objntfc_all,
                   'etlnobj': etlnobj,
                   'EditPer': EditPer,
                   'objmsgs': objmsg,
                   }

    return render(request, 'threesaapptemp/edit_ill_noc.html', context)


@login_required(login_url='login')
def rejectillnoc(request, rnid):
    objnn = IllNotification.objects.get(id=rnid)
    objillfiber = ThreesaIllFiberTeam.objects.get(id=objnn.ill_prev_assign_obj_id)
    objillfiber.assign_status = False
    objillfiber.save()

    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objnn.ill_ntfc_sender,
                                                conn_code=objillfiber.conn_code.ill_custid, rej_module_name='Noc')
    rejmsgobj.save()

    delobj = objnn.id
    objnn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'threesaillnocdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def threesaillfieldenggdetails(request):
    return redirect('threesaillconnections')


@login_required(login_url='login')
def addillfieldengg(request, afeid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objfen = IllNotification.objects.get(id=afeid)
    finst = {'conn_code': objfen.conn_code, }
    form = AddFieldEnggDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddFieldEnggDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.conn_code = objfen.conn_code
            newform.assign_date_time = objfen.assign_date_time
            newform.ill_field_engg_receiver = objfen.ill_ntfc_receiver
            newform.ill_sign_id = request.user.username
            newform.ill_sign_time = datetime.now()

            if not newform.assign_date_time == objfen.assign_date_time:
                newform.assign_date_time = objfen.assign_date_time
            newform.save()

            doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.get(conn_code=newform.conn_code)

            doneconn_obj.fe_code = newform
            doneconn_obj.save()

            if newform.assign_status:
                billing_notification_obj = IllNotification.objects.create(
                    conn_code=newform.conn_code, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_billing.username,
                    assign_date_time=newform.ill_sign_time,
                    accept_mod_url="addillbilling", reject_mod_url="rejectillbilling", ill_app_name="1")
                billing_notification_obj.save()

            objfen.delete()

            return redirect('threesaillconnections')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objfen': objfen, 'objmsgs': objmsg}
    return render(request, 'threesaapptemp/add_ill_fieldengg.html', context)


@login_required(login_url='login')
def editillfieldengg(request, efeid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    etlfeobj = ThreesaIllFieldEngineerDetails.objects.get(id=efeid)

    if request.user.username == etlfeobj.ill_field_engg_receiver or request.user.is_staff:
        form = EditFieldEnggDetailsForm(instance=etlfeobj)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditFieldEnggDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                etlfeobj.link_status = newform.link_status
                etlfeobj.cust_cpn_name = newform.cust_cpn_name
                etlfeobj.cust_cpn_num = newform.cust_cpn_num
                etlfeobj.connectivity_img = newform.connectivity_img
                etlfeobj.ill_sign_id = request.user.username
                etlfeobj.ill_sign_time = datetime.now()

                if not newform.connectivity_img == 'emptyfile':
                    etlfeobj.connectivity_img = newform.connectivity_img

                if not etlfeobj.assign_status:
                    etlfeobj.assign_billing = newform.assign_billing
                    if newform.assign_status:
                        etlfeobj.assign_status = newform.assign_status
                        billing_notification_obj = IllNotification.objects.create(
                            conn_code=etlfeobj.conn_code, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=etlfeobj.id,
                            ill_ntfc_receiver=etlfeobj.assign_billing.username,
                            assign_date_time=etlfeobj.ill_sign_time,
                            accept_mod_url="addillbilling", reject_mod_url="rejectillbilling", ill_app_name="1")
                        billing_notification_obj.save()

                etlfeobj.save()

                return redirect(prevurl)

        EditPer = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'etlfeobj': etlfeobj, 'EditPer': EditPer,
                   'objmsgs': objmsg}
    else:
        EditPer = False
        context = {'objntfc_all': objntfc_all, 'etlfeobj': etlfeobj, 'EditPer': EditPer, 'objmsgs': objmsg}

    return render(request, 'threesaapptemp/edit_ill_fieldengg.html', context)


@login_required(login_url='login')
def rejectillfieldengg(request, rfeid):
    objfen = IllNotification.objects.get(id=rfeid)
    objillnoc = ThreesaIllNocDetails.objects.get(id=objfen.ill_prev_assign_obj_id)
    objillnoc.assign_status = False
    objillnoc.save()
    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objfen.ill_ntfc_sender,
                                                conn_code=objillnoc.conn_code.ill_custid, rej_module_name='FieldEngg')
    rejmsgobj.save()
    delobj = objfen.id
    objfen.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'threesaillfieldenggdetails' in request.META.get(
            'HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def threesaillbillingdetails(request):
    return redirect('threesaillconnections')


@login_required(login_url='login')
def addillbilling(request, abid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objbn = IllNotification.objects.get(id=abid)
    finst = {'conn_code': objbn.conn_code, }
    form = AddBillingDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddBillingDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.conn_code = objbn.conn_code
            newform.assign_date_time = objbn.assign_date_time
            newform.ill_billing_receiver = objbn.ill_ntfc_receiver
            newform.ill_sign_id = request.user.username
            newform.ill_sign_time = datetime.now()
            if not newform.assign_date_time == objbn.assign_date_time:
                newform.assign_date_time = objbn.assign_date_time
            newform.save()
            doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.get(conn_code=newform.conn_code)
            doneconn_obj.billing_code = newform
            if newform.conn_start_date <= date.today():
                doneconn_obj.active_status = True
            doneconn_obj.save()

            objbn.delete()

            return redirect('threesaillconnections')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objbn': objbn, 'objmsgs': objmsg}
    return render(request, 'threesaapptemp/add_ill_billing.html', context)


@login_required(login_url='login')
def editillbilling(request, ebid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    etlbobj = ThreesaIllBillingDetails.objects.get(id=ebid)

    if request.user.username == etlbobj.ill_billing_receiver or request.user.is_staff:
        form = EditBillingDetailsForm(instance=etlbobj)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditBillingDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                etlbobj.payment_status = newform.payment_status
                etlbobj.bandwidth = newform.bandwidth
                etlbobj.transaction_id = newform.transaction_id
                etlbobj.amount = newform.amount

                etlbobj.ill_sign_id = request.user.username
                etlbobj.ill_sign_time = datetime.now()

                if not newform.transaction_receipt == 'emptyfile':
                    etlbobj.transaction_receipt = newform.transaction_receipt

                if not newform.billing_img == 'emptyfile':
                    etlbobj.billing_img = newform.billing_img

                etlbobj.save()

                return redirect(prevurl)

        EditPer = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'etlbobj': etlbobj, 'EditPer': EditPer, 'objmsgs': objmsg}

    else:
        EditPer = False
        context = {'objntfc_all': objntfc_all, 'etlbobj': etlbobj, 'EditPer': EditPer, 'objmsgs': objmsg}

    return render(request, 'threesaapptemp/edit_ill_billing.html', context)


@login_required(login_url='login')
def rejectillbilling(request, rbid):
    objbn = IllNotification.objects.get(id=rbid)
    objillfieldengg = ThreesaIllFieldEngineerDetails.objects.get(id=objbn.ill_prev_assign_obj_id)
    objillfieldengg.assign_status = False
    objillfieldengg.save()
    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username,
                                                msg_receiver=objbn.ill_ntfc_sender,
                                                conn_code=objillfieldengg.conn_code.ill_custid,
                                                rej_module_name='Billing')
    rejmsgobj.save()
    delobj = objbn.id
    objbn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'threesaillbillingdetails' in request.META.get(
            'HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='login')
def renewillbilling(request, rebid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    retlbobj = ThreesaIllBillingDetails.objects.get(id=rebid)

    form = RenewBillingDetailsForm()
    if request.method == 'POST':
        prevurl = request.POST.get('prevurl')
        form = RenewBillingDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)

            connbillinghistory = IllBillingHistory.objects.create(conn_code=retlbobj.conn_code.ill_custid,
                                                                  conn_type=retlbobj.conn_code.get_ill_conn_type_display(),
                                                                  assign_date_time=retlbobj.assign_date_time,
                                                                  conn_start_date=retlbobj.conn_start_date,
                                                                  conn_end_date=retlbobj.conn_end_date,
                                                                  bandwidth=retlbobj.bandwidth,
                                                                  link_validity=retlbobj.link_validity,
                                                                  payment_method=retlbobj.payment_method,
                                                                  netbanking_type=retlbobj.netbanking_type,
                                                                  transaction_id=retlbobj.transaction_id,
                                                                  payment_status=retlbobj.payment_status,
                                                                  amount=retlbobj.amount,
                                                                  transaction_receipt=retlbobj.transaction_receipt,
                                                                  billing_img=retlbobj.billing_img,
                                                                  ill_billing_receiver=retlbobj.ill_billing_receiver,
                                                                  )

            connbillinghistory.save()

            retlbobj.conn_start_date = newform.conn_start_date
            retlbobj.conn_end_date = newform.conn_end_date
            retlbobj.link_validity = newform.link_validity
            retlbobj.amount = newform.amount

            retlbobj.payment_method = newform.payment_method

            if newform.payment_method == '2':
                retlbobj.netbanking_type = newform.netbanking_type
            else:
                retlbobj.netbanking_type = None
            retlbobj.payment_status = newform.payment_status
            retlbobj.bandwidth = newform.bandwidth
            retlbobj.transaction_id = newform.transaction_id
            retlbobj.ill_billing_receiver = request.user.username

            retlbobj.ill_sign_id = request.user.username
            retlbobj.ill_sign_time = datetime.now()
            doneconn_obj = ThreesaIllDoneConnectionsDetails.objects.get(conn_code=retlbobj.conn_code)
            if newform.conn_start_date <= date.today():
                doneconn_obj.active_status = True
            doneconn_obj.save()

            if not newform.transaction_receipt == 'emptyfile':
                retlbobj.transaction_receipt = newform.transaction_receipt

            if not newform.billing_img == 'emptyfile':
                retlbobj.billing_img = newform.billing_img

            retlbobj.save()

            return redirect(prevurl)

    context = {'objntfc_all': objntfc_all, 'retlbobj': retlbobj, 'form': form, 'objmsgs': objmsg}

    return render(request, 'threesaapptemp/renew_ill_billing.html', context)
