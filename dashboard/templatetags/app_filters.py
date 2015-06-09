from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    return value.replace(arg, '_')