from datetime import datetime, date

import xlwt
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from sitemanager.forms import Num_Item_Per_Page
from sitemanager.models import IllNotification, RejectionMessage
from threesaoperators.filters import NetOperatorsDetailsFilter
from threesaoperators.forms import AddOperatorDetailsForm, AddZoneForm, EditOperatorDetailsForm, \
    AddOperatorFiberDetailsForm, EditOperatorFiberDetailsForm, AddOperatorNocDetailsForm, EditOperatorNocDetailsForm, \
    AddOperatorBillingDetailsForm, EditOperatorBillingDetailsForm, RenewOperatorBillingDetailsForm
from threesaoperators.models import NetOperatorsDetails, NetOperatorsZones, NetOperatorsFiberDetails, \
    NetOperatorsNocDetails, NetOperatorsBillingDetails, OpBillingHistory

@login_required(login_url='login')
def netoperators(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objnetop_all = NetOperatorsDetails.objects.all()

    connfilter = NetOperatorsDetailsFilter(request.GET, queryset=objnetop_all)
    objnetop_all = connfilter.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        objnetop_all = NetOperatorsDetails.objects.filter(Q(operator_id__icontains=searchguery)
                                                          | Q(operator_name__icontains=searchguery)
                                                          | Q(Operator_register__icontains=searchguery)
                                                          | Q(zones__zone_name__icontains=searchguery)
                                                          | Q(zones__zone_area__icontains=searchguery)
                                                          | Q(operator_dealer__username__icontains=searchguery)
                                                          | Q(op_contact_pname__icontains=searchguery)
                                                          | Q(op_contact_pnum__icontains=searchguery)
                                                          | Q(assign_fiber__username__icontains=searchguery)
                                                          | Q(assign_status__icontains=searchguery)
                                                          )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="operator-details.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Operator Details')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        ws.write_merge(0, 0, 0, 11, 'Operator Details', font_style)
        ws.write_merge(0, 0, 12, 19, 'Fiber details', font_style)
        ws.write_merge(0, 0, 20, 34, 'Noc details', font_style)
        ws.write_merge(0, 0, 35, 46, 'Billing details', font_style)

        row_num = 1
        columns = ['Operator Id',
                   'Name', 'Operator Registration', 'Zones', 'Dealer', 'Operator Contact Person Name',
                   'Operator Contact Person Number', 'Status', 'Assign Fiber Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Core Details', 'Core Color', 'Pop Name', 'Assign NOC Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assigned Date and time',
                   'Server IP', 'Subnet',
                   'Gateway', 'DNS',
                   'DNS2', 'Switch IP',
                   'Switch Port No', 'VLAND', 'MAC Address',
                   'Routing Status', 'Assign Billing',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Payment Start Date', 'Payment End Date', 'No Topup', 'Payment Validity',
                   'Payment Status','amount', 'Payment Method', 'Net Banking Type', 'Transaction ID',
                   'Sign Verification ID', 'Sign Verification Time']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = []

        for objnetop in objnetop_all:
            zna = ''
            for x in objnetop.zones.all():
                if zna == '':
                    zna = x.zone_name+" - "+x.zone_area
                else:
                    zna = zna + " , " + x.zone_name+" - "+x.zone_area
            rows.append([objnetop.operator_id if objnetop.operator_id else '',
                         objnetop.operator_name if objnetop.operator_name else '',
                         str(objnetop.Operator_register.strftime(
                             "%d/%m/%Y %I:%M %p")) if objnetop.Operator_register else '',
                         zna if zna else '',
                         objnetop.operator_dealer.username if objnetop.operator_dealer else '',
                         objnetop.op_contact_pname if objnetop.op_contact_pname else '',
                         objnetop.op_contact_pnum if objnetop.op_contact_pnum else '',
                         objnetop.get_active_status_display() if objnetop.active_status else 'Deactive',
                         objnetop.assign_fiber.username if objnetop.assign_fiber else '',
                         objnetop.get_assign_status_display() if objnetop.assign_status else '',
                         objnetop.sign_id if objnetop.sign_id else '',
                         str(objnetop.sign_time.strftime("%d/%m/%Y %I:%M %p")) if objnetop.sign_time else '',
                         str(objnetop.op_fiber_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objnetop.op_fiber_code else '',
                         objnetop.op_fiber_code.core_details if objnetop.op_fiber_code else '',
                         objnetop.op_fiber_code.core_color if objnetop.op_fiber_code else '',
                         objnetop.op_fiber_code.pop_name if objnetop.op_fiber_code else '',
                         objnetop.op_fiber_code.assign_noc.username if objnetop.op_fiber_code else '',
                         objnetop.op_fiber_code.get_assign_status_display() if objnetop.op_fiber_code else '',
                         objnetop.op_fiber_code.sign_id if objnetop.op_fiber_code else '',
                         str(objnetop.op_fiber_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objnetop.op_fiber_code else '',
                         str(objnetop.op_noc_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.server_ip if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.subnet if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.gateway if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.dns if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.dns2 if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.switch_ip if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.switch_port_no if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.vland if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.mac_add if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.get_routing_status_display() if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.assign_billing.username if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.get_assign_status_display() if objnetop.op_noc_code else '',
                         objnetop.op_noc_code.sign_id if objnetop.op_noc_code else '',
                         str(objnetop.op_noc_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objnetop.op_noc_code else '',
                         str(objnetop.op_billing_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objnetop.op_billing_code else '',
                         str(objnetop.op_billing_code.payment_start_date.strftime(
                             "%d/%m/%Y")) if objnetop.op_billing_code else '',
                         str(objnetop.op_billing_code.payment_end_date.strftime(
                             "%d/%m/%Y")) if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.no_topup if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.payment_validity if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.get_payment_status_display() if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.amount if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.get_payment_method_display() if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.get_netbanking_type_display() if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.transaction_id if objnetop.op_billing_code else '',
                         objnetop.op_billing_code.sign_id if objnetop.op_billing_code else '',
                         str(objnetop.op_billing_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objnetop.op_billing_code else '',
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

    paginator = Paginator(objnetop_all, num_page)
    try:
        objnetop_all = paginator.page(page)
    except PageNotAnInteger:
        objnetop_all = paginator.page(1)
    except EmptyPage:
        objnetop_all = paginator.page(paginator.num_pages)

    context = {'objnetop_all': objnetop_all,
               'objntfc_all': objntfc_all,
               'objmsgs': objmsg,
               'itemperform': itemperform,
               'rowcount': str(num_page),
               'connfilter': connfilter
               }
    return render(request, "netoperator/operators_temp.html", context)

@login_required(login_url='login')
def addnetoperator(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    form = AddOperatorDetailsForm()
    AddZoneFormSet = formset_factory(AddZoneForm)
    if request.method == 'POST':
        formset = AddZoneFormSet(request.POST)
        form = AddOperatorDetailsForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            newform = form.save(commit=False)
            newform.Operator_register = datetime.now()
            newform.sign_id = request.user.username
            newform.sign_time = datetime.now()
            newform.save()
            if newform.assign_status:
                fibereng_notification_obj = IllNotification.objects.create(
                    link_code=newform.operator_id, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_fiber.username, assign_date_time=newform.sign_time,
                    accept_mod_url="addnetopfiber", reject_mod_url="rejnetopfiber")
                fibereng_notification_obj.save()

            for i in range(0, formset.total_form_count()):
                zform = formset.forms[i]
                try:
                    zn = zform.cleaned_data['zone_name']
                except:
                    zn = None

                try:
                    za = zform.cleaned_data['zone_area']
                except:
                    za = None
                if zn and za:
                    zoneobj = NetOperatorsZones.objects.create(zone_name=zn, zone_area=za)
                    zoneobj.zone_set.add(newform)
                    zoneobj.save()

            return redirect('netoperators')

    formset = AddZoneFormSet()
    context = {'objntfc_all': objntfc_all,
               'objmsgs': objmsg, 'form': form, 'formset': formset}
    return render(request, "netoperator/add_op.html", context)


@login_required(login_url='login')
def editnetoperator(request, enetopid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    objnetop = NetOperatorsDetails.objects.get(id=enetopid)

    if request.user.is_staff or request.user.username == objnetop.operator_dealer:

        form = EditOperatorDetailsForm(instance=objnetop)
        AddZoneFormSet = formset_factory(AddZoneForm)

        if request.method == 'POST':
            # if editble:
            formset = AddZoneFormSet(request.POST)
            form = EditOperatorDetailsForm(request.POST, request.FILES)
            if form.is_valid() and formset.is_valid():
                newform = form.save(commit=False)
                objnetop.operator_name = newform.operator_name
                objnetop.op_contact_pname = newform.op_contact_pname
                objnetop.op_contact_pnum = newform.op_contact_pnum
                if not newform.op_kyc == 'emptyfile':
                    objnetop.op_kyc = newform.op_kyc

                objnetop.sign_id = request.user.username
                objnetop.sign_time = datetime.now()
                if not objnetop.assign_status:
                    objnetop.assign_fiber = newform.assign_fiber
                    if newform.assign_status:
                        objnetop.assign_status = newform.assign_status
                        fibereng_notification_obj = IllNotification.objects.create(
                            link_code=objnetop.operator_id, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=objnetop.id,
                            ill_ntfc_receiver=objnetop.assign_fiber.username, assign_date_time=objnetop.sign_time,
                            accept_mod_url="addnetopfiber", reject_mod_url="rejnetopfiber")
                        fibereng_notification_obj.save()

                objnetop.save()
                for i in range(0, formset.total_form_count()):
                    zform = formset.forms[i]
                    try:
                        zn = zform.cleaned_data['zone_name']
                    except:
                        zn = None

                    try:
                        za = zform.cleaned_data['zone_area']
                    except:
                        za = None
                    if zn and za:
                        zoneobj = NetOperatorsZones.objects.create(zone_name=zn, zone_area=za)
                        zoneobj.zone_set.add(objnetop)
                        zoneobj.save()
                return redirect('netoperators')

        formset = AddZoneFormSet()
        editper = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'editper': editper,
                   'objnetop': objnetop, 'formset': formset}
    else:
        editper = False
        context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'objnetop': objnetop, 'editper': editper}

    return render(request, 'netoperator/edit_op.html', context)


@login_required(login_url='login')
def fiberdetails(request):
    return redirect("netoperators")


@login_required(login_url='login')
def addnetopfiber(request, anetopfid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objnn = IllNotification.objects.get(id=anetopfid)
    finst = {'operator_id': objnn.link_code, }
    form = AddOperatorFiberDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddOperatorFiberDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.operator_id = objnn.link_code
            newform.assign_date_time = objnn.assign_date_time
            newform.fiber_receiver = objnn.ill_ntfc_receiver
            newform.sign_id = request.user.username
            newform.sign_time = datetime.now()

            newform.save()

            doneconn_obj = NetOperatorsDetails.objects.get(operator_id=newform.operator_id)
            doneconn_obj.op_fiber_code = newform
            doneconn_obj.save()

            if newform.assign_status:
                noc_notification_obj = IllNotification.objects.create(
                    link_code=newform.operator_id, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_noc.username, assign_date_time=newform.sign_time,
                    accept_mod_url="addnetopnoc", reject_mod_url="rejnetopnoc")
                noc_notification_obj.save()

            objnn.delete()

            return redirect('netoperators')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objnn': objnn, 'objmsgs': objmsg}
    return render(request, 'netoperator/add_op_fiber.html', context)


@login_required(login_url='login')
def editnetopfiber(request, enetopfid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objfiber = NetOperatorsFiberDetails.objects.get(id=enetopfid)
    if request.user.username == objfiber.fiber_receiver or request.user.is_staff:
        form = EditOperatorFiberDetailsForm(instance=objfiber)
        if request.method == 'POST':
            form = EditOperatorFiberDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                objfiber.core_details = newform.core_details
                objfiber.core_color = newform.core_color
                objfiber.pop_name = newform.pop_name
                objfiber.op_switch_img = newform.op_switch_img
                objfiber.sign_id = request.user.username
                objfiber.sign_time = datetime.now()

                if not objfiber.assign_status:
                    objfiber.assign_noc = newform.assign_noc
                    if newform.assign_status:
                        objfiber.assign_status = newform.assign_status
                        noc_notification_obj = IllNotification.objects.create(
                            link_code=objfiber.operator_id, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=objfiber.id,
                            ill_ntfc_receiver=objfiber.assign_noc.username, assign_date_time=objfiber.sign_time,
                            accept_mod_url="addnetopnoc", reject_mod_url="rejnetopnoc")
                        noc_notification_obj.save()

                objfiber.save()

                return redirect('netoperators')
        editper = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objfiber': objfiber, 'editper': editper,
                   'objmsgs': objmsg}
    else:
        editper = False
        context = {'objntfc_all': objntfc_all,
                   'objfiber': objfiber,
                   'editper': editper,
                   'objmsgs': objmsg,
                   }

    return render(request, 'netoperator/edit_op_fiber.html', context)


@login_required(login_url='login')
def rejnetopfiber(request, rnetopfid):
    objnn = IllNotification.objects.get(id=rnetopfid)
    objnetop = NetOperatorsDetails.objects.get(id=objnn.ill_prev_assign_obj_id)
    objnetop.assign_status = False
    objnetop.save()

    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objnn.ill_ntfc_sender,
                                                conn_code=objnetop.operator_id, rej_module_name='Operator')
    rejmsgobj.save()
    delobj = objnn.id
    objnn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'fiberdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def opnocdetails(request):
    return redirect("netoperators")


@login_required(login_url='login')
def addnetopnoc(request, anetopnid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objnn = IllNotification.objects.get(id=anetopnid)
    finst = {'operator_id': objnn.link_code, }
    form = AddOperatorNocDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddOperatorNocDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.operator_id = objnn.link_code
            newform.assign_date_time = objnn.assign_date_time
            newform.noc_receiver = objnn.ill_ntfc_receiver
            newform.sign_id = request.user.username
            newform.sign_time = datetime.now()

            newform.save()

            doneconn_obj = NetOperatorsDetails.objects.get(operator_id=newform.operator_id)
            doneconn_obj.op_noc_code = newform
            doneconn_obj.save()

            if newform.assign_status:
                billing_notification_obj = IllNotification.objects.create(
                    link_code=newform.operator_id, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_billing.username, assign_date_time=newform.sign_time,
                    accept_mod_url="addnetopbill", reject_mod_url="rejnetopbill")
                billing_notification_obj.save()

            objnn.delete()

            return redirect('netoperators')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objnn': objnn, 'objmsgs': objmsg}
    return render(request, 'netoperator/add_op_noc.html', context)


@login_required(login_url='login')
def editnetopnoc(request, enetopnid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objnoc = NetOperatorsNocDetails.objects.get(id=enetopnid)

    if request.user.username == objnoc.noc_receiver or request.user.is_staff:
        form = EditOperatorNocDetailsForm(instance=objnoc)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditOperatorNocDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                objnoc.server_ip = newform.server_ip
                objnoc.subnet = newform.subnet
                objnoc.gateway = newform.gateway
                objnoc.dns = newform.dns
                objnoc.dns2 = newform.dns2
                objnoc.switch_ip = newform.switch_ip
                objnoc.switch_port_no = newform.switch_port_no
                objnoc.vland = newform.vland
                objnoc.mac_add = newform.mac_add
                objnoc.routing_status = newform.routing_status
                objnoc.sign_id = request.user.username
                objnoc.sign_time = datetime.now()

                if not objnoc.assign_status:
                    objnoc.assign_billing = newform.assign_billing
                    if newform.assign_status:
                        objnoc.assign_status = newform.assign_status
                        billing_notification_obj = IllNotification.objects.create(
                            link_code=objnoc.operator_id, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=objnoc.id,
                            ill_ntfc_receiver=objnoc.assign_billing.username, assign_date_time=objnoc.sign_time,
                            accept_mod_url="addnetopbill", reject_mod_url="rejnetopbill")
                        billing_notification_obj.save()

                objnoc.save()

                return redirect(prevurl)

        EditPer = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objnoc': objnoc, 'EditPer': EditPer, 'objmsgs': objmsg}
    else:
        EditPer = False
        context = {'objntfc_all': objntfc_all,
                   'objnoc': objnoc,
                   'EditPer': EditPer,
                   'objmsgs': objmsg,
                   }

    return render(request, 'netoperator/edit_op_noc.html', context)


@login_required(login_url='login')
def rejnetopnoc(request, rnetopnid):
    objnn = IllNotification.objects.get(id=rnetopnid)
    objnetopf = NetOperatorsFiberDetails.objects.get(id=objnn.ill_prev_assign_obj_id)
    objnetopf.assign_status = False
    objnetopf.save()

    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objnn.ill_ntfc_sender,
                                                conn_code=objnetopf.operator_id, rej_module_name='OperatorNoc')
    rejmsgobj.save()
    delobj = objnn.id
    objnn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'nocdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def opbilldetails(request):
    return redirect('netoperator')


@login_required(login_url='login')
def addnetopbill(request, anetopbid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objbn = IllNotification.objects.get(id=anetopbid)
    finst = {'operator_id': objbn.link_code, }
    form = AddOperatorBillingDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddOperatorBillingDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.operator_id = objbn.link_code
            newform.assign_date_time = objbn.assign_date_time
            newform.billing_receiver = objbn.ill_ntfc_receiver
            newform.sign_id = request.user.username
            newform.sign_time = datetime.now()
            newform.save()
            doneconn_obj = NetOperatorsDetails.objects.get(operator_id=newform.operator_id)
            doneconn_obj.op_billing_code = newform
            if newform.payment_start_date <= date.today():
                doneconn_obj.active_status = True
            doneconn_obj.save()

            objbn.delete()

            return redirect('netoperators')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objbn': objbn, 'objmsgs': objmsg}
    return render(request, 'netoperator/add_op_billing.html', context)


@login_required(login_url='login')
def editnetopbill(request, enetopbid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objopbill = NetOperatorsBillingDetails.objects.get(id=enetopbid)

    if request.user.username == objopbill.billing_receiver or request.user.is_staff:
        form = EditOperatorBillingDetailsForm(instance=objopbill)
        if request.method == 'POST':
            prevurl = request.POST.get('prevurl')
            form = EditOperatorBillingDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                objopbill.transaction_id = newform.transaction_id
                objopbill.sign_id = request.user.username
                objopbill.sign_time = datetime.now()
                objopbill.amount = newform.amount


                if not newform.transaction_receipt == 'emptyfile':
                    objopbill.transaction_receipt = newform.transaction_receipt

                if not newform.op_payment_receipt == 'emptyfile':
                    objopbill.op_payment_receipt = newform.op_payment_receipt

                objopbill.save()

                return redirect(prevurl)

        editper = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objopbill': objopbill, 'editper': editper,
                   'objmsgs': objmsg}

    else:
        EditPer = False
        context = {'objntfc_all': objntfc_all, 'objopbill': objopbill, 'EditPer': EditPer, 'objmsgs': objmsg}

    return render(request, 'netoperator/edit_op_billing.html', context)


@login_required(login_url='login')
def rejnetopbill(request, rnetopbid):
    objnn = IllNotification.objects.get(id=rnetopbid)
    objnetopn = NetOperatorsNocDetails.objects.get(id=objnn.ill_prev_assign_obj_id)
    objnetopn.assign_status = False
    objnetopn.save()

    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objnn.ill_ntfc_sender,
                                                conn_code=objnetopn.operator_id, rej_module_name='OperatorBilling')
    rejmsgobj.save()
    delobj = objnn.id
    objnn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'billingdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def renewnetopbill(request, rennetopbid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    retlbobj = NetOperatorsBillingDetails.objects.get(id=rennetopbid)

    form = RenewOperatorBillingDetailsForm()
    if request.method == 'POST':
        prevurl = request.POST.get('prevurl')
        form = RenewOperatorBillingDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)

            opbillinghistory = OpBillingHistory.objects.create(operator_id=retlbobj.operator_id,
                                                               assign_date_time=retlbobj.assign_date_time,
                                                               payment_start_date=retlbobj.payment_start_date,
                                                               payment_end_date=retlbobj.payment_end_date,
                                                               no_topup=retlbobj.no_topup,
                                                               payment_validity=retlbobj.payment_validity,
                                                               payment_method=retlbobj.payment_method,
                                                               netbanking_type=retlbobj.netbanking_type,
                                                               transaction_id=retlbobj.transaction_id,
                                                               payment_status=retlbobj.payment_status,
                                                               amount=retlbobj.amount,
                                                               transaction_receipt=retlbobj.transaction_receipt,
                                                               op_payment_receipt=retlbobj.op_payment_receipt,
                                                               billing_receiver=retlbobj.billing_receiver,
                                                               )

            opbillinghistory.save()

            retlbobj.payment_start_date = newform.payment_start_date
            retlbobj.payment_end_date = newform.payment_end_date
            retlbobj.payment_validity = newform.payment_validity
            retlbobj.amount = newform.amount

            retlbobj.payment_method = newform.payment_method

            if newform.payment_method == '2':
                retlbobj.netbanking_type = newform.netbanking_type
            else:
                retlbobj.netbanking_type = None
            retlbobj.payment_status = newform.payment_status
            retlbobj.transaction_id = newform.transaction_id
            retlbobj.billing_receiver = request.user.username

            retlbobj.sign_id = request.user.username
            retlbobj.sign_time = datetime.now()
            op_obj = NetOperatorsDetails.objects.get(operator_id=retlbobj.operator_id)
            if newform.payment_start_date <= date.today():
                op_obj.active_status = True
            op_obj.save()

            retlbobj.transaction_receipt = newform.transaction_receipt

            retlbobj.op_payment_receipt = newform.op_payment_receipt

            retlbobj.save()

            return redirect(prevurl)

    context = {'objntfc_all': objntfc_all, 'retlbobj': retlbobj, 'form': form, 'objmsgs': objmsg}

    return render(request, 'netoperator/renew_op_billing.html', context)


@login_required(login_url='login')
def netopbillhistory(request, opid):
    objbillinghs = OpBillingHistory.objects.filter(operator_id=opid)
    if request.method == 'POST' and request.POST.get('exportexcelbillhistory'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Operator-Billing-History.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Operator Billing History')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Operator ID', 'Assigned Date and time',
                   'Payment Start Date', 'Payment End Date', 'Validity','No of TopUp',
                   'Payment Status','amount', 'Payment Method', 'Net Banking Type', 'Transaction ID', 'Accountant ID']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = []

        for objbillinghs_1 in objbillinghs:
            rows.append([objbillinghs_1.operator_id if objbillinghs_1.operator_id else '',
                         str(objbillinghs_1.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objbillinghs_1.assign_date_time else '',
                         str(objbillinghs_1.payment_start_date) if objbillinghs_1.payment_start_date else '',
                         str(objbillinghs_1.payment_end_date) if objbillinghs_1.payment_end_date else '',
                         str(objbillinghs_1.no_topup) if objbillinghs_1.no_topup else '',
                         objbillinghs_1.payment_validity if objbillinghs_1.payment_validity else '',
                         objbillinghs_1.get_payment_status_display() if objbillinghs_1.get_payment_status_display() else '',
                         objbillinghs_1.amount if objbillinghs_1.amount else '',
                         objbillinghs_1.get_payment_method_display() if objbillinghs_1.get_payment_method_display() else '',
                         objbillinghs_1.get_netbanking_type_display() if objbillinghs_1.get_netbanking_type_display() else '',
                         objbillinghs_1.transaction_id if objbillinghs_1.transaction_id else '',
                         objbillinghs_1.billing_receiver if objbillinghs_1.billing_receiver else '',
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

    context = { 'objbillinghs': objbillinghs,'opid':opid}
    return render(request, 'netoperator/ophistorymodel.html', context)
