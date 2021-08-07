from datetime import datetime

from django.db import models

# Create your models here.
from sitemanager.models import User


class NetOperatorsFiberDetails(models.Model):
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))
    operator_id = models.CharField(verbose_name='Operator ID', max_length=255, blank=True, null=True)
    assign_date_time = models.DateTimeField(blank=True, null=True)
    core_details = models.CharField(verbose_name='Core Details', max_length=255)
    core_color = models.CharField(verbose_name='Core Color', max_length=255)
    op_switch_img = models.FileField(verbose_name='Switch Image', upload_to='netoperator/switch/',
                                     blank=True, null=True)
    pop_name = models.CharField(verbose_name='POP Name', max_length=255, blank=True, null=True)

    fiber_receiver = models.CharField(max_length=255, blank=True)
    assign_noc = models.ForeignKey(User, models.SET_NULL, verbose_name='noc engineer',
                                   limit_choices_to={'groups__name': 'nocengineer'},
                                   blank=True,
                                   null=True, )
    assign_status = models.BooleanField(verbose_name='assign status', choices=ASBOOL_CHOICES, default=False, )
    sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '2. Fiber Details'


class NetOperatorsNocDetails(models.Model):
    ROUTING_CHOICES = (
        ('1', 'done'),
        ('2', 'pending'),
    )
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))

    operator_id = models.CharField(verbose_name='operator id', max_length=255)
    assign_date_time = models.DateTimeField(blank=True, null=True)

    server_ip = models.CharField(verbose_name='Server IP ', max_length=255)
    subnet = models.CharField(verbose_name='Subnet', max_length=255)
    gateway = models.CharField(verbose_name='Gateway', max_length=255)
    dns = models.CharField(verbose_name='DNS', max_length=255)
    dns2 = models.CharField(verbose_name='DNS2 ', max_length=255)
    switch_ip = models.CharField(verbose_name='Switch IP', max_length=255)
    switch_port_no = models.CharField(verbose_name='Switch Port No.', max_length=255)
    vland = models.CharField(verbose_name='VLAND', max_length=255)
    mac_add = models.CharField(verbose_name='MAC Address', max_length=255)
    routing_status = models.CharField(verbose_name='Routing Status', max_length=20, choices=ROUTING_CHOICES,
                                      default='1')

    assign_billing = models.ForeignKey(User, models.SET_NULL, verbose_name='billing Person Name',
                                       limit_choices_to={'groups__name': 'billingteam'},
                                       blank=True,
                                       null=True, )
    noc_receiver = models.CharField(max_length=255, blank=True)
    assign_status = models.BooleanField(verbose_name='assign status', choices=ASBOOL_CHOICES, default=False, )
    sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '3. NOC Details'


class NetOperatorsBillingDetails(models.Model):
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
    operator_id = models.CharField(verbose_name='operator id', max_length=255)
    assign_date_time = models.DateTimeField(verbose_name='Assign Date Time', blank=True, null=True)
    payment_start_date = models.DateField(verbose_name='Payment Start Date', blank=True, null=True)
    payment_end_date = models.DateField(verbose_name='Payment End Date', blank=True, null=True)
    no_topup = models.IntegerField(verbose_name='Top Up', null=True, blank=True)
    payment_validity = models.CharField(verbose_name='Link Validity', max_length=255, null=True, blank=True)
    payment_method = models.CharField(verbose_name='Payment Method', max_length=20, choices=paymentmethod,
                                      blank=True, null=True)
    netbanking_type = models.CharField(verbose_name='Netbanking Type', max_length=20, choices=NetBankingType,
                                       default='1', blank=True, null=True)
    transaction_id = models.CharField(verbose_name='Transaction Id', max_length=255, blank=True, null=True)
    payment_status = models.CharField(verbose_name='Payment Status', max_length=20, choices=paymentstatus, default='2')
    amount = models.CharField(verbose_name='amount', max_length=255, null=True, blank=True)
    transaction_receipt = models.FileField(verbose_name='Transaction Receipt', upload_to='netoperator/transaction/',
                                           blank=True, null=True)
    op_payment_receipt = models.FileField(verbose_name='payment receipt', upload_to='netoperator/invoice/', blank=True)
    billing_receiver = models.CharField(max_length=255, blank=True, null=True)
    sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '6. Billing Details'


class NetOperatorsZones(models.Model):
    zone_name = models.CharField(verbose_name='Zone name', max_length=255)
    zone_area = models.CharField(verbose_name='zone area', max_length=255)

    def __str__(self):
        return self.zone_name

    class Meta:
        verbose_name_plural = '7. Operator Zones'


class NetOperatorsDetails(models.Model):
    activestatus = (
        (True, 'Active'),
        (False, 'Deactive'),
    )
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))

    operator_id = models.CharField(verbose_name='operator id', max_length=255, unique=True)
    operator_name = models.CharField(verbose_name='operator name', max_length=255)
    Operator_register = models.DateTimeField(verbose_name='Operator Registration Date', default=datetime.now,
                                             blank=True, null=True)

    zones = models.ManyToManyField(NetOperatorsZones, verbose_name='Zone', blank=True, related_name="zone_set",
                                   related_query_name="opzone", )
    operator_dealer = models.ForeignKey(User, models.SET_NULL, verbose_name='operator dealer',
                                        related_name='opoperator_dealer',
                                        limit_choices_to={'groups__name': 'operatormanager'},
                                        blank=True,
                                        null=True, )
    op_contact_pname = models.CharField(verbose_name='Contact Person Name', max_length=255)
    op_contact_pnum = models.CharField(verbose_name='Contact Person Number', max_length=255)
    op_kyc = models.FileField(verbose_name='KYC Document', upload_to='netoperator/kyc/',
                              blank=True, null=True)
    assign_fiber = models.ForeignKey(User, models.SET_NULL, verbose_name='Fiber', related_name='opassign_fiber',
                                     limit_choices_to={'groups__name': 'fiberengineer'},
                                     blank=True,
                                     null=True, )
    assign_status = models.BooleanField(verbose_name='assign status', choices=ASBOOL_CHOICES, default=False, null=True,
                                        blank=True)
    sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)
    active_status = models.BooleanField(choices=activestatus, verbose_name='active status', default=False)

    op_fiber_code = models.ForeignKey(NetOperatorsFiberDetails, models.SET_NULL, verbose_name='Fiber details',
                                      blank=True,
                                      null=True)
    op_noc_code = models.ForeignKey(NetOperatorsNocDetails, models.SET_NULL, verbose_name='NOC details',
                                    blank=True,
                                    null=True)
    op_billing_code = models.ForeignKey(NetOperatorsBillingDetails, models.SET_NULL, verbose_name='billing details',
                                        blank=True, null=True)

    def __str__(self):
        return self.operator_id

    class Meta:
        verbose_name_plural = '1. NetOperators Details'


class OpBillingHistory(models.Model):
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
    operator_id = models.CharField(verbose_name='operator id', max_length=255)
    assign_date_time = models.DateTimeField(verbose_name='Assign Date Time', blank=True, null=True)
    payment_start_date = models.DateField(verbose_name='Payment Start Date', blank=True, null=True)
    payment_end_date = models.DateField(verbose_name='Payment End Date', blank=True, null=True)
    no_topup = models.IntegerField(verbose_name='Top Up', null=True, blank=True)
    payment_validity = models.CharField(verbose_name='Link Validity', max_length=255, null=True, blank=True)
    payment_method = models.CharField(verbose_name='Payment Method', max_length=20, choices=paymentmethod,
                                      blank=True, null=True)
    netbanking_type = models.CharField(verbose_name='Netbanking Type', max_length=20, choices=NetBankingType,
                                       default='1', blank=True, null=True)
    transaction_id = models.CharField(verbose_name='Transaction Id', max_length=255, blank=True, null=True)
    payment_status = models.CharField(verbose_name='Payment Status', max_length=20, choices=paymentstatus, default='2')
    amount = models.CharField(verbose_name='Amount', max_length=255, blank=True, null=True)
    transaction_receipt = models.FileField(verbose_name='Transaction Receipt', upload_to='netoperator/transaction/',
                                           blank=True, null=True)
    op_payment_receipt = models.FileField(verbose_name='payment receipt', upload_to='netoperator/invoice/', blank=True)
    billing_receiver = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Operator Billing History'
