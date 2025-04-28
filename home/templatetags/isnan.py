from django import template
# import numpy as np
import math

register = template.Library()

@register.filter(name='isnan')
def isnan(value) :
    if value == None :
        return False
    else :
        nn = float(value)
        return math.isnan(nn)