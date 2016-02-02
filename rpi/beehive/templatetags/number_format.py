from django import template
from django.template.defaultfilters import floatformat, safe


register = template.Library()


@register.filter('numberformat')
def number_format(number):
    """Prints float with 2 decimals and changes minus sign."""

    return safe(floatformat(number).replace('-', '&minus;'))
