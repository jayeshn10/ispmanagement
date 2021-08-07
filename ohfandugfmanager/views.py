from datetime import datetime, date

import xlwt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from ohfandugfmanager.filters import OhfAndUgfFilter
from ohfandugfmanager.forms import AddOhfAndUgfDetailsForm, EditOhfAndUgfDetailsForm, AddOandUFiberDetailsForm, \
    EditOandUFiberDetailsForm, AddOandUBillingDetailsForm, EditOandUBillingDetailsForm, RenewBillingDetailsForm
from ohfandugfmanager.models import OhfAndUgfDetails, OhfAndUgfFiberTeamDetails, OhfAndUgfBillingDetails, \
    OhfAndUgfBillingHistory

from sitemanager.forms import Num_Item_Per_Page
from sitemanager.models import IllNotification, RejectionMessage


@login_required(login_url='login')
def ohfandugf(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    objoau_all = OhfAndUgfDetails.objects.all()

    oandufilter = OhfAndUgfFilter(request.GET, queryset=objoau_all)
    objoau_all = oandufilter.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        objoau_all = OhfAndUgfDetails.objects.filter(Q(link_code__icontains=searchguery)
                                                     | Q(link_name__icontains=searchguery)
                                                     | Q(link_dealer__username__icontains=searchguery)
                                                     | Q(link_vendor__v_code__icontains=searchguery)
                                                     | Q(link_type_g_t__icontains=searchguery)
                                                     | Q(link_type__icontains=searchguery)
                                                     | Q(link_point_a__icontains=searchguery)
                                                     | Q(link_point_via__icontains=searchguery)
                                                     | Q(link_point_b__icontains=searchguery)
                                                     )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ohf-and-ugf-link-details.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Ohf and Ugf Link Details')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        ws.write_merge(0, 0, 0, 16, 'Link Details', font_style)
        ws.write_merge(0, 0, 17, 25, 'Fiber details', font_style)
        ws.write_merge(0, 0, 26, 33, 'Billing details', font_style)

        row_num = 1
        columns = ['Link Code',
                   'Name', 'Link Dealer', 'Vendor', 'Taken Or Given',
                   'Link Type', 'Point A', 'Link Via', 'Point B',
                   'Link Start Date', 'Link End Date', 'Link Validity', 'Link Status',
                   'Assign Fiber Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Core Details', 'Core Color', 'Distance', 'OTDR Value', 'Assign Billing',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Payment Status','amount', 'Payment Method', 'Net Banking Type', 'Transaction ID',
                   'Sign Verification ID', 'Sign Verification Time']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = []

        for objoau in objoau_all:
            rows.append([objoau.link_code if objoau.link_code else '',
                         objoau.link_name if objoau.link_name else '',
                         objoau.link_dealer.username if objoau.link_dealer else '',
                         objoau.link_vendor.v_code if objoau.link_vendor else '',
                         objoau.get_link_type_g_t_display() if objoau.link_type_g_t else '',
                         objoau.get_link_type_display() if objoau.link_type else '',
                         objoau.link_point_a if objoau.link_point_a else '',
                         objoau.link_point_via if objoau.link_point_via else '',
                         objoau.link_point_b if objoau.link_point_b else '',
                         str(objoau.link_billing_code.link_start_date.strftime(
                             "%d/%m/%Y")) if objoau.link_billing_code else '',
                         str(objoau.link_billing_code.link_end_date.strftime(
                             "%d/%m/%Y")) if objoau.link_billing_code else '',
                         objoau.link_billing_code.link_validity if objoau.link_billing_code else '',
                         objoau.get_link_status_display() if objoau.link_status else 'Deactive',
                         objoau.assign_fiber.username if objoau.assign_fiber else '',
                         objoau.get_assign_status_display() if objoau.assign_status else '',
                         objoau.sign_id if objoau.sign_id else '',
                         str(objoau.sign_time.strftime("%d/%m/%Y %I:%M %p")) if objoau.sign_time else '',
                         str(objoau.link_fiber_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.core_details if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.core_color if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.distance if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.otdr if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.assign_billing.username if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.get_assign_status_display() if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.sign_id if objoau.link_fiber_code else '',
                         str(objoau.link_fiber_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_fiber_code else '',
                         str(objoau.link_billing_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_payment_status_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.amount if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_payment_method_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_netbanking_type_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.transaction_id if objoau.link_billing_code else '',
                         objoau.link_billing_code.sign_id if objoau.link_billing_code else '',
                         str(objoau.link_billing_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_billing_code else '',
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
    paginator = Paginator(objoau_all, num_page)
    try:
        objoau_all = paginator.page(page)
    except PageNotAnInteger:
        objoau_all = paginator.page(1)
    except EmptyPage:
        objoau_all = paginator.page(paginator.num_pages)

    context = {'objntfc_all': objntfc_all,
               'objmsgs': objmsg,
               'objoau_all': objoau_all,
               'oandufilter': oandufilter,
               'itemperform': itemperform,
               'rowcount': str(num_page),
               }
    return render(request, 'ohfandugf/oandu_app_temp.html', context)


@login_required(login_url='login')
def ohfandugf_g(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    objoau_all = OhfAndUgfDetails.objects.filter(link_type_g_t='2')

    oandufilter = OhfAndUgfFilter(request.GET, queryset=objoau_all)
    objoau_all = oandufilter.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        objoau_all = OhfAndUgfDetails.objects.filter(Q(link_code__icontains=searchguery)
                                                     | Q(link_name__icontains=searchguery)
                                                     | Q(link_dealer__username__icontains=searchguery)
                                                     | Q(link_vendor__v_code__icontains=searchguery)
                                                     | Q(link_type_g_t__icontains=searchguery)
                                                     | Q(link_type__icontains=searchguery)
                                                     | Q(link_point_a__icontains=searchguery)
                                                     | Q(link_point_via__icontains=searchguery)
                                                     | Q(link_point_b__icontains=searchguery)
                                                     )
    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ohf-and-ugf-g-link-details.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Ohf and Ugf Given Link Details')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        ws.write_merge(0, 0, 0, 16, 'Link Details', font_style)
        ws.write_merge(0, 0, 17, 25, 'Fiber details', font_style)
        ws.write_merge(0, 0, 26, 32, 'Billing details', font_style)

        row_num = 1
        columns = ['Link Code',
                   'Name', 'Link Dealer', 'Vendor', 'Taken Or Given',
                   'Link Type', 'Point A', 'Link Via', 'Point B',
                   'Link Start Date', 'Link End Date', 'Link Validity', 'Link Status',
                   'Assign Fiber Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Core Details', 'Core Color', 'Distance', 'OTDR Value', 'Assign Billing',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Payment Status','amount', 'Payment Method', 'Net Banking Type', 'Transaction ID',
                   'Sign Verification ID', 'Sign Verification Time']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = []

        for objoau in objoau_all:
            rows.append([objoau.link_code if objoau.link_code else '',
                         objoau.link_name if objoau.link_name else '',
                         objoau.link_dealer.username if objoau.link_dealer else '',
                         objoau.link_vendor.v_code if objoau.link_vendor else '',
                         objoau.get_link_type_g_t_display() if objoau.link_type_g_t else '',
                         objoau.get_link_type_display() if objoau.link_type else '',
                         objoau.link_point_a if objoau.link_point_a else '',
                         objoau.link_point_via if objoau.link_point_via else '',
                         objoau.link_point_b if objoau.link_point_b else '',
                         str(objoau.link_billing_code.link_start_date.strftime(
                             "%d/%m/%Y")) if objoau.link_billing_code else '',
                         str(objoau.link_billing_code.link_end_date.strftime(
                             "%d/%m/%Y")) if objoau.link_billing_code else '',
                         objoau.link_billing_code.link_validity if objoau.link_billing_code else '',
                         objoau.get_link_status_display() if objoau.link_status else 'Deactive',
                         objoau.assign_fiber.username if objoau.assign_fiber else '',
                         objoau.get_assign_status_display() if objoau.assign_status else '',
                         objoau.sign_id if objoau.sign_id else '',
                         str(objoau.sign_time.strftime("%d/%m/%Y %I:%M %p")) if objoau.sign_time else '',
                         str(objoau.link_fiber_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.core_details if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.core_color if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.distance if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.otdr if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.assign_billing.username if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.get_assign_status_display() if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.sign_id if objoau.link_fiber_code else '',
                         str(objoau.link_fiber_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_fiber_code else '',
                         str(objoau.link_billing_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_payment_status_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.amount if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_payment_method_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_netbanking_type_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.transaction_id if objoau.link_billing_code else '',
                         objoau.link_billing_code.sign_id if objoau.link_billing_code else '',
                         str(objoau.link_billing_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_billing_code else '',
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

    paginator = Paginator(objoau_all, num_page)
    try:
        objoau_all = paginator.page(page)
    except PageNotAnInteger:
        objoau_all = paginator.page(1)
    except EmptyPage:
        objoau_all = paginator.page(paginator.num_pages)

    context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'objoau_all': objoau_all, 'oandufilter': oandufilter,
               'itemperform': itemperform, 'rowcount': str(num_page)}
    return render(request, 'ohfandugf/oandu_g_app_temp.html', context)


@login_required(login_url='login')
def ohfandugf_t(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    objoau_all = OhfAndUgfDetails.objects.filter(link_type_g_t='1')

    oandufilter = OhfAndUgfFilter(request.GET, queryset=objoau_all)
    objoau_all = oandufilter.qs

    if request.method == 'GET' and request.GET.get('searchqry'):
        searchguery = request.GET.get('searchqry')
        objoau_all = OhfAndUgfDetails.objects.filter(Q(link_code__icontains=searchguery)
                                                     | Q(link_name__icontains=searchguery)
                                                     | Q(link_dealer__username__icontains=searchguery)
                                                     | Q(link_vendor__v_code__icontains=searchguery)
                                                     | Q(link_type_g_t__icontains=searchguery)
                                                     | Q(link_type__icontains=searchguery)
                                                     | Q(link_point_a__icontains=searchguery)
                                                     | Q(link_point_via__icontains=searchguery)
                                                     | Q(link_point_b__icontains=searchguery)
                                                     )

    if request.method == 'POST' and request.POST.get('exportexcel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ohf-and-ugf-t-link-details.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Ohf and Ugf Taken Link Details')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        ws.write_merge(0, 0, 0, 16, 'Link Details', font_style)
        ws.write_merge(0, 0, 17, 25, 'Fiber details', font_style)
        ws.write_merge(0, 0, 26, 33, 'Billing details', font_style)

        row_num = 1
        columns = ['Link Code',
                   'Name', 'Link Dealer', 'Vendor', 'Taken Or Given',
                   'Link Type', 'Point A', 'Link Via', 'Point B',
                   'Link Start Date', 'Link End Date', 'Link Validity', 'Link Status',
                   'Assign Fiber Engineer',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Core Details', 'Core Color', 'Distance', 'OTDR Value', 'Assign Billing',
                   'Assign Status', 'Sign Verification ID', 'Sign Verification Time',
                   'Assign Date and Time',
                   'Payment Status','amount', 'Payment Method', 'Net Banking Type', 'Transaction ID',
                   'Sign Verification ID', 'Sign Verification Time']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = []

        for objoau in objoau_all:
            rows.append([objoau.link_code if objoau.link_code else '',
                         objoau.link_name if objoau.link_name else '',
                         objoau.link_dealer.username if objoau.link_dealer else '',
                         objoau.link_vendor.v_code if objoau.link_vendor else '',
                         objoau.get_link_type_g_t_display() if objoau.link_type_g_t else '',
                         objoau.get_link_type_display() if objoau.link_type else '',
                         objoau.link_point_a if objoau.link_point_a else '',
                         objoau.link_point_via if objoau.link_point_via else '',
                         objoau.link_point_b if objoau.link_point_b else '',
                         str(objoau.link_billing_code.link_start_date.strftime(
                             "%d/%m/%Y")) if objoau.link_billing_code else '',
                         str(objoau.link_billing_code.link_end_date.strftime(
                             "%d/%m/%Y")) if objoau.link_billing_code else '',
                         objoau.link_billing_code.link_validity if objoau.link_billing_code else '',
                         objoau.get_link_status_display() if objoau.link_status else 'Deactive',
                         objoau.assign_fiber.username if objoau.assign_fiber else '',
                         objoau.get_assign_status_display() if objoau.assign_status else '',
                         objoau.sign_id if objoau.sign_id else '',
                         str(objoau.sign_time.strftime("%d/%m/%Y %I:%M %p")) if objoau.sign_time else '',
                         str(objoau.link_fiber_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.core_details if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.core_color if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.distance if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.otdr if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.assign_billing.username if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.get_assign_status_display() if objoau.link_fiber_code else '',
                         objoau.link_fiber_code.sign_id if objoau.link_fiber_code else '',
                         str(objoau.link_fiber_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_fiber_code else '',
                         str(objoau.link_billing_code.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_payment_status_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.amount if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_payment_method_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.get_netbanking_type_display() if objoau.link_billing_code else '',
                         objoau.link_billing_code.transaction_id if objoau.link_billing_code else '',
                         objoau.link_billing_code.sign_id if objoau.link_billing_code else '',
                         str(objoau.link_billing_code.sign_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if objoau.link_billing_code else '',
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

    paginator = Paginator(objoau_all, num_page)
    try:
        objoau_all = paginator.page(page)
    except PageNotAnInteger:
        objoau_all = paginator.page(1)
    except EmptyPage:
        objoau_all = paginator.page(paginator.num_pages)

    context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'objoau_all': objoau_all, 'oandufilter': oandufilter,
               'itemperform': itemperform, 'rowcount': str(num_page)}
    return render(request, 'ohfandugf/oandu_t_app_temp.html', context)


@login_required(login_url='login')
def addohfandugf(request):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    form = AddOhfAndUgfDetailsForm()
    if request.method == 'POST':
        form = AddOhfAndUgfDetailsForm(request.POST)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.sign_id = request.user.username
            newform.sign_time = datetime.now()
            newform.save()
            if newform.assign_status:
                fibereng_notification_obj = IllNotification.objects.create(
                    link_code=newform.link_code, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_fiber.username, assign_date_time=newform.sign_time,
                    accept_mod_url="addohfandugffiber", reject_mod_url="rejohfandugffiber")
                fibereng_notification_obj.save()

            return redirect('ohfandugf')
    context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'form': form}
    return render(request, 'ohfandugf/oandu_add.html', context)


@login_required(login_url='login')
def editohfandugf(request, eoauid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)
    objoau = OhfAndUgfDetails.objects.get(id=eoauid)

    if request.user.is_staff or request.user.username == objoau.link_dealer:

        form = EditOhfAndUgfDetailsForm(instance=objoau)

        if request.method == 'POST':
            # if editble:
            form = EditOhfAndUgfDetailsForm(request.POST)
            if form.is_valid():
                newform = form.save(commit=False)
                objoau.link_name = newform.link_name
                objoau.link_point_a = newform.link_point_a
                objoau.link_point_via = newform.link_point_via
                objoau.link_point_b = newform.link_point_b
                objoau.link_point_a_lat = newform.link_point_a_lat
                objoau.link_point_a_long = newform.link_point_a_long
                objoau.link_point_via_lat = newform.link_point_via_lat
                objoau.link_point_via_long = newform.link_point_via_long
                objoau.link_point_b_lat = newform.link_point_b_lat
                objoau.link_point_b_long = newform.link_point_b_long
                objoau.sign_id = request.user.username
                objoau.sign_time = datetime.now()
                if not objoau.assign_status:
                    objoau.assign_fiber = newform.assign_fiber
                    if newform.assign_status:
                        objoau.assign_status = newform.assign_status
                        fibereng_notification_obj = IllNotification.objects.create(
                            link_code=objoau.link_code, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=objoau.id,
                            ill_ntfc_receiver=objoau.assign_fiber.username, assign_date_time=objoau.sign_time,
                            accept_mod_url="addohfandugffiber", reject_mod_url="rejohfandugffiber")
                        fibereng_notification_obj.save()

                objoau.save()
                return redirect('ohfandugf')

        editper = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'editper': editper,
                   'objoau': objoau}
    else:
        editper = False
        context = {'objntfc_all': objntfc_all, 'objmsgs': objmsg, 'objoau': objoau, 'editper': editper}

    return render(request, 'ohfandugf/oandu_edit.html', context)


@login_required(login_url='login')
def addohfandugffiber(request, aoaufid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objnn = IllNotification.objects.get(id=aoaufid)
    finst = {'link_code': objnn.link_code, }
    form = AddOandUFiberDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddOandUFiberDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.link_code = objnn.link_code
            newform.assign_date_time = objnn.assign_date_time
            newform.fiber_receiver = objnn.ill_ntfc_receiver
            newform.sign_id = request.user.username
            newform.sign_time = datetime.now()

            if not newform.assign_date_time == objnn.assign_date_time:
                newform.assign_date_time = objnn.assign_date_time
            newform.save()

            doneconn_obj = OhfAndUgfDetails.objects.get(link_code=newform.link_code)
            doneconn_obj.link_fiber_code = newform
            doneconn_obj.save()

            if newform.assign_status:
                billing_notification_obj = IllNotification.objects.create(
                    link_code=newform.link_code, ill_ntfc_sender=request.user.username,
                    ill_prev_assign_obj_id=newform.id,
                    ill_ntfc_receiver=newform.assign_billing.username, assign_date_time=newform.sign_time,
                    accept_mod_url="addohfandugfbilling", reject_mod_url="rejohfandugfbilling")
                billing_notification_obj.save()

            objnn.delete()

            return redirect('ohfandugf')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objnn': objnn, 'objmsgs': objmsg}
    return render(request, 'ohfandugf/add_oau_fiber.html', context)


@login_required(login_url='login')
def editohfandugffiber(request, eoaufid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objfiber = OhfAndUgfFiberTeamDetails.objects.get(id=eoaufid)
    if request.user.username == objfiber.fiber_receiver or request.user.is_staff:
        form = EditOandUFiberDetailsForm(instance=objfiber)
        if request.method == 'POST':
            form = EditOandUFiberDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)
                objfiber.core_details = newform.core_details
                objfiber.core_color = newform.core_color
                objfiber.distance = newform.distance
                objfiber.otdr = newform.otdr
                objfiber.sign_id = request.user.username
                objfiber.sign_time = datetime.now()

                if not objfiber.assign_status:
                    objfiber.assign_billing = newform.assign_billing
                    if newform.assign_status:
                        objfiber.assign_status = newform.assign_status
                        billing_notification_obj = IllNotification.objects.create(
                            link_code=objfiber.link_code, ill_ntfc_sender=request.user.username,
                            ill_prev_assign_obj_id=objfiber.id,
                            ill_ntfc_receiver=objfiber.assign_billing.username, assign_date_time=objfiber.sign_time,
                            accept_mod_url="addohfandugfbilling", reject_mod_url="rejohfandugfbilling")
                        billing_notification_obj.save()

                objfiber.save()

                return redirect('ohfandugf')
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

    return render(request, 'ohfandugf/edit_oau_fiber.html', context)


@login_required(login_url='login')
def rejohfandugffiber(request, roaufid):
    objnn = IllNotification.objects.get(id=roaufid)
    objoandu = OhfAndUgfDetails.objects.get(id=objnn.ill_prev_assign_obj_id)
    objoandu.assign_status = False
    objoandu.save()

    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objnn.ill_ntfc_sender,
                                                conn_code=objoandu.link_code, rej_module_name='Ohf and Ugf')
    rejmsgobj.save()
    delobj = objnn.id
    objnn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'fiberdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def fiberdetails(request):
    return redirect('ohfandugf')


@login_required(login_url='login')
def billingdetails(request):
    return redirect('billingdetails')


@login_required(login_url='login')
def addohfandugfbilling(request, aoaubid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objnn = IllNotification.objects.get(id=aoaubid)
    finst = {'link_code': objnn.link_code, }
    form = AddOandUBillingDetailsForm(initial=finst)
    if request.method == 'POST':
        form = AddOandUBillingDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.link_code = objnn.link_code
            newform.assign_date_time = objnn.assign_date_time
            newform.billing_receiver = objnn.ill_ntfc_receiver
            newform.sign_id = request.user.username
            newform.sign_time = datetime.now()
            newform.save()
            doneconn_obj = OhfAndUgfDetails.objects.get(link_code=newform.link_code)
            doneconn_obj.link_billing_code = newform
            if newform.link_start_date <= date.today():
                doneconn_obj.link_status = True
            doneconn_obj.save()

            objnn.delete()

            return redirect('ohfandugf')

    context = {'form': form, 'objntfc_all': objntfc_all, 'objnn': objnn, 'objmsgs': objmsg}
    return render(request, 'ohfandugf/add_oau_billing.html', context)


@login_required(login_url='login')
def editohfandugfbilling(request, eoaubid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objbilling = OhfAndUgfBillingDetails.objects.get(id=eoaubid)
    if request.user.username == objbilling.billing_receiver or request.user.is_staff:
        form = EditOandUBillingDetailsForm(instance=objbilling)
        if request.method == 'POST':
            form = EditOandUBillingDetailsForm(request.POST, request.FILES)
            if form.is_valid():
                newform = form.save(commit=False)

                objbilling.sign_id = request.user.username
                objbilling.sign_time = datetime.now()
                objbilling.amount = newform.amount

                if not newform.billing_img == 'emptyfile':
                    objbilling.billing_img = newform.billing_img

                objbilling.transaction_id = newform.transaction_id

                if not newform.transaction_receipt == 'emptyfile':
                    objbilling.transaction_receipt = newform.transaction_receipt

                if not newform.agreement_file == 'emptyfile':
                    objbilling.agreement_file = newform.agreement_file

                objbilling.save()

                return redirect('ohfandugf')
        editper = True
        context = {'form': form, 'objntfc_all': objntfc_all, 'objbilling': objbilling, 'editper': editper,
                   'objmsgs': objmsg}
    else:
        editper = False
        context = {'objntfc_all': objntfc_all,
                   'objbilling': objbilling,
                   'editper': editper,
                   'objmsgs': objmsg,
                   }

    return render(request, 'ohfandugf/edit_oau_billing.html', context)


@login_required(login_url='login')
def rejohfandugfbilling(request, roaubid):
    objnn = IllNotification.objects.get(id=roaubid)
    objfiber = OhfAndUgfFiberTeamDetails.objects.get(id=objnn.ill_prev_assign_obj_id)
    objfiber.assign_status = False
    objfiber.save()

    rejmsgobj = RejectionMessage.objects.create(msg_sender=request.user.username, msg_receiver=objnn.ill_ntfc_sender,
                                                conn_code=objfiber.link_code, rej_module_name='Fiber')
    rejmsgobj.save()

    delobj = objnn.id
    objnn.delete()
    if str(delobj) in request.META.get('HTTP_REFERER') and 'billingdetails' in request.META.get('HTTP_REFERER'):
        return redirect('index')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def renewohfandugfbilling(request, reoaubid):
    objntfc_all = IllNotification.objects.filter(ill_ntfc_receiver=request.user.username)
    objmsg = RejectionMessage.objects.filter(msg_receiver=request.user.username)

    objrebilling = OhfAndUgfBillingDetails.objects.get(id=reoaubid)

    form = RenewBillingDetailsForm()
    if request.method == 'POST':
        prevurl = request.POST.get('prevurl')
        form = RenewBillingDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)

            linkbillinghistory = OhfAndUgfBillingHistory.objects.create(link_code=objrebilling.link_code,
                                                                        assign_date_time=objrebilling.assign_date_time,
                                                                        link_start_date=objrebilling.link_start_date,
                                                                        link_end_date=objrebilling.link_end_date,
                                                                        link_validity=objrebilling.link_validity,
                                                                        payment_method=objrebilling.payment_method,
                                                                        netbanking_type=objrebilling.netbanking_type,
                                                                        transaction_id=objrebilling.transaction_id,
                                                                        payment_status=objrebilling.payment_status,
                                                                        amount=objrebilling.amount,
                                                                        transaction_receipt=objrebilling.transaction_receipt,
                                                                        billing_img=objrebilling.billing_img,
                                                                        billing_receiver=objrebilling.billing_receiver,
                                                                        agreement_file=objrebilling.agreement_file)

            linkbillinghistory.save()

            objrebilling.link_start_date = newform.link_start_date
            objrebilling.link_end_date = newform.link_end_date
            objrebilling.link_validity = newform.link_validity
            objrebilling.amount = newform.amount

            objrebilling.payment_method = newform.payment_method

            if newform.payment_method == '2':
                objrebilling.netbanking_type = newform.netbanking_type
            else:
                objrebilling.netbanking_type = None

            objrebilling.payment_status = newform.payment_status
            objrebilling.transaction_id = newform.transaction_id
            objrebilling.billing_receiver = request.user.username

            if not newform.transaction_receipt == 'emptyfile':
                objrebilling.transaction_receipt = newform.transaction_receipt

            if not newform.billing_img == 'emptyfile':
                objrebilling.billing_img = newform.billing_img

            objrebilling.sign_id = request.user.username
            objrebilling.sign_time = datetime.now()
            donelink_obj = OhfAndUgfDetails.objects.get(link_code=objrebilling.link_code)
            if newform.link_start_date <= date.today():
                donelink_obj.link_status = True
            donelink_obj.save()
            objrebilling.save()

            return redirect(prevurl)

    context = {'objntfc_all': objntfc_all, 'objrebilling': objrebilling, 'form': form, 'objmsgs': objmsg}
    return render(request, 'ohfandugf/renew_oau_billing.html', context)


@login_required(login_url='login')
def historyohfandugfbilling(request, hioaubid):
    billhistobj_all = OhfAndUgfBillingHistory.objects.filter(link_code=hioaubid)
    if request.method == 'POST' and request.POST.get('exportexcelbillhistory'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Ohf-And-Ugf-Billing-History.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('OHF And UGF Billing History')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Link Code', 'Assigned Date and time',
                   'Agreement Start Date', 'Agreement End Date', 'Validity',
                   'Payment Status','amount', 'Payment Method', 'Net Banking Type', 'Transaction ID', 'Accountant ID']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = []

        for billhistobj in billhistobj_all:
            rows.append([billhistobj.link_code if billhistobj.link_code else '',
                         str(billhistobj.assign_date_time.strftime(
                             "%d/%m/%Y %I:%M %p")) if billhistobj.assign_date_time else '',
                         str(billhistobj.link_start_date) if billhistobj.link_start_date else '',
                         str(billhistobj.link_end_date) if billhistobj.link_end_date else '',
                         billhistobj.link_validity if billhistobj.link_validity else '',
                         billhistobj.get_payment_status_display() if billhistobj.get_payment_status_display() else '',
                         billhistobj.amount if billhistobj.amount else '',
                         billhistobj.get_payment_method_display() if billhistobj.get_payment_method_display() else '',
                         billhistobj.get_netbanking_type_display() if billhistobj.get_netbanking_type_display() else '',
                         billhistobj.transaction_id if billhistobj.transaction_id else '',
                         billhistobj.billing_receiver if billhistobj.billing_receiver else '',
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

    context = {'billhistobj_all': billhistobj_all, 'hioaubid': hioaubid}
    return render(request, 'ohfandugf/bill_hist_temp_modal.html', context)
