from re_member.models import *
from re_auth.functions import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import connection
from django.forms.models import model_to_dict
from django.core.files.storage import default_storage  # file save
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import os
import time
import json


def createUser(email, name) :
    # 로그인을 위한 user 생성
    user = User.objects.filter(Q(username=email)).last()
    if user is None:
        data = {
            'first_name': name,
            'last_name': "",
            'email': email,
            'username': email,
        }
        user = User.objects.create(**data)
        user.set_password("vgwdjemals12")
        user.save()
        user = User.objects.filter(Q(username=email)).last()
    return user

def createMember(request) :
    memberEmail = request.POST.get("member_email").lower()
    mebmerCompanyId = request.POST.get("member_company_id")
    memberName = request.POST.get("member_name")
    memberBirthday = request.POST.get("member_birthday")
    memberHp = request.POST.get("member_hp")
    joinDate = request.POST.get("join_date")


    if ReMember.objects.filter(Q(check_discard = False) & Q(member_company_id = mebmerCompanyId)).count() > 0 :
        return False, "동일한 사번이 있습니다. 다른 사번을 사용해 주세요"

    if ReMember.objects.filter(Q(check_discard = False) & Q(member_email = memberEmail)).count() > 0 :
        return False, "동일한 이메일이 있습니다. 다른 이메일을 사용해 주세요"

    try :
        user = createUser(memberEmail, memberName)
        memberId = user.id

        reMember = ReMember()
        reMember.member_id = user.id
        reMember.user_id = memberId
        reMember.member_company_id = mebmerCompanyId
        reMember.member_name= memberName
        reMember.member_birthday = memberBirthday
        reMember.member_email = memberEmail
        reMember.member_hp = memberHp
        reMember.join_date = joinDate

        # 연차 시작일
        joinDate =  datetime.strptime(reMember.join_date, '%Y-%m-%d')
        yearsAgo = datetime.now() + relativedelta(years=-1)
        if joinDate < yearsAgo :
            # 입사일이 현재 날짜 기준 1년 전이면 현재 년도 + 입사일 날짜
            reMember.working_off_start_date =  str(datetime.now().year) + "-" + joinDate.strftime("%m-%d")
        else :
            # 입사일이 현재 날짜 기준 1년 후이면 입사일이 연차 시작일
            reMember.working_off_start_date = reMember.join_date
        ReMember.save(reMember)

        # 초기 권한 설정
        initAuth(memberId)

        """
        lsh@voronoi.io : member_id 와 user_id가 다를 경우가 생길 수 있음 / 확인 필요 : 2025.01.02
        member = Member.objects.filter(user=user).last()
        member.member_name = memberName
        member.save()

        data = {
            'user': user,
            'member': member,
            'first_name': "",
            'last_name': "",
            'name_korean': memberName,
            'email': memberEmail,
            'phone_mobile': memberHp,
            'phone_office': "",
            'date_joined': joinDate,
            'date_of_birth': memberBirthday,
        }
        Profile.objects.create(**data)
        """

        print("success create member")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def uploadMemberImage(request, memberId) :
        memberImage = request.FILES["file"]
        ext = os.path.splitext(memberImage.name)[1:]
        try :
            filename = str(round(time.time() * 1000)) + ext[0] # 파일명 생성
            default_storage.save("re-member/" + filename, memberImage)

            print("success upload member image")
        except Exception as e :
            print("Exception::", e)
            return False, e

        return True, filename

def getMembers(request) :
    is_leave = request.GET.get("is_leave")
    join_date_month = request.GET.get("join_date_month")
    order_by = request.GET.get("order_by")

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_member.get_members)

    searchStr = ""
    if is_leave != "Y" :
        searchStr = " AND LEAVE_DATE IS NULL"

    if join_date_month is not None and join_date_month != '' :
        searchStr += " AND to_char(a.join_date, 'MM') = '" + join_date_month + "'"

    query = query.replace("__SEARCH_QUERY__", searchStr)

    if order_by is not None and order_by != '' :
        if "join_date" in order_by :
            query = query.replace("__ORDER_BY__", "ORDER BY to_char(a.join_date, 'DD') DESC")
        else :
            query = query.replace("__ORDER_BY__", "ORDER BY " + order_by)
    else :
        if join_date_month is not None and join_date_month != '' :
            query = query.replace("__ORDER_BY__", "ORDER BY to_char(a.join_date, 'DD') DESC")
        else :
            query = query.replace("__ORDER_BY__", "ORDER BY a.member_company_id ASC, a.id DESC")

    print(query)
    cur.execute(query)

    members = dictfetchall(cur)
    if cur != None :
        cur.close()

    return members

def getMe(request) :
    return getMember(request.user.id)

def getMember(memberId) :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_member.get_member)
    query = query.replace("__MEMBER_ID__", str(memberId))

    cur.execute(query)
    list = dictfetchall(cur)

    if cur != None :
        cur.close()

    return list[0]

def getReMember(memberId) :
    return ReMember.objects.get(member_id = memberId)

def getReMembers(memberIds) :
    return ReMember.objects.filter(member_id__in = memberIds).all()

def getMemberColleges(member) :
    memberColleges = ReMemberCollege.objects.filter(re_member=member)
    if len(memberColleges) == 0 :
        return [ model_to_dict(ReMemberCollege()) ]
    else :
        return list(memberColleges.values())


def getMemberCertificates(member) :
    memberCertificates = ReMemberCertificate.objects.filter(re_member=member)
    if len(memberCertificates) == 0 :
        return [ model_to_dict(ReMemberCertificate()) ]
    else :
        return list(memberCertificates.values())

def getMemberForeginLangs(member) :
    memberForeignLangs = ReMemberForeignLang.objects.filter(re_member=member)
    if len(memberForeignLangs) == 0 :
        return [ model_to_dict(ReMemberForeignLang()) ]
    else :
        return list(memberForeignLangs.values())

def getMemberCompanys(member) :
    memberCompanys = ReMemberCompany.objects.filter(re_member=member)
    if len(memberCompanys) == 0 :
        return [ model_to_dict(ReMemberCompany()) ]
    else :
        return list(memberCompanys.values())

def getMemberFamilys(member) :
    memberFamilys = ReMemberFamily.objects.filter(re_member=member)
    if len(memberFamilys) == 0 :
        return [ model_to_dict(ReMemberFamily()) ]
    else :
        return list(memberFamilys.values())

def getSearch(request) :
    search = request.GET.get("search")
    return ReMember.objects.filter(Q(member_name__contains = search) & Q(leave_date = None) & Q(check_discard = False)).order_by("member_name").all()

def updateUser(memberId, email) :
    # 로그인을 위한 user 생성
    user = User.objects.filter(Q(id = memberId)).last()
    if user is not None:
        user.username = email
        user.email = email
        user.save()
    return user

def updateMemberInfoDefault(request) :
    try :
        memberId = request.POST.get("member_id")
        mebmerCompanyId = request.POST.get("member_company_id")
        memberEmail = request.POST.get("member_email")

        if ReMember.objects.filter(~Q(member_id = memberId) & Q(check_discard = False) & Q(member_company_id = mebmerCompanyId)).count() > 0 :
            return False, "동일한 사번이 있습니다. 다른 사번으로 변경해 주세요"

        if ReMember.objects.filter(~Q(member_id = memberId) & Q(check_discard = False) & Q(member_email = memberEmail)).count() > 0 :
            return False, "동일한 이메일이 있습니다. 다른 이메일로 변경해 주세요"

        reMember = ReMember.objects.get(Q(member_id = memberId))

        # 이메일 변경인 경우
        if reMember.member_email != memberEmail :
            updateUser(memberId, memberEmail)

        reMember.member_name= request.POST.get("member_name")
        reMember.member_company_id= mebmerCompanyId
        reMember.member_birthday = request.POST.get("member_birthday")
        reMember.member_email = memberEmail
        reMember.member_hp = request.POST.get("member_hp")
        reMember.join_date = request.POST.get("join_date")

        # 연차 시작일
        joinDate =  datetime.strptime(reMember.join_date, '%Y-%m-%d')
        yearsAgo = datetime.now() + relativedelta(years=-1)
        if joinDate < yearsAgo :
            # 입사일이 현재 날짜 기준 1년 전이면 현재 년도 + 입사일 날짜
            reMember.working_off_start_date =  str(datetime.now().year) + "-" + joinDate.strftime("%m-%d")
        else :
            # 입사일이 현재 날짜 기준 1년 후이면 입사일이 연차 시작일
            reMember.working_off_start_date = reMember.join_date

        if request.POST.get("leave_date") == '' :
            reMember.leave_date = None
        else :
            reMember.leave_date = request.POST.get("leave_date")
        reMember.save()
        print("success update member default info")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateMemberInfo(request) :
    memberId = request.POST.get("member_id")

    try :
        reMember = ReMember.objects.get(member_id=memberId)
        reMember.member_type = request.POST.get("member_type")
        reMember.working_type = request.POST.get("working_type")
        reMember.working_type_detail = request.POST.get("working_type_detail")
        reMember.lab = request.POST.get("lab")
        reMember.working_place = request.POST.get("working_place")
        reMember.memo = request.POST.get("memo")
        if request.POST.get("check_working") == "Y" :
            reMember.check_working = True
        else :
            reMember.check_working = False
        if request.POST.get("check_working_off_promote") == "Y" :
            reMember.check_working_off_promote = True
        else :
            reMember.check_working_off_promote = False

        ReMember.save(reMember)
        print("success update member info")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateMemberInfoCard(request, memberId) :
    data = json.loads(request.body.decode('utf-8'))

    try :
        member = ReMember.objects.get(member_id=memberId)

        # 개인정보
        memberPrivateInfo = data["member_private_info"]
        member.member_eng_name = memberPrivateInfo["member_eng_name"]
        member.member_chinese_name = memberPrivateInfo["member_chinese_name"]
        member.member_social_id = memberPrivateInfo["member_social_id_first"] + "-" + memberPrivateInfo["member_social_id_second"]
        member.member_addr = memberPrivateInfo["member_addr"]
        member.member_hp_er = memberPrivateInfo["member_hp_er"]
        member.member_hp_er_name = memberPrivateInfo["member_hp_er_name"]
        member.member_bank = memberPrivateInfo["member_bank"]
        member.member_bank_num = memberPrivateInfo["member_bank_num"]

        # 군대
        memberMilitary = data["member_military"]
        member.military_discharge_type = memberMilitary["military_discharge_type"]
        member.military_etc_type = memberMilitary["military_etc_type"]
        member.military_type = memberMilitary["military_type"]
        member.military_discharge_rank = memberMilitary["military_discharge_rank"]
        member.military_skill = memberMilitary["military_skill"]
        member.military_start_date = memberMilitary["military_start_date"]
        member.military_end_date = memberMilitary["military_end_date"]
        member.military_num = memberMilitary["military_num"]
        member.military_memo = memberMilitary["military_memo"]

        # etc 정보
        memberEtcInfo = data["member_etc_info"]
        member.researcher_num = memberEtcInfo["researcher_num"]
        member.ministry_patriots = memberEtcInfo["ministry_patriots"]
        member.disabled_level = memberEtcInfo["disabled_level"]
        member.disabled_type = memberEtcInfo["disabled_type"]

        ReMember.save(member)

        # 학교
        ReMemberCollege.objects.filter(re_member=member).delete()
        memberColleges = data["member_colleges"]
        for memberCollege in memberColleges :
            ReMemberCollege.objects.create(
                re_member = member,
                college_type = memberCollege["college_type"],
                college_name = memberCollege["college_name"],
                college_start_date = memberCollege["college_start_date"],
                college_end_date = memberCollege["college_end_date"],
                college_status = memberCollege["college_status"],
                college_major = memberCollege["college_major"],
                college_degree_num = memberCollege["college_degree_num"],
            )

        # 자격증
        ReMemberCertificate.objects.filter(re_member=member).delete()
        memberCertificates = data["member_certificates"]
        for memberCertificate in memberCertificates :
            ReMemberCertificate.objects.create(
                re_member = member,
                certificate_name = memberCertificate["certificate_name"],
                certificate_date = memberCertificate["certificate_date"],
                certificate_issuer = memberCertificate["certificate_issuer"],
            )

        # 어학능력
        ReMemberForeignLang.objects.filter(re_member=member).delete()
        memberForeignLangs = data["member_foreign_langs"]
        for memberForeignLang in memberForeignLangs :
            ReMemberForeignLang.objects.create(
                re_member = member,
                foreign_lang_name = memberForeignLang["foreign_lang_name"],
                foreign_lang_exam = memberForeignLang["foreign_lang_exam"],
                foreign_lang_exam_level = memberForeignLang["foreign_lang_exam_level"],
                foreign_lang_date = memberForeignLang["foreign_lang_date"],
            )

        # 경력사항
        ReMemberCompany.objects.filter(re_member=member).delete()
        memberCompanys = data["member_companys"]
        for memberCompany in memberCompanys :
            ReMemberCompany.objects.create(
                re_member = member,
                company_name = memberCompany["company_name"],
                working_start_date = memberCompany["working_start_date"],
                working_end_date = memberCompany["working_end_date"],
                division = memberCompany["division"],
                position = memberCompany["position"],
                job = memberCompany["job"],
                annual_income = memberCompany["annual_income"],
                resign_memo = memberCompany["resign_memo"],
            )

        # 가족관계
        ReMemberFamily.objects.filter(re_member=member).delete()
        memberFamilys = data["member_familys"]
        for memberFamily in memberFamilys :
            ReMemberFamily.objects.create(
                re_member = member,
                relationship = memberFamily["relationship"],
                name = memberFamily["name"],
                birthday = memberFamily["birthday"],
                is_live = memberFamily["is_live"],
                addr = memberFamily["addr"],
            )
        print("success update member info card")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateMemberImage(request, memberId) :
        data = json.loads(request.body.decode('utf-8'))

        try :
            reMember = ReMember.objects.get(member_id=memberId)
            reMember.member_image = data["member_image"]
            ReMember.save(reMember)
            print("success update member image")
        except Exception as e :
            print("Exception::", e)
            return False, e

        return True, "success"

def reJoinMember(memberId) :
    try :
        reMember = ReMember.objects.get(member_id=memberId)
        reMember.leave_date = None
        ReMember.save(reMember)
        print("success re join member")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def leaveMember(request, memberId) :
    data = json.loads(request.body)["data"]
    try :
        deleteAuth(memberId)

        reMember = ReMember.objects.get(member_id=memberId)
        reMember.leave_date = datetime.strptime(data["leave_date"], '%Y-%m-%d')
        ReMember.save(reMember)
        print("success leave member")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def deleteMember(memberId) :
    try :
        reMember = ReMember.objects.get(member_id=memberId)
        reMember.check_discard = True
        ReMember.save(reMember)
        print("success delete member")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

# Function
def makeMemberCompanyId() :
    try:
        member = ReMember.objects.filter(Q(member_company_id__startswith = '15', check_discard = False)).order_by('-member_company_id').first()
        memberCompanyId = "15" + "{:03d}".format(int(member.member_company_id[2:]) + 1)

        if ReMember.objects.filter(Q(check_discard = False, member_company_id = memberCompanyId)).count() > 0 :
            return 0
    except ReMember.DoesNotExist:
        return "15001"

    return memberCompanyId

def makeMemberId() :
    try:
        return ReMember.objects.order_by('-member_id')[:1].get().member_id + 1
    except ReMember.DoesNotExist:
        return 1

def makeAge(birth_date):
    if birth_date is not None :
        today = datetime.now()
        birth_datetime = datetime.strptime(birth_date, '%Y-%m-%d')  # 생년월일을 문자열에서 datetime 객체로 변환
        return today.year - birth_datetime.year - ((today.month, today.day) < (birth_datetime.month, birth_datetime.day))
    return ""


def getCodes() :
    cur = connection.cursor()
    query = "SELECT * FROM code"
    cur.execute(query)
    result = dictfetchall(cur)
    if cur != None :
        cur.close()

    return result


def getCodeDtls() :
    cur = connection.cursor()
    query = "SELECT * FROM code_dtl"
    cur.execute(query)
    result = dictfetchall(cur)
    if cur != None :
        cur.close()

    return result

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
