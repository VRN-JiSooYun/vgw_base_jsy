from django import template

register = template.Library()

@register.filter(name="getItem")
def getItem(dictionary, key) :
    # print("dictionary::",dictionary)
    # print("key::", key)
    return dictionary.get(key)
