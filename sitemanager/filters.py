import django_filters
from django import forms
from django.contrib.auth.models import Group

from sitemanager.models import User, ThreesaIllConnectionsDetails, IllVendors


class UserFilter(django_filters.FilterSet):
    groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple(
                                                          attrs={'class': 'checkbox-template'}))

    class Meta:
        model = User
        fields = ['groups', ]


class IllConnDetailsFilter(django_filters.FilterSet):
    ASTATUS_CHOICES = (
        (0, 'NotAssigned'),
        (1, 'Assigned'),
    )

    FSTATUS_CHOICES = (
        (0, 'NotPossible'),
        (1, 'Possible'),
    )

    CONNTYPE_CHOICES = (('1', 'Threesa'), ('2', 'Threesa Through Vendor'), ('3', 'Vendor Through Threesa'))

    ill_custid = django_filters.CharFilter(field_name='ill_custid', lookup_expr='icontains',
                                           widget=forms.TextInput(
                                               attrs={'class': 'mr-2 form-control', 'placeholder': 'Connection ID'}))

    lgstrd = django_filters.DateFilter(field_name='ill_gendate',
                                       lookup_expr='date__gte', widget=forms.HiddenInput(
            attrs={'id': 'lgstrd', }))

    lgendd = django_filters.DateFilter(field_name='ill_gendate', lookup_expr='date__lte', widget=forms.HiddenInput(
        attrs={'id': 'lgendd', }))

    ill_sales_person = django_filters.ModelChoiceFilter(field_name='ill_sales_person',
                                                        queryset=User.objects.filter(
                                                            groups__name='salesperson'),
                                                        widget=forms.Select(
                                                            attrs={'class': 'form-control'})
                                                        , empty_label='Sales Person'
                                                        )
    assign_status = django_filters.ChoiceFilter(field_name='assign_status', choices=ASTATUS_CHOICES,
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control'}), empty_label='Assign Status')

    ill_feasibility = django_filters.ChoiceFilter(field_name='ill_feasibility', choices=FSTATUS_CHOICES,
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control'}),
                                                  empty_label='Feasibility Status')

    ill_conn_type = django_filters.ChoiceFilter(field_name='ill_conn_type',
                                                choices=CONNTYPE_CHOICES,
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control'})
                                                , empty_label='Connection Type')

    class Meta:
        model = ThreesaIllConnectionsDetails
        fields = ['ill_custid', ]




class IllVendorFilter(django_filters.FilterSet):
    v_code = django_filters.CharFilter(field_name='v_code', lookup_expr='icontains',
                                         widget=forms.TextInput(
                                             attrs={'class': 'mr-2 form-control', 'placeholder': 'Vendor Code'}))
    v_name = django_filters.CharFilter(field_name='v_name', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'Customer Name'}))
    v_contactno = django_filters.CharFilter(field_name='v_contactno', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'Contact No.'}))
    v_address = django_filters.CharFilter(field_name='v_address', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'Address'}))
    v_gstno = django_filters.CharFilter(field_name='v_gstno', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'Gst No.'}))

    class Meta:
        model = IllVendors
        fields = ['v_code', ]


class OhfAndUgfVendorFilter(django_filters.FilterSet):
    v_code = django_filters.CharFilter(field_name='v_code', lookup_expr='icontains',
                                         widget=forms.TextInput(
                                             attrs={'class': 'mr-2 form-control', 'placeholder': 'Vendor Code'}))
    v_name = django_filters.CharFilter(field_name='v_name', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'Customer Name'}))
    v_address = django_filters.CharFilter(field_name='v_address', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'Address'}))
    v_contact_person_name = django_filters.CharFilter(field_name='v_contact_person_name', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'contact person name'}))

    v_contact_person_no = django_filters.CharFilter(field_name='v_contact_person_no', lookup_expr='icontains',
                                                      widget=forms.TextInput(
                                                          attrs={'class': 'mr-2 form-control',
                                                                 'placeholder': 'contact person No'}))

    class Meta:
        model = IllVendors
        fields = ['v_code', ]