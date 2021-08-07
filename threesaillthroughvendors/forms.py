from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, Textarea, Select, HiddenInput, CheckboxInput, FileInput, DateInput

from sitemanager.models import ThreesaIllConnectionsDetails
from threesaillthroughvendors.models import TTVIllSalesDetails, TTVIllNocDetails, \
    TTVIllFieldEngineerDetails, TTVIllBillingDetails


class AddIllConForm(forms.ModelForm):
    conn_type_CHOICES = (
        ('2', "Threesa Through Vendor"),
    )
    ill_conn_type = forms.ChoiceField(choices=conn_type_CHOICES,
                                      widget=forms.Select(attrs={"class": "form-control", }), )

    assign_status = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            "class": "checkbox-template",
        }), )

    def clean_ill_custid(self):
        vill_custid = self.cleaned_data['ill_custid']
        if ' ' in vill_custid:
            raise forms.ValidationError('Connection ID should not contain any space')
        return vill_custid

    class Meta:
        model = ThreesaIllConnectionsDetails
        fields = '__all__'
        widgets = {

            "ill_custid": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "ill_cust_name": TextInput(
                attrs={
                    "class": "form-control",
                }),
            "ill_cust_address": Textarea(
                attrs={
                    "class": "form-control",

                }),
            "ill_cust_address_lat": TextInput(
                attrs={
                    "class": "form-control",
                }),
            "ill_cust_address_long": TextInput(
                attrs={
                    "class": "form-control",
                }),

            "ill_vendor_code": Select(
                attrs={
                    "class": "form-control",

                }),

            "ill_sales_person": Select(
                attrs={
                    "class": "form-control",

                }),
            "ill_feasibility": Select(
                attrs={
                    "class": "form-control"
                }),
        }


class AddSalesDetailsForm(forms.ModelForm):
    class Meta:
        model = TTVIllSalesDetails
        fields = ['conn_code', 'location_pin', 'purchase_order_no', 'po_img', 'kyc_details', 'gst_no', 'cust_cpn_name',
                  'ill_sales_receiver',
                  'cust_cpn_num', 'assign_noc', 'assign_date_time', 'ill_sign_id', 'ill_sign_time',
                  'assign_status']
        widgets = {
            "location_pin": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "purchase_order_no": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "po_img": FileInput(
                attrs={
                    "class": "form-control-file",

                }),
            "kyc_details": FileInput(
                attrs={
                    "class": "form-control-file",

                }),
            "gst_no": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "cust_cpn_name": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "cust_cpn_num": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "assign_noc": Select(
                attrs={
                    "class": "form-control",

                }),

            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),
            "conn_code": HiddenInput(),

        }


class EditSalesDetailsForm(forms.ModelForm):
    class Meta:
        model = TTVIllSalesDetails
        fields = ['location_pin', 'purchase_order_no', 'po_img', 'kyc_details', 'gst_no', 'cust_cpn_name',
                  'cust_cpn_num', 'assign_noc', 'assign_status']
        widgets = {
            "location_pin": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "purchase_order_no": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "gst_no": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "cust_cpn_name": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "cust_cpn_num": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "assign_noc": Select(
                attrs={
                    "class": "form-control",

                }),
            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),
        }

    def clean_po_img(self):
        po_img = self.cleaned_data['po_img']
        if po_img:
            return po_img
        else:
            po_img = 'emptyfile'
            return po_img

    def clean_kyc_details(self):
        kyc_details = self.cleaned_data['kyc_details']
        if kyc_details:
            return kyc_details
        else:
            kyc_details = 'emptyfile'
            return kyc_details


class AddNocDetailsForm(forms.ModelForm):
    class Meta:
        model = TTVIllNocDetails
        fields = ['conn_code', 'assign_date_time', 'ill_ip', 'ill_subnet', 'ill_gateway', 'ill_dns',
                  'ill_dns2', 'ill_bandwidth', 'ill_vland', 'ill_mac_add',
                  'ill_routing_status', 'assign_field_engg', 'ill_sign_id', 'ill_sign_time', 'assign_status',
                  'ill_noc_receiver']
        widgets = {
            "ill_ip": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "ill_subnet": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_gateway": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_dns": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_dns2": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_bandwidth": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_vland": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "ill_mac_add": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "ill_routing_status": Select(
                attrs={
                    "class": "form-control",

                }),
            "assign_field_engg": Select(
                attrs={
                    "class": "form-control",

                }),

            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),

            "conn_code": HiddenInput(),

        }


class EditNocDetailsForm(forms.ModelForm):
    class Meta:
        model = TTVIllNocDetails
        fields = ['ill_ip', 'ill_subnet', 'ill_gateway', 'ill_dns',
                  'ill_dns2', 'ill_bandwidth', 'ill_vland', 'ill_mac_add',
                  'ill_routing_status', 'assign_field_engg', 'assign_status', ]
        widgets = {

            "ill_ip": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "ill_subnet": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_gateway": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_dns": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_dns2": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_bandwidth": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "ill_vland": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "ill_mac_add": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "ill_routing_status": Select(
                attrs={
                    "class": "form-control",

                }),
            "assign_field_engg": Select(
                attrs={
                    "class": "form-control",

                }),

            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),
        }


class AddFieldEnggDetailsForm(forms.ModelForm):
    class Meta:
        model = TTVIllFieldEngineerDetails
        fields = ['conn_code', 'assign_date_time', 'link_status', 'cust_cpn_name', 'cust_cpn_num', 'connectivity_img',
                  'assign_billing', 'ill_sign_id', 'ill_sign_time', 'assign_status', 'ill_field_engg_receiver']
        widgets = {
            "link_status": Select(
                attrs={
                    "class": "form-control",

                }),
            "cust_cpn_name": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "cust_cpn_num": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "connectivity_img": FileInput(
                attrs={
                    "class": "form-control-file",

                }),

            "assign_billing": Select(
                attrs={
                    "class": "form-control",

                }),

            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),

            "conn_code": HiddenInput(),

        }


class EditFieldEnggDetailsForm(forms.ModelForm):
    class Meta:
        model = TTVIllFieldEngineerDetails
        fields = ['link_status', 'cust_cpn_name', 'cust_cpn_num', 'connectivity_img',
                  'assign_billing', 'assign_status']
        widgets = {

            "link_status": Select(
                attrs={
                    "class": "form-control",

                }),
            "cust_cpn_name": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "cust_cpn_num": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "assign_billing": Select(
                attrs={
                    "class": "form-control",

                }),

            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),

        }

    def clean_connectivity_img(self):
        connectivity_img = self.cleaned_data['connectivity_img']
        if connectivity_img:
            return connectivity_img
        else:
            connectivity_img = 'emptyfile'
            return connectivity_img


class AddBillingDetailsForm(forms.ModelForm):
    def clean_amount(self):
        v_amount = self.cleaned_data["amount"]
        if not v_amount:
            raise ValidationError("this field required")
        else:
            if v_amount.replace('.', '', 1).isdigit():
                return v_amount
            else:
                raise ValidationError("Enter valid value")

    def clean_netbanking_type(self):
        cleaned_data = super().clean()
        v_payment_method = cleaned_data.get("payment_method")
        v_netbanking_type = cleaned_data.get("netbanking_type")

        if v_payment_method == '2':
            if not v_netbanking_type:
                raise ValidationError("please select type")
            else:
                return v_netbanking_type

    def clean_transaction_receipt(self):
        v_transaction_receipt = self.cleaned_data["transaction_receipt"]
        if not v_transaction_receipt:
            raise ValidationError("this field required")
        else:
            return v_transaction_receipt

    def clean_transaction_id(self):
        v_transaction_id = self.cleaned_data["transaction_id"]
        if not v_transaction_id:
            raise ValidationError("this field required")
        else:
            return v_transaction_id

    class Meta:
        model = TTVIllBillingDetails
        fields = ['conn_code', 'assign_date_time', 'conn_start_date', 'conn_end_date', 'bandwidth', 'link_validity',
                  'payment_status','amount' ,'billing_img', 'ill_sign_id', 'ill_sign_time',
                  'ill_billing_receiver', 'payment_method', 'netbanking_type', 'transaction_id', 'transaction_receipt',
                  ]
        widgets = {
            "conn_start_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "conn_end_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "bandwidth": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_validity": TextInput(
                attrs={
                    "class": "form-control",
                    'readonly': 'true',

                }),
            "payment_status": Select(
                attrs={
                    "class": "form-control",

                }),
            "amount": TextInput(
                attrs={
                    "class": "form-control",
                    "required": True,

                }),
            "payment_method": Select(
                attrs={
                    "class": "form-control",

                }),
            "netbanking_type": Select(
                attrs={
                    "class": "form-control",

                }),
            "transaction_id": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "transaction_receipt": FileInput(
                attrs={
                    "class": "form-control-file",

                }),
            "billing_img": FileInput(
                attrs={
                    "class": "form-control-file",

                }),

            "conn_code": HiddenInput(),

        }


class EditBillingDetailsForm(forms.ModelForm):
    def clean_amount(self):
        v_amount = self.cleaned_data["amount"]
        if not v_amount:
            raise ValidationError("this field required")
        else:
            if v_amount.replace('.', '', 1).isdigit():
                return v_amount
            else:
                raise ValidationError("Enter valid value")

    class Meta:
        model = TTVIllBillingDetails

        fields = ['bandwidth', 'billing_img','amount', 'transaction_id', 'transaction_receipt', ]
        widgets = {
            "bandwidth": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "transaction_id": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "amount": TextInput(
                attrs={
                    "class": "form-control",
                    "required": True,

                }),

        }

    def clean_billing_img(self):
        billing_img = self.cleaned_data['billing_img']
        if billing_img:
            return billing_img
        else:
            billing_img = 'emptyfile'
            return billing_img

    def clean_transaction_receipt(self):
        transaction_receipt = self.cleaned_data['transaction_receipt']
        if transaction_receipt:
            return transaction_receipt
        else:
            transaction_receipt = 'emptyfile'
            return transaction_receipt


class RenewBillingDetailsForm(forms.ModelForm):
    def clean_amount(self):
        v_amount = self.cleaned_data["amount"]
        if not v_amount:
            raise ValidationError("this field required")
        else:
            if v_amount.replace('.', '', 1).isdigit():
                return v_amount
            else:
                raise ValidationError("Enter valid value")

    def clean_netbanking_type(self):
        cleaned_data = super().clean()
        v_payment_method = cleaned_data.get("payment_method")
        v_netbanking_type = cleaned_data.get("netbanking_type")

        if v_payment_method == '2':
            if not v_netbanking_type:
                raise ValidationError("please select type")
            else:
                return v_netbanking_type

    def clean_transaction_receipt(self):
        v_transaction_receipt = self.cleaned_data["transaction_receipt"]
        if not v_transaction_receipt:
            raise ValidationError("this field required")
        else:
            return v_transaction_receipt

    def clean_transaction_id(self):
        v_transaction_id = self.cleaned_data["transaction_id"]
        if not v_transaction_id:
            raise ValidationError("this field required")
        else:
            return v_transaction_id

    class Meta:
        model = TTVIllBillingDetails
        fields = ['conn_start_date', 'conn_end_date', 'bandwidth', 'link_validity',
                  'payment_status','amount', 'billing_img', 'ill_sign_id', 'ill_sign_time',
                  'payment_method', 'netbanking_type', 'transaction_id', 'transaction_receipt',
                  ]
        widgets = {
            "conn_start_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "conn_end_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "bandwidth": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_validity": TextInput(
                attrs={
                    "class": "form-control",
                    'readonly': 'true',

                }),
            "payment_status": Select(
                attrs={
                    "class": "form-control",

                }),
            "amount": TextInput(
                attrs={
                    "class": "form-control",
                    "required": True,

                }),
            "payment_method": Select(
                attrs={
                    "class": "form-control",

                }),
            "netbanking_type": Select(
                attrs={
                    "class": "form-control",

                }),
            "transaction_id": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "transaction_receipt": FileInput(
                attrs={
                    "class": "form-control-file",

                }),
            "billing_img": FileInput(
                attrs={
                    "class": "form-control-file",

                }),

        }
