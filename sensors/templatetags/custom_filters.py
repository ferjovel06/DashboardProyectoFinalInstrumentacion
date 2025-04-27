from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return value * int(arg)
    except (ValueError, TypeError):
        return value
