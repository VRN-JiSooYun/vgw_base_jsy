from django.shortcuts import render
from re_working_admin.functions import *
# from project.views import authority
#from re_working_admin.scheduler import sendWorkingOffPromote
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import FileResponse
from urllib import parse

# page
@login_required(login_url='/security/login/')
def working_month_admin_page(request) :
    print("working_month_admin_page :", request.user.id)
    return render(request, "working_month_admin.html")

@login_required(login_url='/security/login/')
def working_week_admin_page(request) :
    print("working_week_admin_page :", request.user.id)
    return render(request, "working_week_admin.html")

@login_required(login_url='/security/login/')
def working_off_admin_page(request) :
    print("working_off_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_off_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_off_yearly_admin_page(request) :
    print("working_off_yearly_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_off_yearly_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_off_promote_admin_page(request) :
    print("working_off_promote_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_off_promote_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_admin_page(request) :
    print("working_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_time_admin_page(request) :
    print("working_time_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_time_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_time_change_admin_page(request) :
    print("working_time_change_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_time_change_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_stat_admin_page(request) :
    print("working_stat_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_stat_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_part_admin_page(request) :
    print("working_part_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_part_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_approval_admin_page(request) :
    print("working_approval_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["D"] == True :
        return render(request, "working_approval_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def working_weekend_stat_admin_page(request) :
    print("working_weekend_stat_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_weekend_stat_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")


@login_required(login_url='/security/login/')
def working_certificate_admin_page(request) :
    print("working_certificate_admin_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "working_certificate_admin.html")
    else :
        return render(request, "working_admin_access_auth.html")

@login_required(login_url='/security/login/')
def holiday_page(request) :
    print("holiday_page :", request.user.id)
    # auth = authority("hr", request)
    auth = {"P":True, "R": True, "V": True, "D": True}
    if auth["R"] == True or auth["V"] == True or auth["D"] == True:
        return render(request, "holiday.html")
    else :
        return render(request, "working_admin_access_auth.html")

# api
@csrf_exempt
def create_holiday(request) :
    print("create_holiday :", request.user.id)
    if request.method == "POST":
        process = createHoliday(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def create_working_time(request) :
    print("create_working_time :", request.user.id)
    if request.method == "POST":
        process = createWorkingTime(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def get_working_month_data(request) :
    print("get_working_month_data :", request.user.id)
    context = {
        "workings": getWorkingMonthData(request),
        "holidays": list(getHolidays(request).values())
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_week_data(request) :
    print("get_working_week_data :", request.user.id)
    context = {
        "workingOffs": getWeekWorkingOffs(request),
        "workingOuts": getWeekWorkingOuts(request),
        "holidays": list(getHolidays(request).values())
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_workings(request) :
    print("get_workings :", request.user.id)
    context = {
        "workings": getWorkings(request),
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_historys(request) :
    print("get_working_historys :", request.user.id)
    context = {
        "workingHistorys": getWorkingHistorys(request),
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_change_working_times(request) :
    print("get_change_working_times :", request.user.id)
    context = {
        "workings": getChangeWorkingTimes(request),
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_off_historys(request) :
    print("get_working_off_historys :", request.user.id)
    return JsonResponse(getWorkingOffHistorys(request), safe=False)

@csrf_exempt
def get_holidays(request) :
    print("get_holidays :", request.user.id)
    return JsonResponse(list(getYearHolidays(request).values()), safe=False)

@csrf_exempt
def get_holiday(request) :
    print("get_holiday :", request.user.id)
    return JsonResponse(model_to_dict(getHoliday(request)), safe=False)

@csrf_exempt
def get_working_times(request) :
    print("get_working_times :", request.user.id)
    return JsonResponse(getWorkingTimes(), safe=False)

@csrf_exempt
def get_working_stats(request) :
    print("get_working_stats :", request.user.id)
    return JsonResponse(getWorkingStats(request), safe=False)

def get_working_parts(request) :
    print("get_working_parts :", request.user.id)
    return JsonResponse(getWorkingParts(request), safe=False)

def get_projects(request) :
    print("get_projects :", request.user.id)
    return JsonResponse(list(getProjects().values()), safe=False)

@csrf_exempt
def get_working_time_group_tree(request) :
    print("get_working_time_group_tree :", request.user.id)
    return JsonResponse(json.loads(getWorkingTimeGroupTree().toJSON()), safe=False)

@csrf_exempt
def get_working_approvals(request, limit, offset) :
    print("get_working_approvals :", request.user.id)
    context = {
        "totalCount": getWorkingApprovalsCount(request),
        "workingApprovals": getWorkingApprovals(request, limit, offset)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_weekend_stats(request) :
    print("get_working_weekend_stats :", request.user.id)
    return JsonResponse(getWorkingWeekendStats(request), safe=False)

@csrf_exempt
def get_working_weekend_stats_daily(request, memberId) :
    print("get_working_weekend_stats_daily :", request.user.id, memberId)
    return JsonResponse(getWorkingWeekendStatsDaily(request, memberId), safe=False)

@csrf_exempt
def get_working_off_promotes(request) :
    print("get_working_off_promotes :", request.user.id)
    return JsonResponse(getWorkingOffPromotes(request), safe=False)

@csrf_exempt
def get_working_off_promote_plans(request, workingOffPromoteId) :
    print("get_working_off_promote_plans :", request.user.id, workingOffPromoteId)
    return JsonResponse(list(getWorkingOffPromotePlans(request, workingOffPromoteId).values()) , safe=False)

@csrf_exempt
def get_working_certificates(request) :
    print("get_working_certificates :", request.user.id)
    return JsonResponse(getWorkingCertificates(request), safe=False)

@csrf_exempt
def get_working_off_yearlys(request) :
    print("get_working_off_yearlys :", request.user.id)
    return JsonResponse(getWorkingOffYearlys(request), safe=False)

@csrf_exempt
def update_working_off_cancel(request, workingOffFormId) :
    print("update_working_off_cancel :", request.user.id)
    process = updateWorkingOffCancel(request, workingOffFormId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_prev_working_off_cancel(request, workingOffFormId) :
    print("update_prev_working_off_cancel :", request.user.id)
    process = updatePrevWorkingOffCancel(request, workingOffFormId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_off_days(request, memberId) :
    print("update_working_off_days :", request.user.id, memberId)
    process = updateWorkingOffDays(request, memberId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_off_add_days(request) :
    print("update_working_off_add_days :", request.user.id)
    process = updateWorkingOffAddDays(request)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_time(request) :
    print("update_working_time :", request.user.id)
    process = updateWorkingTime(request)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_change_time(request) :
    print("update_working_change_time :", request.user.id)
    process = updateWorkingChangeTime(request)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_time_change(request) :
    print("update_working_time_change :", request.user.id)
    process = updateWorkingTimeChange(request)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_off_promote(request, workingOffPromoteId) :
    print("update_working_off_promote :", request.user.id, workingOffPromoteId)
    process = updateWorkingOffPromote(request, workingOffPromoteId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def resend_working_off_promote(request) :
    data = json.loads(request.body)["data"]
    print("resend_working_off_promote :", request.user.id, data["memberId"])
    #process = sendWorkingOffPromote(data["memberId"])
    return JsonResponse({}, safe=False)

@csrf_exempt
def update_working_certificate_status_done(request, workingCertificateId) :
    print("update_working_certificate_status_done :", request.user.id, workingCertificateId)
    process = updateWorkingCertificateStatusDone(request, workingCertificateId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_certificate_status_reject(request, workingCertificateId) :
    print("update_working_certificate_status_reject :", request.user.id, workingCertificateId)
    process = updateWorkingCertificateStatusReject(request, workingCertificateId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_certificate_join_date(request, workingCertificateId) :
    print("update_working_certificate_join_date :", request.user.id, workingCertificateId)
    process = updateWorkingCertificateJoinDate(request, workingCertificateId)
    return JsonResponse(process, safe=False)


@csrf_exempt
def update_working_off_yearly_days(request, workingOffYearlyId) :
    print("update_working_off_yearly_days :", request.user.id, workingOffYearlyId)
    process = updateWorkingOffYearlyDays(request, workingOffYearlyId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def update_holiday(request) :
    print("update_holiday :", request.user.id)
    process = updateHoliday(request)
    return JsonResponse(process, safe=False)

@csrf_exempt
def delete_working_change_time(request, workingId) :
    print("delete_working_change_time :", request.user.id, workingId)
    process = deleteWorkingChangeTime(request, workingId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def delete_working_time(request, workingTimeId) :
    print("delete_working_time :", request.user.id, workingTimeId)
    process = deleteWorkingTime(request, workingTimeId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def delete_holiday(request, holidayId) :
    print("delete_holiday :", request.user.id, holidayId)
    process = deleteHoliday(request, holidayId)
    return JsonResponse(process, safe=False)

@csrf_exempt
def working_download(request) :
    print("working_download :", request.user.id)
    return workingDownload(request)

@csrf_exempt
def working_off_promote_download(request) :
    try :
        print("working_off_promote_download :", request.user.id)
        path, zipFileName = WorkingOffPromoteDownload(request)

        response = FileResponse(default_storage.open(path + os.path.sep + str(zipFileName)), content_type='application/octet-stream')
        filename = parse.quote(zipFileName.encode('utf-8'))
        response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % filename
        print("success download_file promote file")
    except Exception as e :
        print("Exception::", e)
        return False, e
    return response

@csrf_exempt
def load_holiday(request, year) :
    print("load_holiday :", request.user.id, year)
    process = loadHoliday(year)
    return JsonResponse(process, safe=False)


@csrf_exempt
def make_wokring_stat(request) :
    print("make_wokring_stat :", request.user.id)
    process = makeWokringStat(request)
    return JsonResponse(process, safe=False)

@csrf_exempt
def run_schedule(request) :
    print("run_schedule :", request.user.id)
    process = runSchedule(request)
    return JsonResponse(process, safe=False)
