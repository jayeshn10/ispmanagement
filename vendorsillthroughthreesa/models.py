from datetime import datetime

from django.db import models

# Create your models here.

from sitemanager.models import ThreesaIllConnectionsDetails, User


class VTTIllSalesDetails(models.Model):
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))
    conn_code = models.ForeignKey(ThreesaIllConnectionsDetails, on_delete=models.CASCADE,
                                  verbose_name='Ill Connection ID')
    location_pin = models.CharField(verbose_name='Location Pin', max_length=255)
    purchase_order_no = models.CharField(verbose_name='Purchase Order No', max_length=255)
    po_img = models.FileField(upload_to='illdata/po_file/', blank=True)
    kyc_details = models.FileField(upload_to='illdata/kyc_file/', blank=True)
    gst_no = models.CharField(verbose_name='Gst No', max_length=255)
    cust_cpn_name = models.CharField(verbose_name='Contact Person Name', max_length=255)
    cust_cpn_num = models.CharField(verbose_name='Contact Person Number', max_length=255)
    assign_fiber_engg = models.ForeignKey(User, models.SET_NULL, verbose_name='Fiber Person Name',
                                          limit_choices_to={'groups__name': 'fiberengineer'},
                                          blank=True,
                                          null=True, )
    assign_date_time = models.DateTimeField(blank=True, null=True)
    ill_sales_receiver = models.CharField(max_length=255, blank=True)
    ill_sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    ill_sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)
    assign_status = models.BooleanField(verbose_name='assign status',choices=ASBOOL_CHOICES, default=False, )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '2. Sales Details'


class VTTIllFiberTeam(models.Model):
    MEDIA_CHOICES = (
        ('1', '1000'),
        ('2', '100'),
    )
    CORE_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))
    conn_code = models.ForeignKey(ThreesaIllConnectionsDetails, on_delete=models.CASCADE,
                                  verbose_name='Ill Connection ID')
    media_img = models.FileField(verbose_name='Upload Media Image', upload_to='illdata/mediaimages/', blank=True)
    switch_img = models.FileField(verbose_name='Upload switch Image', upload_to='illdata/switchimages/', blank=True)
    port_media_type = models.CharField(verbose_name='Port Media Type', max_length=20, choices=MEDIA_CHOICES,
                                       default='1')
    fiber_core = models.CharField(verbose_name='Fiber Core', max_length=20, choices=CORE_CHOICES, default='1')
    pop_name = models.CharField(verbose_name='POP Name', max_length=255)
    assign_noc = models.ForeignKey(User, models.SET_NULL, verbose_name='noc Person Name',
                                   limit_choices_to={'groups__name': 'nocengineer'},
                                   blank=True,
                                   null=True, )
    assign_date_time = models.DateTimeField(blank=True, null=True)
    ill_fiber_receiver = models.CharField(max_length=255, blank=True)
    ill_sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    ill_sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)
    assign_status = models.BooleanField(verbose_name='assign status',choices=ASBOOL_CHOICES, default=False, )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '3. Fiber Team'


class VTTIllNocDetails(models.Model):
    ROUTING_CHOICES = (
        ('1', 'done'),
        ('2', 'pending'),
    )
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))

    conn_code = models.ForeignKey(ThreesaIllConnectionsDetails, on_delete=models.CASCADE,
                                  verbose_name='Ill Connection ID')
    ill_ip = models.CharField(verbose_name=' IP ', max_length=255)
    ill_subnet = models.CharField(verbose_name='Subnet', max_length=255)
    ill_gateway = models.CharField(verbose_name='Gateway', max_length=255)
    ill_dns = models.CharField(verbose_name='DNS', max_length=255)
    ill_dns2 = models.CharField(verbose_name='DNS2 ', max_length=255)
    ill_switch_ip = models.CharField(verbose_name='Switch IP', max_length=255)
    ill_switch_port_no = models.CharField(verbose_name='Switch Port No.', max_length=255)
    ill_bandwidth = models.CharField(verbose_name='bandwidth', max_length=255)
    ill_vland = models.CharField(verbose_name='VLAND', max_length=255)
    ill_mac_add = models.CharField(verbose_name='MAC Address', max_length=255)
    ill_routing_status = models.CharField(verbose_name='Routing Status', max_length=20, choices=ROUTING_CHOICES,
                                          default='1')

    assign_field_engg = models.ForeignKey(User, models.SET_NULL, verbose_name='Field Engineer Name',
                                          limit_choices_to={'groups__name': 'fieldengineer'},
                                          blank=True,
                                          null=True, )
    assign_date_time = models.DateTimeField(blank=True, null=True)
    ill_noc_receiver = models.CharField(max_length=255, blank=True)
    ill_sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    ill_sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)
    assign_status = models.BooleanField(verbose_name='assign status',choices=ASBOOL_CHOICES, default=False, )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '4. NOC Details'


class VTTIllFieldEngineerDetails(models.Model):
    linkstatus = (
        ('1', 'up'),
        ('2', 'down'),
    )
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))
    conn_code = models.ForeignKey(ThreesaIllConnectionsDetails, on_delete=models.CASCADE,
                                  verbose_name='Ill Connection ID')
    link_status = models.CharField(verbose_name='Link Status', max_length=20, choices=linkstatus, default='1')
    cust_cpn_name = models.CharField(verbose_name='Company Contact Person Name', max_length=255)
    cust_cpn_num = models.CharField(verbose_name='Company Contact Person Number', max_length=255)
    connectivity_img = models.FileField(verbose_name='Upload Connectivity Proof', upload_to='illdata/connectivityproofimages/',
                                        blank=True)
    assign_billing = models.ForeignKey(User, models.SET_NULL, verbose_name='Billing person',
                                       limit_choices_to={'groups__name': 'billingteam'},
                                       blank=True,
                                       null=True, )
    assign_date_time = models.DateTimeField(blank=True, null=True)
    ill_field_engg_receiver = models.CharField(max_length=255, blank=True)
    ill_sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    ill_sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)
    assign_status = models.BooleanField(verbose_name='assign status',choices=ASBOOL_CHOICES, default=False, )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '5. Field Engineer Details'


class VTTIllBillingDetails(models.Model):
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
    conn_code = models.ForeignKey(ThreesaIllConnectionsDetails, on_delete=models.CASCADE,
                                  verbose_name='Ill Connection ID')
    assign_date_time = models.DateTimeField(verbose_name='Assign Date Time', blank=True, null=True)
    conn_start_date = models.DateField(verbose_name='Connection Start Date', blank=True, null=True)
    conn_end_date = models.DateField(verbose_name='Connection End Date', blank=True, null=True)
    bandwidth = models.CharField(verbose_name='Bandwidth', max_length=255, null=True, blank=True)
    link_validity = models.CharField(verbose_name='Link Validity', max_length=255, null=True, blank=True)

    payment_method = models.CharField(verbose_name='Payment Method', max_length=20, choices=paymentmethod,
                                      blank=True, null=True)
    netbanking_type = models.CharField(verbose_name='Netbanking Type', max_length=20, choices=NetBankingType,
                                       default='1', blank=True, null=True)
    transaction_id = models.CharField(verbose_name='Transaction Id', max_length=255, blank=True, null=True)
    payment_status = models.CharField(verbose_name='Payment Status', max_length=20, choices=paymentstatus, default='2')
    amount = models.CharField(verbose_name='Amount', max_length=255, blank=True, null=True)
    transaction_receipt = models.FileField(verbose_name='Transaction Receipt', upload_to='illdata/transaction/',
                                           blank=True, null=True)
    billing_img = models.FileField(verbose_name='Invoice', upload_to='illdata/billingimages/', blank=True)
    ill_billing_receiver = models.CharField(max_length=255, blank=True, null=True)
    ill_sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    ill_sign_time = models.DateTimeField(verbose_name='sign time', default=datetime.now, blank=True)


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '6. Billing Details'


class VTTIllDoneConnectionsDetails(models.Model):
    linkstatus = (
        (True, 'Active'),
        (False, 'Deactive'),
    )
    conn_code = models.ForeignKey(ThreesaIllConnectionsDetails, on_delete=models.CASCADE,
                                  verbose_name='Ill Connection ID')
    active_status = models.BooleanField(choices=linkstatus, verbose_name='active status', default=False)
    sale_code = models.ForeignKey(VTTIllSalesDetails, models.SET_NULL, verbose_name='sales details', blank=True,
                                  null=True)
    fiber_code = models.ForeignKey(VTTIllFiberTeam, models.SET_NULL, verbose_name='Fiber details', blank=True,
                                   null=True)
    noc_code = models.ForeignKey(VTTIllNocDetails, models.SET_NULL, verbose_name='NOC details', blank=True,
                                 null=True)
    fe_code = models.ForeignKey(VTTIllFieldEngineerDetails, models.SET_NULL, verbose_name='FE details', blank=True,
                                null=True)
    billing_code = models.ForeignKey(VTTIllBillingDetails, models.SET_NULL, verbose_name='billing details',
                                     blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = '1. VTT ILL Done Connections'