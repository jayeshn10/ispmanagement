from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, Select, CheckboxInput, HiddenInput, FileInput, DateInput

from ohfandugfmanager.models import OhfAndUgfDetails, OhfAndUgfFiberTeamDetails, OhfAndUgfBillingDetails


class AddOhfAndUgfDetailsForm(forms.ModelForm):
    def clean_link_code(self):
        vlink_code = self.cleaned_data['link_code']
        if ' ' in vlink_code:
            raise forms.ValidationError('Link Code should not contain any space')
        return vlink_code

    class Meta:
        model = OhfAndUgfDetails
        fields = ['link_code', 'link_name', 'link_dealer', 'link_vendor', 'link_type_g_t', 'link_type', 'link_point_a',
                  'link_point_a_lat', 'link_point_a_long',
                  'link_point_via', 'link_point_via_lat',
                  'link_point_via_long',
                  'link_point_b', 'link_point_b_lat',
                  'link_point_b_long', 'assign_fiber', 'assign_status', 'sign_id', 'sign_time', ]
        widgets = {
            "link_code": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_name": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_dealer": Select(
                attrs={
                    "class": "form-control",

                }),
            "link_vendor": Select(
                attrs={
                    "class": "form-control",

                }),
            "link_type_g_t": Select(
                attrs={
                    "class": "form-control",

                }),
            "link_type": Select(
                attrs={
                    "class": "form-control",

                }),
            "link_point_a": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_a_lat": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_a_long": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_via": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_via_lat": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_via_long": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_b": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_b_lat": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_b_long": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "assign_fiber": Select(
                attrs={
                    "class": "form-control",

                }),
            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),

        }


class EditOhfAndUgfDetailsForm(forms.ModelForm):
    class Meta:
        model = OhfAndUgfDetails
        fields = ['link_name', 'link_point_a', 'link_point_a_lat', 'link_point_a_long',
                  'link_point_via', 'link_point_via_lat', 'link_point_via_long',
                  'link_point_b', 'link_point_b_lat', 'link_point_b_long', 'assign_fiber', 'sign_id', 'sign_time',
                  'assign_status']
        widgets = {

            "link_name": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_a": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_a_lat": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_a_long": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_via": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_via_lat": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_via_long": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_b": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_b_lat": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "link_point_b_long": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "assign_fiber": Select(
                attrs={
                    "class": "form-control",

                }),
            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template"
                }),

        }


class AddOandUFiberDetailsForm(forms.ModelForm):
    class Meta:
        model = OhfAndUgfFiberTeamDetails
        fields = ['link_code', 'core_details', 'core_color', 'distance', 'otdr', 'assign_date_time',
                  'fiber_receiver', 'sign_id', 'sign_time', 'assign_billing', 'assign_status']
        widgets = {
            "core_details": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "core_color": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "distance": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "otdr": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "fiber_receiver": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "assign_billing": Select(
                attrs={
                    "class": "form-control",

                }),
            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template",

                }),
            "assign_date_time": HiddenInput(),
            "link_code": HiddenInput(),

        }


class EditOandUFiberDetailsForm(forms.ModelForm):
    class Meta:
        model = OhfAndUgfFiberTeamDetails
        fields = ['core_details', 'core_color', 'distance', 'otdr', 'sign_id', 'sign_time', 'assign_billing',
                  'assign_status']
        widgets = {
            "core_details": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "core_color": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "distance": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "otdr": TextInput(
                attrs={
                    "class": "form-control",

                }),
            "assign_billing": Select(
                attrs={
                    "class": "form-control",

                }),
            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template",

                }),

        }



class AddOandUBillingDetailsForm(forms.ModelForm):

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
        model = OhfAndUgfBillingDetails
        fields = ['link_code', 'payment_status','amount','link_start_date','link_end_date','billing_img','link_validity', 'assign_date_time', 'sign_id', 'sign_time',
                  'billing_receiver','payment_method', 'netbanking_type', 'transaction_id', 'transaction_receipt','agreement_file']
        widgets = {
            "link_start_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "link_end_date": DateInput(
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
            "agreement_file": FileInput(
                attrs={
                    "class": "form-control-file",

                }),

            "link_code": HiddenInput(),
            "assign_date_time": HiddenInput(),
            "sign_id": HiddenInput(),
            "sign_time": HiddenInput(),

        }



class EditOandUBillingDetailsForm(forms.ModelForm):
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
        model = OhfAndUgfBillingDetails
        fields = ['billing_img','sign_id', 'sign_time',
                  'transaction_id','amount', 'transaction_receipt','agreement_file']
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


            "sign_id": HiddenInput(),
            "sign_time": HiddenInput(),

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

    def clean_agreement_file(self):
        agreement_file = self.cleaned_data['agreement_file']
        if agreement_file:
            return agreement_file
        else:
            agreement_file = 'emptyfile'
            return agreement_file



class RenewBillingDetailsForm(forms.ModelForm):
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
        model = OhfAndUgfBillingDetails
        fields = ['payment_status', 'link_start_date', 'link_end_date', 'billing_img', 'link_validity', 'sign_id', 'sign_time',
                  'amount','payment_method', 'netbanking_type', 'transaction_id', 'transaction_receipt',
                  'agreement_file']
        widgets = {
            "link_start_date": DateInput(
                attrs={
                    "class": "form-control",

                }),
            "link_end_date": DateInput(
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
                    'required': True,

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
            "agreement_file": FileInput(
                attrs={
                    "class": "form-control-file",

                }),

           "sign_id": HiddenInput(),
            "sign_time": HiddenInput(),

        }


