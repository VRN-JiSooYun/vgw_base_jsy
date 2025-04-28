import pytz
import calendar
calendar.setfirstweekday(calendar.SUNDAY)
import datetime
import os
from django.db.models import Q, Count, F, Value
# import pandas as pd

from django.views.generic import *
from django.http import JsonResponse
from django.conf import settings

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
# from django.views.generic import *
from member.forms import *
from member.models import *
from hr.functions import *
from hr.models import *
from home.models import *
from home.functions import *



###################################################################################################################################################
#
# 전략
# 1. Asynchronous Communication 적용 없이 작동할 수 있도록(사용자 Action에 따른 쿼리 생성으로 대체)
# 2. 추후 서버에서 Asynchronous Communication 셋업이 되면 수정 적용
#
###################################################################################################################################################

###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                       Daily Check / Query Generation
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


#--------------------------------------------------------------------------------------------------------------------------
# 입력한 날이 주말 여부 체크 함수
#--------------------------------------------------------------------------------------------------------------------------
def member_check_date_weekend(input_date):
    # input_date : datetime.date() 오브젝트  /  datetime.datetime.today()
    # 주말체크
    list_day_of_week = [5, 6]
    day_of_week = input_date.weekday()
    if day_of_week not in list_day_of_week:
        check_weekend = False
    else:
        check_weekend = True
    return check_weekend


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                     Member Vacation Control
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


#--------------------------------------------------------------------------------------------------------------------------
# 근무년차 계산 알고리즘 Ver.1.2
#     # Profile 근무년차 업데이트
#     delta_working_days = ls_today - date_joined
#     delta_working_days_str = str(delta_working_days)
#     delta_working_days_int = int(delta_working_days_str.split(' ')[0])
#     status_working_year_now = (delta_working_days_int//365) + 1
# delta_working_days = ls_today - date_joined
# delta_working_days_str = str(delta_working_days)
# delta_working_days_int = int(delta_working_days_str.split(' ')[0])
# status_working_year_now = (delta_working_days_int//365) + 1
# if status_working_year_now < status_working_year:
#     status_working_year = status_working_year_now   # 오늘날짜 근무년차보다 클 수 없다.
#--------------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------------------
# 근무년차 업데이트, 근무년차 계산 알고리즘 Ver.1
#--------------------------------------------------------------------------------------------------------------------------
# status_working_year = (delta_joined_date_to_today // time_delta_365days) + 1  # 년차 계산법


#--------------------------------------------------------------------------------------------------------------------------
# 근무년차 업데이트, 근무년차 계산 알고리즘 Ver.2
#--------------------------------------------------------------------------------------------------------------------------
def calculate_status_working_year_ver_2(q_profile, date_selected):
    date_joined = q_profile.date_joined
    year_selected = date_selected.year
    month_selected= date_selected.month
    day_selected = date_selected.day
    if date_joined is None:
        return False
    year_joined = date_joined.year
    month_joined = date_joined.month
    day_joined = date_joined.day

    delta_year = year_selected - year_joined
    delta_month = month_selected - month_joined
    delta_day = day_selected - day_joined

    if delta_month < 0:
        status_working_year_selected = delta_year
    else:
        if delta_month == 0:
            if delta_day < 0:
                status_working_year_selected = delta_year
            else:
                status_working_year_selected = delta_year + 1
        else:
            status_working_year_selected = delta_year + 1
    return status_working_year_selected


#--------------------------------------------------------------------------------------------------------------------------
# 멤버 근무년수 관련 종합 정보 획득함수 (2023-3-3)
#
# status_working_month_first_year : 첫 해의 근무달수, 첫해가 넘어가면 11
# status_working_year : 근무년수 (1년(365일) 못채웠으면 1년차, 1년이 지나면 2년차)
# delta_year_joined : 입사일 기준 만 근무 년수
# delta_month_joined : 입사일 기준 만 근무 달수
# date_workingyear_start : 해당 근무년차의 근무시작일
# date_workingyear_end : 해당 근무년차의 근무종료일
#--------------------------------------------------------------------------------------------------------------------------
def calculate_status_working_year_overall(q_profile):
    date_joined = q_profile.date_joined
    ls_today = datetime.date.today()
    ls_year = ls_today.year
    ls_month = ls_today.month
    ls_day = ls_today.day

    year_joined = date_joined.year
    month_joined = date_joined.month
    day_joined = date_joined.day

    time_delta_1day = datetime.timedelta(days=1)
    time_delta_365days = datetime.timedelta(days=365)
    delta_joined_date_to_today = ls_today - date_joined  # 입사한 날부터 오늘까지 델타시간

    # 근무년차 업데이트, 근무년차 계산 알고리즘 Ver.2
    date_joined = q_profile.date_joined
    status_working_year_selected = calculate_status_working_year_ver_2(q_profile, ls_today)
    data = {
        'status_working_year': status_working_year_selected,
    }
    Profile.objects.filter(id=q_profile.id).update(**data)
    q_profile.refresh_from_db()
    status_working_year = q_profile.status_working_year
    # print('status_working_year', status_working_year, '년차')

    delta_year_joined = 0
    delta_month_joined = 0
    if status_working_year == 1:
        if ls_year == year_joined:
            # 입사일과 같은 해이면
            delta_month_joined = ls_month - month_joined
        else:
            # 해가 넘어가면
            delta_month_joined = ls_month + (12 - month_joined)

        if ls_day - day_joined >= 0:
            # 오늘이 입사일의 day를 지난 경우
            delta_month_joined = delta_month_joined
        else:
            # 오늘이 입사일의 day를 못지난 경우
            delta_month_joined = delta_month_joined - 1
        # 1년차의 첫해 근무달수
        status_working_month_first_year = delta_month_joined
        # status_working_year =  status_working_year
    else:
        # 다년차의 첫해 근무달수 == 11로 고정
        status_working_month_first_year = 11
        if ls_day - day_joined >= 0:
        # 오늘이 입사일의 day를 지난 경우
            if ls_month - month_joined > 0:
                # print('case 1')
                delta_year_joined = ls_year - year_joined
                delta_month_joined = ls_month - month_joined
                # 입사일과 같은 해이면
            else:
                # print('case 2')
                delta_year_joined = ls_year - year_joined - 1
                # 해가 넘어가면
                delta_month_joined = ls_month + (12 - month_joined)
        else:
        # 오늘이 입사일의 day를 못지난 경우
            if ls_month - month_joined > 0:
                # print('case 3')
                delta_year_joined = ls_year - year_joined
                delta_month_joined = ls_month - month_joined -1
                # 입사일과 같은 해이면
            else:
                # print('case 4')
                delta_year_joined = ls_year - year_joined -1
                # 해가 넘어가면
                delta_month_joined = ls_month + (12 - month_joined) -1
            pass
    # status_working_year = delta_year_joined + 1
    # print('status_working_year2', status_working_year)

    # 해당근무년차의 근무시작일
    date_workingyear_start = datetime.date(year_joined + delta_year_joined, month_joined , day_joined)

    # 해당근무년차의 근무종료일
    date_joined_ond_day_ago = date_joined - time_delta_1day
    if month_joined == 1 and day_joined == 1:
        date_workingyear_end = datetime.date(year_joined + delta_year_joined, date_joined_ond_day_ago.month, date_joined_ond_day_ago.day)
    else:
        date_workingyear_end = datetime.date(year_joined + delta_year_joined + 1, date_joined_ond_day_ago.month, date_joined_ond_day_ago.day)

    return status_working_month_first_year, status_working_year, delta_year_joined, delta_month_joined, date_workingyear_start, date_workingyear_end


#--------------------------------------------------------------------------------------------------------------------------
# 프로필에 근무년수 업데이트 하기 (그룹웨어 접속시 실행)
#--------------------------------------------------------------------------------------------------------------------------
def update_member_working_year_and_working_month(q_profile):
    #--------------------------------------------------------------------------------------------------------------------------
    # 년차 / 월차 계산하기
    date_joined = q_profile.date_joined
    if date_joined is None:
        return False

    from hr.functions import get_my_position_title_and_update_to_q_hrlayout, get_my_highest_q_hrlayout_among_many
    q_hrlayout_highest = get_my_highest_q_hrlayout_among_many(q_profile)
    position_str = get_my_position_title_and_update_to_q_hrlayout(q_hrlayout_highest)
    return_value = calculate_status_working_year_overall(q_profile)
    status_working_month_first_year = return_value[0]
    status_working_year = return_value[1]
    delta_year_joined = return_value[2]
    delta_month_joined = return_value[3]
    date_workingyear_start = return_value[4]
    date_workingyear_end = return_value[5]
    data = {
        'status_working_month_first_year': status_working_month_first_year,
        'status_working_year': status_working_year,
        'delta_year_joined': delta_year_joined,
        'delta_month_joined': delta_month_joined,
        'date_workingyear_start': date_workingyear_start,
        'date_workingyear_end': date_workingyear_end,
        'position': position_str,
    }
    Profile.objects.filter(id=q_profile.id).update(**data)
    q_profile.refresh_from_db()
    return q_profile





###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                       Member Old 메인 함수
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################



#--------------------------------------------------------------------------------------------------------------------------
# Register User
#--------------------------------------------------------------------------------------------------------------------------
def register_user_by_form_function(request):
    # Register one by one via Register Page
    # print('here///////////////////////1')
    if request.method == 'GET':
        u_form = UserReigsterForm()
        p_form = ProfileUpdateForm()
        b_form = ProfileUpdateBirthdayForm()
        c_form = UserRegisterCodeForm()
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'b_form': b_form,
            'c_form':c_form,
        }
        return context

    if request.method == 'POST':
        # print('here///////////////////////2')
        u_form = UserReigsterForm(request.POST)
        p_form = ProfileUpdateForm(request.POST)
        input_date_of_birth = request.POST.get('date_of_birth')
        input_date_joined = request.POST.get('date_joined')
        input_code = request.POST.get('code')
        date_of_birth = datetime.datetime.strptime(input_date_of_birth, '%Y-%m-%d').date()
        date_joined = datetime.datetime.strptime(input_date_joined, '%Y-%m-%d').date()

        if input_code == 'jason0506':
            # print('here///////////////////////3')

            if u_form.is_valid():
                # print('here///////////////////////4')
                u_form.save()
                q_user = User.objects.last()
                username = u_form.cleaned_data.get('username')
                email = u_form.cleaned_data.get('email')
                messages.success(
                    request, f'{username}! Your account has been created')
                data = {
                    'user':q_user,
                    'member_name':username,
                }
                Member.objects.create(**data)
                q_member = Member.objects.last()

            # Create Profile and Update more information
            if p_form.is_valid():
                p_form.save()
                q_profile = Profile.objects.last()
                data = {
                    'user': q_user,
                    'email': email,
                    'member': q_member,
                    'nickname' : username,
                    'date_of_birth': date_of_birth,
                    'date_joined': date_joined,
                }
                Profile.objects.filter(id=q_profile.id).update(**data)

            # Create Vacation, Career, Education, Education Internal
            data = {
                'user': q_user,
            }
            Career.objects.create(**data)
            Education.objects.create(**data)
            EducationInternalTreatment.objects.create(**data)

            return True
        else:
            return False





###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                       개인 접속 권한 요약/요청
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################



def authorityHomeFunction(request):
    # prerequisites
    q_authority = Authority.objects.filter(check_discard=False).last()

    if q_authority is not None:
        q_hrlayout = HR_Layout.objects.filter(Q(check_discard=False) & Q(member__user=request.user)).last()
    else:
        q_hrlayout = None

    # print('q_uesr', q_user)
    q_profile = Profile.objects.filter(Q(check_discard=False) & Q(user=request.user)).last()
    qs_profile = Profile.objects.filter(user=request.user)

    # print('q_profile', q_profile)
    # print('qs_profile', qs_profile)
    ###################################################
    if request.method == 'GET':
        context = {
            'q_hrlayout': q_hrlayout,
            'q_authority': q_authority,
        }
        return context
    ###################################################
    if request.method == 'POST':
        # Panel 페이지 넘기기 ################################################################
        if request.POST.get('button-check-authpanel-status') == 'true':

            current_check_status_a = q_profile.check_auth_panel_status_a
            current_check_status_b = q_profile.check_auth_panel_status_b
            if current_check_status_a == True and current_check_status_b == True:
                current_check_status_a = True
                current_check_status_b = False
            else:
                if current_check_status_a == True and current_check_status_b == False:
                    current_check_status_a = False
                    current_check_status_b = False
                else:
                    current_check_status_a = True
                    current_check_status_b = True
            data = {
                'check_auth_panel_status_a': current_check_status_a,
                'check_auth_panel_status_b': current_check_status_b,
            }
            Profile.objects.filter(id=q_profile.id).update(**data)
        return True























