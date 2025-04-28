from django import template

register = template.Library()

@register.filter(name="getCodeDtl")
def getCodeDtl(dictionary, cd_dtl_no) :
    if cd_dtl_no == None :
        return ''
    for data in dictionary :
        if data["cd_dtl_no"] == cd_dtl_no :
            return data