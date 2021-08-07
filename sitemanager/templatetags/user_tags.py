import datetime
from datetime import date

from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False


@register.simple_tag
def relative_url(value, field_name, value2, field_name2, urlencode=None):
    url = '{}={}&{}={}'.format(field_name, value, field_name2, value2)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name and p.split('=')[0] != field_name2, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '?{}&{}'.format(encoded_querystring, url)
    else:
        url = '?{}'.format(url)
    return url


@register.simple_tag
def connectionpurplemaker(exdate):
    x = exdate - date.today()
    print(x.days)
    if x.days <= 6:
        return True
    else:
        return False
