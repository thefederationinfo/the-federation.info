from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def with_sign(value):
    number_value = float(value)
    if number_value > 0:
        return f"+{value}"
    return value
