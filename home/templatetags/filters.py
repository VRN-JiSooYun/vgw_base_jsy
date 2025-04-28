from django import template
from urllib import parse
import datetime
# from project.common import *

register = template.Library()

@register.filter()
def ranges(count) :
    cnt = count if count is not None else 0
    return range(1, cnt+1)

@register.filter()
def addStr(arg, value) :
    return str(arg) + str(value)

@register.filter()
def get_value(arg, key) :
    return getattr(arg, key)

@register.filter()
def decodeurl(arg, val) :
    if arg is None :
        return ""
    else :
        return parse.unquote(arg)

@register.filter()
def abss(arg) :
    return abs(float(arg))

@register.filter()
def subtractify(a1, a2):
    newval = a1 - a2
    return newval

@register.filter()
def getRequestStatus(cd) :
    # {% if data.status == 'request' %}의뢰중{% elif data.status == 'analysis' %}분석중{% elif data.status == 'review' %}분석검토{% elif data.status == 'deny' %}<span class='font-red'>반려</span>{% elif data.status == 'hold' %}<span class='font-green'>보류</span>{% elif data.status == 'assay' %}<span class='font-green'>실험중</span>{% else %}분석 완료{% endif %}
    rtn = ''
    if cd == 'request' :
        rtn = '의뢰중'
    elif cd == 'assay' :
        rtn = '실험중'
    elif cd == 'analysis' :
        rtn = '분석중'
    elif cd == 'deny' :
        rtn = '반려'
    elif cd == 'hold' :
        rtn = '보류'
    elif cd == 'review' :
        rtn = '분석검토'
    elif cd == 'complete' :
        rtn = '분석완료'

    return rtn


@register.filter()
def getRequestStatusColor(cd) :
    # {% if data.status == 'request' %}의뢰중{% elif data.status == 'analysis' %}분석중{% elif data.status == 'review' %}분석검토{% elif data.status == 'deny' %}<span class='font-red'>반려</span>{% elif data.status == 'hold' %}<span class='font-green'>보류</span>{% elif data.status == 'assay' %}<span class='font-green'>실험중</span>{% else %}분석 완료{% endif %}
    rtn = ''
    if cd == 'request' :
        rtn = ''
    elif cd == 'assay' :
        rtn = 'background-color: rgb(168, 233, 151); position: sticky;'
    elif cd == 'analysis' :
        rtn = 'background-color: rgb(255, 224, 196);'
    elif cd == 'deny' :
        rtn = ''
    elif cd == 'hold' :
        rtn = ''
    elif cd == 'review' :
        rtn = 'background-color: rgb(193, 195, 248);'
    elif cd == 'complete' :
        rtn = 'background-color: rgb(184, 233, 255);'

    return rtn

@register.filter()
def getStudyStatus(cd) :
    # 종료 : 5-END
    # 강제종료 : 6-STOP
    # 진행 : 3-PROGRESS
    # 신청검토요청 : 1-REG-REQ
    # 종료검토요청 : 2-END-REQ
    rtn = ''
    if cd == '1-REG-REQ' :
        rtn = '신청검토요청'
    elif cd == '2-END-REQ' :
        rtn = '종료검토요청'
    elif cd == '3-PROGRESS' :
        rtn = '진행'
    elif cd == '6-STOP' :
        rtn = '강제종료'
    elif cd == '5-END' :
        rtn = '종료'

    return rtn

@register.filter()
def fillStudyNo(cd) :
    rtn = str(cd).zfill(4)
    return rtn

@register.filter()
def getIdx(arr, idx) :
    return arr[idx]

@register.filter()
def multiplex(a, b) :
    return a*b

@register.filter()
def getNow(a) :
    return datetime.datetime.now()

@register.filter()
def getPosArray(a, b) :
    rtn = -1
    i = 0
    for f in a :
        if f == b :
            rtn = i
        i+=1
    return rtn

@register.filter()
def checkValidUrl(path) :
    # True면 content보임
    rtn = True
    if 'my.voronoi.app' in path : 
        if '/re-working/' not in path and '/my/' not in path and 'member/login' not in path \
            and 'member/logout' not in path and 're-todo/' not in path and 're-member/' not in path \
            and '/re-working-admin/' not in path and '/re-group/' not in path and '/re-auth/' not in path \
            and '/security/login' not in path and '/conference/' not in path and '/ips/' not in path:
            rtn = False
        else :
            rtn = True
    else :
        rtn = True

    return rtn

@register.filter()
def lengthFind(arr, str) :
    # array에서 문자열이 포함된 갯수 리턴
    rtn = 0
    for a in arr :
        if a.find(str) >= 0 :
            rtn += 1
    return rtn

@register.filter()
def lengthFindEqual(arr, str) :
    # array에서 문자열이 포함된 갯수 리턴
    rtn = 0
    for a in arr :
        if a == str :
            rtn += 1
    return rtn

@register.filter()
def getValueForStringArray(str, idx):
    arr = str.split("#_#")
    if len(arr) > int(idx) :
        rtn = arr[int(idx)]
    else :
        rtn = ""
    return rtn

@register.filter()
def find(a, b) :
    return a.find(b)

@register.filter()
def getColumnName(a) :
    return dashboardColumns.get(a)

@register.filter()
def strTodict(a) :
    rtn = eval(a)
    return rtn

@register.filter()
def strAdd(a, b) :
    rtn = str(a) + str(b)
    return rtn

@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, '')

@register.filter
def devide(a, b):
    return int(a/b)

@register.filter
def indexK(a, b) :
    r = -1
    try :
        r = a.index(b)
    except Exception as e :
        pass
    return r

@register.filter
def getArrayValue(a, b) :
    return a[b]

@register.filter
def minus(a, b) :
    return int(a)-int(b)