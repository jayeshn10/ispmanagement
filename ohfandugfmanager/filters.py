import django_filters
from django import forms

from ohfandugfmanager.models import OhfAndUgfDetails, OhfAndUgfVendors
from sitemanager.models import User


class OhfAndUgfFilter(django_filters.FilterSet):
    link_type_g_t_choice = (
        ('1', 'Taken From Vendor'),
        ('2', 'Given By Threesa'),
    )

    link_type_choice = (
        ('1', 'OHF'),
        ('2', 'UGF'),
    )
    link_code = django_filters.CharFilter(field_name='link_code', lookup_expr='icontains',
                                         widget=forms.TextInput(
                                             attrs={'class': 'mr-2 form-control', 'placeholder': 'Link Code'}))
    link_name = django_filters.CharFilter(field_name='link_name', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control', 'placeholder': 'Link Name'}))
    link_dealer = django_filters.ModelChoiceFilter(field_name='link_dealer',
                                                        queryset=User.objects.filter(
                                                            groups__name='OhfAndUgfManager'),
                                                        widget=forms.Select(
                                                            attrs={'class': 'form-control'})
                                                        , empty_label='Link Dealer'
                                                        )
    link_vendor = django_filters.ModelChoiceFilter(queryset=OhfAndUgfVendors.objects.all(),
                                                                  widget=forms.Select(
                                                                      attrs={'class': 'mr-2 form-control'}),
                                                                  empty_label='Select Vendor')
    link_type_g_t = django_filters.ChoiceFilter(field_name='link_type_g_t', choices=link_type_g_t_choice, widget=forms.Select(
        attrs={'class': 'mr-2 form-control'}), empty_label='Given or Taken')

    link_type = django_filters.ChoiceFilter(field_name='link_type', choices=link_type_choice, widget=forms.Select(
        attrs={'class': 'mr-2 form-control'}), empty_label='Link Type')

    link_point_a = django_filters.CharFilter(field_name='link_point_a', lookup_expr='icontains',
                                             widget=forms.TextInput(
                                                 attrs={'class': 'mr-2 form-control',
                                                        'placeholder': 'Link Point A'}))
    link_point_via = django_filters.CharFilter(field_name='link_point_via', lookup_expr='icontains',
                                                      widget=forms.TextInput(
                                                          attrs={'class': 'mr-2 form-control',
                                                                 'placeholder': 'Link Point Via'}))
    link_point_b = django_filters.CharFilter(field_name='link_point_b', lookup_expr='icontains',
                                                      widget=forms.TextInput(
                                                          attrs={'class': 'mr-2 form-control',
                                                                 'placeholder': 'Link Point B'}))

    class Meta:
        model = OhfAndUgfDetails
        fields = ['link_code', ]