from django.db import connection
from re_working.models import *
from re_working_admin.models import *
from re_member.models import *
from re_group.models import *
# from project.models import *
from re_group.functions import *
from re_member.functions import *
# from dashboard.sendMailByGoogle import *
from django.forms.models import model_to_dict
from django.conf import settings
from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.parser import parse
from home.code_singleton import Code
import json
import requests
from django.http import HttpResponse
import xlwt
import xmltodict # pip install xmltodict
from zipfile import ZipFile
from django.core.files.base import ContentFile

# pdf
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import HRFlowable

def createHoliday(request) :
    data = json.loads(request.body)["data"]
    try :
        holidayStartDatetime = data["holiday_start_datetime"]
        if  holidayStartDatetime == "" :
            holidayStartDatetime = None

        holidayEndDatetime = data["holiday_end_datetime"]
        if  holidayEndDatetime == "" :
            holidayEndDatetime = None

        reHoliday = ReHoliday(
            holiday_name = data["holiday_name"],
            holiday_date = data["holiday_date"],
            holiday_start_datetime = holidayStartDatetime,
            holiday_end_datetime = holidayEndDatetime,
            holiday_create_type = Code().getCodeDtlNoByAlias("HOLIDAY_CREATE_TYPE_MANUAL"),
        )
        reHoliday.save()
        print("success create holiday")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def createWorkingTime(request) :
    data = json.loads(request.body)["data"]
    try :
        memberIds = data["member_ids"]
        workingTimeStartTime1 = data["working_time_start_time_1"]
        workingTimeEndTime1 = data["working_time_end_time_1"]
        workingTimeStartTime2 = data["working_time_start_time_2"]
        workingTimeEndTime2 = data["working_time_end_time_2"]
        workingTimeStartTime3 = data["working_time_start_time_3"]
        workingTimeEndTime3 = data["working_time_end_time_3"]
        workingTimeStartTime4 = data["working_time_start_time_4"]
        workingTimeEndTime4 = data["working_time_end_time_4"]
        workingTimeStartTime5 = data["working_time_start_time_5"]
        workingTimeEndTime5 = data["working_time_end_time_5"]

        for memberId in memberIds :
            reWorkingTime = ReWorkingTime(
                member_id = memberId,
                working_time_start_time_1 = workingTimeStartTime1,
                working_time_end_time_1 = workingTimeEndTime1,
                working_time_start_time_2 = workingTimeStartTime2,
                working_time_end_time_2 = workingTimeEndTime2,
                working_time_start_time_3 = workingTimeStartTime3,
                working_time_end_time_3 = workingTimeEndTime3,
                working_time_start_time_4 = workingTimeStartTime4,
                working_time_end_time_4 = workingTimeEndTime4,
                working_time_start_time_5 = workingTimeStartTime5,
                working_time_end_time_5 = workingTimeEndTime5,
            )
            reWorkingTime.save()
        print("success create working time")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def getWorkingMonthData(request) :
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_month_working)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    query = query.replace('__WORKING_OFF_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))

    print(query)
    cur.execute(query)

    workings = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workings

def getWeekWorkingOffs(request) :
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_week_working_offs)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    query = query.replace('__WORKING_OFF_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))

    cur.execute(query)
    workingOffs = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingOffs

def getWeekWorkingOuts(request) :
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_week_working_outs)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)

    cur.execute(query)
    workingOuts = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingOuts

def getWorkings(request) :
    workingDate = request.GET.get('working_date')
    orderCol = request.GET.get('orderCol')
    orderType = request.GET.get('orderType')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_workings)
    query = query.replace('__WORKING_OFF_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))
    query = query.replace('__WORKING_DATE__', workingDate)
    query = query.replace('__ORDER_BY__', orderCol + " " + orderType)

    print(query)
    cur.execute(query)

    workings = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workings

def getWorkingHistorys(request) :
    memberId = request.GET.get('memberId')
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_historys)
    query = query.replace('__WORKING_OFF_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))
    query = query.replace('__MEMBER_ID__', memberId)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)

    print(query)
    cur.execute(query)

    workingHistorys = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingHistorys

def getChangeWorkingTimes(request) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_change_working_times)

    print(query)
    cur.execute(query)

    workings = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workings

def getHolidays(request) :
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")

    return ReHoliday.objects.filter(Q(holiday_date__range=(startDate, endDate)))

def getMonthHolidays(request) :
    date = request.GET.get('date')
    return ReHoliday.objects.filter(Q(holiday_date__startswith=date[:7]))

def getYearHolidays(request) :
    year = request.GET.get('year')
    return ReHoliday.objects.filter(Q(holiday_date__startswith=year)).order_by('holiday_date')

def getHoliday(request) :
    holidayId = request.GET.get('holiday_id')
    return ReHoliday.objects.get(holiday_id=holidayId)

def getWorkingOffHistorys(request) :
    memberId = request.GET.get('member_id')
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_off_historys)
    query = query.replace('__MEMBER_ID__', memberId)
    query = query.replace('__APPROVAL_DONE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE")).replace("__APPROVAL_CANCEL_ADMIN__", Code().getCodeDtlNoByAlias("APPROVAL_CANCEL_ADMIN"))
    query = query.replace('__START_DATE__', "AND a.working_off_form_start_date >= '" + startDate + "'")
    if endDate != '' :
        query = query.replace('__END_DATE__', "AND a.working_off_form_end_date <= '" + endDate + "'")
    else :
        query = query.replace('__END_DATE__', "")

    print(query)
    cur.execute(query)

    workingOffHistorys = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingOffHistorys

def getWorkingTimes() :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_times)

    print(query)
    cur.execute(query)

    workingTimes = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingTimes

def getWorkingStats(request) :
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    groupKey = request.GET.get('groupKey')
    groupFilter = ""
    if (int(groupKey) > 0) :
        groupFilter = "WHERE parent_group_key = '" + groupKey + "'"

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_stats)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    query = query.replace('__GROUP_FILTER__', groupFilter)

    print(query)
    cur.execute(query)

    workingStats = dictfetchall(cur)
    if cur != None :
        cur.close()


    return workingStats

def getWorkingParts(request) :
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_parts)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)

    print(query)
    cur.execute(query)

    workingParts = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingParts

def getProjects() :
    return Project_Project.objects.filter(Q(check_discard = False))

def getWorkingTimeGroupTree() :
    groups = getGroups()
    groupMembers = getGroupMembers()
    workingTimes = ReWorkingTime.objects.all()

    memberIds = []
    for workingTime in workingTimes :
        memberIds.append(workingTime.member_id)


    groupMembersDic = {}
    for groupMember in groupMembers :
        groupKey = groupMember["group_key"]
        for inx in range(len(groupMember["member_id"])) :

            if groupKey in groupMembersDic :
                groupMembersDic[groupKey].append({
                    "member_id": groupMember["member_id"][inx],
                    "member_name": groupMember["member_name"][inx]
                })
            else :
                groupMembersDic[groupKey] = [{
                    "member_id": groupMember["member_id"][inx],
                    "member_name": groupMember["member_name"][inx]
                }]

    node_map = {}
    for group in groups :
        node_map[group.group_key] = TreeNode(group.group_key, group.group_name)

    for group in groups :
        if group.parent_group_key != 0 :
            node = node_map.get(group.group_key)
            parent_node = node_map.get(group.parent_group_key)

            if parent_node is None : continue

            parent_node.addChildren(node)

            if group.group_key in groupMembersDic :
                childrens = groupMembersDic[group.group_key]
                for children in childrens :
                    if children["member_id"] in memberIds :
                        continue

                    node.addChildren(TreeNode(str(group.group_key) + "_" + str(children["member_id"]), children["member_name"]))

    return node_map.get(1)

def getWorkingApprovals(request, limit, offset) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_approvals)
    query = query.replace('__APPROVAL_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))
    query = query.replace('__LIMIT__', "LIMIT " + str(limit)).replace('__OFFSET__', "OFFSET " + str(offset))

    # search
    searchType = request.GET.get('searchType')
    searchStr = request.GET.get('searchStr')
    if searchStr != "" :
        query = query.replace('__WHERE__', "WHERE " + searchType + " LIKE '%" + searchStr + "%'")
    else :
        query = query.replace('__WHERE__', "")

    cur.execute(query)
    workingApprovals = dictfetchall(cur)

    if cur != None :
        cur.close()

    return workingApprovals

def getWorkingApprovalsCount(request) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_approvals)
    query = query.replace('__APPROVAL_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))
    query = query.replace('__LIMIT__', "").replace('__OFFSET__', "")

    # search
    searchType = request.GET.get('searchType')
    searchStr = request.GET.get('searchStr')
    if searchStr != "" :
        query = query.replace('__WHERE__', "WHERE " + searchType + " LIKE '%" + searchStr + "%'")
    else :
        query = query.replace('__WHERE__', "")

    cur.execute(query)
    workingApprovals = dictfetchall(cur)

    if cur != None :
        cur.close()

    return len(workingApprovals)

def getWorkingWeekendStats(request) :
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_weekend_stats)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    query = query.replace('__WORKING_WEEKEND_NOTE_FORM_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))

    print(query)
    cur.execute(query)
    workingWeekendStats = dictfetchall(cur)

    if cur != None :
        cur.close()

    return workingWeekendStats

def getWorkingWeekendStatsDaily(request, memberId) :
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_weekend_stats_daily)
    query = query.replace('__MEMBER_ID__', str(memberId))
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    query = query.replace('__WORKING_WEEKEND_NOTE_FORM_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))

    print(query)
    cur.execute(query)
    workingWeekendStatsDaily = dictfetchall(cur)

    if cur != None :
        cur.close()

    return workingWeekendStatsDaily

def getWorkingOffPromotes(request) :
    searchYear = request.GET.get('searchYear')
    searchMonth = request.GET.get('searchMonth')
    workingOffPromoteNum = request.GET.get('workingOffPromoteNum')

    if workingOffPromoteNum is None :
        workingOffPromoteNum = 0
    else :
        workingOffPromoteNum = int(workingOffPromoteNum)

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_off_promotes)

    whereStr = ""
    if searchYear != "" :
        whereStr = "AND SUBSTRING(FIRST_PROMOTE_DATE, 1, 4) = '" + str(searchYear) + "'"

    if (workingOffPromoteNum == 1) :
        whereStr += "AND SUBSTRING(FIRST_PROMOTE_DATE, 1, 7) = '" + searchMonth + "' "
    elif (workingOffPromoteNum == 2) :
        whereStr += "AND SUBSTRING(SECOND_PROMOTE_DATE, 1, 7) = '" + searchMonth + "' "

    query = query.replace('__WORKING_OFF_PROMOTE_DATE__', whereStr)
    print(query)
    cur.execute(query)
    workingOffPromotes = dictfetchall(cur)

    if cur != None :
        cur.close()

    return workingOffPromotes

def getWorkingOffPromotePlans(request, workingOffPromoteId) :
    workingOffPromoteNum = request.GET.get('workingOffPromoteNum')
    return ReWorkingOffPromotePlan.objects.filter(Q(working_off_promote_id = workingOffPromoteId) & Q(working_off_promote_num = workingOffPromoteNum))

def getWorkingCertificates(request) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_certificates)

    print(query)
    cur.execute(query)
    workingCertificates = dictfetchall(cur)

    if cur != None :
        cur.close()

    return workingCertificates

def getWorkingOffYearlys(request) :
    searchDate = request.GET.get('searchDate')
    searchStr = request.GET.get('searchStr')

    if searchStr != "" :
        search = "AND b.member_name LIKE '%" + searchStr + "%'"
    else :
        search = "AND to_char(to_date(a.working_off_start_date,'YYYY-MM'), 'YYYY-MM') = '" + searchDate + "'"

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working_admin.get_working_off_yearlys)
    query = query.replace('__SEARCH__', search)

    print(query)
    cur.execute(query)
    workingOffYearlys = dictfetchall(cur)

    if cur != None :
        cur.close()

    return workingOffYearlys

def getDateWorkingTime(memberId, date) :
    reWorkingTimes = ReWorkingTime.objects.filter(member_id = memberId)
    if len(reWorkingTimes) > 0 :
        reWorkingTime = reWorkingTimes.last()
        weekday = datetime.strptime(date, "%Y-%m-%d").isoweekday()
        if weekday == 1 :
            # 월
            workingTimeStartTime = datetime.strptime(date + " " + reWorkingTime.working_time_start_time_1, "%Y-%m-%d %H:%M")
            workingTimeEndTime = datetime.strptime(date + " " + reWorkingTime.working_time_end_time_1, "%Y-%m-%d %H:%M")
        elif weekday == 2 :
            # 화
            workingTimeStartTime = datetime.strptime(date + " " + reWorkingTime.working_time_start_time_2, "%Y-%m-%d %H:%M")
            workingTimeEndTime = datetime.strptime(date + " " + reWorkingTime.working_time_end_time_2, "%Y-%m-%d %H:%M")
        elif weekday == 3 :
            # 수
            workingTimeStartTime = datetime.strptime(date + " " + reWorkingTime.working_time_start_time_3, "%Y-%m-%d %H:%M")
            workingTimeEndTime = datetime.strptime(date + " " + reWorkingTime.working_time_end_time_3, "%Y-%m-%d %H:%M")
        elif weekday == 4 :
            # 목
            workingTimeStartTime = datetime.strptime(date + " " + reWorkingTime.working_time_start_time_4, "%Y-%m-%d %H:%M")
            workingTimeEndTime = datetime.strptime(date + " " + reWorkingTime.working_time_end_time_4, "%Y-%m-%d %H:%M")
        elif weekday == 5 :
            # 금
            workingTimeStartTime = datetime.strptime(date + " " + reWorkingTime.working_time_start_time_5, "%Y-%m-%d %H:%M")
            workingTimeEndTime = datetime.strptime(date + " " + reWorkingTime.working_time_end_time_5, "%Y-%m-%d %H:%M")
        else :
            # 주말인 경우
            workingTimeStartTime = datetime.strptime(date + " 09:00", "%Y-%m-%d %H:%M")
            workingTimeEndTime = datetime.strptime(date + " 18:00", "%Y-%m-%d %H:%M")
    else :
        # 기본값
        workingTimeStartTime = datetime.strptime(date + " 09:00", "%Y-%m-%d %H:%M")
        workingTimeEndTime = datetime.strptime(date + " 18:00", "%Y-%m-%d %H:%M")

    return workingTimeStartTime, workingTimeEndTime

def updateWorkingOffCancel(request, workingOffFormId) :
    try :
        reWorkingOffForm = ReWorkingOffForm.objects.get(working_off_form_id = workingOffFormId)

        # 현재 상태가 어드민 취소 인 경우 처리
        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL_ADMIN") :
            return True, "success"

        reWorkingOffForm.working_off_form_state = Code().getCodeDtlNoByAlias("APPROVAL_CANCEL_ADMIN")
        reWorkingOffForm.save()

        reWorkingOffs = ReWorkingOff.objects.filter(working_off_form_id = workingOffFormId)
        for reWorkingOff in reWorkingOffs :
            reWorkingOff.working_off_state = Code().getCodeDtlNoByAlias("APPROVAL_CANCEL_ADMIN")
            reWorkingOff.save()

        reMember = ReMember.objects.get(member_id = reWorkingOffForm.member_id)
        workingOffDays = reMember.working_off_days + reMember.working_off_etc_days
        workingOffUseDays = reMember.working_off_use_days - reWorkingOffForm.working_off_form_use_num
        workingOffRemainDays = workingOffDays - workingOffUseDays

        reMember.working_off_use_days = workingOffUseDays
        reMember.working_off_remain_days = workingOffRemainDays
        reMember.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updatePrevWorkingOffCancel(request, workingOffFormId) :
    try :
        reWorkingOffForm = ReWorkingOffForm.objects.get(working_off_form_id = workingOffFormId)
        reWorkingOffForm.working_off_form_state = Code().getCodeDtlNoByAlias("APPROVAL_DONE")
        reWorkingOffForm.save()

        reWorkingOffs = ReWorkingOff.objects.filter(working_off_form_id = workingOffFormId)
        for reWorkingOff in reWorkingOffs :
            reWorkingOff.working_off_state = Code().getCodeDtlNoByAlias("APPROVAL_DONE")
            reWorkingOff.save()

        reMember = ReMember.objects.get(member_id = reWorkingOffForm.member_id)
        workingOffDays = reMember.working_off_days + reMember.working_off_etc_days
        workingOffUseDays = reMember.working_off_use_days + reWorkingOffForm.working_off_form_use_num
        workingOffRemainDays = workingOffDays - workingOffUseDays

        reMember.working_off_use_days = workingOffUseDays
        reMember.working_off_remain_days = workingOffRemainDays
        reMember.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"


def updateWorkingOffDays(request, memberId) :
    data = json.loads(request.body)["data"]
    try :
        reMember = ReMember.objects.get(member_id = memberId)
        reMember.working_off_acc_days = data["working_off_acc_days"]
        reMember.working_off_acc_use_days = data["working_off_acc_use_days"]
        reMember.working_off_acc_remain_days = data["working_off_acc_remain_days"]
        reMember.working_off_days = data["working_off_days"]
        reMember.working_off_use_days = data["working_off_use_days"]
        reMember.working_off_remain_days = data["working_off_remain_days"]
        reMember.working_off_etc_days = data["working_off_etc_days"]
        reMember.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingOffAddDays(request) :
    data = json.loads(request.body)["data"]
    try :
        reMember = ReMember.objects.get(member_id = data["member_id"])
        reMember.working_off_add_days = data["working_off_add_days"]
        reMember.working_off_add_remain_days = data["working_off_add_remain_days"]
        reMember.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingTime(request) :
    data = json.loads(request.body)["data"]
    try :
        workingId =  data["working_id"]
        memberId = data["member_id"]
        workingDate = data["working_date"]

        workingStartCheckDatetime = None
        if (data["working_start_check_datetime"] != '') :
            workingStartCheckDatetime = data["working_start_check_datetime"]

        workingEndCheckDatetime = None
        if (data["working_end_check_datetime"] != '') :
            workingEndCheckDatetime = data["working_end_check_datetime"]

        if workingId is None :
            workingTime = getDateWorkingTime(memberId, workingDate)

            reWorking = ReWorking(
                member_id = memberId,
                working_date = workingDate,
                working_start_datetime = workingTime[0],
                working_end_datetime = workingTime[1],
                working_start_check_datetime = workingStartCheckDatetime,
                working_end_check_datetime = workingEndCheckDatetime,
                is_working_time_change = "Y",
            )
        else :
            reWorking = ReWorking.objects.get(working_id = workingId)
            reWorking.working_start_check_datetime = workingStartCheckDatetime
            reWorking.working_end_check_datetime = workingEndCheckDatetime
            reWorking.is_working_time_change = "Y"
        reWorking.save()

        # 통계 처리
        makeWokringStatMember(workingDate, memberId)

    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingChangeTime(request) :
    data = json.loads(request.body)["data"]
    try :
        reWorking = ReWorking.objects.get(working_id = data["working_id"])
        if data["working_start_change_datetime"] != None :
            reWorking.working_start_check_datetime = data["working_start_change_datetime"]

        if data["working_end_change_datetime"] != None :
            reWorking.working_end_check_datetime = data["working_end_change_datetime"]

        reWorking.working_start_change_datetime = None
        reWorking.working_end_change_datetime = None
        reWorking.save()

        # 통계 처리
        makeWokringStatMember(reWorking.working_date, reWorking.member_id)
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingTimeChange(request) :
    data = json.loads(request.body)["data"]
    try :
        reWorkingTime = ReWorkingTime.objects.get(working_time_id = data["working_time_id"])
        reWorkingTime.working_time_start_time_1 = data["working_time_start_time_1"]
        reWorkingTime.working_time_end_time_1 = data["working_time_end_time_1"]

        reWorkingTime.working_time_start_time_2 = data["working_time_start_time_2"]
        reWorkingTime.working_time_end_time_2 = data["working_time_end_time_2"]

        reWorkingTime.working_time_start_time_3 = data["working_time_start_time_3"]
        reWorkingTime.working_time_end_time_3 = data["working_time_end_time_3"]

        reWorkingTime.working_time_start_time_4 = data["working_time_start_time_4"]
        reWorkingTime.working_time_end_time_4 = data["working_time_end_time_4"]

        reWorkingTime.working_time_start_time_5 = data["working_time_start_time_5"]
        reWorkingTime.working_time_end_time_5 = data["working_time_end_time_5"]

        reWorkingTime.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingOffPromote(request, workingOffPromoteId) :
    data = json.loads(request.body)["data"]
    try :
        reWorkingOffPromote = ReWorkingOffPromote.objects.get(working_off_promote_id = workingOffPromoteId)
        reWorkingOffPromote.first_promote_date = data["first_promote_date"]
        reWorkingOffPromote.first_promote_status = data["first_promote_status"]
        reWorkingOffPromote.second_promote_date = data["second_promote_date"]
        reWorkingOffPromote.second_promote_status = data["second_promote_status"]
        reWorkingOffPromote.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingCertificateStatusDone(request, workingCertificateId) :
    try :
        reWorkingCertificate = ReWorkingCertificate.objects.get(working_certificate_id = workingCertificateId)
        reWorkingCertificate.working_certificate_status = Code().getCodeDtlNoByAlias("WORKING_CERTIFICATE_STATUS_DONE")
        reWorkingCertificate.working_certificate_done_date = datetime.now().strftime("%Y-%m-%d")
        reWorkingCertificate.save()

        # 메일 발송
        reMember = getReMember(reWorkingCertificate.member_id)
        receiverEmail  = reMember.member_email

        emailTitle = "[증명서] 발급 알림"
        emailContents = "안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>"+ \
                        reMember.member_name + "님의 [증명서] 발급 완료 알림 입니다." + "<br>"+ \
                        "<a href='https://voronoi.app/re-working/working-certificate-view'>[증명서]</a> 에서 확인 가능합니다."+ \
                        "<br><br>감사합니다."

        email_service = gmail_authenticate()
        message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
        send_message(email_service, "me", message)

    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingCertificateStatusReject(request, workingCertificateId) :
    data = json.loads(request.body)["data"]
    try :
        reWorkingCertificate = ReWorkingCertificate.objects.get(working_certificate_id = workingCertificateId)
        reWorkingCertificate.working_certificate_status = Code().getCodeDtlNoByAlias("WORKING_CERTIFICATE_STATUS_REJECT")
        reWorkingCertificate.save()

        # 메일 발송
        reMember = getReMember(reWorkingCertificate.member_id)
        receiverEmail  = reMember.member_email

        emailTitle = "[증명서] 반려 알림"
        emailContents = "안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>"+ \
                        reMember.member_name + "님의 [증명서] 신청 반려 알림 입니다.<br>"+ \
                        "반려 사유 : " + data["reason"] + \
                        "<br><br>감사합니다."

        email_service = gmail_authenticate()
        message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
        send_message(email_service, "me", message)

    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingCertificateJoinDate(request, workingCertificateId) :
    data = json.loads(request.body)["data"]
    try :
        reWorkingCertificate = ReWorkingCertificate.objects.get(working_certificate_id = workingCertificateId)
        reWorkingCertificate.join_date = data["join_date"]
        reWorkingCertificate.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingOffYearlyDays(request, workingOffYearlyId) :
    data = json.loads(request.body)["data"]
    try :
        reWorkingOffYearly = ReWorkingOffYearly.objects.get(working_off_yearly_id = workingOffYearlyId)
        reWorkingOffYearly.working_off_days = data["working_off_total_days"]
        reWorkingOffYearly.working_off_days = data["working_off_days"]
        reWorkingOffYearly.working_off_use_days = data["working_off_use_days"]
        reWorkingOffYearly.working_off_remain_days = data["working_off_remain_days"]
        reWorkingOffYearly.working_off_etc_days = data["working_off_etc_days"]
        reWorkingOffYearly.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateHoliday(request) :
    data = json.loads(request.body)["data"]
    try :
        holidayDate = data["holiday_date"]

        holidayStartDatetime = data["holiday_start_datetime"]
        if  holidayStartDatetime == "" :
            holidayStartDatetime = None
        else :
            holidayStartDatetime = datetime.strptime(holidayStartDatetime, "%Y-%m-%d %H:%M:%S")

        holidayEndDatetime = data["holiday_end_datetime"]
        if  holidayEndDatetime == "" :
            holidayEndDatetime = None
        else :
            holidayEndDatetime = datetime.strptime(holidayEndDatetime, "%Y-%m-%d %H:%M:%S")

        reHoliday = ReHoliday.objects.get(holiday_id = data["holiday_id"])
        reHoliday.holiday_name = data["holiday_name"]
        reHoliday.holiday_date = holidayDate
        reHoliday.holiday_start_datetime = holidayStartDatetime
        reHoliday.holiday_end_datetime = holidayEndDatetime
        reHoliday.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"


def deleteWorkingChangeTime(request, workingId) :
    try :
        reWorking = ReWorking.objects.get(working_id = workingId)
        reWorking.working_start_change_datetime = None
        reWorking.working_end_change_datetime = None
        reWorking.working_time_change_reason = ""
        reWorking.is_working_time_change = "N"
        reWorking.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"


def deleteWorkingTime(request, workingTimeId) :
    try :
        ReWorkingTime.objects.get(working_time_id = workingTimeId).delete()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def deleteHoliday(request, holidayId) :
    try :
        ReHoliday.objects.get(Q(holiday_id = holidayId)).delete()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def loadHoliday(year) :
    endPoint = "https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo"
    serviceKey = "&ServiceKey=M0pWG%2BNa5WilJaYB2DRKPLLf6%2FPUH6cpVsIbhIa4sq1d1s6i%2BtD%2Fug1O0kK271OpBIYkxWHhtgD8%2FLB%2BsffHWA%3D%3D"
    headers = {"Content-Type": "application/json"}

    ReHoliday.objects.filter(Q(holiday_date__startswith=year) & Q(holiday_create_type = Code().getCodeDtlNoByAlias("HOLIDAY_CREATE_TYPE_AUTO"))).all().delete()
    try:
        for i in range(1, 13) :
            print('{:02d}'.format(i))
            search = "?solYear=" + year + "&solMonth=" + '{:02d}'.format(i)
            url = endPoint + search + serviceKey
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            xmlObject = xmltodict.parse(response.content)
            totalCount = int(xmlObject["response"]["body"]["totalCount"])

            if totalCount > 0:
                if totalCount > 1:
                    list = xmlObject["response"]["body"]["items"]["item"]
                    for data in list :
                        if data["isHoliday"] == 'Y' :
                            dateName = data["dateName"]
                            locdate = data["locdate"]
                            year = locdate[:4]
                            month = locdate[4:6]
                            day = locdate[6:8]

                            ReHoliday(
                                holiday_name = dateName,
                                holiday_date = year + "-" + month + "-" + day,
                                holiday_create_type = Code().getCodeDtlNoByAlias("HOLIDAY_CREATE_TYPE_AUTO")
                            ).save()
                else :
                    data = xmlObject["response"]["body"]["items"]["item"]
                    if data["isHoliday"] == 'Y' :
                        dateName = data["dateName"]
                        locdate = data["locdate"]
                        year = locdate[:4]
                        month = locdate[4:6]
                        day = locdate[6:8]

                        ReHoliday(
                            holiday_name = dateName,
                            holiday_date = year + "-" + month + "-" + day,
                            holiday_create_type = Code().getCodeDtlNoByAlias("HOLIDAY_CREATE_TYPE_AUTO")
                        ).save()

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    return True, "success"

def makeWokringStatMember(workingStatDate, memberId) :
    print("Make working stat member start")

    print("workingStatDate  : " + workingStatDate)
    print("memberId  : " + str(memberId))

    print(datetime.now().strftime("%Y-%m-%d"))
    if workingStatDate != datetime.now().strftime("%Y-%m-%d") :
        ReWorkingStat.objects.filter(Q(working_stat_date = workingStatDate) & Q(member_id = memberId)).delete()

        isWeekday = True
        weekday = datetime.strptime(workingStatDate, "%Y-%m-%d").isoweekday()
        if weekday == 6 or weekday == 7 or ReHoliday.objects.filter(Q(holiday_date = workingStatDate)).count() == 1:
            isWeekday = False

        # 순환참조 (Circular Import)로 인하여 여기서 import
        from re_working_admin.scheduler import wokringStat
        wokringStat(workingStatDate, memberId, isWeekday)

    print("Make working stat member end")

def makeWokringStat(request) :
    print("Make working stat start")
    try :
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')

        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        endDate = datetime.strptime(endDate, "%Y-%m-%d")

        # 순환참조 (Circular Import)로 인하여 여기서 import
        from re_working_admin.scheduler import makeWokringStatPeriod
        makeWokringStatPeriod(startDate, endDate)

    except Exception as e :
        print("Exception::", e)
        return False, e

    print("Make working stat end")
    return True, "success"

def runSchedule(request) :
    print("Make runSchedule start")
    try :
        # 순환참조 (Circular Import)로 인하여 여기서 import
        from re_working_admin.scheduler import makeWorkingOffDays, makeWorkingDays
        makeWorkingOffDays()
        makeWorkingDays()

    except Exception as e :
        print("Exception::", e)
        return False, e

    print("Make runSchedule end")
    return True, "success"

def workingDownload(request) :
    workingDate = request.GET.get('working_date')
    workings = getWorkings(request)

    response = HttpResponse(content_type="application/vnd.ms-excel")

    # 다운로드 받을 때 생성될 파일명 설정
    response["Content-Disposition"] = "attachment; filename=working_" + str(workingDate) + ".xls"

    # 인코딩 설정
    wb = xlwt.Workbook(encoding='utf-8')
    # 생성될 시트명 설정
    ws = wb.add_sheet(str(workingDate))

    # 엑셀 스타일: 첫번째 열(=title)과 나머지 열(=data) 구분 위한 설정
    title_style = xlwt.easyxf('pattern: pattern solid, fore_color indigo; align: horizontal center; font: color_index white;')
    data_style = xlwt.easyxf('align: horizontal right')

    # 첫번째 열에 들어갈 컬럼명 설정
    col_names = ["사번","이름","부서","출근시간","출근상태","퇴근시간","퇴근상태","실근무시간","근무상태","변경요청"]

    # 엑셀에 쓸 데이터 리스트화
    rows = []
    for working in workings:

        workingStartCheckDatetime = ""
        if working["working_start_check_datetime"] is not None :
            workingStartCheckDatetime = working["working_start_check_datetime"].strftime("%H:%M")

        workingStartStatus = ""
        if working["working_start_check_datetime"] is not None :
            if (working["working_start_check_datetime"] < datetime.strptime(workingDate + " " + "09:01:00", "%Y-%m-%d %H:%M:%S")) :
                workingStartStatus = "출근"
            else :
                workingStartStatus = "지각"

        workingEndCheckDatetime = ""
        if working["working_end_check_datetime"] is not None :
            workingEndCheckDatetime = working["working_end_check_datetime"].strftime("%H:%M")

        workingEndStatus = ""
        if working["working_end_check_datetime"] is not None :
            if (working["working_end_check_datetime"] >= datetime.strptime(workingDate + " " + "19:00:00", "%Y-%m-%d %H:%M:%S")) :
                workingEndStatus = "연장근로"
            elif (working["working_end_check_datetime"] < datetime.strptime(workingDate + " " + "17:30:00", "%Y-%m-%d %H:%M:%S")) :
                workingEndStatus = "조기퇴근"
            else :
                workingEndStatus = "퇴근"

        workingTime = ""
        if working["working_start_check_datetime"] is not None :
            if working["working_end_check_datetime"] is None :
                working["working_end_check_datetime"] = datetime.now()
            workingTime = str(working["working_end_check_datetime"].replace(microsecond=0) - working["working_start_check_datetime"].replace(microsecond=0))

        workingStatus = "출근"
        if working["working_off_type"] is not None :
            workingStatus = Code().getCodeDtlNm(working["working_off_type"])

        if working["working_out_type"] is not None :
            workingStatus = Code().getCodeDtlNm(working["working_out_type"])

        if working["working_start_check_datetime"] is None and working["working_end_check_datetime"] is None :
            workingStatus = ""

        isWorkingTimeChange = ""
        if working["is_working_time_change"] == "Y" :
            isWorkingTimeChange = "출퇴근시간변경"

        rows.append([
            working["member_company_id"],
            working["member_name"],
            working["group_name"],
            workingStartCheckDatetime,
            workingStartStatus,
            workingEndCheckDatetime,
            workingEndStatus,
            workingTime,
            workingStatus,
            isWorkingTimeChange,
        ])

    # 첫번째 열: 설정한 컬럼명 순서대로 스타일 적용하여 생성
    row_num = 0
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name, title_style)

    # 두번째 이후 열: 설정한 컬럼명에 맞춘 데이터 순서대로 스타일 적용하여 생성
    for row in rows:
        row_num +=1
        for col_num, attr in enumerate(row):
            ws.write(row_num, col_num, attr, data_style)

    wb.save(response)

    return response

def WorkingOffPromoteDownload(request) :
    searchYear = request.GET.get('searchYear')
    workingOffPromotes = getWorkingOffPromotes(request)

    path = "re-promote" + os.path.sep + str(searchYear)
    default_storage.save(path + os.path.sep + "temp.txt", ContentFile(b""))
    for workingOffPromote in workingOffPromotes :
        if workingOffPromote["first_promote_status"] == Code().getCodeDtlNoByAlias("WORKING_OFF_PROMOTE_STATUS_DONE") :
            workingOffPromotePlans = ReWorkingOffPromotePlan.objects.filter(Q(working_off_promote_id = workingOffPromote["working_off_promote_id"]) & Q(working_off_promote_num = 1))
            makeWorkingOffPromotePdf(path, str(searchYear), "1", workingOffPromote, workingOffPromotePlans)

        if workingOffPromote["second_promote_status"] == Code().getCodeDtlNoByAlias("WORKING_OFF_PROMOTE_STATUS_DONE") :
            workingOffPromotePlans = ReWorkingOffPromotePlan.objects.filter(Q(working_off_promote_id = workingOffPromote["working_off_promote_id"]) & Q(working_off_promote_num = 2))
            makeWorkingOffPromotePdf(path, str(searchYear), "2", workingOffPromote, workingOffPromotePlans)

    filelist = os.listdir(default_storage.path(path))

    zipFileName = str(searchYear) + "_annual_leave.zip"
    # zip 압축
    with ZipFile(default_storage.path(path) + os.path.sep + zipFileName, "w") as zip :
        for file in filelist :
            if os.path.splitext(file)[1] == '.zip' or os.path.splitext(file)[1] == '.txt': continue
            src = default_storage.path(path) + os.path.sep + file
            zip.write(src, os.path.basename(src))
        zip.close()

    print("Make zip file : " + zipFileName)

    return path, zipFileName

def makeWorkingOffPromotePdf(path, searchYear, workingOffPromoteNum, workingOffPromote, workingOffPromotePlans) :
    # 연차 사용 기간
    workingOffStartDate = workingOffPromote["working_off_start_date"]
    workingOffEndDate = (datetime.strptime(workingOffStartDate, "%Y-%m-%d") + relativedelta(years=1) - relativedelta(days=1)).strftime("%Y-%m-%d")
    workingOffPeriod = workingOffStartDate  + " ~ " + workingOffEndDate
    # 그룹명
    groupName = ""
    if workingOffPromote["group_name"] is not None :
        groupName = workingOffPromote["group_name"]

    # 1차 2차 Data
    if workingOffPromoteNum == "1" :
        workingOffDays = workingOffPromote["first_working_off_days"]
        workingOffUseDays = workingOffPromote["first_working_off_use_days"]
        workingOffRemainDays = workingOffPromote["first_working_off_remain_days"]
        promote_submit_datetime = workingOffPromote["first_promote_submit_datetime"]
    elif workingOffPromoteNum == "2" :
        workingOffDays = workingOffPromote["second_working_off_days"]
        workingOffUseDays = workingOffPromote["second_working_off_use_days"]
        workingOffRemainDays = workingOffPromote["second_working_off_remain_days"]
        promote_submit_datetime = workingOffPromote["second_promote_submit_datetime"]

    # 폰트 등록
    pdfmetrics.registerFont(TTFont('NotoSansKR', settings.BASE_DIR + '/static/font/NotoSansKR-Regular.ttf'))
    styles = getSampleStyleSheet()

    # 구분줄
    hr = HRFlowable(width="100%", thickness=0.3, color=colors.black, spaceBefore=10, spaceAfter=10)

    # 기본 스타일에 한글 폰트 설정
    styles.add(ParagraphStyle(
        name='KoreanNormal',
        fontName='NotoSansKR',
        fontSize=10
    ))

    filename = default_storage.path(path) + os.path.sep + searchYear + "_" + workingOffPromoteNum + "_" + workingOffPromote["member_company_id"]  + ".pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    year = Paragraph(searchYear + "년", ParagraphStyle(
        name='Year',
        fontName='NotoSansKR',
        fontSize=12,
        leading=22,
        alignment=TA_RIGHT,
    ))
    elements.append(year)
    elements.append(Spacer(1, 12))

    # 제목 추가
    title = Paragraph(str(workingOffPromoteNum) + "차 미사용 연차유급휴가 사용촉진 통지서 및 사용계획서", ParagraphStyle(
        name='Title',
        fontName='NotoSansKR',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
    ))
    elements.append(title)
    elements.append(Spacer(1, 20))

    # 연차 정보
    data = [
        [
            Paragraph("<b>" + workingOffPromote["member_name"] + "</b>", styles['KoreanNormal']),
            Paragraph("<b>연차휴가 사용대상기간</b> (" + workingOffPeriod + ")", styles['KoreanNormal']),
            ""
        ],
        [
            Paragraph(groupName, styles['KoreanNormal']),
            Paragraph("전체일수", styles['KoreanNormal']),
            Paragraph("사용일수", styles['KoreanNormal']),
            Paragraph("미사용", styles['KoreanNormal']),
        ],
        [
            groupName,
            str(workingOffDays),
            str(workingOffUseDays),
            Paragraph(str(workingOffRemainDays), ParagraphStyle(
                name='text',
                fontName='NotoSansKR',
                fontSize=10,
                textColor= colors.red,
                alignment=TA_CENTER,
            ))
        ],
    ]

    # 테이블 생성 및 스타일 적용
    table = Table(data, colWidths=[100, 150, 100, 100])
    table.setStyle(TableStyle([
        ('SPAN', (0, 0), (0, 1)),  # 첫번째 셀 병합
        ('SPAN', (0, 1), (0, -1)),  # 두번째 셀 병합
        ('SPAN', (1, 0), (-1, 0)),  # 첫번째 행 병합
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 테두리 스타일
        ('BACKGROUND', (1, 1), (-1, 1), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # 본문 내용 추가
    text = """
    [근로기준법] 제 61조 연차 유급휴가의 사용 촉진 조항에 근거하여 <b>2024년 05월 20일</b> 까지
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 5))

    text = """
    '미사용 연차유급휴가 사용계획서'를 작성하여 통보 바랍니다.
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 15))

    text = """
    회사의 사용촉구에도 불구하고
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 5))

    text = """
    미사용 연차에 대해서는 다음 시기로 이월되거나 수당으로 지급되지 않고 자동 소멸됩니다.
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 5))

    text = """
    연차유급휴가를 적극적으로 사용해 주시기 바랍니다.
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_CENTER)
    ))
    elements.append(Spacer(1, 12))
    elements.append(hr)
    if len(workingOffPromotePlans) > 0 :
        #  연차 촉진 계획

        text = """
        미사용 연차유급휴가 사용계획서
        """
        elements.append(Paragraph(text, ParagraphStyle(
            name='text',
            fontName='NotoSansKR',
            fontSize=11,
            leading=22,
            alignment=TA_LEFT)
        ))
        elements.append(Spacer(1, 12))

        data = []
        count = 1
        total = 0
        for workingOffPromotePlan in workingOffPromotePlans :
            data.append(
                [
                    Paragraph("연차 " + str(count), styles['KoreanNormal']),
                    workingOffPromotePlan.working_off_start_date,
                    workingOffPromotePlan.working_off_end_date,
                    str(workingOffPromotePlan.working_off_use_num),
                ]
            )
            count = count + 1
            total += workingOffPromotePlan.working_off_use_num

        data.append(
            [
                Paragraph("총합", styles['KoreanNormal']),
                "",
                "",
                Paragraph(str(total), ParagraphStyle(
                    name='text',
                    fontName='NotoSansKR',
                    fontSize=11,
                    alignment=TA_CENTER,
                ))
            ]
        )

        # 테이블 생성 및 스타일 적용
        table = Table(data, colWidths=[100, 100, 100, 100])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 테두리 스타일
            ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
        elements.append(hr)

    # 연차 사용 계획 안내 및 하단 내용 추가
    text = """
    ※ 연차 사용 계획 안내
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_LEFT)
    ))
    elements.append(Spacer(1, 5))

    text = """
    - 본인이 사용하고자 하는 지정 일자 및 일수를 계획서 란에 기입해 주시기 바랍니다.
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_LEFT)
    ))
    elements.append(Spacer(1, 1))

    text = """
    - 본 계획은 예정사항으로, 실제 휴가 사용 시에는 전자결재를 통해 신청하셔야 합니다.
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_LEFT)
    ))
    elements.append(Spacer(1, 1))

    text = """
    - 또한, 사용하지 않은 연차 유급 휴가의 사용 시기를 별도로 지정하지 않는 경우,
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_LEFT)
    ))
    text = """
    회사 측에서 사용 시기를 결정할 수 있습니다.
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_LEFT)
    ))
    elements.append(Spacer(1, 1))

    text = """
    - 연차 전예일이 이미 연하얼 경우에는 통지서 내용을 확인하신 후 제출하시기 바랍니다.
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=10,
        leading=22,
        alignment=TA_LEFT)
    ))
    elements.append(Spacer(1, 20))
    if promote_submit_datetime is not None :
        text = """
        {}
        """.format(promote_submit_datetime.strftime("%Y년 %m월 %d일"))
        elements.append(Paragraph(text, ParagraphStyle(
            name='text',
            fontName='NotoSansKR',
            fontSize=10,
            leading=22,
            alignment=TA_CENTER)
        ))
        elements.append(Spacer(1, 20))

    text = """
    보로노이 주식회사
    """
    elements.append(Paragraph(text, ParagraphStyle(
        name='text',
        fontName='NotoSansKR',
        fontSize=15,
        leading=22,
        alignment=TA_CENTER)
    ))

    # PDF 저장
    doc.build(elements)

def queryConv(queryArr) :
    listQuery = ''
    for queryStr in queryArr :
        listQuery += queryStr
    return listQuery

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]
