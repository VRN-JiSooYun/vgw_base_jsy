from django.shortcuts import render
from re_member.functions import *
# from project.views import authority
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required
from home.code_singleton import Code


@login_required(login_url='/security/login/')
def member_list_page(request) :
    print("member_list_page :", request.user.id)
    # auth = authority("hr", request)
    auth = False
    if auth["D"] == True :
        context = {
            "members": getMembers(request)
        }
        return render(request, "member_list.html", context)
    else :
        return render(request, "member_access_auth.html")

@login_required(login_url='/security/login/')
def member_page(request, memberId) :
    print("member_page :", request.user.id, memberId)
    member = getMember(memberId)

    # 생일
    birthday = ""
    if member["member_birthday"] is not None :
        birthday = parse(member["member_birthday"]).strftime("%m월 %d일")

    # 나이
    age = makeAge(member["member_birthday"])

    # 성별
    gender = ""
    if member["member_social_id"] != '' and member["member_social_id"] is not None :
        if member["member_social_id"][7] == "1" or member["member_social_id"][7] == "3" or member["member_social_id"][7] == "5" or member["member_social_id"][7] == "7":
            gender = "남자"
        elif member["member_social_id"][7] == "2" or member["member_social_id"][7] == "4" or member["member_social_id"][7] == "6" or member["member_social_id"][7] == "8":
            gender = "여자"
    # code
    codes = getCodes()
    codeDtls = getCodeDtls()

    context = {
        "member": member,
        "birthday": birthday,
        "age": age,
        "gender": gender,
        "codes": codes,
        "codeDtls": codeDtls,
    }
    return render(request, "member_view.html", context)

@login_required(login_url='/security/login/')
def member_card_page(request) :
    print("member_card_page :", request.user.id)
    context = {
        "member": getMember(request.user.id),
        "codes": getCodes(),
        "codeDtls": getCodeDtls(),
    }
    return render(request, "member_card.html", context)

@csrf_exempt
def create_member(request) :
    print("create_member :", request.user.id)
    if request.method == "POST":
        process = createMember(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def upload_member_image(request, memberId) :
    print("upload_member_image :", request.user.id)
    if request.method == "POST":
        process = uploadMemberImage(request, memberId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def get_members(request) :
    print("get_members :", request.user.id)
    return JsonResponse(getMembers(request), safe=False)

def get_me(request) :
    print("get_me :", request.user.id)
    return JsonResponse(getMe(request), safe=False)

def get_member(request, memberId) :
    print("get_member :", request.user.id, memberId)
    return JsonResponse(getMember(memberId), safe=False)

@csrf_exempt
def get_member_colleges(request, memberId) :
    print("get_member_colleges :", request.user.id, memberId)
    member = getReMember(memberId)
    return JsonResponse(getMemberColleges(member), safe=False)

@csrf_exempt
def get_member_certificates(request, memberId) :
    print("get_member_certificates :", request.user.id, memberId)
    member = getReMember(memberId)
    return JsonResponse(getMemberCertificates(member), safe=False)

@csrf_exempt
def get_member_foregin_langs(request, memberId) :
    print("get_member_foregin_langs :", request.user.id, memberId)
    member = getReMember(memberId)
    return JsonResponse(getMemberForeginLangs(member), safe=False)

@csrf_exempt
def get_member_companys(request, memberId) :
    print("get_member_companys :", request.user.id, memberId)
    member = getReMember(memberId)
    return JsonResponse(getMemberCompanys(member), safe=False)

@csrf_exempt
def get_member_familys(request, memberId) :
    print("get_member_familys :", request.user.id, memberId)
    member = getReMember(memberId)
    return JsonResponse(getMemberFamilys(member), safe=False)

@csrf_exempt
def get_search(request) :
    print("get_search :", request.user.id)
    return JsonResponse(list(getSearch(request).values()), safe=False)

@csrf_exempt
def update_member_info_default(request) :
    print("update_member_info_default :", request.user.id)
    if request.method == "POST":
        process = updateMemberInfoDefault(request)

        if process[0] :
            member = getMember(request.POST.get("member_id"))

            # 입사일
            joinDate = member["join_date"].strftime('%Y-%m-%d')
            # 퇴사일
            if member["leave_date"] is None :
                leaveDate = ""
            else :
                leaveDate = member["leave_date"].strftime('%Y-%m-%d')
            # 생일
            birthDay = parse(member["member_birthday"]).strftime("%m월 %d일")
            # 나이
            age = makeAge(member["member_birthday"])

            gender = ""
            if member["member_social_id"] is not None and member["member_social_id"] != '' :
                if member["member_social_id"][7] == "1" or member["member_social_id"][7] == "2" :
                    gender = "남자"
                else :
                    gender = "여자"

            context = {
                "member": member,
                "join_date": joinDate,
                "leave_date": leaveDate,
                "birthday": birthDay,
                "age": age,
                "gender": gender
            }
            return JsonResponse(context, safe=False)

        return JsonResponse(process, safe=False)

@csrf_exempt
def update_member_info(request) :
    print("update_member_info :", request.user.id)
    if request.method == "POST":
        process = updateMemberInfo(request)

        if process[0] :
            member = getMember(request.POST.get("member_id"))

            if member["member_type"] != "" :
                memberType = Code().getCodeDtlNm(member["member_type"])
            else :
                memberType = ""

            if member["working_type"] != "" :
                workingType = Code().getCodeDtlNm(member["working_type"])
            else :
                workingType = ""

            if member["working_type_detail"] != "" :
                workingTypeDetail = Code().getCodeDtlNm(member["working_type_detail"])
            else :
                workingTypeDetail = ""

            if member["lab"] != "" :
                lab = Code().getCodeDtlNm(member["lab"])
            else :
                lab = ""

            if member["working_place"] != "" :
                workingPlace = Code().getCodeDtlNm(member["working_place"])
            else :
                workingPlace = ""

            if member["memo"] != "" :
                memo = member["memo"]
            else :
                memo = ""

            if member["check_working"] != "" :
                checkWorking = member["check_working"]
            else :
                checkWorking = ""

            if member["check_working_off_promote"] != "" :
                checkWorkingOffPromote = member["check_working_off_promote"]
            else :
                checkWorkingOffPromote = ""

            context = {
                "member_type": memberType,
                "working_type": workingType,
                "working_type_detail": workingTypeDetail,
                "lab": lab,
                "working_place": workingPlace,
                "memo": memo,
                "check_working": checkWorking,
                "check_working_off_promote": checkWorkingOffPromote,
            }

            return JsonResponse(context, safe=False)

        return JsonResponse(process, safe=False)


@csrf_exempt
def update_member_info_card(request, memberId) :
    print("update_member_info_card :", request.user.id, memberId)
    if request.method == "POST":
        process = updateMemberInfoCard(request, memberId)

        if process[0] :
            member = getMember(memberId)

            context = {
                "member_eng_name": member["member_eng_name"],
                "member_social_id": member["member_social_id"],
                "member_bank": member["member_bank"],
                "member_bank_num": member["member_bank_num"],
                "member_addr": member["member_addr"],
                "member_hp_er": member["member_hp_er"],
                "member_hp_er_name": member["member_hp_er_name"],
                "disabled_level": member["disabled_level"],
                "disabled_type": member["disabled_type"],
                "researcher_num": member["researcher_num"],
                "memo": member["memo"],
            }

            return JsonResponse(context, safe=False)

        return JsonResponse(process, safe=False)

@csrf_exempt
def update_member_image(request, memberId) :
    print("update_member_image :", request.user.id, memberId)
    if request.method == "POST":
        process = updateMemberImage(request, memberId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def re_join_member(request, memberId) :
    print("re_join_member :", request.user.id, memberId)
    if request.method == "POST":
        process = reJoinMember(memberId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def leave_member(request, memberId) :
    print("leave_member :", request.user.id, memberId)
    if request.method == "POST":
        process = leaveMember(request, memberId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def delete_member(request, memberId) :
    print("delete_member :", request.user.id, memberId)
    if request.method == "POST":
        process = deleteMember(memberId)
        return JsonResponse(process, safe=False)

