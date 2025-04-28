import datetime
import os
from django.db.models import Q, Count, F, Value
from django.views.generic import *
from django.http import JsonResponse
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from member.models import *
from member.forms import *
from member.tasks import *
from member.functions import *
from hr.models import *
from hr.functions import check_authority_function, initiate_authority_for_superuser






def memberMyprofiledashboardView(request, pk):
    return HttpResponse('<h1> hi this is member dashboard page</h1>')



def memberPublicDashboardView(request, pk):
    # pk is q_member.id
    return HttpResponse('<h1> hi this my public dashboard page</h1>')



#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#
#                                                      Member Home
#
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# Member Home View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def member_home_view(request):
    # redirect dashboard
    if request.user.is_superuser == True:
        initiate_authority_for_superuser(request)
    #--------------------------------------------------------------------------------------------------------------------------
    # 로그인 하면 실행되야 하는 함수
    # 사용자 근무년수/달수 계산
    """
    q_profile = request.user.profile
    return_value = update_member_working_year_and_working_month(q_profile)
    if return_value == False:
        messages.warning(request, f'{q_profile.name_korean}님의 입사일 정보가 없습니다.')
    """
    from hr.functions import update_member_vacation_and_inform_to_promote_comsuming_vc
    # return_value = update_member_vacation_and_inform_to_promote_comsuming_vc(request, q_profile)

    # 사용자 연차 자동 발행
    #--------------------------------------------------------------------------------------------------------------------------
    # if 'voronoi.app' in request._current_scheme_host :
    #     return redirect('dashboard-home')
    # else :
    #     return redirect('my-home')

    # return redirect('my-home')
    return redirect('re-working-month-home')


    # list_access_level = ['auth_member',]
    # check_authority = check_authority_function(request, list_access_level)
    # if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
    #     template = 'member/member_home.html'
    # else:
    #     template = 'member/unauthorized_member.html'

    # if request.method == 'GET':
    #     context = member_home_function(request)
    #     return render(request, template, context)
    # if request.method == 'POST':
    #     return_value = member_home_function(request)
    #     if return_value == True:
    #         return redirect('member-home')
    #     elif return_value == False:
    #         return redirect('member-home')
    #     else:
    #         return redirect('member-home')





# #--------------------------------------------------------------------------------------------------------------------------
# # Member Daily Todo View
# #--------------------------------------------------------------------------------------------------------------------------

# @login_required(login_url='/security/login/')
# def member_daily_todo_view(request):
#     list_access_level = ['auth_member',]
#     check_authority = check_authority_function(request, list_access_level)
#     if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
#         template = 'member/member_daily_todo.html'
#     else:
#         template = 'member/unauthorized_member.html'

#     if request.method == 'GET':
#         context = member_daily_todo_function(request)
#         return render(request, template, context)
#     if request.method == 'POST':
#         return_value = member_daily_todo_function(request)
#         if return_value == True:
#             return redirect('member-daily-todo')
#         elif return_value == False:
#             return redirect('member-daily-todo')
#         else:
#             return redirect('member-daily-todo')



# #--------------------------------------------------------------------------------------------------------------------------
# # Member My Workingtime View
# #--------------------------------------------------------------------------------------------------------------------------

# @login_required(login_url='/security/login/')
# def member_my_workingtime_view(request):
#     list_access_level = ['auth_member',]
#     check_authority = check_authority_function(request, list_access_level)
#     if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
#         template = 'member/member_workingtime.html'
#     else:
#         template = 'member/unauthorized_member.html'

#     if request.method == 'GET':
#         context = member_my_workingtime_function(request)
#         return render(request, template, context)
#     if request.method == 'POST':
#         return_value = member_my_workingtime_function(request)
#         if return_value == True:
#             return redirect('member-my-workingtime')
#         elif return_value == False:
#             return redirect('member-my-workingtime')
#         else:
#             return redirect('member-my-workingtime')



# #--------------------------------------------------------------------------------------------------------------------------
# # Member My Vacation View
# #--------------------------------------------------------------------------------------------------------------------------

# @login_required(login_url='/security/login/')
# def member_my_vacation_view(request):
#     list_access_level = ['auth_member',]
#     check_authority = check_authority_function(request, list_access_level)
#     if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
#         template = 'member/member_my_vacation.html'
#     else:
#         template = 'member/unauthorized_member.html'

#     if request.method == 'GET':
#         context = member_my_vacation_function(request)
#         return render(request, template, context)
#     if request.method == 'POST':
#         return_value = member_my_vacation_function(request)
#         if return_value == True:
#             return redirect('member-my-vacation')
#         elif return_value == False:
#             return redirect('member-my-vacation')
#         else:
#             return redirect('member-my-vacation')




#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#
#                                                   User Register
#
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


def registerView(request):
    template = 'member/register.html'
    print('register member /////')

    if request.method == 'GET':
        context = register_user_by_form_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        print('register member /////post')
        return_value = register_user_by_form_function(request)
        print('register member ///// get the return value')
        if return_value == True:
            return redirect('member')
        else:
            messages.warning(
                    request, 'Hi Guest! You need verification code to register. Ask system manager')
            return redirect('member-register')




###################################################
#                  Working Status
###################################################


def workingStatusView(request, pk):
    template = 'member/member_workingstatus.html'
    if request.method == 'GET':
        context = workingStatusFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = workingStatusFunction(request, pk)
        if return_value == True:
            return redirect('member-workingstatus')
        else:
            messages.warning(request, 'Hi Guest! You need verification code to register. Ask system manager')
            return redirect('member')


###################################################
#                  Profile Register
###################################################


@login_required(login_url='/security/login/')
def profileView(request):
    username = request.user.username

    if request.method == 'POST':
        u_form = UserReigsterForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(
        #     request.POST, request.FILES, instance=request.user.profile)
        # if u_form.is_valid() and p_form.is_valid():
        if u_form.is_valid():
            u_form.save()
            # p_form.save()
            # print(p_form)
            username = u_form.cleaned_data.get('username')

            messages.success(
                request, f'{username}! Your account has been updated')
            return redirect('member')
    else:
        u_form = UserReigsterForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'username': username,
        # 'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'member/member_profile.html', context)



###################################################
#                  출/퇴근 등록
###################################################


@login_required(login_url='/security/login/')
def worktimeStartEndRegisterView(request, pk):
    template = 'member/member_worktimeregister.html'
    if request.method == 'GET':
        context = worktimeStartEndRegisterFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return redirect('member')
        # return redirect(reverse('member-worktimeregister', kwargs={'pk': pk}))

###################################################
#                  나의 프로파일 dashboard
###################################################


@login_required(login_url='/security/login/')
def myProfileDashboardView(request, pk):
    template = 'member/member_myprofiledashboard.html'
    print('======= My Profile Dashboard View Start !! ========')
    if request.method == 'GET':
        context = myProfileDashboardFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return redirect('member')


@login_required(login_url='/security/login/')
def myProfilePersonalInfoView(request, pk):
    template = 'member/member_myprofile_personalinfo.html'

    ##### Queryset #####
    profileform = ProfileUpdateForm(instance=request.user.profile)

    # Form 승인/거절 데이터 처리
    if request.method == 'POST':
        profileform = ProfileUpdateForm(
            request.POST, instance=request.user.profile)

        if profileform.is_valid():
            profileform.save()

            messages.success(
                request, f"Hi! {req_user.profile.name_korean}, You have updated profile information!")
            return redirect(reverse('member-myprofiledashboard', kwargs={'pk': pk}))
        else:
            messages.warning(
                request, f"Hi! {req_user.profile.name_korean}, You have failed updating profile information!")
            return redirect('member')
    else:
        print('POST전송없이 페이지정보요청')
    context = {
        'profileform': profileform,
    }
    return render(request, template, context)


@login_required(login_url='/security/login/')
def myProfileEducationInfoView(request, pk):
    template = 'member/member_myprofile_educationinfo.html'

    ##### Queryset #####
    educationform = EducationUpdateForm(instance=request.user.education)

    # Form 승인/거절 데이터 처리
    if request.method == 'POST':
        educationform = EducationUpdateForm(
            request.POST, instance=request.user.education)

        if educationform.is_valid():
            educationform.save()

            messages.success(
                request, f"Hi! {req_user.profile.name_korean}, You have updated profile information!")
            return redirect(reverse('member-myprofiledashboard', kwargs={'pk': pk}))
        else:
            messages.warning(
                request, f"Hi! {req_user.profile.name_korean}, You have failed updating profile information!")
            return redirect('member-myprofiledashboard')
    else:
        print('POST전송없이 페이지정보요청')
    context = {
        'educationform': educationform,
    }
    return render(request, template, context)


@login_required(login_url='/security/login/')
def myProfileWorkExperienceInfoView(request, pk):
    template = 'member/member_myprofile_workexperienceinfo.html'

    ##### Queryset #####
    careerform = CareerUpdateForm(instance=request.user.career)

    # Form 승인/거절 데이터 처리
    if request.method == 'POST':
        careerform = CareerUpdateForm(
            request.POST, instance=request.user.career)

        if careerform.is_valid():
            careerform.save()

            messages.success(
                request, f"Hi! {req_user.profile.name_korean}, You have updated profile information!")
            return redirect(reverse('member-myprofiledashboard', kwargs={'pk': pk}))
        else:
            messages.warning(
                request, f"Hi! {req_user.profile.name_korean}, You have failed updating profile information!")
            return redirect('member-myprofiledashboard')
    else:
        print('POST전송없이 페이지정보요청')
    context = {
        'careerform': careerform,
    }
    return render(request, template, context)

###################################################
#                  휴가 등록
###################################################


@login_required(login_url='/security/login/')
def vacationRegisterView(request, pk):

    template = 'member/member_vacationregister.html'
    ## 연차 등록하기 Form을 Submit했을 경우에만 작동 ######################################
    if request.method == 'GET':
        context = vacationRegisterFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return redirect(reverse('member-vacationregister', kwargs={'pk': pk}))





###################################################
#                  휴가 등록 취소
###################################################
@login_required(login_url='/security/login/')
def vacationRequestCancelView(request, pk):
    print('==== Start vacationRequestCancelView ====')
    template = 'member/member_vacationrequestcancel.html'
    if request.method == 'GET':
        context = vacationRequestCancelFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return redirect('member')



###################################################
#                  나의 휴가 리스트
###################################################


@login_required(login_url='/security/login/')
def vacationMylistView(request, pk):

    template = 'member/member_vacationmylist.html'

    # get a holiday count
    q_vacation = Vacation.objects.get(user=request.user)
    vacationusedlog_qs = VacationUsedLog.objects.filter(
        vacation=q_vacation)

    # print('-------------')
    print(request.user.id)

    context = {
        'q_vacation': q_vacation,
        'vacationusedlog_qs': vacationusedlog_qs,
    }
    return render(request, template, context)


###################################################
#                  휴가 디테일 뷰
###################################################


@login_required(login_url='/security/login/')
def vacationDetailView(request, pk):

    template = 'member/member_vacationdetail.html'

    # get a holiday count
    q_vacation = Vacation.objects.get(user=request.user)
    vacationusedlog_qs = VacationUsedLog.objects.filter(
        vacation=q_vacation).order_by('-date_updated')
    vacationusedlog_q = VacationUsedLog.objects.get(id=pk)
    # print('-------------')
    print(request.user.id)

    context = {
        'q_vacation': q_vacation,
        'vacationusedlog_qs': vacationusedlog_qs,
        'vacationusedlog_q': vacationusedlog_q,
    }
    return render(request, template, context)


###################################################
#                  휴가 승인 대기 리스트
###################################################
@login_required(login_url='/security/login/')
def vacationApprovallistSemiView(request, pk):
    template = 'member/member_vacationapprovallistsemi.html'
    areyousupervisor = areYouSupervisor2(request)
    iamsuperviser = areyousupervisor[0]
    count_iamsupervisor = areyousupervisor[1]
    list_iamsupervisor = areyousupervisor[2]

    context = {
        'iamsuperviser': iamsuperviser,
        'count_iamsupervisor': count_iamsupervisor,
        'list_iamsupervisor': list_iamsupervisor,
    }
    return render(request, template, context)


@login_required(login_url='/security/login/')
def vacationApprovallistSemifinalView(request, pk):
    template = 'member/member_vacationapprovallistsemifinal.html'
    areyousupervisor = areYouSupervisor2(request)
    iamsuperviser = areyousupervisor[0]
    count_iamsupervisor = areyousupervisor[1]
    list_iamsupervisor = areyousupervisor[2]

    context = {
        'iamsuperviser': iamsuperviser,
        'count_iamsupervisor': count_iamsupervisor,
        'list_iamsupervisor': list_iamsupervisor,
    }

    return render(request, template, context)


@login_required(login_url='/security/login/')
def vacationApprovallistFinalView(request, pk):
    template = 'member/member_vacationapprovallistfinal.html'

    areyousupervisor = areYouSupervisor2(request)
    iamsuperviser = areyousupervisor[0]
    count_iamsupervisor = areyousupervisor[1]
    list_iamsupervisor = areyousupervisor[2]

    # # get a holiday count
    # vacationusedlog_qs = VacationUsedLog.objects.filter(
    #     vc_supervisor_lv4=pk).order_by('date_updated')

    context = {
        'iamsuperviser': iamsuperviser,
        'count_iamsupervisor': count_iamsupervisor,
        'list_iamsupervisor': list_iamsupervisor,
    }
    return render(request, template, context)


@login_required(login_url='/security/login/')
def vacationApprovallistView(request, pk):
    template = 'member/member_vacationapprovallist.html'
    areyousupervisor = areYouSupervisor2(request)
    iamsuperviser = areyousupervisor[0]
    count_iamsupervisor = areyousupervisor[1]
    list_iamsupervisor = areyousupervisor[2]
    print(list_iamsupervisor[0].vc_approved_final)
    # # get a holiday count
    # vacationusedlog_qs = VacationUsedLog.objects.filter(
    #     vc_supervisor_lv4=pk).order_by('date_updated')
    context = {
        'iamsuperviser': iamsuperviser,
        'count_iamsupervisor': count_iamsupervisor,
        'list_iamsupervisor': list_iamsupervisor,
    }

    return render(request, template, context)



###################################################
#                  휴가 승인/거절 등록
###################################################


@login_required(login_url='/security/login/')
def vacationApprovalFormSemiView(request, pk):

    template = 'member/member_vacationapprovalformsemi.html'

    ## Queryset ##############################
    # q_vacation = Vacation.objects.get(user=request.user)
    vacationusedlog_q = VacationUsedLog.objects.get(id=pk)

    ################ 휴가 관리 ##################
    # for update purpose #
    vcapvform = VacationApprovalSemiForm(instance=vacationusedlog_q)
    # Form 승인/거절 데이터 처리
    if request.method == 'POST':
        get_approve = get_approval_vacation2(request, pk)
        if get_approve == True:
            messages.success(
                request, f"Hi! {req_user.profile.name_korean}, You have approved {vacationusedlog_q.vacation.user.profile.name_korean}'s vacation!")
        else:
            messages.warning(
                request, f"Hi! {req_user.profile.name_korean}, You have declined {vacationusedlog_q.vacation.user.profile.name_korean}'s vacation!")
        return redirect('member')

    context = {
        # 'q_vacation': q_vacation,
        'vacationusedlog_q': vacationusedlog_q,
        'vcapvform': vcapvform,
        'pk': pk,
    }
    return render(request, template, context)


@login_required(login_url='/security/login/')
def vacationApprovalFormSemifinalView(request, pk):

    template = 'member/member_vacationapprovalformsemifinal.html'

    ## Queryset ##############################
    # q_vacation = Vacation.objects.get(user=request.user)
    vacationusedlog_q = VacationUsedLog.objects.get(id=pk)

    ################ 휴가 관리 ##################
    # for update purpose #
    vcapvform = VacationApprovalSemifinalForm(instance=vacationusedlog_q)
    # Form 승인/거절 데이터 처리
    if request.method == 'POST':
        get_approve = get_approval_vacation2(request, pk)
        if get_approve == True:
            messages.success(
                request, f"Hi! {req_user.profile.name_korean}, You have approved {vacationusedlog_q.vacation.user.profile.name_korean}'s vacation!")
        else:
            messages.warning(
                request, f"Hi! {req_user.profile.name_korean}, You have declined {vacationusedlog_q.vacation.user.profile.name_korean}'s vacation!")
        return redirect('member')

    context = {
        # 'q_vacation': q_vacation,
        'vacationusedlog_q': vacationusedlog_q,
        'vcapvform': vcapvform,
        'pk': pk,
    }
    return render(request, template, context)


@login_required(login_url='/security/login/')
def vacationApprovalFormFinalView(request, pk):

    template = 'member/member_vacationapprovalformfinal.html'

    ## Queryset ##############################
    # q_vacation = Vacation.objects.get(user=request.user)
    vacationusedlog_q = VacationUsedLog.objects.get(id=pk)

    ################ 휴가 관리 ##################
    # for update purpose #
    vcapvform = VacationApprovalFinalForm(instance=vacationusedlog_q)
    # Form 승인/거절 데이터 처리
    if request.method == 'POST':
        get_approve = get_approval_vacation2(request, pk)
        if get_approve == True:
            messages.success(
                request, f"Hi! {req_user.profile.name_korean}, You have approved {vacationusedlog_q.vacation.user.profile.name_korean}'s vacation!")
        else:
            messages.warning(
                request, f"Hi! {req_user.profile.name_korean}, You have declined {vacationusedlog_q.vacation.user.profile.name_korean}'s vacation!")
        return redirect('member')

    context = {
        # 'q_vacation': q_vacation,
        'vacationusedlog_q': vacationusedlog_q,
        'vcapvform': vcapvform,
        'pk': pk,
    }
    return render(request, template, context)





################################################################################################
################################################################################################
################################################################################################
#
#                                       Authority
#
################################################################################################
################################################################################################
################################################################################################


@login_required(login_url='/security/login/')
def authorityHomeView(request):
    template = 'member/member_authority_home.html'
    if request.method == 'GET':
        print('get!')
        context = authorityHomeFunction(request)
        print('context')
        return render(request, template, context)
    if request.method == 'POST':
        return_value = authorityHomeFunction(request)
        return redirect('member-authority-home')
