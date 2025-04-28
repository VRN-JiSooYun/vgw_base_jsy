from django import template

register = template.Library()

@register.filter(name="getCodeDtls")
def getCodeDtls(dictionary, cd_no) :
    codeDtls = []
    for data in dictionary :
        if data["cd_no"] == cd_no:
            codeDtls.append(data)

    return codeDtls