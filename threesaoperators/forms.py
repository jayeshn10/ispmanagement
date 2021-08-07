from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, Select, CheckboxInput, FileInput, DateInput, HiddenInput

from threesaoperators.models import NetOperatorsDetails, NetOperatorsFiberDetails, NetOperatorsNocDetails, \
    NetOperatorsBillingDetails


class AddOperatorDetailsForm(forms.ModelForm):
    def clean_operator_id(self):
        voperator_id = self.cleaned_data['operator_id']
        if ' ' in voperator_id:
            raise forms.ValidationError('Operator ID should not contain any space')
        return voperator_id

    class Meta:
        model = NetOperatorsDetails
        fields = ['operator_id', 'operator_name', 'Operator_register', 'operator_dealer', 'op_contact_pname',
                  'op_contact_pnum', 'op_kyc', 'assign_fiber', 'assign_status', 'sign_id', 'sign_time', ]
        widgets = {

            "operator_id": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "operator_name": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "Operator_register": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "zones": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "operator_dealer": Select(
                attrs={
                    "class": "form-control",

                }),
            "op_contact_pname": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "op_contact_pnum": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "op_kyc": FileInput(
                attrs={
                    "class": "form-control-file",

                }),
            "assign_fiber": Select(
                attrs={
                    "class": "form-control",
                    'required': True

                }),
            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),

        }


class EditOperatorDetailsForm(forms.ModelForm):
    class Meta:
        model = NetOperatorsDetails
        fields = ['operator_name', 'op_contact_pname', 'op_contact_pnum', 'op_kyc', 'assign_fiber', 'assign_status',
                  'sign_id', 'sign_time', ]
        widgets = {
            "operator_name": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "op_contact_pname": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "op_contact_pnum": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "assign_fiber": Select(
                attrs={
                    "class": "form-control",
                    'required': True

                }),
            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),

        }

    def clean_op_kyc(self):
        vop_kyc = self.cleaned_data['op_kyc']
        if vop_kyc:
            return vop_kyc
        else:
            vop_kyc = 'emptyfile'
            return vop_kyc


class AddZoneForm(forms.Form):
    zone_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control znvald', 'required': True}))
    zone_area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))


class AddOperatorFiberDetailsForm(forms.ModelForm):
    class Meta:
        model = NetOperatorsFiberDetails
        fields = ['operator_id', 'assign_date_time', 'core_details', 'core_color', 'op_switch_img', 'pop_name',
                  'fiber_receiver', 'assign_noc',
                  'sign_id', 'sign_time', 'assign_status', ]
        widgets = {
            "op_switch_img": FileInput(
                attrs={
                    "class": "form-control-file",

                }),

            "core_details": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "core_color": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "pop_name": TextInput(
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

            "operator_id": HiddenInput(),
            "assign_date_time": HiddenInput(),

        }


class EditOperatorFiberDetailsForm(forms.ModelForm):
    class Meta:
        model = NetOperatorsFiberDetails
        fields = ['assign_date_time', 'core_details', 'core_color', 'op_switch_img', 'pop_name',
                  'fiber_receiver', 'assign_noc',
                  'sign_id', 'sign_time', 'assign_status', ]
        widgets = {
            "core_details": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "core_color": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "pop_name": TextInput(
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


class AddOperatorNocDetailsForm(forms.ModelForm):
    class Meta:
        model = NetOperatorsNocDetails
        fields = ['operator_id', 'assign_date_time', 'server_ip', 'subnet', 'gateway', 'dns',
                  'dns2', 'switch_ip', 'switch_port_no', 'vland', 'mac_add',
                  'routing_status', 'assign_billing', 'sign_id', 'sign_time', 'assign_status',
                  'noc_receiver']
        widgets = {
            "server_ip": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "subnet": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "gateway": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "dns": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "dns2": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "switch_ip": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "switch_port_no": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "vland": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "mac_add": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "routing_status": Select(
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

            "operator_id": HiddenInput(),
            "assign_date_time": HiddenInput(),

        }


class EditOperatorNocDetailsForm(forms.ModelForm):
    class Meta:
        model = NetOperatorsNocDetails
        fields = ['server_ip', 'subnet', 'gateway', 'dns',
                  'dns2', 'switch_ip', 'switch_port_no', 'vland', 'mac_add',
                  'routing_status', 'assign_billing', 'sign_id', 'sign_time', 'assign_status',
                  ]
        widgets = {
            "server_ip": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "subnet": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "gateway": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "dns": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "dns2": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "switch_ip": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "switch_port_no": TextInput(
                attrs={
                    "class": "form-control",

                }),

            "vland": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "mac_add": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "routing_status": Select(
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


class AddOperatorBillingDetailsForm(forms.ModelForm):
    def clean_amount(self):
        v_amount = self.cleaned_data["amount"]
        if not v_amount:
            raise ValidationError("this field required")
        else:
            if v_amount.replace('.','',1).isdigit():
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
        model = NetOperatorsBillingDetails
        fields = ['operator_id', 'assign_date_time', 'payment_start_date', 'payment_end_date', 'no_topup',
                  'payment_validity', 'payment_status','amount', 'payment_method', 'netbanking_type',
                  'transaction_id', 'transaction_receipt','op_payment_receipt',
                  'sign_id', 'sign_time', 'billing_receiver',]
        widgets = {
            "payment_start_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "payment_end_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "no_topup": TextInput(
                attrs={
                    "class": "form-control",
                }),
            "payment_validity": TextInput(
                attrs={
                    "class": "form-control",
                    'readonly': 'true',

                }),
            "amount": TextInput(
                attrs={
                    "class": "form-control",
                    "required":True,

                }),
            "payment_status": Select(
                attrs={
                    "class": "form-control",

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
            "op_payment_receipt": FileInput(
                attrs={
                    "class": "form-control-file",

                }),


            "operator_id": HiddenInput(),
            "assign_date_time": HiddenInput(),

        }


class EditOperatorBillingDetailsForm(forms.ModelForm):
    def clean_amount(self):
        v_amount = self.cleaned_data["amount"]
        if not v_amount:
            raise ValidationError("this field required")
        else:
            if v_amount.replace('.','',1).isdigit():
                return v_amount
            else:
                raise ValidationError("Enter valid value")


    class Meta:
        model = NetOperatorsBillingDetails
        fields = ['transaction_id', 'transaction_receipt', 'amount','op_payment_receipt',
                  'sign_id', 'sign_time',]
        widgets = {

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

    def clean_transaction_receipt(self):
        vtransaction_receipt = self.cleaned_data['transaction_receipt']
        if vtransaction_receipt:
            return vtransaction_receipt
        else:
            vtransaction_receipt = 'emptyfile'
            return vtransaction_receipt

    def clean_op_payment_receipt(self):
        vop_payment_receipt = self.cleaned_data['op_payment_receipt']
        if vop_payment_receipt:
            return vop_payment_receipt
        else:
            vop_payment_receipt = 'emptyfile'
            return vop_payment_receipt


class RenewOperatorBillingDetailsForm(forms.ModelForm):
    def clean_amount(self):
        v_amount = self.cleaned_data["amount"]
        if not v_amount:
            raise ValidationError("this field required")
        else:
            if v_amount.replace('.','',1).isdigit():
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
        model = NetOperatorsBillingDetails
        fields = ['payment_start_date', 'payment_end_date', 'no_topup',
                  'payment_validity', 'payment_status','amount' ,'payment_method', 'netbanking_type',
                  'transaction_id', 'transaction_receipt','op_payment_receipt',
                  'sign_id', 'sign_time', 'billing_receiver',]
        widgets = {
            "payment_start_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "payment_end_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "no_topup": TextInput(
                attrs={
                    "class": "form-control",
                }),
            "payment_validity": TextInput(
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
            "op_payment_receipt": FileInput(
                attrs={
                    "class": "form-control-file",

                }),

        }

