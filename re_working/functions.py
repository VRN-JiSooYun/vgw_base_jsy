from django.db import connection
from re_working.models import *
from re_working_admin.models import *
# from project.models import *
from re_member.functions import *
from django.forms.models import model_to_dict
from django.conf import settings
from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from re_member.functions import *
from re_group.functions import *
from home.code_singleton import Code
# from dashboard.sendMailByGoogle import *
from django.core.files.storage import default_storage  # file save
import json

def createWorkingOut(request) :
    data = json.loads(request.body)["data"]
    try :
        memberId = request.user.id
        if "member_id" in data:
            memberId = data["member_id"]

        working_out_form_type = data["working_out_form_type"]
        working_out_form_start_date = parse(data["working_out_form_start_date"])
        working_out_form_end_date = parse(data["working_out_form_end_date"])

        reWorkingOutForm = ReWorkingOutForm(
            member_id = memberId,
            working_out_form_type = working_out_form_type,
            working_out_form_start_date = working_out_form_start_date.strftime("%Y-%m-%d"),
            working_out_form_end_date = working_out_form_end_date.strftime("%Y-%m-%d"),
        )
        reWorkingOutForm.save()

        working_out_date = working_out_form_start_date
        while working_out_date <= working_out_form_end_date :
            reWorkingOut = ReWorkingOut(
                working_out_form_id = reWorkingOutForm.working_out_form_id,
                member_id = memberId,
                working_out_type = working_out_form_type,
                working_out_date = working_out_date.strftime("%Y-%m-%d"),
            )
            reWorkingOut.save()
            working_out_date = working_out_date + timedelta(days=1)

        print("success create working out")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def createWorkingOff(request) :
    data = json.loads(request.body)["data"]

    try :
        approvalState = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST")
        approvalMembers = data["approval_members"]
        approvalRefMembers = data["approval_ref_members"]
        approvalRecvMembers = data["approval_recv_members"]

        approvalId = makeApprovalId()

        reApproval = ReApproval(
            approval_id = approvalId,
            approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
            req_member_id = request.user.id,
            res_member_id = approvalMembers[0]["member_id"],
            step = approvalMembers[0]["step"],
            approval_state = approvalState,
        )
        reApproval.save()
        print("success create appropval")

        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = reApproval.approval_state,
        )
        reApprovalHistory.save()
        print("success create appropval history")

        for approvalMember in approvalMembers :
            reApprovalMember = ReApprovalMember(
                approval_id = approvalId,
                approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
                member_id = approvalMember["member_id"],
                step = approvalMember["step"],
            )
            reApprovalMember.save()
        print("success create appropval members")

        for approvalRefMember in approvalRefMembers :
            reApprovalEtcMember = ReApprovalEtcMember(
                approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF"),
                approval_id = approvalId,
                member_id = approvalRefMember["member_id"],
            )
            reApprovalEtcMember.save()
        print("success create appropval ref members")

        for approvalRecvMember in approvalRecvMembers :
            reApprovalEtcMember = ReApprovalEtcMember(
                approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_RECV"),
                approval_id = approvalId,
                member_id = approvalRecvMember["member_id"],
            )
            reApprovalEtcMember.save()
        print("success create appropval recv members")


        reWorkingOffForm = ReWorkingOffForm(
            member_id = request.user.id,
            approval_id = approvalId,
            working_off_form_title = data["working_off_form_title"],
            working_off_form_type = data["working_off_form_type"],
            working_off_form_state = approvalState,
            working_off_form_start_date = data["working_off_form_start_date"],
            working_off_form_end_date = data["working_off_form_end_date"],
            working_off_form_use_num = float(data["working_off_form_use_num"]),
            reason = data["reason"],
        )
        reWorkingOffForm.save()

        workingOffs = data["working_offs"]
        for workingOff in workingOffs :
            reWorkingOff = ReWorkingOff(
                working_off_form_id = reWorkingOffForm.working_off_form_id,
                member_id = request.user.id,
                working_off_type = workingOff["working_off_type"],
                working_off_time = workingOff["working_off_time"],
                working_off_state = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST"),
                working_off_date = workingOff["working_off_date"],
                working_off_start_datetime = workingOff["working_off_start_datetime"],
                working_off_end_datetime = workingOff["working_off_end_datetime"],
            )
            reWorkingOff.save()

        print("success create working off")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, approvalId

def sendMailWorkingOff(request, approvalId) :
    reWorkingOffForm = ReWorkingOffForm.objects.get(Q(approval_id = approvalId))
    approvalMember = ReApprovalMember.objects.filter(Q(approval_id = approvalId) & Q(step = 1)).get()
    approvalRefMembers = ReApprovalEtcMember.objects.filter(Q(approval_id = approvalId) & Q(approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF")))

    # 상신 메일
    receiverMemberIds = []
    receiverMemberIds.append(reWorkingOffForm.member_id)
    for approvalRefMember in approvalRefMembers :
        receiverMemberIds.append(approvalRefMember.member_id)

    emailTitle, emailContents = makeRequestMail("working_off", approvalId)
    sendMail(receiverMemberIds, emailTitle, emailContents)

    # 결재 메일
    receiverMemberIds = []
    receiverMemberIds.append(approvalMember.member_id) # 결재자
    emailTitle, emailContents = makeApprovalMail("working_off", approvalId)
    sendMail(receiverMemberIds, emailTitle, emailContents)
    print("success send mail working off")
    return True

def createWorkingWeekend(request) :
    data = json.loads(request.body)["data"]

    try :
        approvalState = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST")
        approvalMembers = data["approval_members"]
        approvalRefMembers = data["approval_ref_members"]
        approvalRecvMembers = data["approval_recv_members"]

        approvalId = makeApprovalId()

        reApproval = ReApproval(
            approval_id = approvalId,
            approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
            req_member_id = request.user.id,
            res_member_id = approvalMembers[0]["member_id"],
            step = approvalMembers[0]["step"],
            approval_state = approvalState,
        )
        reApproval.save()
        print("success create appropval")

        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = reApproval.approval_state,
        )
        reApprovalHistory.save()
        print("success create appropval history")

        for approvalMember in approvalMembers :
            reApprovalMember = ReApprovalMember(
                approval_id = approvalId,
                approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
                member_id = approvalMember["member_id"],
                step = approvalMember["step"],
            )
            reApprovalMember.save()
        print("success create appropval members")

        for approvalRefMember in approvalRefMembers :
            reApprovalEtcMember = ReApprovalEtcMember(
                approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF"),
                approval_id = approvalId,
                member_id = approvalRefMember["member_id"],
            )
            reApprovalEtcMember.save()
        print("success create appropval ref members")

        for approvalRecvMember in approvalRecvMembers :
            reApprovalEtcMember = ReApprovalEtcMember(
                approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_RECV"),
                approval_id = approvalId,
                member_id = approvalRecvMember["member_id"],
            )
            reApprovalEtcMember.save()
        print("success create appropval recv members")

        reWorkingWeekendForm = ReWorkingWeekendForm(
            member_id = request.user.id,
            approval_id = approvalId,
            working_weekend_form_title = data["working_weekend_form_title"],
            working_weekend_form_state = approvalState,
            working_weekend_date = data["working_weekend_date"],
            working_weekend_start_datetime = data["working_weekend_start_datetime"],
            working_weekend_end_datetime = data["working_weekend_end_datetime"],
            working_weekend_time = data["working_weekend_time"],
            reason = data["reason"],
        )
        reWorkingWeekendForm.save()

        print("success create working weekend")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, approvalId

def sendMailWorkingWeekend(request, approvalId) :
    reWorkingWeekendForm = ReWorkingWeekendForm.objects.get(Q(approval_id = approvalId))
    approvalMember = ReApprovalMember.objects.filter(Q(approval_id = approvalId) & Q(step = 1)).get()
    approvalRefMembers = ReApprovalEtcMember.objects.filter(Q(approval_id = approvalId) & Q(approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF")))

    # 상신 메일
    receiverMemberIds = []
    receiverMemberIds.append(reWorkingWeekendForm.member_id)
    for approvalRefMember in approvalRefMembers :
        receiverMemberIds.append(approvalRefMember.member_id)

    emailTitle, emailContents = makeRequestMail("working_weekend", approvalId)
    sendMail(receiverMemberIds, emailTitle, emailContents)

    # 결재 메일
    receiverMemberIds = []
    receiverMemberIds.append(approvalMember.member_id) # 결재자
    emailTitle, emailContents = makeApprovalMail("working_weekend", approvalId)
    sendMail(receiverMemberIds, emailTitle, emailContents)

    print("success send mail working weekend")
    return True

def createWorkingWeekendNote(request) :
    data = json.loads(request.body)["data"]

    try :
        approvalState = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST")
        approvalMembers = data["approval_members"]
        approvalRefMembers = data["approval_ref_members"]
        approvalRecvMembers = data["approval_recv_members"]

        approvalId = makeApprovalId()

        reApproval = ReApproval(
            approval_id = approvalId,
            approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
            req_member_id = request.user.id,
            res_member_id = approvalMembers[0]["member_id"],
            step = approvalMembers[0]["step"],
            approval_state = approvalState,
        )
        reApproval.save()
        print("success create appropval")

        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = reApproval.approval_state,
        )
        reApprovalHistory.save()
        print("success create appropval history")

        for approvalMember in approvalMembers :
            reApprovalMember = ReApprovalMember(
                approval_id = approvalId,
                approval_type = Code().getCodeDtlNoByAlias("APPROVAL_TYPE_APPROVAL"),
                member_id = approvalMember["member_id"],
                step = approvalMember["step"],
            )
            reApprovalMember.save()
        print("success create appropval members")

        for approvalRefMember in approvalRefMembers :
            reApprovalEtcMember = ReApprovalEtcMember(
                approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF"),
                approval_id = approvalId,
                member_id = approvalRefMember["member_id"],
            )
            reApprovalEtcMember.save()
        print("success create appropval ref members")

        for approvalRecvMember in approvalRecvMembers :
            reApprovalEtcMember = ReApprovalEtcMember(
                approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_RECV"),
                approval_id = approvalId,
                member_id = approvalRecvMember["member_id"],
            )
            reApprovalEtcMember.save()
        print("success create appropval recv members")

        reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm(
            member_id = request.user.id,
            approval_id = approvalId,
            ref_approval_id = data["ref_approval_id"],
            working_weekend_note_form_title = data["working_weekend_note_form_title"],
            working_weekend_note_form_state = approvalState,
            working_weekend_date = data["working_weekend_date"],
            working_weekend_start_datetime = data["working_weekend_start_datetime"],
            working_weekend_end_datetime = data["working_weekend_end_datetime"],
            working_weekend_free_time = data["working_weekend_free_time"],
            working_project_name = data["working_project_name"],
            working_note = data["working_note"],
        )
        reWorkingWeekendNoteForm.save()

        print("success create working weekend note")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, approvalId

def sendMailWorkingWeekendNote(request, approvalId) :
    reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(Q(approval_id = approvalId))
    approvalMember = ReApprovalMember.objects.filter(Q(approval_id = approvalId) & Q(step = 1)).get()
    approvalRefMembers = ReApprovalEtcMember.objects.filter(Q(approval_id = approvalId) & Q(approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF")))

    # 상신 메일
    receiverMemberIds = []
    receiverMemberIds.append(reWorkingWeekendNoteForm.member_id)
    for approvalRefMember in approvalRefMembers :
        receiverMemberIds.append(approvalRefMember.member_id)

    emailTitle, emailContents = makeRequestMail("working_weekend_note", approvalId)
    sendMail(receiverMemberIds, emailTitle, emailContents)

    # 결재 메일
    receiverMemberIds = []
    receiverMemberIds.append(approvalMember.member_id) # 결재자
    emailTitle, emailContents = makeApprovalMail("working_weekend_note", approvalId)
    sendMail(receiverMemberIds, emailTitle, emailContents)

    print("success send mail working weekend note")
    return True

def createWorkingPart(request) :
    data = json.loads(request.body)["data"]

    try :
        reWorkingPart = ReWorkingPart(
            working_part_date = data["working_part_date"],
            member_id = request.user.id,
            working_part_projects = data["working_part_projects"],
        )
        reWorkingPart.save()
        print("success create working part")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def createWorkingCertificate(request) :
    data = json.loads(request.body)["data"]

    try :
        now = datetime.now().strftime("%Y%m%d")
        lastDocId = ReWorkingCertificate.objects.filter(Q(doc_id__contains=now)).last()

        numbering = "90001"
        if lastDocId is not None :
            numbering = "{:05d}".format(int(lastDocId.doc_id[12:]) + 1)

        docId = "vn_" + now + "_" + numbering

        reWorkingCertificate = ReWorkingCertificate(
            doc_id = docId,
            member_id = request.user.id,
            working_certificate_status = Code().getCodeDtlNoByAlias("WORKING_CERTIFICATE_STATUS_REQ"),
            is_blind = data["is_blind"],
            working_certificate_type = data["working_certificate_type"],
            working_certificate_date = data["working_certificate_date"],
            working_certificate_purpose = data["working_certificate_purpose"],
            working_certificate_destination = data["working_certificate_destination"],
            receive_date = data["receive_date"],
            receive_type = data["receive_type"],
            receive_email = data["receive_email"],
            join_date = data["join_date"],
            working_certificate_req_date = datetime.now().strftime("%Y-%m-%d"),
        )
        reWorkingCertificate.save()

        # 메일 발송
        reMember = getReMember(request.user.id)
        receiverEmail  = "boram@voronoi.io"

        emailTitle = "[증명서] 발급 알림"
        emailContents = "안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>"+ \
                        reMember.member_name + "님의 [증명서] 발급 요청 알림 입니다." + "<br>"+ \
                        "<a href='https://voronoi.app/re-working-admin/working-certificate-admin-view'>[증명서]</a> 에서 확인 가능합니다."+ \
                        "<br><br>감사합니다."

        email_service = gmail_authenticate()
        message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
        send_message(email_service, "me", message)
        print("success create working certificate")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def getShareWorkingMonthData(request) :
    memberId = request.user.id
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_share_working_month_data)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    query = query.replace('__WORKING_OFF_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))

    memberIds = getMemberIdsInGroup(memberId)
    query = query.replace('__MEMBER_IDS__', "AND member_id IN (" + ",".join(memberIds) + ") ")

    print(query)
    cur.execute(query)

    workings = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workings

def getShareWorkingOffs(request) :
    memberId = request.user.id
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_share_week_working_offs)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    query = query.replace('__WORKING_OFF_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))

    memberIds = getMemberIdsInGroup(memberId)
    query = query.replace('__MEMBER_IDS__', "AND a.member_id IN (" + ",".join(memberIds) + ") ")
    cur.execute(query)

    workingOffs = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingOffs

def getShareWorkingOuts(request) :
    memberId = request.user.id
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_share_week_working_outs)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)

    memberIds = getMemberIdsInGroup(memberId)
    query = query.replace('__MEMBER_IDS__', "AND a.member_id IN (" + ",".join(memberIds) + ") ")

    cur.execute(query)
    workingOuts = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingOuts

def getWorkings(request) :
    memberId = request.user.id
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')
    return ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date__range = (startDate, endDate))).order_by('working_date').all()

def getWorking(request, workingDate) :
    memberId = request.user.id
    return ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = workingDate)).all()

def getWorkingOuts(request) :
    memberId = request.user.id
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')
    return ReWorkingOut.objects.filter(Q(check_discard = False) & Q(member_id = memberId) & Q(working_out_date__range = (startDate, endDate))).order_by('working_out_date').all()

def getWorkingOutForm(workingOutFormId) :
    return ReWorkingOutForm.objects.filter(Q(working_out_form_id = workingOutFormId)).get()

def getWorkingOffs(request) :
    memberId = request.user.id
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')
    return ReWorkingOff.objects.filter(Q(member_id = memberId) & Q(working_off_state__in=[Code().getCodeDtlNoByAlias("APPROVAL_REQUEST"), Code().getCodeDtlNoByAlias("APPROVAL_OK"), Code().getCodeDtlNoByAlias("APPROVAL_DONE")]) & Q(working_off_date__range = (startDate, endDate))).order_by('working_off_date').all()

def getWorkingOffForm(workingOffFormId) :
    return ReWorkingOffForm.objects.filter(Q(working_off_form_id = workingOffFormId)).values()[0]

def getWorkingOffForms(request) :
    memberId = request.user.id

    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_working_off_forms)
    query = query.replace('__MEMBER_ID__', str(memberId))
    query = query.replace('__START_DATE__', startDate)

    if endDate != '' :
        query = query.replace('__END_DATE__', "AND a.working_off_form_end_date <= '" + endDate + " '")
    else :
        query = query.replace('__END_DATE__', "")
    print(query)
    cur.execute(query)

    workingOffForms = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingOffForms

def getWorkingOffByWorkingOffFormId(workingOffFormId) :
    return ReWorkingOff.objects.filter(Q(working_off_form_id = workingOffFormId)).all()

def getPrevWorkingWeekendForms(request) :
    return ReWorkingWeekendForm.objects.filter(Q(member_id=request.user.id) & Q(working_weekend_form_state = Code().getCodeDtlNoByAlias("APPROVAL_DONE"))).order_by("-approval_id")

def getWorkingWeekendForm(workingWeekendFormId) :
    return ReWorkingWeekendForm.objects.filter(Q(working_weekend_form_id = workingWeekendFormId)).values()[0]

def getWorkingWeekendForms(request) :
    memberId = request.user.id

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_working_weekend_forms)
    query = query.replace('__MEMBER_ID__', str(memberId))

    print(query)
    cur.execute(query)

    workingWeekendForms = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingWeekendForms

def getWorkingWeekendNoteForm(workingWeekendNoteFormId) :
    return ReWorkingWeekendNoteForm.objects.filter(Q(working_weekend_note_form_id = workingWeekendNoteFormId)).values()[0]

def getWorkingWeekendNoteForms(request) :
    memberId = request.user.id

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_working_weekend_note_forms)
    query = query.replace('__MEMBER_ID__', str(memberId))

    print(query)
    cur.execute(query)

    workingWeekendForms = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingWeekendForms

def getWorkingApprovalRequest(request) :
    memberId = request.user.id

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_working_approval_request)
    query = query.replace('__APPROVAL_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_REQUEST"))
    query = query.replace('__MEMBER_ID__', str(memberId))

    cur.execute(query)

    workingApprovalRequest = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingApprovalRequest

def getWorkingApprovals(request) :
    memberId = request.user.id

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_working_approvals)
    query = query.replace('__APPROVAL_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_REQUEST"))
    query = query.replace('__MEMBER_ID__', str(memberId))

    cur.execute(query)

    workingApprovals = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingApprovals

def getWorkingApprovalEtcRefs(request) :
    memberId = request.user.id

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_working_approval_etc_refs)
    query = query.replace('__APPROVAL_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_REJECT"))
    query = query.replace('__APPROVAL_ETC_MEMBER_TYPE__', Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF"))
    query = query.replace('__MEMBER_ID__', str(memberId))

    cur.execute(query)

    workingApprovalEtcRefs = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingApprovalEtcRefs

def getWorkingApprovalEtcRecvs(request) :
    memberId = request.user.id

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_working_approval_etc_recvs)
    query = query.replace('__APPROVAL_STATE__', Code().getCodeDtlNoByAlias("APPROVAL_DONE"))
    query = query.replace('__APPROVAL_ETC_MEMBER_TYPE__', Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_RECV"))
    query = query.replace('__MEMBER_ID__', str(memberId))
    cur.execute(query)

    workingApprovalEtcRecvs = dictfetchall(cur)
    if cur != None :
        cur.close()

    return workingApprovalEtcRecvs

def getApprovalMembers(approvalId) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_approval_members)
    query = query.replace('__APPROVAL_ID__', approvalId)

    cur.execute(query)

    approvalMembers = dictfetchall(cur)
    if cur != None :
        cur.close()

    return approvalMembers

def getApprovalEtcMembers(approvalId) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_approval_etc_members)
    query = query.replace('__APPROVAL_ID__', approvalId)

    cur.execute(query)

    approvalEtcMembers = dictfetchall(cur)
    if cur != None :
        cur.close()

    return approvalEtcMembers

def getPrevApprovalMembers(request) :
    memberId = request.user.id
    reWorkingOffForm = ReWorkingOffForm.objects.filter(Q(member_id = memberId) & Q(working_off_form_state = Code().getCodeDtlNoByAlias("APPROVAL_DONE"))).order_by("-approval_id").first()

    approvalId = reWorkingOffForm.approval_id
    reApprovalMembers = getApprovalMembers(approvalId)
    reApprovalEtcMembers = getApprovalEtcMembers(approvalId)

    return reApprovalMembers, reApprovalEtcMembers

def getApprovalUploadFile(uploadFileId) :
    return ReApprovalUploadFile.objects.filter(Q(upload_file_id = uploadFileId)).first()

def getApprovalHistorys(approvalId) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_approval_historys)
    query = query.replace('__APPROVAL_ID__', approvalId)

    print(query)
    cur.execute(query)

    approvalHitorys= dictfetchall(cur)
    if cur != None :
        cur.close()

    return approvalHitorys

def getStepApprovalMembers(approvalId) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_step_approval_members)
    query = query.replace('__APPROVAL_ID__', approvalId)

    print(query)
    cur.execute(query)

    approvalMembers = dictfetchall(cur)
    if cur != None :
        cur.close()

    return approvalMembers

def getRecommendApprovalMembers(request) :
    memberId = request.user.id

    recommendApprovalMembers = []
    if isGroupLeader(memberId) :
        memberIds = getParentGroupLeader(memberId)
        recommendApprovalMembers = ReMember.objects.filter(Q(member_id__in = memberIds))
    else :
        memberIds = getGroupLeaderInMyGroup(memberId)
        recommendApprovalMembers = ReMember.objects.filter(Q(member_id__in = memberIds))

    return recommendApprovalMembers

def getRecommendApprovalRefMembers(request) :
    memberId = request.user.id

    recommendApprovalRefMembers = []
    if isGroupLeader(memberId) :
        memberIds = getGroupLeadersInMyParentGroup(memberId)
        recommendApprovalRefMembers = ReMember.objects.filter(Q(member_id__in = memberIds))
    else :
        memberIds = getMemberIdsInMyGroup(memberId)
        recommendApprovalRefMembers = ReMember.objects.filter(Q(member_id__in = memberIds))

    return recommendApprovalRefMembers

def getWorkingTime(request) :
    reWorkings = ReWorkingTime.objects.filter(Q(member_id = request.user.id))
    if len(reWorkings) > 0 :
        return model_to_dict(reWorkings.last())

    return ""

def getWorkingOffPromoteNum(request) :
    workingOffStartDate = request.GET.get('workingOffStartDate')

    reWorkingOffPromote = ReWorkingOffPromote.objects.filter(Q(member_id = request.user.id) & Q(working_off_start_date = workingOffStartDate)).last()

    workingOffPromoteNUm = 0
    if reWorkingOffPromote is not None :
        if reWorkingOffPromote.first_promote_status != '' and reWorkingOffPromote.first_promote_status != Code().getCodeDtlNoByAlias("WORKING_OFF_PROMOTE_STATUS_DONE") :
            workingOffPromoteNUm = 1
        if reWorkingOffPromote.second_promote_status != '' and reWorkingOffPromote.second_promote_status != Code().getCodeDtlNoByAlias("WORKING_OFF_PROMOTE_STATUS_DONE") :
            workingOffPromoteNUm = 2

    return workingOffPromoteNUm

def getWorkingOffPromote(request) :
    workingOffStartDate = request.GET.get('workingOffStartDate')
    return ReWorkingOffPromote.objects.filter(Q(member_id = request.user.id) & Q(working_off_start_date = workingOffStartDate)).last()

def getWorkingOffPromotePlans(request, workingOffPromoteId) :
    workingOffPromoteNum = request.GET.get('workingOffPromoteNum')
    return ReWorkingOffPromotePlan.objects.filter(Q(working_off_promote_id = workingOffPromoteId) & Q(working_off_promote_num = workingOffPromoteNum))

def getWorkingPart(request) :
    reWorkingPart = ReWorkingPart.objects.filter(Q(member_id = request.user.id)).order_by("-working_part_date").first()
    if reWorkingPart is None :
        return ""

    return model_to_dict(reWorkingPart)

def getProjects(request) :
    return Project_Project.objects.filter(Q(check_discard = False))

def getWorkingCertificates(request) :
    return ReWorkingCertificate.objects.filter(Q(member_id = request.user.id)).order_by("-doc_id")

def getWorkingOffYearlys(request) :
    return ReWorkingOffYearly.objects.filter(Q(member_id = request.user.id)).order_by("-since_years")

def getWorkingOffTeams(request) :
    memberId = request.user.id

    memberIds = getMemberIdsInReaderGroup(memberId)
    return ReMember.objects.filter(Q(check_discard = False) & Q(leave_date = None) & Q(member_id__in = memberIds))

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

def getHolidays(request) :
    startDate = request.GET.get('start_date')
    endDate = request.GET.get('end_date')

    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")

    return ReHoliday.objects.filter(Q(holiday_date__range=(startDate, endDate)))

def getApprovalUploadFiles(approvalId) :
    return ReApprovalUploadFile.objects.filter(Q(approval_id = approvalId))

def getApprovalRequestCount(memberId) :
    return ReApproval.objects.filter(Q(res_member_id = memberId) & Q(approval_state = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST"))).count()


def getChartData(request):
    memberId = request.user.id

    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')

    workingStartTime = []
    workingEndTime = []
    allWorkingStartTime = []
    allWorkingEndTime = []
    reWorkingStats = ReWorkingStat.objects.filter(Q(member_id = memberId) & Q(working_stat_date__range=(startDate, endDate)))
    for reWorkingStat in reWorkingStats :
        # 출근 시간
        mintue, sec = divmod(reWorkingStat.working_start_time, 60)
        hour, mintue = divmod(mintue, 60)
        workingStartTime.append((hour + (mintue * 0.01)))

        # 퇴근 시간
        mintue, sec = divmod(reWorkingStat.working_end_time, 60)
        hour, mintue = divmod(mintue, 60)
        workingEndTime.append((hour + (mintue * 0.01)))

    # 전체 출퇴근 시간
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_working.get_all_working_stats)
    query = query.replace('__START_DATE__', startDate).replace('__END_DATE__', endDate)
    print(query)
    cur.execute(query)

    allReWorkingStats = dictfetchall(cur)
    if cur != None :
        cur.close()

    for allReWorkingStat in allReWorkingStats :
        # 출근 시간
        mintue, sec = divmod(allReWorkingStat["working_start_time"], 60)
        hour, mintue = divmod(mintue, 60)
        allWorkingStartTime.append((hour + (mintue * 0.01)))

        # 퇴근 시간
        mintue, sec = divmod(allReWorkingStat["working_end_time"], 60)
        hour, mintue = divmod(mintue, 60)
        allWorkingEndTime.append((hour + (mintue * 0.01)))

    chartData = []
    chartData.append({'name': '나의 출근', 'data': workingStartTime})
    chartData.append({'name': '나의 퇴근', 'data': workingEndTime})
    chartData.append({'name': '전체 출근', 'data': allWorkingStartTime})
    chartData.append({'name': '전체 퇴근', 'data': allWorkingEndTime})

    return chartData

def updateWorkingOut(request, workingOutFormId) :
    data = json.loads(request.body)["data"]

    try :
        reWorkingOutForm = ReWorkingOutForm.objects.get(working_out_form_id = workingOutFormId)
        reWorkingOutForm.working_out_form_type = data["working_out_form_type"]
        reWorkingOutForm.working_out_form_start_date = data["working_out_form_start_date"]
        reWorkingOutForm.working_out_form_end_date = data["working_out_form_end_date"]
        reWorkingOutForm.save()

        ReWorkingOut.objects.filter(Q(working_out_form_id = workingOutFormId)).delete()

        working_out_type = data["working_out_form_type"]
        working_out_form_start_date = parse(data["working_out_form_start_date"])
        working_out_form_end_date = parse(data["working_out_form_end_date"])

        working_out_date = working_out_form_start_date
        while working_out_date <= working_out_form_end_date :
            reWorkingOut = ReWorkingOut(
                working_out_form_id = reWorkingOutForm.working_out_form_id,
                member_id = request.user.id,
                working_out_type = working_out_type,
                working_out_date = working_out_date.strftime("%Y-%m-%d"),
            )
            reWorkingOut.save()
            working_out_date = working_out_date + timedelta(days=1)

        print("success update working out")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateWorkingOffOk(request, workingOffFormId) :
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "승인함"

        workingOffState = Code().getCodeDtlNoByAlias("APPROVAL_OK")

        # 휴가 문서
        reWorkingOffForm = ReWorkingOffForm.objects.get(working_off_form_id = workingOffFormId)
        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingOffForm.approval_id))
        reApproval.comment = comment
        nextStep = reApproval.step + 1
        nextReApprovalMember = ReApprovalMember.objects.filter(Q(approval_id = reWorkingOffForm.approval_id) & Q(step = nextStep)).all()
        if len(nextReApprovalMember) > 0 :
            # 다음 결재자가 있을 경우
            reApprovalHistory = ReApprovalHistory(
                approval_id = reApproval.approval_id,
                req_member_id = reApproval.req_member_id,
                res_member_id = reApproval.res_member_id,
                step = reApproval.step,
                approval_state = workingOffState,
                comment = comment,
            )
            reApprovalHistory.save()

            workingOffState = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST")
            reApproval.req_member_id = request.user.id
            reApproval.res_member_id = nextReApprovalMember[0].member_id
            reApproval.step = nextStep
            reApproval.approval_state = workingOffState
            reApproval.save()

        else :
            # 다음 결재자가 없을 경우
            workingOffState = Code().getCodeDtlNoByAlias("APPROVAL_DONE")
            reApprovalHistory = ReApprovalHistory(
                approval_id = reApproval.approval_id,
                req_member_id = reApproval.req_member_id,
                res_member_id = reApproval.res_member_id,
                step = reApproval.step,
                approval_state = workingOffState,
                comment = comment,
            )
            reApprovalHistory.save()

            reApproval.approval_state = workingOffState
            reApproval.save()

            # 휴가 일수 처리
            if reWorkingOffForm.working_off_form_type == Code().getCodeDtlNoByAlias("WORKING_OFF_TYPE_PRIVATE") :
                # 연차
                reMember = ReMember.objects.get(member_id = reWorkingOffForm.member_id)
                workingOffDays = reMember.working_off_days + reMember.working_off_etc_days
                workingOffUseDays = reMember.working_off_use_days + reWorkingOffForm.working_off_form_use_num
                workingOffRemainDays = workingOffDays - workingOffUseDays

                reMember.working_off_use_days = workingOffUseDays
                reMember.working_off_remain_days = workingOffRemainDays
                reMember.save()
            elif reWorkingOffForm.working_off_form_type == Code().getCodeDtlNoByAlias("WORKING_OFF_TYPE_ADD") :
                # 대체휴가
                reMember = ReMember.objects.get(member_id = reWorkingOffForm.member_id)
                workingOffAddDays = reMember.working_off_add_days
                workingOffAddUseDays = reMember.working_off_add_use_days + reWorkingOffForm.working_off_form_use_num
                workingOffAddRemainDays = workingOffAddDays - workingOffAddUseDays

                reMember.working_off_add_use_days = workingOffAddUseDays
                reMember.working_off_add_remain_days = workingOffAddRemainDays
                reMember.save()

            # 휴가 문서
            reWorkingOffForm.working_off_form_state = workingOffState
            reWorkingOffForm.save()

            # 휴가
            reWorkingOffs = ReWorkingOff.objects.filter(Q(working_off_form_id = workingOffFormId)).all()
            for reWorkingOff in reWorkingOffs :
                reWorkingOff.working_off_state = workingOffState
                reWorkingOff.save()


        print("success update working off ok")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingOffForm.approval_id

def updateWorkingOffReject(request, workingOffFormId) :
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "반려함"

        workingOffState = Code().getCodeDtlNoByAlias("APPROVAL_REJECT")

        # 휴가 문서
        reWorkingOffForm = ReWorkingOffForm.objects.get(working_off_form_id = workingOffFormId)
        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingOffForm.approval_id))

        # 결재 히스토리
        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = workingOffState,
            comment = comment,
        )
        reApprovalHistory.save()

        reApproval.approval_state = workingOffState
        reApproval.comment = comment
        reApproval.save()

        # 휴가 문서
        reWorkingOffForm.working_off_form_state = workingOffState
        reWorkingOffForm.save()

        # 휴가
        reWorkingOffs = ReWorkingOff.objects.filter(Q(working_off_form_id = workingOffFormId)).all()
        for reWorkingOff in reWorkingOffs :
            reWorkingOff.working_off_state = workingOffState
            reWorkingOff.save()

        print("success update working off reject")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingOffForm.approval_id

def updateWorkingOffCancel(request, workingOffFormId) :
    workingOffState = Code().getCodeDtlNoByAlias("APPROVAL_CANCEL")
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "취소함"

        # 휴가 문서
        reWorkingOffForm = ReWorkingOffForm.objects.get(working_off_form_id = workingOffFormId)
        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingOffForm.working_off_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."


        # 결재 히스토리
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingOffForm.approval_id))

        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = workingOffState,
            comment = comment,
        )
        reApprovalHistory.save()

        # 결재
        reApproval.approval_state = workingOffState
        reApproval.comment = comment
        reApproval.save()

        # 휴가 문서
        reWorkingOffForm.working_off_form_state = workingOffState
        reWorkingOffForm.save()

        # 휴가
        reWorkingOffs = ReWorkingOff.objects.filter(Q(working_off_form_id = workingOffFormId)).all()
        for reWorkingOff in reWorkingOffs :
            reWorkingOff.working_off_state = workingOffState
            reWorkingOff.save()

        print("success update working off cancel")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingOffForm.approval_id

def updateWorkingWeekendOk(request, workingWeekendFormId) :
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "승인함"

        workingWeekendState = Code().getCodeDtlNoByAlias("APPROVAL_OK")
        # 휴일 근무 문서
        reWorkingWeekendForm = ReWorkingWeekendForm.objects.get(working_weekend_form_id = workingWeekendFormId)
        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingWeekendForm.approval_id))
        reApproval.comment = comment
        nextStep = reApproval.step + 1
        nextReApprovalMember = ReApprovalMember.objects.filter(Q(approval_id = reWorkingWeekendForm.approval_id) & Q(step = nextStep)).all()
        if len(nextReApprovalMember) > 0 :
            # 다음 결재자가 있을 경우
            reApprovalHistory = ReApprovalHistory(
                approval_id = reApproval.approval_id,
                req_member_id = reApproval.req_member_id,
                res_member_id = reApproval.res_member_id,
                step = reApproval.step,
                approval_state = workingWeekendState,
                comment = comment,
            )
            reApprovalHistory.save()

            workingWeekendState = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST")
            reApproval.req_member_id = request.user.id
            reApproval.res_member_id = nextReApprovalMember[0].member_id
            reApproval.step = nextStep
            reApproval.approval_state = workingWeekendState
            reApproval.save()

        else :
            # 다음 결재자가 없을 경우
            workingWeekendState = Code().getCodeDtlNoByAlias("APPROVAL_DONE")
            reApprovalHistory = ReApprovalHistory(
                approval_id = reApproval.approval_id,
                req_member_id = reApproval.req_member_id,
                res_member_id = reApproval.res_member_id,
                step = reApproval.step,
                approval_state = workingWeekendState,
                comment = comment,
            )
            reApprovalHistory.save()

            reApproval.approval_state = workingWeekendState
            reApproval.save()

        # 휴일근무 문서
        reWorkingWeekendForm.working_weekend_form_state = workingWeekendState
        reWorkingWeekendForm.save()

        print("success update working weekend ok")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingWeekendForm.approval_id

def updateWorkingWeekendReject(request, workingWeekendFormId) :
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "반려함"

        workingWeekendState = Code().getCodeDtlNoByAlias("APPROVAL_REJECT")

        # 휴일 근무 문서
        reWorkingWeekendForm = ReWorkingWeekendForm.objects.get(working_weekend_form_id = workingWeekendFormId)
        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingWeekendForm.approval_id))

        # 결재 히스토리
        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = workingWeekendState,
            comment = comment,
        )
        reApprovalHistory.save()

        reApproval.approval_state = workingWeekendState
        reApproval.comment = comment
        reApproval.save()

        # 휴일 근무 일지 문서
        reWorkingWeekendForm.working_weekend_form_state = workingWeekendState
        reWorkingWeekendForm.save()

        print("success update working weekend reject")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingWeekendForm.approval_id


def updateWorkingWeekendCancel(request, workingWeekendFormId) :
    workingWeekendState = Code().getCodeDtlNoByAlias("APPROVAL_CANCEL")
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "취소함"

        # 휴일 근무 문서
        reWorkingWeekendForm = ReWorkingWeekendForm.objects.get(working_weekend_form_id = workingWeekendFormId)
        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingWeekendForm.working_weekend_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingWeekendForm.approval_id))

        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = workingWeekendState,
            comment = comment,
        )
        reApprovalHistory.save()

        # 결재 히스토리
        reApproval.approval_state = workingWeekendState
        reApproval.comment = comment
        reApproval.save()

        # 휴일 근무 문서
        reWorkingWeekendForm.working_weekend_form_state = workingWeekendState
        reWorkingWeekendForm.save()

        print("success update working weekend cancel")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingWeekendForm.approval_id

def updateWorkingWeekendNoteOk(request, workingWeekendNoteFormId) :
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "승인함"

        workingWeekendNoteState = Code().getCodeDtlNoByAlias("APPROVAL_OK")

        # 휴일 근무 일지 문서
        reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(working_weekend_note_form_id = workingWeekendNoteFormId)
        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingWeekendNoteForm.approval_id))
        reApproval.comment = comment
        nextStep = reApproval.step + 1
        nextReApprovalMember = ReApprovalMember.objects.filter(Q(approval_id = reWorkingWeekendNoteForm.approval_id) & Q(step = nextStep)).all()
        if len(nextReApprovalMember) > 0 :
            # 다음 결재자가 있을 경우
            reApprovalHistory = ReApprovalHistory(
                approval_id = reApproval.approval_id,
                req_member_id = reApproval.req_member_id,
                res_member_id = reApproval.res_member_id,
                step = reApproval.step,
                approval_state = workingWeekendNoteState,
                comment = comment,
            )
            reApprovalHistory.save()

            workingWeekendNoteState = Code().getCodeDtlNoByAlias("APPROVAL_REQUEST")
            reApproval.req_member_id = request.user.id
            reApproval.res_member_id = nextReApprovalMember[0].member_id
            reApproval.step = nextStep
            reApproval.approval_state = workingWeekendNoteState
            reApproval.save()

        else :
            # 다음 결재자가 없을 경우
            workingWeekendNoteState = Code().getCodeDtlNoByAlias("APPROVAL_DONE")
            reApprovalHistory = ReApprovalHistory(
                approval_id = reApproval.approval_id,
                req_member_id = reApproval.req_member_id,
                res_member_id = reApproval.res_member_id,
                step = reApproval.step,
                approval_state = workingWeekendNoteState,
                comment = comment,
            )
            reApprovalHistory.save()

            reApproval.approval_state = workingWeekendNoteState
            reApproval.save()

        # 휴가 문서
        reWorkingWeekendNoteForm.working_weekend_note_form_state = workingWeekendNoteState
        reWorkingWeekendNoteForm.save()

        print("success update working weekend ok")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingWeekendNoteForm.approval_id

def updateWorkingWeekendNoteReject(request, workingWeekendNoteFormId) :
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "반려함"

        workingWeekendNoteState = Code().getCodeDtlNoByAlias("APPROVAL_REJECT")

        # 휴일 근무 문서
        reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(working_weekend_note_form_id = workingWeekendNoteFormId)
        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingWeekendNoteForm.approval_id))

        # 결재 히스토리
        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = workingWeekendNoteState,
            comment = comment,
        )
        reApprovalHistory.save()

        reApproval.approval_state = workingWeekendNoteState
        reApproval.comment = comment
        reApproval.save()

        # 휴일 근무 문서
        reWorkingWeekendNoteForm.working_weekend_note_form_state = workingWeekendNoteState
        reWorkingWeekendNoteForm.save()

        print("success update working weekend reject")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingWeekendNoteForm.approval_id

def updateWorkingWeekendNoteCancel(request, workingWeekendNoteFormId) :
    workingWeekendNoteState = Code().getCodeDtlNoByAlias("APPROVAL_CANCEL")
    try :
        data = json.loads(request.body)["data"]
        comment = data["comment"]
        if comment == "" :
            comment = "취소함"

        # 휴일 근무 일지 문서
        reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(working_weekend_note_form_id = workingWeekendNoteFormId)
        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_REJECT") :
            return False, "이미 반려 처리 되었습니다."

        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_CANCEL") :
            return False, "이미 취소 처리 되었습니다."

        if reWorkingWeekendNoteForm.working_weekend_note_form_state == Code().getCodeDtlNoByAlias("APPROVAL_DONE") :
            return False, "이미 승인 완료 처리 되었습니다."

        # 결재
        reApproval = ReApproval.objects.get(Q(approval_id = reWorkingWeekendNoteForm.approval_id))

        reApprovalHistory = ReApprovalHistory(
            approval_id = reApproval.approval_id,
            req_member_id = reApproval.req_member_id,
            res_member_id = reApproval.res_member_id,
            step = reApproval.step,
            approval_state = workingWeekendNoteState,
            comment = comment,
        )
        reApprovalHistory.save()

        # 결재 히스토리
        reApproval.approval_state = workingWeekendNoteState
        reApproval.comment = comment
        reApproval.save()

        # 휴일 근무 문서
        reWorkingWeekendNoteForm.working_weekend_note_form_state = workingWeekendNoteState
        reWorkingWeekendNoteForm.save()

        print("success update working weekend note cancel")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, reWorkingWeekendNoteForm.approval_id

def sendMailWorkingOk(request, formType, approvalId) :
    if formType == "working_off" :
        reWorkingOffForm = ReWorkingOffForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingOffForm.member_id

    elif formType == "working_weekend" :
        reWorkingWeekendForm = ReWorkingWeekendForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingWeekendForm.member_id

    elif formType == "working_weekend_note" :
        reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingWeekendNoteForm.member_id

    reApprovalHistory = ReApprovalHistory.objects.filter(Q(approval_id = approvalId)).last()

    nextStep = reApprovalHistory.step + 1
    nextReApprovalMembers = ReApprovalMember.objects.filter(Q(approval_id = approvalId) & Q(step = nextStep))

    if len(nextReApprovalMembers) > 0 :
        nextMemberId = nextReApprovalMembers[0].member_id

        # 진행 알림메일 (상신자)
        emailTitle, emailContents = makeNotifyMail(formType, approvalId)

        receiverMemberIds = []
        receiverMemberIds.append(memberId)
        sendMail(receiverMemberIds, emailTitle, emailContents)

        # 다음 결재자가 있을 경우 결재 요청 메일 (다음 결재자)
        emailTitle, emailContents = makeApprovalMail(formType, approvalId)

        receiverMemberIds = []
        receiverMemberIds.append(nextMemberId)
        sendMail(receiverMemberIds, emailTitle, emailContents)
    else :
        # 다음 결재자가 없을 경우 결재 완료 메일 (모두)
        emailTitle, emailContents = makeApprovalDoneMail(formType, approvalId)

        receiverMemberIds = []
        receiverMemberIds.append(memberId)
        approvalMembers = ReApprovalMember.objects.filter(Q(approval_id = approvalId))
        for approvalMember in approvalMembers :
            receiverMemberIds.append(approvalMember.member_id)

        approvalEtcMembers = ReApprovalEtcMember.objects.filter(Q(approval_id = approvalId))
        for approvalEtcMember in approvalEtcMembers :
            receiverMemberIds.append(approvalEtcMember.member_id)

        sendMail(receiverMemberIds, emailTitle, emailContents)

    print("success send mail working ok " + formType)
    return True


def sendMailWorkingReject(request, formType, approvalId) :
    if formType == "working_off" :
        reWorkingOffForm = ReWorkingOffForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingOffForm.member_id

    elif formType == "working_weekend" :
        reWorkingWeekendForm = ReWorkingWeekendForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingWeekendForm.member_id

    elif formType == "working_weekend_note" :
        reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingWeekendNoteForm.member_id

    approvalRefMembers = ReApprovalEtcMember.objects.filter(Q(approval_id = approvalId) & Q(approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF")))

    emailTitle, emailContents = makeApprovalRejectMail(formType, approvalId)

    receiverMemberIds = []
    # 상신자
    receiverMemberIds.append(memberId)

    # 현재 & 이전 결재자
    reApprovalHistory = ReApprovalHistory.objects.filter(Q(approval_id = approvalId)).last()
    prevReApprovalMembers = ReApprovalMember.objects.filter(Q(approval_id = approvalId) & Q(step__lte = reApprovalHistory.step))
    for prevReApprovalMember in prevReApprovalMembers :
        receiverMemberIds.append(prevReApprovalMember.member_id)

    # 참조자
    for approvalRefMember in approvalRefMembers :
        receiverMemberIds.append(approvalRefMember.member_id)

    sendMail(receiverMemberIds, emailTitle, emailContents)

    print("success send mail working reject " + formType)
    return True

def sendMailWorkingCancel(request, formType, approvalId) :
    if formType == "working_off" :
        reWorkingOffForm = ReWorkingOffForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingOffForm.member_id
        formTitle = reWorkingOffForm.working_off_form_title

    elif formType == "working_weekend" :
        reWorkingWeekendForm = ReWorkingWeekendForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingWeekendForm.member_id
        formTitle = reWorkingWeekendForm.working_weekend_form_title

    elif formType == "working_weekend_note" :
        reWorkingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(Q(approval_id = approvalId))
        memberId = reWorkingWeekendNoteForm.member_id
        formTitle = reWorkingWeekendNoteForm.working_weekend_note_form_title

    approvalRefMembers = ReApprovalEtcMember.objects.filter(Q(approval_id = approvalId) & Q(approval_etc_member_type = Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF")))
    reApprovalHistory = ReApprovalHistory.objects.filter(Q(approval_id = approvalId)).last()

    emailTitle, emailContents = makeApprovalCancelMail(memberId, formTitle, reApprovalHistory.comment)

    receiverMemberIds = []
    # 상신자
    receiverMemberIds.append(memberId)

    # 현재 & 이전 결재자

    prevReApprovalMembers = ReApprovalMember.objects.filter(Q(approval_id = approvalId) & Q(step__lte = reApprovalHistory.step))
    for prevReApprovalMember in prevReApprovalMembers :
        receiverMemberIds.append(prevReApprovalMember.member_id)

    # 참조자
    for approvalRefMember in approvalRefMembers :
        receiverMemberIds.append(approvalRefMember.member_id)

    sendMail(receiverMemberIds, emailTitle, emailContents)

    print("success send mail working cancel " + formType)
    return True

def updateWorkingOffPromoteDone(request, workingOffPromoteId) :
    try :
        data = json.loads(request.body)["data"]

        workingOffPromoteNum = data["workingOffPromoteNum"]
        reWorkingOffPromote = ReWorkingOffPromote.objects.get(working_off_promote_id = workingOffPromoteId)
        reMember = getReMember(reWorkingOffPromote.member_id)
        if workingOffPromoteNum == 1 :
            reWorkingOffPromote.first_promote_status = Code().getCodeDtlNoByAlias("WORKING_OFF_PROMOTE_STATUS_DONE")
            reWorkingOffPromote.first_promote_submit_datetime = datetime.now()
            reWorkingOffPromote.first_working_off_days = reMember.working_off_days + reMember.working_off_etc_days
            reWorkingOffPromote.first_working_off_use_days = reMember.working_off_use_days
            reWorkingOffPromote.first_working_off_remain_days = reMember.working_off_remain_days
        elif workingOffPromoteNum == 2 :
            reWorkingOffPromote.second_promote_status = Code().getCodeDtlNoByAlias("WORKING_OFF_PROMOTE_STATUS_DONE")
            reWorkingOffPromote.second_promote_submit_datetime = datetime.now()
            reWorkingOffPromote.second_working_off_days = reMember.working_off_days + reMember.working_off_etc_days
            reWorkingOffPromote.second_working_off_use_days = reMember.working_off_use_days
            reWorkingOffPromote.second_working_off_remain_days = reMember.working_off_remain_days
        reWorkingOffPromote.save()

        ReWorkingOffPromotePlan.objects.filter(Q(working_off_promote_id = workingOffPromoteId) & Q(working_off_promote_num = workingOffPromoteNum)).delete()

        workingOffPromotePlans = data["workingOffPromotePlans"]
        for workingOffPromotePlan in workingOffPromotePlans :
            reWorkingOffPromotePlan = ReWorkingOffPromotePlan(
                working_off_promote_id = workingOffPromoteId,
                member_id = request.user.id,
                working_off_promote_num = workingOffPromoteNum,
                working_off_start_date = workingOffPromotePlan["working_off_start_date"],
                working_off_end_date = workingOffPromotePlan["working_off_end_date"],
                working_off_use_num = workingOffPromotePlan["working_off_use_num"],
            )
            reWorkingOffPromotePlan.save()

        print("success update working weekend ok")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True

def updateWorkingPart(request, workingPartId) :
    data = json.loads(request.body)["data"]
    try :
        reWorkingPart = ReWorkingPart.objects.get(working_part_id = workingPartId)
        reWorkingPart.working_part_projects = data["working_part_projects"]
        reWorkingPart.save()
        print("success update working part")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def workingStart(request) :
    if checkOpenDomain(request) :
        return True

    memberId = request.user.id
    workingDate = datetime.now().strftime("%Y-%m-%d")
    reWorking = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = workingDate)).all()
    if len(reWorking) == 0 :
        try :
            workingTime = getDateWorkingTime(memberId, workingDate)
            reWorking = ReWorking(
                member_id = memberId,
                working_date = datetime.now().strftime("%Y-%m-%d"),
                working_start_datetime = workingTime[0],
                working_end_datetime = workingTime[1],
                working_start_check_datetime = datetime.now(),
                working_start_check_ori_datetime = datetime.now(),
            )
            reWorking.save()
            print("success working start")
        except Exception as e :
            print("Exception::", e)
            return False, e
    else :
        working = reWorking.last()
        working.working_start_check_datetime = datetime.now()
        working.working_start_check_ori_datetime = datetime.now()
        ReWorking.save(working)

    return True, "success"

def workginEnd(request, memberId) :
    if checkOpenDomain(request) :
        return True, "success"

    try :
        # 근무 체크 안함
        reMember = ReMember.objects.get(member_id = memberId)
        if reMember.check_working is False :
            return True, "success"

        # 새벽 시간 퇴근 처리(00시 ~ 04시 전까지)
        workingStartLimitTime = int(datetime.now().strftime("%H"))
        if 0 <= workingStartLimitTime and workingStartLimitTime <= 4 :
            workingDate = (datetime.now() + timedelta(days=-1))
        else :
            workingDate = datetime.now()

        reWorking = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = workingDate.strftime("%Y-%m-%d"))).last()
        reWorking.working_end_check_datetime = datetime.now()
        reWorking.working_end_check_ori_datetime = datetime.now()
        reWorking.save()
        print("success working end")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def changeWorkingTime(request) :
    if checkOpenDomain(request) :
        return True, "success"

    memberId = request.user.id

    data = json.loads(request.body)["data"]

    workingStartChangeDatetime = None
    if data["working_start_change_datetime"] != '' :
        workingStartChangeDatetime = datetime.strptime(data["working_start_change_datetime"], "%Y-%m-%d %H:%M")

    workingEndChangeDatetime = None
    if data["working_end_change_datetime"] != '' :
        workingEndChangeDatetime = datetime.strptime(data["working_end_change_datetime"], "%Y-%m-%d %H:%M")

    workingTimeChangeReason = data["working_time_change_reason"]

    workingDate = data["working_date"]
    reWorkings = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = workingDate)).all()
    try :
        if len(reWorkings) == 0 :
            workingTime = getDateWorkingTime(memberId, workingDate)

            reWorking = ReWorking(
                member_id = memberId,
                working_date = workingDate,
                working_start_datetime = workingTime[0],
                working_end_datetime = workingTime[1],
                working_start_change_datetime = workingStartChangeDatetime,
                working_end_change_datetime = workingEndChangeDatetime,
                working_time_change_reason = workingTimeChangeReason,
                is_working_time_change = "Y",
            )
            reWorking.save()
        else :
            reWorking = reWorkings.first()
            reWorking.working_start_change_datetime = workingStartChangeDatetime
            reWorking.working_end_change_datetime = workingEndChangeDatetime
            reWorking.working_time_change_reason = workingTimeChangeReason
            reWorking.is_working_time_change = "Y"
            reWorking.save()

        print("success change working time")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"


def checkWorkingStart(request) :
    if checkOpenDomain(request) :
        return True, "success"

    memberId = request.user.id

    # 근무 체크 안함
    reMember = ReMember.objects.get(member_id = memberId)
    if reMember.check_working is False :
        return True

    isWorkingStart = True
    workingStartLimitTime = int(datetime.now().strftime("%H"))
    if 0 <= workingStartLimitTime and workingStartLimitTime <= 4 :
        # 0시 ~ 5시이전 출근 확인
        yeseterday = datetime.now() + timedelta(days=-1)
        reWorkings = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = yeseterday.strftime("%Y-%m-%d"))).all()

        if len(reWorkings) == 0 :
            # 근무가 없는 경우 출근 처리
            return False

        # 퇴근 하고 새벽 출근 인 경우
        if reWorkings.last().working_end_check_datetime is not None :
            reWorking = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = datetime.now().strftime("%Y-%m-%d"))).all()
            if len(reWorking) == 0  :
                isWorkingStart = False
            else :
                if reWorking.last().working_start_check_datetime is None :
                    isWorkingStart = False
                else :
                    isWorkingStart = True
    else :
        reWorking = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = datetime.now().strftime("%Y-%m-%d"))).all()
        if len(reWorking) == 0  :
            isWorkingStart = False
        else :
            if reWorking.last().working_start_check_datetime is None :
                isWorkingStart = False
            else :
                isWorkingStart = True

    return isWorkingStart

def checkWorkingYesterday(request) :
    if checkOpenDomain(request) :
        return True, "success"

    memberId = request.user.id

    # 근무 체크 안함
    reMember = ReMember.objects.get(member_id = memberId)
    if reMember.check_working is False :
        return False, ""

    # 출퇴근 이력이 없는 경우 (신규입사자인 경우)
    if ReWorking.objects.filter(member_id = memberId).count() <= 1 :
        return False, ""

    workingStartLimitTime = int(datetime.now().strftime("%H"))
    if 0 <= workingStartLimitTime and workingStartLimitTime <= 4 :
        yeseterday = datetime.now() + timedelta(days=-2)
    else :
        yeseterday = datetime.now() + timedelta(days=-1)

    yesterdayStr = yeseterday.strftime("%Y-%m-%d")
    reWorkings = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = yesterdayStr)).all()
    if len(reWorkings) == 0 or (reWorkings.last().working_start_check_datetime is None and reWorkings.last().working_end_check_datetime is None) :
        # 출퇴근이 없는 경우

        isHolidays = False
        if ReHoliday.objects.filter(Q(holiday_date = yesterdayStr)).count() > 0 : # 공휴일
            isHolidays = True

        # 휴일
        if yeseterday.weekday() > 4 or isHolidays :
            # 휴일 근무 체크 (주말 or 휴일)
            if ReWorkingWeekendForm.objects.filter(Q(member_id = memberId, working_weekend_date = yeseterday, working_weekend_form_state = Code().getCodeDtlNoByAlias("APPROVAL_DONE"))).count() > 0 :
                return True, yesterdayStr

            if yeseterday.weekday() > 4 :
                # 평일로 근무 날짜로 변경
                if yeseterday.weekday() == 5 :
                    # 토요일
                    if 0 <= workingStartLimitTime and workingStartLimitTime <= 4 :
                        yeseterday = datetime.now() + timedelta(days = -3)
                    else :
                        yeseterday = datetime.now() + timedelta(days = -2)
                elif yeseterday.weekday() == 6 :
                    # 일요일
                    if 0 <= workingStartLimitTime and workingStartLimitTime <= 4 :
                        yeseterday = datetime.now() + timedelta(days = -4)
                    else :
                        yeseterday = datetime.now() + timedelta(days = -3)

                yesterdayStr = yeseterday.strftime("%Y-%m-%d")
                reWorkings = ReWorking.objects.filter(Q(member_id = memberId) & Q(working_date = yesterdayStr)).all()

                # 공휴일 체크
                if ReHoliday.objects.filter(Q(holiday_date = yesterdayStr)).count() > 0 : # 공휴일
                    isHolidays = True

        # 평일
        # 공휴일인 경우
        if isHolidays :
            return False, yesterdayStr

        # 외부근무
        if ReWorkingOut.objects.filter(Q(member_id = memberId) & Q(working_out_date = yesterdayStr)).count() > 0 :
            return False, yesterdayStr

        if len(reWorkings) == 0 or (reWorkings.last().working_start_check_datetime is None and reWorkings.last().working_end_check_datetime is None) :
            # 휴가체크
            reWorkingOffs = ReWorkingOff.objects.filter(Q(member_id = memberId, working_off_date = yesterdayStr, working_off_state = Code().getCodeDtlNoByAlias("APPROVAL_DONE")))
            if len(reWorkingOffs) > 0 :
                workingOffUseDay = 0
                for reWorkingOff in reWorkingOffs :
                    if reWorkingOff.working_off_time == Code().getCodeDtlNoByAlias("WORKING_OFF_TIME_DAY") :
                        workingOffUseDay += 1
                    elif reWorkingOff.working_off_time == Code().getCodeDtlNoByAlias("WORKING_OFF_TIME_AM") :
                        workingOffUseDay += 0.5
                    elif reWorkingOff.working_off_time == Code().getCodeDtlNoByAlias("WORKING_OFF_TIME_PM") :
                        workingOffUseDay += 0.5
                    elif reWorkingOff.working_off_time == Code().getCodeDtlNoByAlias("WORKING_OFF_TIME_TIME") :
                        workingOffUseDay += 0.25

                if workingOffUseDay >= 1 :
                    return False, yesterdayStr
                else :
                    # 반차, 반반차인 경우 출퇴근 확인
                    return True, yesterdayStr
            else :
                if len(reWorkings) > 0 :
                    # 누락 수정  요청 중인 경우
                    reWorking = reWorkings.last()
                    if reWorking.is_working_time_change == "Y" :
                        return False, yesterdayStr

                return True, yesterdayStr
        else :
            reWorking = reWorkings.last()
            # 누락 수정  요청 중인 경우
            if reWorking.is_working_time_change == "Y" :
                return False, yesterdayStr

            if reWorking.working_start_check_datetime is None or reWorking.working_end_check_datetime is None or reWorking.working_start_check_datetime == "" or reWorking.working_end_check_datetime == "" :
                return True, yesterdayStr
    else :
        reWorking = reWorkings.last()
        # 누락 수정  요청 중인 경우
        if reWorking.is_working_time_change == "Y" :
           return False, yesterdayStr

        if reWorking.working_start_check_datetime is None or reWorking.working_end_check_datetime is None or reWorking.working_start_check_datetime == "" or reWorking.working_end_check_datetime == "" :
            return True, yesterdayStr


    return False, yesterdayStr

def checkWorkingPart(request) :
    today = datetime.now()
    dt = datetime.now().replace(day=1)
    beforeDay = dt - timedelta(days=6)
    afterDay = dt + timedelta(days=5)

    if afterDay < today :
        dt = datetime.now().replace(day=1) + relativedelta(months=1)
        beforeDay = dt - timedelta(days=6)
        afterDay = dt + timedelta(days=5)

    if beforeDay < today and today < afterDay :
        workingPartDate = beforeDay.strftime("%Y-%m")
        if ReWorkingPart.objects.filter(Q(member_id = request.user.id) & Q(working_part_date = workingPartDate)).count() > 0 :
            return False, True

        return True, workingPartDate

    return False, ""

def uploadFile(request, approvalId) :
    for i in range(len(request.FILES)) :
        file = request.FILES["files_" + str(i)]
        ext = os.path.splitext(file.name)[1:]
        try :
            uploadFileId = str(round(time.time() * 1000)) # 파일명 생성
            default_storage.save("re-approval/" + uploadFileId, file)

            reApprovalUploadFile = ReApprovalUploadFile(
                upload_file_id = uploadFileId,
                approval_id = approvalId,
                upload_file_ext = ext[0].replace(".", ""),
                upload_file_name = file,
            )
            reApprovalUploadFile.save()
            print("success upload member file")
        except Exception as e :
            print("Exception::", e)
            return False, e

    return True

def deleteWorkingOut(workingOutFormId) :
    try :
        reWorkingOutForm = ReWorkingOutForm.objects.get(Q(working_out_form_id = workingOutFormId))
        reWorkingOutForm.check_discard = True
        reWorkingOutForm.save()

        ReWorkingOut.objects.filter(Q(working_out_form_id = workingOutFormId)).update(check_discard = True)
        print("success delete working out")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def makeRequestMail(formType, approvalId) :
    emailTitle = """[[title]] 상신 알림"""
    emailContents = """안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>[member_name] 님의 [[title]] 상신 되었습니다.<br><br>"""
    return makeMailTemplate(formType, approvalId, emailTitle, emailContents)

def makeApprovalMail(formType,  approvalId) :
    emailTitle = """[[title]] 결재 요청"""
    emailContents = """안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>
                        [member_name] 님의 [[title]] 결재 요청 입니다.<br><br>
                        <a href='https://voronoi.app/re-working/working-approval-view'>[휴가·휴일 승인]</a>에서 확인 가능합니다.<br><br>
                        <a href='https://my.voronoi.app/re-working/working-approval-view'>[외부접속링크: 휴가.휴일 승인]</a><br><br>"""
    return makeMailTemplate(formType, approvalId, emailTitle, emailContents)

def makeNotifyMail(formType, approvalId) :
    emailTitle = """[[title]] 진행사항 알림"""
    emailContents = """안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>
                        [member_name] 님의 [[title]] 진행 알림 입니다.<br><br>"""
    return makeMailTemplate(formType, approvalId, emailTitle, emailContents)

def makeApprovalDoneMail(formType, approvalId) :
    emailTitle = """[[title]] 완결 문서"""
    emailContents = """안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>
                        [member_name] 님의 [[title]] 결재 완료 입니다.<br><br>"""
    return makeMailTemplate(formType, approvalId, emailTitle, emailContents, isDone = True)

def makeApprovalRejectMail(formType, approvalId) :
    emailTitle = """[[title]] 반려 알림"""
    emailContents = """안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>
                        [member_name] 님의 [[title]] 반려 알림 입니다.<br><br>"""
    return makeMailTemplate(formType, approvalId, emailTitle, emailContents)

def makeApprovalCancelMail(memberId, title, comment) :
    reqReMember = getReMember(memberId)

    emailTitle = "[" + title + "] 상신 취소 알림"

    emailContents = "안녕하세요.<br>VORONOI GROUPWARE에서 알립니다.<br><br>"+ \
                    reqReMember.member_name + "님의 [" + title + "] 상신 취소 알림 입니다.<br><br>" + \
                    "상신자 " + reqReMember.member_name + "님이 결재 상신을 취소 하였습니다.<br><br>" + \
                    "(취소 사유: " + comment + ")" + \
                    "<br><br>감사합니다."

    return emailTitle, emailContents

def makeMailTemplate(formType, approvalId, emailTitle, emailContents, isDone = False) :
    if formType == 'working_off' :
        workingOffForm = ReWorkingOffForm.objects.get(Q(approval_id = approvalId))
        workingOffs = getWorkingOffByWorkingOffFormId(workingOffForm.working_off_form_id)

        title = workingOffForm.working_off_form_title
        memberId = workingOffForm.member_id
        workingOffFormUseNum = workingOffForm.working_off_form_use_num
        formDatetime = workingOffForm.working_off_form_datetime.strftime("%Y-%m-%d %H:%M:%S")

    elif formType == 'working_weekend' :
        workingWeekendForm = ReWorkingWeekendForm.objects.get(Q(approval_id = approvalId))

        title = workingWeekendForm.working_weekend_form_title
        memberId = workingWeekendForm.member_id
        formDatetime = workingWeekendForm.working_weekend_form_datetime.strftime("%Y-%m-%d %H:%M:%S")
    elif formType == 'working_weekend_note' :
        workingWeekendNoteForm = ReWorkingWeekendNoteForm.objects.get(Q(approval_id = approvalId))

        title = workingWeekendNoteForm.working_weekend_note_form_title
        memberId = workingWeekendNoteForm.member_id
        formDatetime = workingWeekendNoteForm.working_weekend_note_form_datetime.strftime("%Y-%m-%d %H:%M:%S")

    member = getMember(memberId)
    approvalMembers = getApprovalMembers(approvalId)
    approvalEtcMembers = getApprovalEtcMembers(approvalId)
    approvalHistorys = getApprovalHistorys(approvalId)

    # 제목
    emailTitle = emailTitle.replace("[title]",  title)
    emailContents = emailContents.replace("[member_name]", member["member_name"]).replace("[title]", title)

    # 기본 정보
    emailContents += mailTemplate()
    emailContents = emailContents.replace("[member_name]", member["member_name"])
    emailContents = emailContents.replace("[group_name]", member["group_name"])
    emailContents = emailContents.replace("[member_email]", member["member_email"])

    # 양식 내용
    emailContents = emailContents.replace("[form_title]", title)

    workingOffDays = ""
    workingOffDate = ""
    if formType == 'working_off' :
        # 휴가 일
        workingOffFormDate = workingOffForm.working_off_form_start_date + " ~ " + workingOffForm.working_off_form_end_date

        # 내용
        formContents = """
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">상신자</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{} ({})</td>
        </tr>
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">구분</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">요청 사유</th>
            <td colspan="2" style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴가 일</th>
            <td colspan="2" style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        """.format(member["member_name"], member["group_name"], Code().getCodeDtlNm(workingOffForm.working_off_form_type), workingOffForm.reason, workingOffFormDate)
        emailContents = emailContents.replace("[form_contents]", formContents)

        if isDone == False :
            # 휴가 일수

            # 연차 사용 기간
            from datetime import datetime
            workingOffStartDate = member["working_off_start_date"]
            workingOffStartDatetime = datetime.strptime(workingOffStartDate, "%Y-%m-%d")
            workingOffPeriod = workingOffStartDate  + " ~ " + (workingOffStartDatetime + relativedelta(years=1) - relativedelta(days=1)).strftime("%Y-%m-%d")

            workingOffDays = """
            <tr>
                <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">전체일수</th>
                <td style="border: 1px solid #ccc; padding: 8px;">{}</td>
            </tr>
            <tr>
                <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">사용일수</th>
                <td style="border: 1px solid #ccc; padding: 8px;">{} (결재중: {})</td>
            </tr>
            <tr>
                <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">승인 후 잔여일 수</th>
                <td style="border: 1px solid #ccc; padding: 8px;">{}</td>
            </tr>
            <tr>
                <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">연차 사용 기간</th>
                <td style="border: 1px solid #ccc; padding: 8px;">{}</td>
            </tr>
            """.format(member["working_off_days"] + member["working_off_etc_days"], member["working_off_use_days"], workingOffFormUseNum, (member["working_off_days"] + member["working_off_etc_days"] - member["working_off_use_days"]) - workingOffFormUseNum, workingOffPeriod)

        # 휴가 내역
        if len(workingOffs) > 0 :
            workingOffStr = ""
            for workingOff in workingOffs :
                workingOffStr += """
                <tr>
                    <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
                    <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
                    <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
                </tr>
                """.format(workingOff.working_off_date,
                        Code().getCodeDtlNm(workingOff.working_off_time),
                        workingOff.working_off_start_datetime.strftime("%H:%M") + " ~ " + workingOff.working_off_end_datetime.strftime("%H:%M"))

            workingOffDate = """
                <tr>
                    <td colspan="3">
                        <div>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <th colspan="3" style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴가기간</th>
                                </tr>
                                <tr>
                                    <th style="width: 30%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">기간</th>
                                    <th style="width: 30%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">시간 타입</th>
                                    <th style="width: 40%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">시간</th>
                                </tr>
                                {}
                            </table>
                        </div>
                    </td>
                </tr>
                """.format(workingOffStr)
    elif formType == "working_weekend" :
        startTime = workingWeekendForm.working_weekend_start_datetime
        endTime = workingWeekendForm.working_weekend_end_datetime
        workingTime = workingWeekendForm.working_weekend_time

        timeArr = ["0"]
        if workingTime  is not None :
            timeArr = workingTime.split(":")

        workingWeekendTime = startTime.strftime("%H:%M") + " 부터 " +  endTime.strftime("%H:%M") + " 동안 " + str(int(timeArr[0])) + "시간 근무"

        # 내용
        formContents = """
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴일 근무일</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴일 근무 시간</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴일 근무 사유</th>
            <td colspan="2" style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        """.format(workingWeekendForm.working_weekend_date, workingWeekendTime, workingWeekendForm.reason)
        emailContents = emailContents.replace("[form_contents]", formContents)

    elif formType == "working_weekend_note" :
        startTime = workingWeekendNoteForm.working_weekend_start_datetime
        endTime = workingWeekendNoteForm.working_weekend_end_datetime
        freeTime = workingWeekendNoteForm.working_weekend_free_time

        # 휴일 근무 시간
        durationTime = divmod((endTime - startTime).seconds, 60)
        workingWeekendTime = startTime.strftime("%H:%M") + " 부터 " +  endTime.strftime("%H:%M") + " / " + str(int(durationTime[0] / 60)) + " 시간 " + str(durationTime[0] % 60) + "분 근무"

        # 휴일 휴게 시간
        workingWeekendFreeTime = ""
        if freeTime is not None and freeTime != '' :
            freeTimeArr = freeTime.split(":")
            workingWeekendFreeTime = freeTimeArr[0] + "시간 " +  freeTimeArr[1] + "분"

        # 총근무 시간
        durationTime = divmod((endTime - startTime).seconds, 60)
        if freeTime is not None and freeTime != '' :
            freeTimeArr = freeTime.split(":")
            datetime = endTime - timedelta(hours=int(freeTimeArr[0]), minutes=int(freeTimeArr[1]))
            durationTime = divmod((datetime - startTime).seconds, 60)

        workingWeekendTotalTime = str(int(durationTime[0] / 60)) + " 시간 " + str(durationTime[0] % 60) + "분 근무"

        # 내용
        formContents = """
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴일 근무일</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴일 근무 시간</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴일 휴게 시간</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">총근무 시간</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">프로젝트 명</th>
            <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        <tr>
            <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">휴일 근무 내용</th>
            <td colspan="2" style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        """.format(workingWeekendNoteForm.working_weekend_date,
                   workingWeekendTime,
                   workingWeekendFreeTime,
                   workingWeekendTotalTime,
                   workingWeekendNoteForm.working_project_name,
                   workingWeekendNoteForm.working_note)
        emailContents = emailContents.replace("[form_contents]", formContents)

    emailContents = emailContents.replace("[working_off_days]", workingOffDays)
    emailContents = emailContents.replace("[working_off_date]", workingOffDate)

    # 결재자
    approvalMemersStr = ""
    for approvalMember in approvalMembers :
        approvalMemersStr += """
        <tr>
            <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
            <td style="border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        """.format(approvalMember["step"], approvalMember["member_name"] + " (" + approvalMember["member_email"] + ")")

    emailContents = emailContents.replace("[approval_members]", approvalMemersStr)

    # 참조자
    approvalRefMembers = ""
    for approvalEtcMember in approvalEtcMembers :
        if approvalEtcMember["approval_etc_member_type"] == Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_REF") :
            if approvalRefMembers == "" :
                approvalRefMembers = approvalEtcMember["member_name"]
            else :
                approvalRefMembers += "," + approvalEtcMember["member_name"]

    approvalRefMembersStr = """
    <tr>
        <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">참조자</th>
        <td colspan="2" style="border: 1px solid #ccc; padding: 8px;">{}</td>
    </tr>
    """.format(approvalRefMembers)
    emailContents = emailContents.replace("[approval_ref_members]", approvalRefMembersStr)

    # 수신자
    approvalRecvMembers = ""
    for approvalEtcMember in approvalEtcMembers :
        if approvalEtcMember["approval_etc_member_type"] == Code().getCodeDtlNoByAlias("APPROVAL_ETC_MEMBER_TYPE_RECV") :
            if approvalEtcMember["member_name"] != None :
                if approvalRecvMembers == "" :
                    approvalRecvMembers = approvalEtcMember["member_name"]
                else :
                    approvalRecvMembers += "," + approvalEtcMember["member_name"]

    approvalRecvMembersStr = """
    <tr>
        <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">수신자</th>
        <td colspan="2" style="border: 1px solid #ccc; padding: 8px;">{}</td>
    </tr>
    """.format(approvalRecvMembers)
    emailContents = emailContents.replace("[approval_recv_members]", approvalRecvMembersStr)

    # 작성일
    emailContents = emailContents.replace("[form_datetime]", formDatetime)

    approvalHistorysStr = ""
    for approvalHistory in approvalHistorys :
        approvalHistorysStr += """
        <tr>
            <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
            <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
            <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
            <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
            <td style="text-align: center; border: 1px solid #ccc; padding: 8px;">{}</td>
        </tr>
        """.format(Code().getCodeDtlNm(approvalHistory["approval_state"]),
                   approvalHistory["res_member_name"],
                   approvalHistory["group_name"],
                   approvalHistory["approval_date"].strftime("%Y-%m-%d %H:%M:%S"),
                   approvalHistory["comment"])

    emailContents = emailContents.replace("[approval_historys]", approvalHistorysStr)

    emailContents += "<br><br>감사합니다."

    return emailTitle, emailContents

def mailTemplate() :
    return """
<h3 style="text-align: center;">결재 정보</h3>
<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
    [working_off_days]
</table>
<h3>내용</h3>
<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; border: 1px solid #ccc;">
    <tr>
        <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">제목</th>
        <td colspan="2"style="border: 1px solid #ccc; padding: 8px;">[form_title]</td>
    </tr>
    [form_contents]
    <tr>
        <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">작성일</th>
        <td colspan="2" style="border: 1px solid #ccc; padding: 8px;">[form_datetime]</td>
    </tr>
    [working_off_date]
    <tr>
        <td colspan="3">
            <div>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <th style="width: 15%; border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">결재순서</th>
                        <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">결재자</th>
                    </tr>
                    [approval_members]
                </table>
            </div>
        </td>
    </tr>
    [approval_ref_members]
    [approval_recv_members]
</table>
<h3>결재 내역</h3>
<table style="width: 100%; border-collapse: collapse;">
    <tr>
        <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">상태</th>
        <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">결재자</th>
        <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">부서</th>
        <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">결재일</th>
        <th style="border: 1px solid #ccc; padding: 8px; background-color: #f2f2f2;">내용</th>
    </tr>
    [approval_historys]
</table>
"""

def sendMail(receiverMemberId, emailTitle, emailContents) :
    receiverEmails = []
    reMembers = getReMembers(receiverMemberId)
    for member in reMembers :
        receiverEmails.append(member.member_email)

    sendEmails = []
    for receiverEmail in receiverEmails :
        if receiverEmail == "" :
            continue

        # 발송 메일 중복 체크
        if receiverEmail in sendEmails :
            continue

        email_service = gmail_authenticate()
        message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
        send_message(email_service, "me", message)

        # 메일 발송 완료 / 발송 메일 중복 체크
        sendEmails.append(receiverEmail)

# 오픈 도메인 경우 출근 체크 안함
def checkOpenDomain(request) :
    if 'my.voronoi.app' in request.build_absolute_uri('/')[:-1]  :
        if request.user.id is not None :
            print(request.build_absolute_uri('/')[:-1] + " : " + str(request.user.id))
        return True
    return False

def makeApprovalId() :
    now = datetime.now().strftime("%Y%m%d")
    lastReApporval = ReApproval.objects.filter(Q(approval_id__contains=now)).last()

    numbering = "00001"
    if lastReApporval is not None :
        numbering = "{:05d}".format(int(lastReApporval.approval_id[12:]) + 1)

    approvalId = "vn_" + now + "_" + numbering
    return approvalId

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