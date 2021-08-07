import django_filters
from django import forms

from sitemanager.models import User
from threesaoperators.models import NetOperatorsDetails


class NetOperatorsDetailsFilter(django_filters.FilterSet):
    LSTATUS_CHOICES = (
        (1, 'active'),
        (0, 'deactive'),
    )
    operator_id = django_filters.CharFilter(field_name='operator_id', lookup_expr='icontains',
                                            widget=forms.TextInput(
                                                attrs={'class': 'mr-2 form-control', 'placeholder': 'Operator Id'}))

    orstrd = django_filters.DateFilter(field_name='Operator_register',
                                       lookup_expr='date__gte', widget=forms.TextInput(
            attrs={'id': 'orstrd', 'type': 'hidden'}))

    orendd = django_filters.DateFilter(field_name='Operator_register', lookup_expr='date__lte',
                                       widget=forms.TextInput(
                                           attrs={'id': 'orendd', 'type': 'hidden'}))

    """psstrd = django_filters.DateFilter(field_name='op_billing_code__payment_start_date', lookup_expr='gte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'psstrd', }))

    psendd = django_filters.DateFilter(field_name='op_billing_code__payment_start_date', lookup_expr='lte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'psendd', }))

    pestrd = django_filters.DateFilter(field_name='op_billing_code__payment_end_date', lookup_expr='gte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'pestrd', }))

    peendd = django_filters.DateFilter(field_name='op_billing_code__payment_end_date', lookup_expr='lte',
                                       widget=forms.HiddenInput(
                                           attrs={'id': 'peendd', }))"""
    zones = django_filters.CharFilter(field_name='zones__zone_name', lookup_expr='icontains',
                                            widget=forms.TextInput(
                                                attrs={'class': 'mr-2 form-control', 'placeholder': 'Zone'}))
    operator_dealer = django_filters.ModelChoiceFilter(field_name='operator_dealer',
                                                       queryset=User.objects.filter(groups__name='operatormanager'),
                                                       widget=forms.Select(
                                                           attrs={'class': 'form-control'})
                                                       , empty_label='Operator Dealer'
                                                       )
    active_status = django_filters.ChoiceFilter(field_name='active_status', choices=LSTATUS_CHOICES,
                                                widget=forms.Select(
                                                    attrs={'class': 'mr-2 form-control'}), empty_label='Active Status')

    class Meta:
        model = NetOperatorsDetails
        fields = ['operator_id', ]
