from django import template

register = template.Library()

@register.filter
def divide(num, val):
    return round(num / val, 2)