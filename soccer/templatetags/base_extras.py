from django import template

register = template.Library()

@register.filter
def dash_if_none(value):
    """
    Returns a dash ('-') if the value is None or an empty string,
    otherwise returns the value itself.
    """
    return '-' if value is None or value == '' else value