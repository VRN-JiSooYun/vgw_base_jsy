from django import template

register = template.Library()

@register.filter(name="getCdNo")
def getCdNo(dictionary, cd_alias) :
    for data in dictionary :
        if data["cd_alias"] == cd_alias:
            return data["cd_no"]