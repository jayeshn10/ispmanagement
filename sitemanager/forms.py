from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.forms import TextInput, EmailInput, FileInput, PasswordInput, CharField, Textarea, Select, CheckboxInput, \
    HiddenInput

from ohfandugfmanager.models import OhfAndUgfVendors
from sitemanager.models import User, IllVendors, ThreesaIllConnectionsDetails


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    user_image = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'form-control-file'}))

    def clean_username(self):
        vusername = self.cleaned_data['username']
        if ' ' in vusername:
            raise forms.ValidationError('Username should not contain any space')
        return vusername

    class Meta:
        model = User
        fields = ['username', 'user_full_name', 'email', 'user_mobile', 'user_image', 'password1',
                  'password2', 'groups']
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control"
                }),

            "user_full_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email"
                }),
            "user_mobile": TextInput(
                attrs={
                    "class": "form-control"
                }),

        }

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'profileimages/user.png'
            return user_image


class EditUserDetailsForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['user_full_name', 'email', 'user_mobile', 'user_image'
                  ]

        widgets = {

            "user_full_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email"
                }),
            "user_mobile": TextInput(
                attrs={
                    "class": "form-control"
                }),

        }

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = ''
            return user_image


class UserChangePasswordCustom(SetPasswordForm):
    new_password1 = CharField(required=True, label='newpassword',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'The password can not be empty'})
    new_password2 = CharField(required=True, label='confirmpassword',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'The password can not be empty'})


class EditUserGroupForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['groups', ]


class EditIllConForm(forms.ModelForm):
    FBOOL_CHOICES = ((True, 'Possible'), (False, 'Not Possible'))
    assign_status = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            "class": "checkbox-template",
        }), )
    ill_feasibility = forms.ChoiceField(choices=FBOOL_CHOICES, widget=forms.Select(
        attrs={
            "class": "form-control"
        }), required=False)

    class Meta:
        model = ThreesaIllConnectionsDetails
        fields = ['ill_cust_address', 'ill_cust_address_lat', 'ill_cust_address_long', 'ill_feasibility', 'ill_sign_id',
                  'ill_sign_time',
                  'assign_status']
        widgets = {

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
            "ill_sales_person": Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "ill_feasibility": Select(
                attrs={
                    "class": "form-control"
                }),

            "assign_status": CheckboxInput(
                attrs={
                    "class": "checkbox-template",
                }),

            "ill_sign_time": HiddenInput(),
        }


class AddIllVendorForm(forms.ModelForm):
    def clean_v_code(self):
        vv_code = self.cleaned_data['v_code']
        if ' ' in vv_code:
            raise forms.ValidationError('Vendor Code should not contain any space')
        return vv_code

    class Meta:
        model = IllVendors
        fields = '__all__'
        widgets = {

            "v_code": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_contactno": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_address": Textarea(
                attrs={
                    "class": "form-control"
                }),
            "v_kyc": FileInput(
                attrs={
                    "class": "form-control-file"
                }),
            "v_gstno": TextInput(
                attrs={
                    "class": "form-control"
                }),
        }


class EditIllVendorForm(forms.ModelForm):
    class Meta:
        model = IllVendors
        fields = ['v_name', 'v_contactno', 'v_address', 'v_kyc', 'v_gstno']
        widgets = {

            "v_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_contactno": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_address": Textarea(
                attrs={
                    "class": "form-control"
                }),

            "v_gstno": TextInput(
                attrs={
                    "class": "form-control"
                }),
        }

    def clean_v_kyc(self):
        v_kyc = self.cleaned_data['v_kyc']
        if v_kyc:
            return v_kyc
        else:
            v_kyc = 'emptyfile'
            return v_kyc


class AddOhfAndUgfVendorForm(forms.ModelForm):
    def clean_v_code(self):
        vv_code = self.cleaned_data['v_code']
        if ' ' in vv_code:
            raise forms.ValidationError('Vendor Code should not contain any space')
        return vv_code

    class Meta:
        model = OhfAndUgfVendors
        fields = '__all__'
        widgets = {

            "v_code": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_address": Textarea(
                attrs={
                    "class": "form-control"
                }),
            "v_contact_person_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_contact_person_no": TextInput(
                attrs={
                    "class": "form-control"
                }),
        }


class EditOhfAndUgfVendorForm(forms.ModelForm):
    class Meta:
        model = OhfAndUgfVendors
        fields = ['v_name', 'v_address', 'v_contact_person_name', 'v_contact_person_no']
        widgets = {
            "v_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_address": Textarea(
                attrs={
                    "class": "form-control"
                }),
            "v_contact_person_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "v_contact_person_no": TextInput(
                attrs={
                    "class": "form-control"
                }),
        }


class Num_Item_Per_Page(forms.Form):
    item_ch = (('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('50', '50'),
               ('100', '100'), ('500', '500'))
    num_page = forms.ChoiceField(required=False, widget=forms.Select(attrs={'name': 'num_page', 'id': 'num_page'}),
                                 choices=item_ch, )


class UserAdminAddForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    user_image = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ['username', 'user_full_name', 'email', 'user_mobile', 'user_image', 'password1',
                  'password2', 'groups', 'is_superuser', 'is_staff', 'is_active', 'user_permissions', 'last_login',
                  'date_joined']

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'profileimages/user.png'
            return user_image


class UserAdminChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = '__all__'

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'profileimages/user.png'
            return user_image
