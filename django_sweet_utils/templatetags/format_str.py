from django import template

register = template.Library()


@register.filter(name='format_string')
def format_string(string, new):
    return string.replace('%s', new)
