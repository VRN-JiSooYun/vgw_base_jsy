from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    if value == None or arg == None :
        return ""
    return value - arg