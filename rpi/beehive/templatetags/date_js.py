from django import template


register = template.Library()


@register.filter('date_js')
def date_js(date):
    return 'Date.UTC({}, {}, {}, {}, {}, {})'.format(
        date.year, date.month - 1, date.day,
        date.hour + 1, date.minute, date.second
    )
