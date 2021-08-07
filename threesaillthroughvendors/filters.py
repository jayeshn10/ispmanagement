import django_filters
from django import forms

from sitemanager.models import IllVendors
from threesaillthroughvendors.models import TTVIllDoneConnectionsDetails


class TTVIllFeasibleConnDetailsFilter(django_filters.FilterSet):
    LSTATUS_CHOICES = (
        (1, 'active'),
        (0, 'deactive'),
    )
    conn_code = django_filters.CharFilter(field_name='conn_code__ill_custid', lookup_expr='icontains',
                                          widget=forms.TextInput(
                                              attrs={'class': 'mr-2 form-control', 'placeholder': 'Connection ID'}))

    lgstrd = django_filters.DateFilter(field_name='conn_code__ill_gendate',
                                       lookup_expr='date__gte', widget=forms.TextInput(
            attrs={'id': 'lgstrd', 'type': 'hidden'}))

    lgendd = django_filters.DateFilter(field_name='conn_code__ill_gendate', lookup_expr='date__lte',
                                       widget=forms.TextInput(
                                           attrs={'id': 'lgendd', 'type': 'hidden'}))

    castrd = django_filters.DateFilter(field_name='billing_code__conn_start_date', lookup_expr='gte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'castrd', }))

    caendd = django_filters.DateFilter(field_name='billing_code__conn_start_date', lookup_expr='lte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'caendd', }))

    cestrd = django_filters.DateFilter(field_name='billing_code__conn_end_date', lookup_expr='gte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'cestrd', }))

    ceendd = django_filters.DateFilter(field_name='billing_code__conn_end_date', lookup_expr='lte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'ceendd', }))

    link_status = django_filters.ChoiceFilter(field_name='active_status', choices=LSTATUS_CHOICES, widget=forms.Select(
        attrs={'class': 'mr-2 form-control'}), empty_label='Link Status')

    conn_code__ill_vendor_code = django_filters.ModelChoiceFilter(queryset=IllVendors.objects.all(),
                                                                  widget=forms.Select(
                                                                      attrs={'class': 'mr-2 form-control'}),
                                                                  empty_label='Select Vendor')

    class Meta:
        model = TTVIllDoneConnectionsDetails
        fields = ['conn_code', ]
