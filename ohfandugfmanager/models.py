from datetime import datetime

from django.db import models

# Create your models here.
from sitemanager.models import User


class OhfAndUgfVendors(models.Model):
    v_code = models.CharField(verbose_name='vendor code', max_length=255, unique=True)
    v_name = models.CharField(verbose_name='vendor name', max_length=255)
    v_address = models.CharField(verbose_name='vendor address', max_length=255)
    v_contact_person_name = models.CharField(verbose_name='vendor contact person name', max_length=255)
    v_contact_person_no = models.CharField(verbose_name='vendor contact person No', max_length=255)

    def __str__(self):
        return self.v_code

    class Meta:
        verbose_name_plural = '1. Ohf and Ugf Vendors'


class OhfAndUgfFiberTeamDetails(models.Model):
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))
    link_code = models.CharField(verbose_name='Link Code', max_length=255, blank=True, null=True)
    core_details = models.CharField(verbose_name='Core Details', max_length=255)
    core_color = models.CharField(verbose_name='Core Color', max_length=255)
    distance = models.CharField(verbose_name='Distance', max_length=255)
    otdr = models.CharField(verbose_name='OTDR', max_length=255)
    assign_date_time = models.DateTimeField(blank=True, null=True)
    fiber_receiver = models.CharField(max_length=255, blank=True)
    sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)
    assign_billing = models.ForeignKey(User, models.SET_NULL, verbose_name='Billing person',
                                       limit_choices_to={'groups__name': 'billingteam'},
                                       blank=True,
                                       null=True, )
    assign_status = models.BooleanField(verbose_name='assign status',choices=ASBOOL_CHOICES, default=False, )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '5. Ohf and ugf Fiber Details'


class OhfAndUgfBillingDetails(models.Model):
    paymentstatus = (
        ('1', 'Done'),
        ('2', 'Pending'),
    )
    paymentmethod = (
        ('1', 'Cash'),
        ('2', 'NetBanking'),
        ('3', 'Cheque'),
    )
    NetBankingType = (
        ('1', 'NEFT'),
        ('2', 'IMPS'),
        ('3', 'RTGS'),
        ('4', 'UPI'),
    )
    link_code = models.CharField(verbose_name='Link Code', max_length=255, blank=True, null=True)
    assign_date_time = models.DateTimeField(verbose_name='Assign Date Time', blank=True, null=True)
    link_start_date = models.DateField(verbose_name='Link Start Date', blank=True, null=True)
    link_end_date = models.DateField(verbose_name='Link End Date', blank=True, null=True)
    link_validity = models.CharField(verbose_name='Link Validity', max_length=255, null=True, blank=True)
    agreement_file = models.FileField(verbose_name='agreement', upload_to='ohfandugf/onuagreement/', blank=True)
    payment_status = models.CharField(verbose_name='Payment Status', max_length=20, choices=paymentstatus, default='2')
    amount = models.CharField(verbose_name='Amount', max_length=255, blank=True, null=True)
    payment_method = models.CharField(verbose_name='Payment Method', max_length=20, choices=paymentmethod,
                                      blank=True, null=True)
    netbanking_type = models.CharField(verbose_name='Netbanking Type', max_length=20, choices=NetBankingType,
                                       default='1', blank=True, null=True)
    transaction_id = models.CharField(verbose_name='Transaction Id', max_length=255, blank=True, null=True)
    transaction_receipt = models.FileField(verbose_name='Transaction Receipt', upload_to='ohfandugf/transaction/',
                                           blank=True, null=True)
    billing_img = models.FileField(verbose_name='Invoice', upload_to='ohfandugf/billingimages/', blank=True)
    billing_receiver = models.CharField(max_length=255, blank=True)
    sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '6. Ohf and ugf Billing Details'


class OhfAndUgfBillingHistory(models.Model):
    paymentstatus = (
        ('1', 'Done'),
        ('2', 'Pending'),
    )
    paymentmethod = (
        ('1', 'Cash'),
        ('2', 'NetBanking'),
        ('3', 'Cheque'),
    )
    NetBankingType = (
        ('1', 'NEFT'),
        ('2', 'IMPS'),
        ('3', 'RTGS'),
        ('4', 'UPI'),
    )
    link_code = models.CharField(verbose_name='Link Code', max_length=255, blank=True, null=True)
    assign_date_time = models.DateTimeField(verbose_name='Assign Date Time', blank=True, null=True)
    link_start_date = models.DateField(verbose_name='Link Start Date', blank=True, null=True)
    link_end_date = models.DateField(verbose_name='Link End Date', blank=True, null=True)
    link_validity = models.CharField(verbose_name='Link Validity', max_length=255, null=True, blank=True)
    agreement_file = models.FileField(verbose_name='agreement', upload_to='ohfandugf/onuagreement/', blank=True)
    payment_status = models.CharField(verbose_name='Payment Status', max_length=20, choices=paymentstatus, default='2')
    amount = models.CharField(verbose_name='Amount', max_length=255, blank=True, null=True)
    payment_method = models.CharField(verbose_name='Payment Method', max_length=20, choices=paymentmethod,
                                      blank=True, null=True)
    netbanking_type = models.CharField(verbose_name='Netbanking Type', max_length=20, choices=NetBankingType,
                                       default='1', blank=True, null=True)
    transaction_id = models.CharField(verbose_name='Transaction Id', max_length=255, blank=True, null=True)
    transaction_receipt = models.FileField(verbose_name='Transaction Receipt', upload_to='ohfandugf/transaction/',
                                           blank=True, null=True)
    billing_img = models.FileField(verbose_name='Invoice', upload_to='ohfandugf/billingimages/', blank=True)
    billing_receiver = models.CharField(max_length=255, blank=True)


class OhfAndUgfDetails(models.Model):
    link_type_choice = (
        ('1', 'OHF'),
        ('2', 'UGF'),
    )
    link_type_g_t_choice = (
        ('1', 'Taken From Vendor'),
        ('2', 'Given By Threesa'),
    )
    linkstatus = (
        (True, 'Active'),
        (False, 'Deactive'),
    )
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))

    link_code = models.CharField(verbose_name='Link code', max_length=255, unique=True)
    link_name = models.CharField(verbose_name='Link Name', max_length=255)
    link_dealer = models.ForeignKey(User, models.SET_NULL, verbose_name='Dealer', related_name='link_dealer',
                                    limit_choices_to={'groups__name': 'OhfAndUgfManager'}, blank=True,
                                    null=True)
    link_vendor = models.ForeignKey(OhfAndUgfVendors, models.SET_NULL, verbose_name='vendor', blank=True,
                                    null=True)
    link_type_g_t = models.CharField(choices=link_type_g_t_choice, verbose_name='Link Taken or Given', max_length=255)
    link_type = models.CharField(choices=link_type_choice, verbose_name='Link Type', max_length=255)
    link_point_a = models.CharField(verbose_name='Link Ponit A', max_length=255)
    link_point_a_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    link_point_a_long = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    link_point_via = models.CharField(verbose_name='Link Ponit Via', max_length=255)
    link_point_via_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    link_point_via_long = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    link_point_b = models.CharField(verbose_name='Link Ponit B', max_length=255)
    link_point_b_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    link_point_b_long = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    assign_fiber = models.ForeignKey(User, models.SET_NULL, verbose_name='Fiber', related_name='assign_fiber',
                                     limit_choices_to={'groups__name': 'fiberengineer'},
                                     blank=True,
                                     null=True, )
    assign_status = models.BooleanField(verbose_name='assign status',choices=ASBOOL_CHOICES, default=False, null=True, blank=True )
    sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)
    link_status = models.BooleanField(choices=linkstatus, verbose_name='Link active status', default=False)

    link_fiber_code = models.ForeignKey(OhfAndUgfFiberTeamDetails, models.SET_NULL, verbose_name='Fiber details',
                                        blank=True,
                                        null=True)
    link_billing_code = models.ForeignKey(OhfAndUgfBillingDetails, models.SET_NULL, verbose_name='billing details',
                                          blank=True, null=True)


    def __str__(self):
        return self.link_code

    class Meta:
        verbose_name_plural = '4. Ohf and Ugf Link Details'