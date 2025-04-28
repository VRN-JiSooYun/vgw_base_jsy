from django.shortcuts import render
from re_working.functions import *
# from project.functions import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import FileResponse
from home.code_singleton import Code
from urllib import parse

@login_required(login_url='/security/login/')
def working_month_page(request) :
    print("working_month_page :", request.user.id)
    context = {
        # "myhome_auth": authority("myhome", request)
        "myhome_auth": True
    }
    return render(request, "working_month.html", context)

@login_required(login_url='/security/login/')
def working_share_month_page(request) :
    print("working_share_month_page :", request.user.id)
    return render(request, "working_share_month.html")

@login_required(login_url='/security/login/')
def working_share_week_page(request) :
    print("working_share_week_page :", request.user.id)
    return render(request, "working_share_week.html")

@login_required(login_url='/security/login/')
def working_off_page(request) :
    print("working_off_page :", request.user.id)
    return render(request, "working_off.html")

@login_required(login_url='/security/login/')
def working_weekend_page(request) :
    print("working_weekend_page :", request.user.id)
    return render(request, "working_weekend.html")

@login_required(login_url='/security/login/')
def working_approval_page(request) :
    print("working_approval_page :", request.user.id)
    return render(request, "working_approval.html")

@login_required(login_url='/security/login/')
def working_approval_etc_page(request) :
    print("working_approval_etc_page :", request.user.id)
    return render(request, "working_approval_etc.html")

@login_required(login_url='/security/login/')
def working_certificate_page(request) :
    print("working_certificate_page :", request.user.id)
    return render(request, "working_certificate.html")

@csrf_exempt
def create_working_out(request) :
    print("create_working_out :", request.user.id)
    if request.method == "POST":
        process = createWorkingOut(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def create_working_off(request) :
    print("create_working_off :", request.user.id)
    if request.method == "POST":
        process = createWorkingOff(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def create_working_weekend(request) :
    print("create_working_weekend :", request.user.id)
    if request.method == "POST":
        process = createWorkingWeekend(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def create_working_weekend_note(request) :
    print("create_working_weekend_note :", request.user.id)
    if request.method == "POST":
        process = createWorkingWeekendNote(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def create_working_part(request) :
    print("create_working_part :", request.user.id)
    if request.method == "POST":
        process = createWorkingPart(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def create_working_certificate(request) :
    print("create_working_certificate :", request.user.id)
    if request.method == "POST":
        process = createWorkingCertificate(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def send_mail_working_off(request, approvalId) :
    print("send_mail_working_off :", request.user.id, approvalId)
    if request.method == "POST":
        process = sendMailWorkingOff(request, approvalId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def send_mail_working_weekend(request, approvalId) :
    print("send_mail_working_weekend :", request.user.id, approvalId)
    if request.method == "POST":
        process = sendMailWorkingWeekend(request, approvalId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def send_mail_working_weekend_note(request, approvalId) :
    print("send_mail_working_weekend_note :", request.user.id, approvalId)
    if request.method == "POST":
        process = sendMailWorkingWeekendNote(request, approvalId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def get_working_month_data(request) :
    print("get_working_month_data :", request.user.id)
    context = {
        "workings": list(getWorkings(request).values()),
        "workingOuts": list(getWorkingOuts(request).values()),
        "workingOffs": list(getWorkingOffs(request).values()),
        "holidays": list(getHolidays(request).values())
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_share_month_data(request) :
    print("get_working_share_month_data :", request.user.id)
    context = {
        "workings": getShareWorkingMonthData(request),
        "holidays": list(getHolidays(request).values())
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_share_week_data(request) :
    print("get_working_share_week_data :", request.user.id)
    context = {
        "workingOffs": getShareWorkingOffs(request),
        "workingOuts": getShareWorkingOuts(request),
        "holidays": list(getHolidays(request).values())
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working(request, workingDate) :
    print("get_working :", request.user.id, workingDate)
    return JsonResponse(list(getWorking(request, workingDate).values()), safe=False)

@csrf_exempt
def get_working_out_form(request, workingOutFormId) :
    print("get_working_out_form :", request.user.id, workingOutFormId)
    return JsonResponse(model_to_dict(getWorkingOutForm(workingOutFormId)), safe=False)

@csrf_exempt
def get_working_off_form(request, workingOffFormId) :
    print("get_working_off_form :", request.user.id, workingOffFormId)
    workingOffForm = getWorkingOffForm(workingOffFormId)
    context = {
        "workingOffForm": workingOffForm,
        "workingOffs": list(getWorkingOffByWorkingOffFormId(workingOffFormId).values()),
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_off_forms(request) :
    print("get_working_off_forms :", request.user.id)
    context = {
        "workingOffForms": getWorkingOffForms(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_off_view(request, workingOffFormId) :
    print("get_working_off_view :", request.user.id, workingOffFormId)
    workingOffForm = getWorkingOffForm(workingOffFormId)
    context = {
        "workingOffForm": workingOffForm,
        "workingOffs": list(getWorkingOffByWorkingOffFormId(workingOffFormId).values()),
        "approvalHistorys": getApprovalHistorys(workingOffForm["approval_id"])
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_prev_approval_members(request) :
    print("get_prev_approval_members :", request.user.id)
    prevApprovalMembers, prevApprovalEtcMembers  = getPrevApprovalMembers(request)
    context = {
        "prevApprovalMembers": prevApprovalMembers,
        "prevApprovalEtcMembers": prevApprovalEtcMembers,
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_recommend_approval_members(request) :
    print("get_recommend_approval_members :", request.user.id)
    return JsonResponse(list(getRecommendApprovalMembers(request).values()), safe=False)

@csrf_exempt
def get_recommend_approval_ref_members(request) :
    print("get_recommend_approval_ref_members :", request.user.id)
    return JsonResponse(list(getRecommendApprovalRefMembers(request).values()), safe=False)

@csrf_exempt
def get_working_weekend_form(request, workingWeekendFormId) :
    print("get_working_weekend_form :", request.user.id, workingWeekendFormId)
    context = {
        "workingWeekendForm": getWorkingWeekendForm(workingWeekendFormId),
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_weekend_forms(request) :
    print("get_working_weekend_forms :", request.user.id)
    context = {
        "workingWeekendForms": getWorkingWeekendForms(request)
    }
    return JsonResponse(context, safe=False)

def get_working_weekend_view(request, workingWeekendFormId) :
    print("get_working_weekend_view :", request.user.id, workingWeekendFormId)
    workingWeekendForm = getWorkingWeekendForm(workingWeekendFormId)
    context = {
        "workingWeekendForm": workingWeekendForm,
        "approvalHistorys": getApprovalHistorys(workingWeekendForm["approval_id"])
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_prev_working_weekend_forms(request) :
    print("get_prev_working_weekend_forms :", request.user.id)
    return JsonResponse(list(getPrevWorkingWeekendForms(request).values()), safe=False)

@csrf_exempt
def get_working_weekend_note_form(request, workingWeekendNoteFormId) :
    print("get_working_weekend_note_form :", request.user.id, workingWeekendNoteFormId)
    context = {
        "workingWeekendNoteForm": getWorkingWeekendNoteForm(workingWeekendNoteFormId)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_weekend_note_forms(request) :
    print("get_working_weekend_note_forms :", request.user.id)
    context = {
        "workingWeekendNoteForms": getWorkingWeekendNoteForms(request)
    }
    return JsonResponse(context, safe=False)

def get_working_weekend_note_view(request, workingWeekendNoteFormId) :
    print("get_working_weekend_note_view :", request.user.id, workingWeekendNoteFormId)
    workingWeekendNoteForm = getWorkingWeekendNoteForm(workingWeekendNoteFormId)
    context = {
        "workingWeekendNoteForm": workingWeekendNoteForm,
        "approvalHistorys": getApprovalHistorys(workingWeekendNoteForm["approval_id"])
    }
    return JsonResponse(context, safe=False)

def get_approval_historys(request, approvalId) :
    print("get_approval_historys :", request.user.id, approvalId)
    context = {
        "approvalHistorys": getApprovalHistorys(approvalId)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_approval_request(request) :
    print("get_working_approval_request :", request.user.id)
    context = {
        "workingApprovalRequest": getWorkingApprovalRequest(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_approvals(request) :
    print("get_working_approvals :", request.user.id)
    context = {
        "workingApprovals": getWorkingApprovals(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_approval_etc_refs(request) :
    print("get_working_approval_etc_refs :", request.user.id)
    context = {
        "workingApprovalEtcRefs": getWorkingApprovalEtcRefs(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_approval_etc_recvs(request) :
    print("get_working_approval_etc_recvs :", request.user.id)
    context = {
        "workingApprovalEtcRecvs": getWorkingApprovalEtcRecvs(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_approval_members(request, approvalId) :
    print("get_approval_members :", request.user.id, approvalId)
    context = {
        "approvalMembers": getApprovalMembers(approvalId)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_approval_etc_members(request, approvalId) :
    print("get_approval_etc_members :", request.user.id, approvalId)
    context = {
        "approvalEtcMembers": getApprovalEtcMembers(approvalId)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_approval_upload_files(request, approvalId) :
    print("get_approval_upload_files :", request.user.id, approvalId)
    return JsonResponse(list(getApprovalUploadFiles(approvalId).values()), safe=False)

@csrf_exempt
def get_approval_request_count(request) :
    print("get_approval_request_count :", request.user.id)
    return JsonResponse(getApprovalRequestCount(request.user.id), safe=False)

@csrf_exempt
def get_working_time(request) :
    print("get_working_time :", request.user.id)
    context = {
        "workingTime": getWorkingTime(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_working_off_promote_num(request) :
    print("get_working_off_promote_num :", request.user.id)
    return JsonResponse(getWorkingOffPromoteNum(request), safe=False)

@csrf_exempt
def get_working_off_promote(request) :
    print("get_working_off_promote :", request.user.id)
    return JsonResponse(model_to_dict(getWorkingOffPromote(request)), safe=False)

@csrf_exempt
def get_working_off_promote_plans(request, workingOffPromoteId) :
    print("get_working_off_promote_plans :", request.user.id, workingOffPromoteId)
    return JsonResponse(list(getWorkingOffPromotePlans(request, workingOffPromoteId).values()), safe=False)

@csrf_exempt
def get_working_part(request) :
    print("get_working_part :", request.user.id)
    return JsonResponse(getWorkingPart(request), safe=False)

@csrf_exempt
def get_projects(request) :
    print("get_projects :", request.user.id)
    return JsonResponse(list(getProjects(request).values()), safe=False)

@csrf_exempt
def get_working_certificates(request) :
    print("get_working_certificates :", request.user.id)
    return JsonResponse(list(getWorkingCertificates(request).values()), safe=False)

@csrf_exempt
def get_working_off_yearlys(request) :
    print("get_working_off_yearlys :", request.user.id)
    return JsonResponse(list(getWorkingOffYearlys(request).values()), safe=False)

@csrf_exempt
def get_working_off_teams(request) :
    print("get_working_off_teams :", request.user.id)
    return JsonResponse(list(getWorkingOffTeams(request).values()), safe=False)

@csrf_exempt
def get_chart_data(request):
    print("get_chart_data :", request.user.id)
    return JsonResponse(getChartData(request), safe=False)

@csrf_exempt
def update_working_out(request, workingOutFormId) :
    print("update_working_out :", request.user.id, workingOutFormId)
    if request.method == "POST":
        process = updateWorkingOut(request, workingOutFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_off_cancel(request, workingOffFormId) :
    print("update_working_off_cancel :", request.user.id, workingOffFormId)
    if request.method == "POST":
        process = updateWorkingOffCancel(request, workingOffFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_off_ok(request, workingOffFormId) :
    print("update_working_off_ok :", request.user.id, workingOffFormId)
    if request.method == "POST":
        process = updateWorkingOffOk(request, workingOffFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_off_reject(request, workingOffFormId) :
    print("update_working_off_reject :", request.user.id, workingOffFormId)
    if request.method == "POST":
        process = updateWorkingOffReject(request, workingOffFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_weekend_ok(request, workingWeekendFormId) :
    print("update_working_weekend_ok :", request.user.id, workingWeekendFormId)
    if request.method == "POST":
        process = updateWorkingWeekendOk(request, workingWeekendFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_weekend_reject(request, workingWeekendFormId) :
    print("update_working_weekend_reject :", request.user.id, workingWeekendFormId)
    if request.method == "POST":
        process = updateWorkingWeekendReject(request, workingWeekendFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_weekend_cancel(request, workingWeekendFormId) :
    print("update_working_weekend_cancel :", request.user.id, workingWeekendFormId)
    if request.method == "POST":
        process = updateWorkingWeekendCancel(request, workingWeekendFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_weekend_note_cancel(request, workingWeekendNoteFormId) :
    print("update_working_weekend_note_cancel :", request.user.id, workingWeekendNoteFormId)
    if request.method == "POST":
        process = updateWorkingWeekendNoteCancel(request, workingWeekendNoteFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_weekend_note_ok(request, workingWeekendNoteFormId) :
    print("update_working_weekend_note_ok :", request.user.id, workingWeekendNoteFormId)
    if request.method == "POST":
        process = updateWorkingWeekendNoteOk(request, workingWeekendNoteFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_weekend_note_reject(request, workingWeekendNoteFormId) :
    print("update_working_weekend_note_reject :", request.user.id, workingWeekendNoteFormId)
    if request.method == "POST":
        process = updateWorkingWeekendNoteReject(request, workingWeekendNoteFormId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def send_mail_working_ok(request, formType, approvalId) :
    print("send_mail_working_ok :", request.user.id, formType, approvalId)
    if request.method == "POST":
        process = sendMailWorkingOk(request, formType, approvalId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def send_mail_working_reject(request, formType, approvalId) :
    print("send_mail_working_reject :", request.user.id, formType, approvalId)
    if request.method == "POST":
        process = sendMailWorkingReject(request, formType, approvalId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def send_mail_working_cancel(request, formType, approvalId) :
    print("send_mail_working_cancel :", request.user.id, formType, approvalId)
    if request.method == "POST":
        process = sendMailWorkingCancel(request, formType, approvalId)
        return JsonResponse(process, safe=False)


@csrf_exempt
def update_working_off_promote_done(request, workingOffPromoteId) :
    print("update_working_off_promote :", request.user.id, workingOffPromoteId)
    if request.method == "POST":
        process = updateWorkingOffPromoteDone(request, workingOffPromoteId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_working_part(request, workingPartId) :
    print("update_working_part :", request.user.id, workingPartId)
    if request.method == "POST":
        process = updateWorkingPart(request, workingPartId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def working_start(request) :
    print("working_start :", request.user.id)
    if request.method == "POST":
        process = workingStart(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def working_end(request, memberId) :
    print("working_end :", memberId)
    if request.method == "POST":
        process = workginEnd(request, memberId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def change_working_time(request) :
    print("change_working_time :", request.user.id)
    if request.method == "POST":
        process = changeWorkingTime(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def check_working_start(request) :
    print("check_working_start :", request.user.id)
    context = {
        "isWorkingStart": checkWorkingStart(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def check_working_yesterday(request) :
    print("check_working_yesterday :", request.user.id)
    context = {
        "checkWorkingYesterday": checkWorkingYesterday(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def check_working_part(request) :
    print("check_working_part :", request.user.id)
    context = {
        "checkWorkingPart": checkWorkingPart(request)
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def upload_file(request, approvalId) :
    print("upload_file :", request.user.id, approvalId)
    if request.method == "POST":
        process = uploadFile(request, approvalId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def download_file(request, uploadFileId) :
    print("download_file :", request.user.id, uploadFileId)
    try :
        approvalUploadFile = getApprovalUploadFile(uploadFileId)

        response = FileResponse(default_storage.open("re-approval/" + str(uploadFileId)), content_type='application/octet-stream')
        filename = parse.quote(approvalUploadFile.upload_file_name.encode('utf-8'))
        response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % filename
        print("success download_file member file")
    except Exception as e :
        print("Exception::", e)
        return False, e
    return response

@csrf_exempt
def delete_working_out(request, workingOutFormId) :
    print("delete_working_out :", request.user.id, workingOutFormId)
    if request.method == "POST":
        process = deleteWorkingOut(workingOutFormId)
        return JsonResponse(process, safe=False)


@login_required(login_url='/security/login/')
def test(request) :
    context = {}
    return render(request, "test.html", context)
