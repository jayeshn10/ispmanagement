from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    user_full_name = models.CharField(max_length=100, null=True)
    user_mobile = models.IntegerField(null=True)
    user_image = models.ImageField(blank=True, null=True, upload_to='profileimages/', )
    objects = UserManager()

    class Meta:
        verbose_name_plural = '1. Users'

    def __str__(self):
        return self.username


class IllVendors(models.Model):
    v_code = models.CharField(verbose_name='vendor code', max_length=255, unique=True)
    v_name = models.CharField(verbose_name='vendor name', max_length=255)
    v_contactno = models.CharField(verbose_name='vendor contact number', max_length=255)
    v_address = models.CharField(verbose_name='vendor address', max_length=255)
    v_kyc = models.FileField(verbose_name='Upload kyc details', upload_to='vendorskyc/',
                             blank=True)
    v_gstno = models.CharField(verbose_name='vendor GST number', max_length=255)

    class Meta:
        verbose_name_plural = '2. ILL Vendors'

    def __str__(self):
        return self.v_code


class ThreesaIllConnectionsDetails(models.Model):
    FBOOL_CHOICES = ((True, 'Possible'), (False, 'Not Possible'))
    ASBOOL_CHOICES = ((True, 'Assigned'), (False, 'Not Assigned'))
    conn_type = (('1', 'Threesa'), ('2', 'Threesa Through Vendor'), ('3', 'Vendor Through Threesa'))
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Connection Code')
    ill_custid = models.CharField(verbose_name='Connection Id', max_length=255, unique=True)
    ill_gendate = models.DateTimeField(verbose_name='Lead Generation Date', auto_now_add=True)
    ill_cust_name = models.CharField(verbose_name='Customer Name', max_length=255)
    ill_cust_address = models.TextField(verbose_name='Customer Address')
    ill_cust_address_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    ill_cust_address_long = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    ill_conn_type = models.CharField(verbose_name='Connection Type', max_length=255, choices=conn_type, default=1)
    ill_vendor_code = models.ForeignKey(IllVendors, models.SET_NULL, verbose_name='vendor details', blank=True,
                                        null=True)
    ill_sales_person = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Sales Person Name',
                                         limit_choices_to={'groups__name': 'salesperson'}, )
    ill_feasibility = models.BooleanField(choices=FBOOL_CHOICES, verbose_name='Feasibility Status', default=False)
    ill_sign_id = models.CharField(verbose_name='sign id', max_length=255, null=True, blank=True)
    ill_sign_time = models.DateTimeField(verbose_name='sign time', null=True, blank=True)
    assign_status = models.BooleanField(choices=ASBOOL_CHOICES, verbose_name='assign status', default=False, )

    class Meta:
        verbose_name_plural = '6. ILL Connections'

    def __str__(self):
        return self.ill_custid


class RejectionMessage(models.Model):
    msg_sender = models.CharField(max_length=255)
    msg_receiver = models.CharField(max_length=255)
    conn_code = models.CharField(max_length=255)
    rej_module_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = '9. ILL Rejection Message'

    def __str__(self):
        return str(self.id)


class IllNotification(models.Model):
    conn_type = (('1', 'Threesa'), ('2', 'Threesa Through Vendor'), ('3', 'Vendor Through Threesa'))

    conn_code = models.ForeignKey(ThreesaIllConnectionsDetails, on_delete=models.SET_NULL,
                                  verbose_name='Ill Connection ID', blank=True, null=True)
    link_code = models.CharField(verbose_name='Link Code', max_length=255, blank=True, null=True)
    ill_prev_assign_obj_id = models.IntegerField(verbose_name="Previous id")
    ill_ntfc_sender = models.CharField(verbose_name='Notification Sender', max_length=255, blank=True)
    ill_ntfc_receiver = models.CharField(verbose_name='Notification Receiver', max_length=255, blank=True)
    assign_date_time = models.DateTimeField(verbose_name='Assign Time')
    accept_mod_url = models.CharField(verbose_name='Accept Url', max_length=255, blank=True)
    reject_mod_url = models.CharField(verbose_name='Reject Url', max_length=255, blank=True)
    ill_app_name = models.CharField(verbose_name='ILL App Name', max_length=255, blank=True, choices=conn_type)

    class Meta:
        verbose_name_plural = '8. ILL Notification'

    def __str__(self):
        return str(self.id)


class IllConnectionShiftHistory(models.Model):
    shifter_user = models.CharField(verbose_name='Shifter Username', max_length=255)
    shift_conn_id = models.CharField(verbose_name='Shifted connection id', max_length=255)
    shift_from = models.CharField(verbose_name='Shifted from', max_length=255)
    shift_to = models.CharField(verbose_name='Shifted to', max_length=255)
    shift_date = models.DateTimeField(verbose_name='shifted Date')

    class Meta:
        verbose_name_plural = '7. ILL Connection Shift History'

    def __str__(self):
        return str(self.id)


class IllBillingHistory(models.Model):
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
    conn_code = models.CharField(verbose_name='Connection Id', max_length=255, null=True, blank=True)
    conn_type = models.CharField(verbose_name='Connection Type', max_length=255, null=True, blank=True)
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

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'ILL Billing History'
