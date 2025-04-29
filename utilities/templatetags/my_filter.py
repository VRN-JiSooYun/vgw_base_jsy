from django import template
import json
import datetime
import pytz
import numpy as np
import math

register = template.Library()

@register.filter
def json_loads(value):
    return json.loads(value).items()

@register.filter
def get_value(value, key):
    dictionary = json.loads(value)

    if key in dictionary:
        return dictionary[key]
    else:
        return ''

@register.simple_tag
def replace(value, target, to):
    if value == None:
        return ''
    return value.replace(target, to)

@register.simple_tag
def replaceNextline(value):
    if value == None:
        return ''
    return value.replace('\n', '<br>')

@register.filter()
def numberic(value):
    if value % 1 == 0:
        return int(value)
    return value

@register.filter
def divide(value, arg):
    try:
        return int(value) // int(arg)
    except:
        return 0

@register.filter(name='mod')
def mod(value, arg):
    try:
        return value % arg
    except:
        return 0

@register.filter
def from_total_seconds_to_hour_minute(total_seconds):
    if total_seconds == None:
        return '00:00'

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    return '{:02}:{:02}'.format(hours, minutes)

@register.filter
def to_hour_minute(value):
    if value == None:
        return '00:00'
    total_seconds = int(value.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{:02}:{:02}'.format(hours, minutes)

@register.filter
def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp / 1000)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts).strftime("%Y.%m.%d")

@register.filter
def get_item(dictionary, key):
    if not key in dictionary or dictionary[key] == None:
        return ''
    if dictionary[key] == True:
        return 1
    if dictionary[key] == False:
        return 0

    return dictionary.get(key)

@register.filter
def concat(value, arg):
    return str(value) + str(arg)

@register.simple_tag
def get_elem(dictionary, string1, string2):

    if string2 == 'today':
        today = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
        item = dictionary.get(string1 + '_' + today)
    else:
        item = dictionary.get(string1 + str(string2))

    if item == None or item == np.nan or (isinstance(item, (int, float, complex)) and not isinstance(item, bool) and math.isnan(item)):
        return ''
    
    if isinstance(item, float):
        if item.is_integer():
            return int(item)
        
    return item

@register.simple_tag
def get_elem_by_date(dataList, group_id, animal_seq, key, date):
    item = ''
    for elem in dataList:
        if elem['group'] == group_id and elem['animal'] == animal_seq and key + '_' + str(date) in elem:
            item = elem[key + '_' + str(date)]
            break

    if item == None or item == np.nan or (isinstance(item, (int, float, complex)) and not isinstance(item, bool) and math.isnan(item)):
        return ''
    
    if isinstance(item, float):
        if item.is_integer():
            return int(item)
        
    return item


@register.simple_tag
def get_elem_from_list(dictList, idx, key):
    # print(dictList, idx, key)
    item = dictList[idx - 1][key]
    
    return item

@register.simple_tag
def calculate_dat(date1, date2):
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    if date2 == "today":
        today = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
        date2 = datetime.datetime.strptime(today, '%Y-%m-%d').date()
    # else:
    #     date2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()

    dat = (date2 - date1).days
    
    return dat

@register.simple_tag
def calculate_day(date1, date2):
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    if date2 == "today":
        today = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
        date2 = datetime.datetime.strptime(today, '%Y-%m-%d').date()
    # else:
    #     date2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()

    dat = (date2 - date1).days + 1
    
    return dat

@register.filter
def check_if_mobile(request):
    if 'Android' in request.META['HTTP_USER_AGENT']:
        return True
    
    return False

@register.simple_tag
def get_color_from_list_by_elem(dataList, group_id, animal_seq, key, date):
    # print("dataList:", dataList)
    # print("get_color_from_list_by_elem::dataList:", dataList)
    if date == "today":
        today = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
        date = datetime.datetime.strptime(today, '%Y-%m-%d').date()

    item = ''
    for elem in dataList:
        # print(key + '_' + str(date), ' : ', elem)
        if elem['group'] == group_id and elem['animal'] == animal_seq and key + '_' + str(date) in elem:
            item = elem[key + '_' + str(date)]
            break
    # print(item)
    if item =='' or item == None or item == np.nan or (isinstance(item, (int, float, complex)) and not isinstance(item, bool) and math.isnan(item)):
        return 'black'
    
    if key == 'bw_change_rate' and float(item) <= -20:
        return 'red'
    elif key == 'tumor_volume' and float(item) >= 2000:
        return 'red'
    return 'black'


@register.simple_tag
def get_color_from_dict_by_elem(dictionary, string1, date):

    if date == 'today':
        date = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
        item = dictionary.get(string1 + '_' + date)
    else:
        item = dictionary.get(string1 + '_' + str(date))

    if item == None or item == np.nan or (isinstance(item, (int, float, complex)) and not isinstance(item, bool) and math.isnan(item)):
        return 'black'
    
    if string1 == 'body_weight':
        # print(dictionary)
        item = dictionary.get('bw_change_rate_' + str(date))

        if item == None or item == np.nan or (isinstance(item, (int, float, complex)) and not isinstance(item, bool) and math.isnan(item)):
            return 'black'

        if float(item) <= -20:
            return 'red'
        else:
            return 'black'

    elif string1 == 'tumor_volume' and float(item) >= 2000:
        return 'red'
    elif string1 == 'bw_change_rate' and float(item) <= -20:
        return 'red'
    return 'black'