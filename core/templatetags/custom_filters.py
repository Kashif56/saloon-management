from django import template

register = template.Library()

@register.filter
def intdiv(value, arg):
    """Integer division filter"""
    try:
        return int(float(value)) // int(arg)
    except (ValueError, ZeroDivisionError):
        return 0
