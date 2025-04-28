from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from hr.models import *
from member.models import *
# from project.models import *

############################################################################################################################
# Member 수동 등록 공통 함수
############################################################################################################################


class DateInput(forms.DateInput):
    input_type = 'date'




class Profile_Update_Date_Form(forms.Form):
    date_of_birth = forms.DateField(widget=DateInput)
    date_joined = forms.DateField(widget=DateInput)
    date_left = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super(Profile_Update_Date_Form, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False
        self.fields['date_joined'].required = False
        self.fields['date_left'].required = False



#--------------------------------------------------------------------------------------------------------------------------
# Profile Update
#--------------------------------------------------------------------------------------------------------------------------

class HR_Profile_Date_of_Birth_Register_Form(forms.Form):
    date_of_birth = forms.DateField(widget=DateInput, label="생일")

    def __init__(self, *args, **kwargs):
        super(HR_Profile_Date_of_Birth_Register_Form, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False


class HR_Profile_Date_Joined_Register_Form(forms.Form):
    date_joined = forms.DateField(widget=DateInput, label="입사일")

    def __init__(self, *args, **kwargs):
        super(HR_Profile_Date_Joined_Register_Form, self).__init__(*args, **kwargs)
        self.fields['date_joined'].required = False

class HR_Profile_Date_Left_Register_Form(forms.Form):
    date_left = forms.DateField(widget=DateInput, label="퇴사일")

    def __init__(self, *args, **kwargs):
        super(HR_Profile_Date_Left_Register_Form, self).__init__(*args, **kwargs)
        self.fields['date_left'].required = False









class Hr_Layout_Register_Member_Intro_Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'introduction',
        ]
        labels = {
            "introduction": "자기소개",
        }
        widgets = {
            'introduction': forms.Textarea(attrs={'cols': 70, 'rows': 3, 'placeholder':'자기소개글 작성'}),
        }


#--------------------------------------------------------------------------------------------------------------------------
# Member Profile 자동 등록 파일 업로드
#--------------------------------------------------------------------------------------------------------------------------

class HR_Member_Profile_Auto_Register_by_Fileupload(forms.ModelForm):
    class Meta:
        model = HR_Vacation_Document_Format_Management
        fields = [
            'file_member_profile_autoupload',
        ]
        labels = {
            'file_member_profile_autoupload': '',
        }

############################################################################################################################


class HrLayoutRegisterGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'group_name',
            'comment',
            'check_is_voronoigroup',
            'check_is_iacuc_member',
        ]


class HrLayoutRegisterCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'company_name',
            'comment',
            'address',
            'company_image',
            'postal_code',
            'business_reg_number',
            'office_phone_number',
        ]


class HrLayoutRegisterDivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = [
            'division_name',
            'comment',
            'check_division_ai',
        ]


class HrLayoutRegisterTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'team_name',
            'comment',
            'check_team_ai_math',
            'check_team_ai_dev',
        ]


class HrMemberSearchLogForm(forms.ModelForm):
    class Meta:
        model = MemberSearchLog
        fields = [
            'check_member_search_duplication',
            'search_keyword',
        ]



class HrTeamSearchLogForm(forms.ModelForm):
    class Meta:
        model = TeamSearchLog
        fields = [
            'check_team_search_duplication',
            'search_keyword',
        ]


class HrDivisionSearchLogForm(forms.ModelForm):
    class Meta:
        model = DivisionSearchLog
        fields = [
            'check_division_search_duplication',
            'search_keyword',
        ]


class HrCompanySearchLogForm(forms.ModelForm):
    class Meta:
        model = CompanySearchLog
        fields = [
            'check_company_search_duplication',
            'search_keyword',
        ]



class HR_Member_Date_Shift_Form(forms.Form):
    date_shift = forms.DateField(widget=DateInput, label='', required=False)







#--------------------------------------------------------------------------------------------------------------------------
# Member 등록 폼

#--------------------------------------------------------------------------------------------------------------------------

class HrLayoutRegisterMemberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name_korean',
            'nickname',
            'first_name',
            'last_name',
            'phone_office',
            'phone_mobile',
            'address',
        ]
        widgets = {
            # 'name_korean': ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            # 'md_simulation_file': '',
        }



class Member_Register_Date_Form(forms.Form):
    date_of_birth = forms.DateField(widget=DateInput)
    date_joined = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super(Member_Register_Date_Form, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False
        self.fields['date_joined'].required = False


#--------------------------------------------------------------------------------------------------------------------------
# Calendar 휴일 등록
#--------------------------------------------------------------------------------------------------------------------------

class HR_Calendar_National_Event_Register_From(forms.ModelForm):
    class Meta:
        model = HR_Calendar_Event
        fields = [
            'name_event',
            'type_event_national',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super(HR_Calendar_National_Event_Register_From, self).__init__(*args, **kwargs)
        self.fields['name_event'].required = True



class HR_Calendar_Voronoi_Event_Register_From(forms.ModelForm):
    class Meta:
        model = HR_Calendar_Event
        fields = [
            'name_event',
            'type_event_voronoi',
            'comment',
        ]

    def __init__(self, *args, **kwargs):
        super(HR_Calendar_Voronoi_Event_Register_From, self).__init__(*args, **kwargs)
        self.fields['name_event'].required = True


class HR_Holiday_Register_Date_Form(forms.Form):
    date_event = forms.DateField(widget=DateInput)



#--------------------------------------------------------------------------------------------------------------------------
# Vacation 정보 등록
#--------------------------------------------------------------------------------------------------------------------------

class HR_Vacation_Member_Date_Joined_Register_Form(forms.Form):
    date_joined = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Member_Date_Joined_Register_Form, self).__init__(*args, **kwargs)
        self.fields['date_joined'].required = False



class HR_Vacation_Member_Date_Issued_Register_Form(forms.Form):
    date_issued = forms.DateField(widget=DateInput, label='발행 일자')

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Member_Date_Issued_Register_Form, self).__init__(*args, **kwargs)
        self.fields['date_issued'].required = False



class HR_Vacation_Member_Date_Expired_Register_Form(forms.Form):
    date_expired = forms.DateField(widget=DateInput, label='만료 일자')

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Member_Date_Expired_Register_Form, self).__init__(*args, **kwargs)
        self.fields['date_expired'].required = False





#--------------------------------------------------------------------------------------------------------------------------
# Vacation Plan 등록
#--------------------------------------------------------------------------------------------------------------------------

class HR_Vacation_Plan_Datetime_Submission_Form(forms.Form):
    datetime_submission = forms.DateField(widget=DateInput, label='작성일')

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Plan_Datetime_Submission_Form, self).__init__(*args, **kwargs)
        self.fields['datetime_submission'].required = False


class HR_Vacation_Plan_Date_Vacation_Start_Form(forms.Form):
    date_vacation_start = forms.DateField(widget=DateInput, label='휴가개시일')

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Plan_Date_Vacation_Start_Form, self).__init__(*args, **kwargs)
        self.fields['date_vacation_start'].required = False


class HR_Vacation_Plan_Date_Vacation_End_Form(forms.Form):
    date_vacation_end = forms.DateField(widget=DateInput, label='휴가종료일')

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Plan_Date_Vacation_End_Form, self).__init__(*args, **kwargs)
        self.fields['date_vacation_end'].required = False






#--------------------------------------------------------------------------------------------------------------------------
# Vacation Promotion 수동공지 등록
#--------------------------------------------------------------------------------------------------------------------------

class Hr_Vacation_Promotion_Inform_Manually_Form(forms.ModelForm):
    class Meta:
        model = HR_Vacation_Promotion_Settings
        fields = [
            'text_promotion_additional_information',
        ]
        labels = {
            'text_promotion_additional_information': '수동 공지시 추가할 멘트',
        }
        widgets = {
            'text_promotion_additional_information': forms.Textarea(attrs={'cols': 70, 'rows': 3, 'placeholder':'수동 공지시 추가할 멘트 작성'}),
        }



#--------------------------------------------------------------------------------------------------------------------------
# Vacation Promotion Settings 등록
#--------------------------------------------------------------------------------------------------------------------------

class Hr_Vacation_Promotion_Settings_Update_Form(forms.ModelForm):
    class Meta:
        model = HR_Vacation_Promotion_Settings
        fields = [
            'delta_days_warning_y1_l1',
            'delta_days_warning_y1_l2',
            'delta_days_warning_y2_l1',
            'delta_days_warning_y2_l2',
            'check_activate_additional_information',
            'check_activate_additional_information_only_manual',
            'text_promotion_additional_information',
            'file_vc_promotion_report',
        ]
        labels = {
            'delta_days_warning_y1_l1': '신입 1차 알람 D-day 기준일',
            'delta_days_warning_y1_l2': '신입 2차 알람 D-day 기준일',
            'delta_days_warning_y2_l1': '다년차 1차 알람 D-day 기준일',
            'delta_days_warning_y2_l2': '다년차 2차 알람 D-day 기준일',
            'check_activate_additional_information': '추가로 강조하여 전달할 메모 활성화',
            'check_activate_additional_information_only_manual': '추가전달 내용을 수동 공지에만 적용',
            'text_promotion_additional_information' : '추가로 강조하여 전달할 메모 입력',
            'file_vc_promotion_report': '연차 유급휴가 사용시기 지정통보서 포맷',
        }
        widgets = {
            # 'text_promotion_additional_information': forms.Textarea(attrs={'cols': 70, 'rows': 3, 'placeholder':'수동 공지시 추가할 멘트 작성'}),
            'file_vc_promotion_report' : forms.FileInput(attrs={'filename': 'filename'})
        }



# form = Provider_Register_Form(request.POST, request.FILES, instance=q_provider)
#     if form.is_valid():
#         form.save()


#--------------------------------------------------------------------------------------------------------------------------
# Vacation 휴가계획서 자동 등록 파일 업로드
#--------------------------------------------------------------------------------------------------------------------------

class HR_Vacation_Plan_Auto_Register_by_Fileupload(forms.ModelForm):
    class Meta:
        model = HR_Vacation_Document_Format_Management
        fields = [
            'file_vc_plan_autoupload',
        ]
        labels = {
            'file_vc_plan_autoupload': '',
        }




#--------------------------------------------------------------------------------------------------------------------------
# 개시된 휴가계획서 수정하기
#--------------------------------------------------------------------------------------------------------------------------

class HR_Vacation_Plan_Date_Vacation_Start_Modify_Form(forms.Form):
    date_vacation_start = forms.DateField(widget=DateInput, label='휴가개시일')

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Plan_Date_Vacation_Start_Modify_Form, self).__init__(*args, **kwargs)
        self.fields['date_vacation_start'].required = False


class HR_Vacation_Plan_Date_Vacation_End_Modify_Form(forms.Form):
    date_vacation_end = forms.DateField(widget=DateInput, label='휴가종료일')

    def __init__(self, *args, **kwargs):
        super(HR_Vacation_Plan_Date_Vacation_End_Modify_Form, self).__init__(*args, **kwargs)
        self.fields['date_vacation_end'].required = False






#--------------------------------------------------------------------------------------------------------------------------
# Task Project 등록
#--------------------------------------------------------------------------------------------------------------------------

class HR_Task_Project_Register_Form(forms.ModelForm):
    class Meta:
        # model = Project_Simple
        fields = [
            'project_name',
            'status_project',
        ]



class HR_Task_Project_Update_Form(forms.ModelForm):
    class Meta:
        # model = Project_Simple
        fields = [
            'project_name',
            'status_project',
        ]


class HR_Task_Project_Register_Date_Start_Form(forms.Form):
    date_project_start = forms.DateField(widget=DateInput, label='프로젝트 개시일')

    def __init__(self, *args, **kwargs):
        super(HR_Task_Project_Register_Date_Start_Form, self).__init__(*args, **kwargs)
        self.fields['date_project_start'].required = False



class HR_Task_Project_Register_Date_End_Form(forms.Form):
    date_project_end = forms.DateField(widget=DateInput, label='프로젝트 종료일')

    def __init__(self, *args, **kwargs):
        super(HR_Task_Project_Register_Date_End_Form, self).__init__(*args, **kwargs)
        self.fields['date_project_end'].required = False






class HR_Workingtime_Plan_Reference_File_Form(forms.ModelForm):
    class Meta:
        model = Workingtime_Plan
        fields = [
            'reference_file',
        ]
        labels = {
            'reference_file': '',
        }
