from django.db import models
from django.contrib.auth.models import User
import datetime









#################################################################################
#
#   다음 버젼 작성시 Member 앱에 작성된 아래 Table들은 모두 HR로 옮긴다.
#   1. 조직도 구성을 위한 Table들 (Member/Team/Division/...)
#   2. 구성원 정보 Table들 (Profile/Education/Career/...)
#
#   Member 앱은 구성원이 수행하는 업무 지원 앱들로 구성한다. (Todo, Calendar, News, 등..)
#
#################################################################################


###################################################
#                  date time
# from django.utils import timezone
###################################################
ls_datetime = datetime.datetime.now()
ls_year = ls_datetime.year
ls_hour = ls_datetime.hour
ls_minute = ls_datetime.minute
time_to_go_home_hour = 17 - ls_hour
time_to_go_home_min = 60 - ls_minute
ls_today = datetime.date.today()
list_holidays = []


def checkWeekend():
    # 주말체크
    list_day_of_week = [5, 6]
    day_of_week = datetime.datetime.today().weekday()
    if day_of_week not in list_day_of_week:
        # 주중임
        check_weekend = False
    else:
        # 주말임
        check_weekend = True
    return check_weekend


def checktimedelta():
    # TimeDelta
    tdd1 = datetime.timedelta(days=1)
    tdh1 = datetime.timedelta(hours=1)
    tdh2 = datetime.timedelta(hours=2)
    tdh0 = datetime.timedelta(hours=0)
    return tdd1, tdh1, tdh2, tdh0


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                         조직도 구성하기 (Member / Team / Division / Company / Group)
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


# 멤버
class Member(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(verbose_name="멤버 코멘트", max_length=100, null=True, blank=True)
    check_dummy = models.BooleanField(default=False)  # 임시로 만든 멤버(더미) 후임자 찾기 전까지 임시로 넣어두기용
    list_hr_layout_id = models.JSONField(null=True, blank=True)  # 멤버가 가지고 있는 포지션 리스트
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.member_name is not None:
            return self.member_name
        else:
            return str(self.id)


#-------------------------------------------------------------------------------------------------------------------

# 팀
class Team(models.Model):
    # M2M
    member = models.ManyToManyField(Member, through='Member2Team',  blank=True) # 팀에 소속된 멤버
    # info
    team_name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(verbose_name="팀 코멘트(동명의 팀 관리시 코멘트에 부연설명)", max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name="Team 주소", max_length=200, null=True, blank=True)
    check_team_ai_math = models.BooleanField(default=False)  # AI Lab 수리응용팀
    check_team_ai_dev = models.BooleanField(default=False)  # AI Lab 플랫폼개발팀
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.team_name is not None:
            return self.team_name
        else:
            return str(self.id)



# 팀에 소속된 멤버
class Member2Team(models.Model):
    # F.Keys
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    #------------------------
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # info
    check_team_leader = models.BooleanField(default=False)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.member is not None and self.team is not None:
            return f'{self.member.member_name}-{self.team.team_name}'
        elif self.member is not None and self.team is None:
            return f'{self.member.member_name}'
        elif self.member is None and self.team is not None:
            return f'{self.team.team_name}'
        else:
            return str(self.id)


#-------------------------------------------------------------------------------------------------------------------

# 부서
class Division(models.Model):
    # M2M
    member2team = models.ManyToManyField(Member2Team, through='Team2Division',  blank=True)  # 부서에 소속된 팀에 소속된 멤버
    #------------------------
    member = models.ManyToManyField(Member, through='Member2Division',  blank=True) # 부서 직속으로 소속된 멤버
    # info
    division_name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(verbose_name="부서 코멘트(동명의 부서 관리시 코멘트에 부연설명)", max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name="Divison 주소", max_length=200, null=True, blank=True)
    check_division_ai = models.BooleanField(default=False)  # True == AI Lab
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.division_name is not None:
            return self.division_name
        else:
            return str(self.id)



# 부서에 소속된 팀에 소속된 멤버
class Team2Division(models.Model):
    # F.Keys
    member2team = models.ForeignKey(Member2Team, on_delete=models.CASCADE, null=True, blank=True)
    #------------------------
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    # info
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)



# 부서 직속으로 소속된 멤버
class Member2Division(models.Model):
    # F.keys
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    #------------------------
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    # info
    check_division_leader = models.BooleanField(default=False)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)



#-------------------------------------------------------------------------------------------------------------------

# 회사
class Company(models.Model):
    # m2m
    team2division = models.ManyToManyField(Team2Division, through='Division2Company', blank=True)
    member2division = models.ManyToManyField(Member2Division, through='Division2Company', blank=True)
    #------------------------
    member = models.ManyToManyField(Member, through='Member2Company',  blank=True)
    # info
    company_name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(verbose_name="회사 코멘트(외부일 경우 업체명 기입)", max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name="Company 주소", max_length=200, null=True, blank=True)
    company_image = models.ImageField(null=True, blank=True, upload_to='company/')
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    business_reg_number = models.CharField(max_length=100, null=True, blank=True)
    office_phone_number = models.CharField(max_length=100, null=True, blank=True)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.company_name is not None:
            return self.company_name
        else:
            return str(self.id)



# 회사에 소속된 부서에 소속된 팀에 소속된 멤버
# 회사에 소속된 부서에 직속으로 소속된 멤버
class Division2Company(models.Model):
    # F.Keys
    team2division = models.ForeignKey(Team2Division, on_delete=models.CASCADE, null=True, blank=True)
    member2division = models.ForeignKey(Member2Division, on_delete=models.CASCADE, null=True, blank=True)
    #------------------------
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # info
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)



# 회사에 직속으로 소속된 멤버
class Member2Company(models.Model):
    # F.Keys
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    #------------------------
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    # info
    check_company_leader = models.BooleanField(default=False)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)



#-------------------------------------------------------------------------------------------------------------------


# 그룹
class Group(models.Model):
    # M2M
    company = models.ManyToManyField(Company, through='Company2Group', blank=True)
    division2company = models.ManyToManyField(Division2Company, through='Company2Group',  blank=True)
    member2company = models.ManyToManyField(Member2Company, through='Company2Group',  blank=True)
    #------------------------
    member = models.ManyToManyField(Member, through='Member2Group',  blank=True)
    # info
    group_name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(verbose_name="그룹 코멘트", max_length=200, null=True, blank=True)
    check_is_voronoigroup = models.BooleanField(default=False)
    check_is_iacuc_member = models.BooleanField(default=False)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.group_name is not None:
            return self.group_name
        else:
            return str(self.id)


# 그룹에 소속된 회사에 소속된 부서에 소속된 팀에 소속된 멤버
# 그룹에 소속된 회사에 소속된 부서에 직속으로 소속된 멤버
# 그룹에 소속된 회사에 직속으로 소속된 멤버
class Company2Group(models.Model):
    # F.keys
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    division2company = models.ForeignKey(Division2Company, on_delete=models.CASCADE, null=True, blank=True)
    member2company = models.ForeignKey(Member2Company, on_delete=models.CASCADE, null=True, blank=True)
    #------------------------
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    # info
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # def __str__(self):
    #     return f'{self.company.company_name}-{self.group.group_name}'


# 그룹에 직속으로 소속된 멤버
class Member2Group(models.Model):
    # F.Keys
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    #------------------------
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    # info
    check_group_leader = models.BooleanField(default=False)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)


#-----------------------------------------------------------------------------------------------------------

###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


class MemberSearchLog(models.Model):
    check_member_search_duplication = models.BooleanField(verbose_name="중복검색허용", default=False)
    search_keyword = models.CharField(max_length=100, null=True, blank=True)
    list_search_keyword = models.JSONField(null=True, blank=True)
    list_member_id_searched = models.JSONField(null=True, blank=True)
    check_discard = models.BooleanField(default=False)


class TeamSearchLog(models.Model):
    check_team_search_duplication = models.BooleanField(verbose_name="중복검색허용", default=False)
    search_keyword = models.CharField(max_length=100, null=True, blank=True)
    list_search_keyword = models.JSONField(null=True, blank=True)
    list_team_id_searched = models.JSONField(null=True, blank=True)
    check_discard = models.BooleanField(default=False)


class DivisionSearchLog(models.Model):
    check_division_search_duplication = models.BooleanField(verbose_name="중복검색허용", default=False)
    search_keyword = models.CharField(max_length=100, null=True, blank=True)
    list_search_keyword = models.JSONField(null=True, blank=True)
    list_division_id_searched = models.JSONField(null=True, blank=True)
    check_discard = models.BooleanField(default=False)


class CompanySearchLog(models.Model):
    check_company_search_duplication = models.BooleanField(verbose_name="중복검색허용", default=False)
    search_keyword = models.CharField(max_length=100, null=True, blank=True)
    list_search_keyword = models.JSONField(null=True, blank=True)
    list_company_id_searched = models.JSONField(null=True, blank=True)
    check_discard = models.BooleanField(default=False)




###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                           Profile
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


COMMENT_HR = (
    ('RESIGN', '퇴사자 코멘트'),
    ('INTERVIEW', '인터뷰 코멘트'),
    ('INTERNSHIP', '인턴쉽 코멘트'),
    ('YEAR_1', '1년차 코멘트'),
    ('YEAR_2', '2년차 코멘트'),
    ('YEAR_3', '3년차 코멘트'),
    ('YEAR_4', '4년차 코멘트'),
    ('YEAR_5', '5년차 코멘트'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    member = models.OneToOneField(Member, null=True, on_delete=models.CASCADE)
    #--------------------------------------------------------------------------------------------------------------------------
    name_korean = models.CharField(verbose_name="한글 이름", max_length=100, null=True, blank=True)
    first_name = models.CharField(verbose_name="영문 이름", max_length=100, null=True, blank=True)
    last_name = models.CharField(verbose_name="영문 성", max_length=100, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name="email 주소", null=True, blank=True)
    phone_mobile = models.CharField(verbose_name="핸드폰 번호", max_length=100, null=True, blank=True)
    phone_office = models.CharField(verbose_name="사내 전화번호", max_length=100, null=True, blank=True)
    position = models.CharField(verbose_name="포지션", max_length=200, null=True, blank=True)  # 본인의 최고 포지션
    #--------------------------------------------------------------------------------------------------------------------------
    # 근무년차 계산
    date_joined = models.DateField(verbose_name="입사일", null=True, blank=True)  # 근무시작일(입사일)
    date_rejoined = models.DateField(verbose_name="재입사일", null=True, blank=True)
    date_left = models.DateField(verbose_name="퇴사일", null=True, blank=True)
    status_working_year = models.IntegerField(null=True, blank=True) # 근무 년차 (예 : 1년차 == 1일 ~ 365일 근무)
    status_working_month_first_year = models.IntegerField(null=True, blank=True) # 근무 월차 (근무 첫해의, 예: 1월차 == 1 ~ 30일 근무)
    delta_year_joined = models.IntegerField(null=True, blank=True) # 만 근무 년수
    delta_month_joined = models.IntegerField(null=True, blank=True) #만 근무 달수 (최대 11)
    delta_day_joined = models.IntegerField(null=True, blank=True) #만 근무 일수
    date_workingyear_start = models.DateField(null=True, blank=True) # 해당근무년차의 근무시작일
    date_workingyear_end = models.DateField(null=True, blank=True) # 해당근무년차의 근무종료일
    #--------------------------------------------------------------------------------------------------------------------------
    address = models.CharField(verbose_name="집주소", max_length=250, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="생일", null=True, blank=True)
    introduction = models.TextField(verbose_name="자기소개", null=True, blank=True)
    dict_comment = models.JSONField(null=True, blank=True)  # 코멘트
    #--------------------------------------------------------------------------------------------------------------------------
    # Check Authority
    check_freepass = models.BooleanField(verbose_name="무제한접속", default=False)  # CEO 만
    check_hr_head = models.BooleanField(verbose_name="인사팀장여부", default=False)  # 인사팀장만
    #--------------------------------------------------------------------------------------------------------------------------
    # Check 퇴사/파기
    check_resign = models.BooleanField(verbose_name="퇴사여부", default=False) # True: 퇴사자 (재입사시 False로 변경)
    check_comeback = models.BooleanField(verbose_name="재입사여부", default=False) # True: 재입사자
    check_discard = models.BooleanField(default=False) # True: 퇴사시 discard 및 resign 모두 True,  퇴사가 아닌 삭제시 discard만 True
    #--------------------------------------------------------------------------------------------------------------------------
    # System
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    autentication_number = models.CharField(max_length=6, null=True, blank=True)
    # 아래 두 필드는 확인 후 삭제.

    # def __str__(self):
    #     if self.name_korean is not None:
    #         return self.member.member_name
    #     else:
    #         return str(self.id)

    # @property
    # def is_oneyear_passed(self):
    #     ls_today = datetime.date.today()
    #     joineddate = self.date_joined
    #     tdy1 = datetime.timedelta(days=365)
    #     date_joined_date_to_a_year_later = joineddate + tdy1
    #     delta_one_year_check = ls_today-date_joined_date_to_a_year_later
    #     delta_one_year_check_days = delta_one_year_check.days

    #     if delta_one_year_check_days > 0:
    #         print('입사한지 1년 지났음.')
    #         status_oneyear_passed = True

    #     else:
    #         print('입사한지 1년 안지났음')
    #         status_oneyear_passed = False

    #     return status_oneyear_passed

    # @property
    # def is_vacation_issue_calculator(self):
    #     print('=== is_vacation_issue_calculator 작동시작 ===')
    #     # 입사한 날짜 기준 1년 이내와 1년 이후로 나누어 휴가생성개수 계산기.
    #     # 파라미터
    #     ls_today = datetime.date.today()
    #     ls_month = ls_today.month
    #     tdy1 = datetime.timedelta(days=365)
    #     tdy2 = datetime.timedelta(days=730)
    #     joineddate = self.date_joined

    #     # delta_one_year_check_days 값이 0보다 크면 입사한지 1년이 지났다.
    #     date_joined_date_to_a_year_later = joineddate + tdy1
    #     delta_one_year_check = ls_today-date_joined_date_to_a_year_later
    #     delta_one_year_check_days = delta_one_year_check.days

    #     # 입사한 날부터 오늘까지 델타시간
    #     delta_joined_date_to_today = ls_today - joineddate

    #     if delta_one_year_check_days > 0:
    #         # 1년이 지난 사람, 2,3연차 15개, 4,5연차 16개, .... 21연차부터 최대 25개로 제한
    #         # 입사한 날부터 오늘까지의 총 델타시간에서 1연차를 뺀 나머지 기간을 2년(730일)로 나눈 몫을 찾는다.
    #         # 몫이 0이면 2,3연차,
    #         # 몫이 1이면 4,5연차,
    #         # 몫이 2이면 6,7연차...
    #         countfactor = (delta_joined_date_to_today-tdy1)//tdy2
    #         print(self.user.profile.name_korean, countfactor)
    #         issue_vc_by_cf = 15 + countfactor
    #         print('발행개수(년간)', issue_vc_by_cf)

    #     else:
    #         # 1년이 지나지 않은 사람, 1달 지나면 1개씩 생성 만 1년동안 최대 11개, 다음연차 되어도 발행한날 기준 만 1년 안되면 연차는 안사라짐
    #         issue_vc_by_cf = 1
    #         print('발행개수(매달)', issue_vc_by_cf)
    #     return issue_vc_by_cf






###################################################
#
#                   Career
#
###################################################


class Career(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    career1_company = models.CharField(verbose_name="(1-1)근무회사", max_length=200, null=True, blank=True)
    career1_position = models.CharField(verbose_name="(1-2)포지션", max_length=250, null=True, blank=True)
    career1_detail = models.CharField(verbose_name="(1-3)대표수행업무", max_length=250, null=True, blank=True)
    career1_start = models.DateField(verbose_name="(1-4)입사년도", null=True, blank=True)
    career1_end = models.DateField(verbose_name="(1-5)퇴사년도", null=True, blank=True)

    career2_company = models.CharField(verbose_name="(2-1)근무회사", max_length=200, null=True, blank=True)
    career2_position = models.CharField(verbose_name="(2-2)포지션", max_length=250, null=True, blank=True)
    career2_detail = models.CharField(verbose_name="(2-3)대표수행업무", max_length=250, null=True, blank=True)
    career2_start = models.DateField(verbose_name="(2-4)입사년도", null=True, blank=True)
    career2_end = models.DateField(verbose_name="(2-5)퇴사년도", null=True, blank=True)

    career3_company = models.CharField(verbose_name="(3-1)근무회사", max_length=200, null=True, blank=True)
    career3_position = models.CharField(verbose_name="(3-2)포지션", max_length=250, null=True, blank=True)
    career3_detail = models.CharField(verbose_name="(3-3)대표수행업무", max_length=250, null=True, blank=True)
    career3_start = models.DateField(verbose_name="(3-4)입사년도",  null=True, blank=True)
    career3_end = models.DateField(verbose_name="(3-5)퇴사년도",  null=True, blank=True)

    career4_company = models.CharField(verbose_name="(4-1)근무회사", max_length=200, null=True, blank=True)
    career4_position = models.CharField(verbose_name="(4-2)포지션", max_length=250, null=True, blank=True)
    career4_detail = models.CharField(verbose_name="(4-3)대표수행업무", max_length=250, null=True, blank=True)
    career4_start = models.DateField(verbose_name="(4-4)입사년도",  null=True, blank=True)
    career4_end = models.DateField(verbose_name="(4-5)퇴사년도",  null=True, blank=True)

    career5_company = models.CharField(verbose_name="(5-1)근무회사", max_length=200, null=True, blank=True)
    career5_position = models.CharField(verbose_name="(5-2)포지션", max_length=250, null=True, blank=True)
    career5_detail = models.CharField(verbose_name="(5-3)대표수행업무", max_length=250, null=True, blank=True)
    career5_start = models.DateField(verbose_name="(5-4)입사년도",  null=True, blank=True)
    career5_end = models.DateField(verbose_name="(5-5)퇴사년도",  null=True, blank=True)

    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # def __str__(self):
    #     return self.user.profile.name_korean


###################################################
#
#                   Education
#
###################################################

class Education(models.Model):

    EDUCATION1 = (
        # 학위
        ('ED_HIGH', '고등학교'),
        ('ED_UNIV', '대학교(학사)'),
        ('ED_MS', '대학원(석사)'),
        ('ED_PHD', '대학원(박사)'),
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    education1_level = models.CharField(verbose_name="(1-1)학위", max_length=200, null=True, choices=EDUCATION1, blank=True, default='ED_HIGH')
    education1_detail = models.CharField(verbose_name="(1-2)고등학교", max_length=250, null=True, blank=True)
    education1_end = models.DateField(verbose_name="(1-3)졸업년도",  null=True, blank=True)

    education2_level = models.CharField(verbose_name="(2-1)학위", max_length=200, null=True, choices=EDUCATION1, blank=True, default='ED_UNIV')
    education2_field = models.CharField(verbose_name="(2-2)전공", max_length=200, null=True, blank=True)
    education2_detail = models.CharField(verbose_name="(2-3)학교", max_length=250, null=True, blank=True)
    education2_start = models.DateField(verbose_name="(2-4)입학년도",  null=True, blank=True)
    education2_end = models.DateField(verbose_name="(2-5)졸업년도",  null=True, blank=True)

    education3_level = models.CharField(verbose_name="(3-1)학위", max_length=200, null=True, choices=EDUCATION1, blank=True)
    education3_field = models.CharField(verbose_name="(3-2)전공", max_length=200, null=True, blank=True)
    education3_detail = models.CharField(verbose_name="(3-3)학교", max_length=250, null=True, blank=True)
    education3_start = models.DateField(verbose_name="(3-4)입학년도",  null=True, blank=True)
    education3_end = models.DateField(verbose_name="(3-5)졸업년도",  null=True, blank=True)

    education4_level = models.CharField(verbose_name="(4-1)학위", max_length=200, null=True, choices=EDUCATION1, blank=True)
    education4_field = models.CharField(verbose_name="(4-2)전공", max_length=200, null=True, blank=True)
    education4_detail = models.CharField(verbose_name="(4-3)학교", max_length=250, null=True, blank=True)
    education4_start = models.DateField(verbose_name="(4-4)입학년도",  null=True, blank=True)
    education4_end = models.DateField(verbose_name="(4-5)졸업년도",  null=True, blank=True)

    education5_level = models.CharField(verbose_name="(5-1)학위", max_length=200, null=True, choices=EDUCATION1, blank=True)
    education5_field = models.CharField(verbose_name="(5-2)전공", max_length=200, null=True, blank=True)
    education5_detail = models.CharField(verbose_name="(5-3)학교", max_length=250, null=True, blank=True)
    education5_start = models.DateField(verbose_name="(5-4)입학년도",  null=True, blank=True)
    education5_end = models.DateField(verbose_name="(5-5)졸업년도",  null=True, blank=True)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # def __str__(self):
    #     return self.user.profile.name_korean



class EducationInternalTreatment(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    animal_treatment_number_registered = models.CharField(verbose_name="실험동물취급 교육이수번호", max_length=150, null=True, blank=True)
    animal_treatment_date_registered = models.DateField(verbose_name="실험동물취급 교육등록날짜",  null=True, blank=True)
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # def __str__(self):
    #     return self.user.profile.name_korean














###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                       IACUC Member
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################

class IACUCCommitteeMember(models.Model):
    committee_edition = models.IntegerField(null=True, blank=True)
    list_member_committee_all = models.JSONField(null=True, blank=True)

    member_committee_chairman = models.ForeignKey(Member, related_name="Committee_Chairman", on_delete=models.CASCADE, null=True, blank=True)
    member_committee_veterinarian = models.ForeignKey(Member, related_name="Committee_Veterinarian", on_delete=models.CASCADE, null=True, blank=True)
    member_committee_animalphd = models.ForeignKey(Member, related_name="Committee_AnimalphD", on_delete=models.CASCADE, null=True, blank=True)
    member_committee_normal = models.ForeignKey(Member, related_name="Committee_Normal", on_delete=models.CASCADE, null=True, blank=True)
    member_committee_extra_1 = models.ForeignKey(Member, related_name="Committee_extra_1", on_delete=models.CASCADE, null=True, blank=True)
    member_committee_extra_2 = models.ForeignKey(Member, related_name="Committee_extra_2", on_delete=models.CASCADE, null=True, blank=True)
    member_committee_extra_3 = models.ForeignKey(Member, related_name="Committee_extra_3", on_delete=models.CASCADE, null=True, blank=True)

    check_member_committee_chairman_outside = models.BooleanField(default=False)
    check_member_committee_veterinarian_outside = models.BooleanField(default=False)
    check_member_committee_animalphd_outside = models.BooleanField(default=False)
    check_member_committee_normal_outside = models.BooleanField(default=False)
    check_member_committee_extra_1_outside = models.BooleanField(default=False)
    check_member_committee_extra_2_outside = models.BooleanField(default=False)
    check_member_committee_extra_3_outside = models.BooleanField(default=False)
    # check_list
    check_activated = models.BooleanField(default=False)
    check_selected = models.BooleanField(default=False)
    check_discard = models.BooleanField(default=False)
    # system
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)









###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                              Calendar
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################



###################################################################################################################################################
# Calendar Meeting
############################


LIST_MEMBER_CALENDAR_EVENT_TIME_HOUR = (
    ('9', 'AM 9시'),
    ('10', 'AM 10시'),
    ('11', 'AM 11시'),
    ('12', 'PM 12시'),
    ('13', 'PM 1시'),
    ('14', 'PM 2시'),
    ('15', 'PM 3시'),
    ('16', 'PM 4시'),
    ('17', 'PM 5시'),
    ('EXTRA', '---------- 시간외 ----------'),
    ('7', 'AM 7시'),
    ('8', 'AM 8시'),
    ('18', 'PM 6시'),
    ('19', 'PM 7시'),
    ('20', 'PM 8시'),
    ('21', 'PM 9시'),
    ('22', 'PM 10시'),
    ('23', 'PM 11시'),
    ('24', 'AM 0시'),
)

LIST_MEMBER_CALENDAR_EVENT_TIME_MINUTE = (
    ('00', '00분'),
    ('15', '15분'),
    ('30', '30분'),
    ('45', '45분'),
    ('EXTRA', '---------- 세부 ----------'),
    ('5', '5분'),
    ('10', '10분'),
    ('20', '20분'),
    ('25', '25분'),
    ('35', '35분'),
    ('40', '40분'),
    ('50', '50분'),
    ('55', '55분'),
)


class Member_Meeting_Calendar(models.Model):
    #-------------------------------------------------------------------------------------------------------------------------------
    # Project Intro
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Host
    # contents
    meeting_title = models.CharField(max_length=240, null=True, blank=True) # 미팅 타이틀
    meeting_comment = models.CharField(max_length=240, null=True, blank=True)  # 미팅 코멘트
    list_meeting_attendee_member_id = models.JSONField(null=True, blank=True) # 미팅 참여자
    # meeting schedule
    meeting_time_hour = models.CharField(max_length=50, choices=LIST_MEMBER_CALENDAR_EVENT_TIME_HOUR, default=LIST_MEMBER_CALENDAR_EVENT_TIME_HOUR[0][0], blank=True)
    meeting_time_minute = models.CharField(max_length=50, choices=LIST_MEMBER_CALENDAR_EVENT_TIME_MINUTE, default=LIST_MEMBER_CALENDAR_EVENT_TIME_MINUTE[0][0], blank=True)
    # date/time
    date_meeting = models.DateField(null=True, blank=True)
    datetime_meeting = models.DateTimeField(null=True, blank=True)
    is_weekend = models.BooleanField(default=False)
    # check list
    check_team_leader_attendance_requested = models.BooleanField(default=False)  # True: Team Leader 참석 요청
    check_division_leader_attendance_requested = models.BooleanField(default=False)  # True: Division Leader 참석 요청
    check_company_leader_attendance_requested = models.BooleanField(default=False)  # True: Company Leader 참석 요청
    check_go_to_form_step2 = models.BooleanField(default=False)  # True: Calendar form step 2로 이동
    # system
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)





def get_upload_member_news_user(instance, dummy):
    return instance.path + "/" + instance.filename


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                              My Settings
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################




LIST_MEMBER_HOME_THEME = (
    ('NEWS', '새로운소식'), # 0
    ('WORKINGTIME', '근무시간'), # 1
    ('VACATION', '휴가'), # 2
    ('TODO', '오늘할일'), # 3
)

LIST_MEMBER_CALENDAR_TYPE = (
    ('FOLD', 'Fold Calendar'),  # 0
    ('TWC', 'Two Weeks Calendar'),  # 1
    # ('FWC', 'Four Weeks Calendar'),  # 2
    ('FULL', 'Full Calendar'),  # 3
    # ('CONTROL', 'Control Calendar'),  # 4
)

class Member_My_Settings(models.Model):
    # Keys
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #-----------------------------------------------------------------------------------------------------------------------------------

    #-----------------------------------------------------------------------------------------------------------------------------------
    # calendar

    calendar_meeting_selected = models.ForeignKey(Member_Meeting_Calendar, on_delete=models.CASCADE, null=True, blank=True)
    check_mode_register_calender = models.BooleanField(default=False)  # True : Calendar register form.
    # selected_year = models.IntegerField(null=True, blank=True)
    # selected_month = models.IntegerField(null=True, blank=True)
    # selected_day = models.IntegerField(null=True, blank=True)
    # Calendar Register
    date_meeting = models.DateField(null=True, blank=True)
    is_weekend = models.BooleanField(default=False)
    list_member_searched_for_host_id = models.JSONField(null=True, blank=True)
    # #-----------------------------------------------------------------------------------------------------------------------------------
    # # News (Notification)
    # news_type = models.CharField(max_length=100, choices=LIST_NEWS_ARTICLE_TYPE, default=LIST_NEWS_ARTICLE_TYPE[0][0], blank=True)
    #-----------------------------------------------------------------------------------------------------------------------------------
    # Working Time
    # workingtime = models.ForeignKey(Working_Time, on_delete=models.CASCADE, null=True, blank=True)
    check_mode_register_workingtime = models.BooleanField(default=False)  # True : Workint Time Register form.
    date_workingtime = models.DateField(null=True, blank=True)
    #-----------------------------------------------------------------------------------------------------------------------------------
    # Theme
    home_theme = models.CharField(max_length=100, choices=LIST_MEMBER_HOME_THEME, default=LIST_MEMBER_HOME_THEME[0][0], blank=True)
    #-----------------------------------------------------------------------------------------------------------------------------------
    # calendar
    #-----------------------------------------------------------------------------------------------------------------------------------
    calendar_type = models.CharField(max_length=100, choices=LIST_MEMBER_CALENDAR_TYPE, default=LIST_MEMBER_CALENDAR_TYPE[1][0], blank=True)
    calendar_meeting_selected = models.ForeignKey(Member_Meeting_Calendar, on_delete=models.CASCADE, null=True, blank=True)
    check_mode_register_calender = models.BooleanField(default=False)  # True : Calendar register form.

    def __str__(self):
        if self.owner.profile.name_korean:
            return self.owner.profile.name_korean
        else:
            return str(self.id)

