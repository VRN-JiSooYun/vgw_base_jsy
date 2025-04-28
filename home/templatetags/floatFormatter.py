from django import template

register = template.Library()

@register.filter(name="floatFormatter")
def floatFormatter(value, pos) :
    str = '{:.'+pos+'f}'
    if value != None and value != '' :
        formatStr = str.format(value)
    else :
        formatStr = ''
    return formatStr