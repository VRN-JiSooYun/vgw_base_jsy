import io
import csv
import os
import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from hr.functions import *
from hr.models import *
# from hr.serializers import *
from member.models import *
from member.functions import *




@login_required(login_url='/security/login/')
def hrHomeView(request):
    template = 'hr/hr_home.html'
    if request.method == 'GET':
        context = hrHomeFunction(request)
        return render(request, template, context)



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
#                                                       조직도 디자인
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





@login_required(login_url='/security/login/')
def hrLayoutHomeView(request):
    template = 'hr/hr_layout_home.html'
    if request.method == 'GET':
        context = hrLayoutHomeFunction(request)
        return render(request, template, context)


############################################################################################################################
# 조직도 디자인 홈 View
############################################################################################################################

@login_required(login_url='/security/login/')
def hrLayoutDesignHomeView(request):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_home.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_layout_design_home_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_layout_design_home_function(request)
        if return_value == True:
            return redirect('hr-layout-design-home')
        else:
            return return_value


############################################################################################################################
# 조직도 디자인
############################################################################################################################

@login_required(login_url='/security/login/')
def hrLayoutDesignM2TStep1View(request):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_m2t_step1.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignM2TStep1Function(request)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hrLayoutDesignM2TStep1Function(request)
        if pk == False:
            return redirect('hr-layout-design-m2t-step1')
        else:
            return redirect(reverse('hr-layout-design-m2t-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignM2TStep2View(request, pk):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_m2t_step2.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignM2TStep2Function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hrLayoutDesignM2TStep2Function(request, pk)
        return redirect(reverse('hr-layout-design-m2t-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignT2DStep1View(request):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_t2d_step1.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignT2DStep1Function(request)
        return render(request, template, context)
    if request.method == 'POST':
        # pk is q_t2d_last.id
        pk = hrLayoutDesignT2DStep1Function(request)
        if pk == False:
            return redirect('hr-layout-design-t2d-step1')
        else:
            return redirect(reverse('hr-layout-design-t2d-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignT2DStep2View(request, pk):
    # pk is q_t2d_last.id
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_t2d_step2.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignT2DStep2Function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hrLayoutDesignT2DStep2Function(request, pk)
        if return_value == False:
            return redirect(reverse('hr-layout-design-t2d-step2', kwargs={'pk': pk}))
        else:
            return redirect(reverse('hr-layout-design-t2d-step2', kwargs={'pk': return_value}))


@login_required(login_url='/security/login/')
def hrLayoutDesignM2DStep1View(request):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_m2d_step1.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignM2DStep1Function(request)
        return render(request, template, context)
    if request.method == 'POST':
        # pk is q_m2d_last.id
        pk = hrLayoutDesignM2DStep1Function(request)
        if pk == False:
            return redirect('hr-layout-design-m2d-step1')
        else:
            return redirect(reverse('hr-layout-design-m2d-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignM2DStep2View(request, pk):
    # pk is q_m2d_last.id
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_m2d_step2.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignM2DStep2Function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hrLayoutDesignM2DStep2Function(request, pk)
        return redirect(reverse('hr-layout-design-m2d-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignD2CStep1View(request):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_d2c_step1.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignD2CStep1Function(request)
        return render(request, template, context)
    if request.method == 'POST':
        # pk is q_d2c_last.id
        pk = hrLayoutDesignD2CStep1Function(request)
        if pk == False:
            return redirect('hr-layout-design-d2c-step1')
        else:
            return redirect(reverse('hr-layout-design-d2c-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignD2CStep2View(request, pk):
    # pk is q_d2c_last.id
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_d2c_step2.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignD2CStep2Function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hrLayoutDesignD2CStep2Function(request, pk)
        if return_value == False:
            return redirect(reverse('hr-layout-design-d2c-step2', kwargs={'pk': pk}))
        else:
            return redirect(reverse('hr-layout-design-d2c-step2', kwargs={'pk': return_value}))


@login_required(login_url='/security/login/')
def hrLayoutDesignM2CStep1View(request):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_m2c_step1.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignM2CStep1Function(request)
        return render(request, template, context)
    if request.method == 'POST':
        # pk is q_m2c_last.id
        pk = hrLayoutDesignM2CStep1Function(request)
        if pk == False:
            return redirect('hr-layout-design-m2c-step1')
        else:
            return redirect(reverse('hr-layout-design-m2c-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignM2CStep2View(request, pk):
    # pk is q_m2c_last.id
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_m2c_step2.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignM2CStep2Function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hrLayoutDesignM2CStep2Function(request, pk)
        return redirect(reverse('hr-layout-design-m2c-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignC2GStep1View(request):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_c2g_step1.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignC2GStep1Function(request)
        return render(request, template, context)
    if request.method == 'POST':

        pk = hrLayoutDesignC2GStep1Function(request)
        if pk == False:
            return redirect('hr-layout-design-c2g-step1')
        else:
            # pk is q_c2g__last.id
            return redirect(reverse('hr-layout-design-c2g-step2', kwargs={'pk': pk}))


@login_required(login_url='/security/login/')
def hrLayoutDesignC2GStep2View(request, pk):
    list_access_level = ['auth_hr',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_design_c2g_step2.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutDesignC2GStep2Function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        # pk is q_c2g_last.id
        return_value = hrLayoutDesignC2GStep2Function(request, pk)
        if return_value == False:
            return redirect(reverse('hr-layout-design-c2g-step2', kwargs={'pk': pk}))
        else:
            return redirect(reverse('hr-layout-design-c2g-step2', kwargs={'pk': return_value}))





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
#                                              조직도 요소 (멤버/팀/부서/회사/그룹) 등록 / 업데이트 / 삭제
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


############################################################################################################################
# Group
############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 그룹 관리
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutRegisterGroupView(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_group_register.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutRegisterGroupFunction(request)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hrLayoutRegisterGroupFunction(request)
        return redirect('hr-layout-register-group')


#--------------------------------------------------------------------------------------------------------------------------
# 그룹 업데이트
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutUpdateGroupView(request, pk):
    # pk is q_group.id
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_group_update.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutUpdateGroupFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hrLayoutUpdateGroupFunction(request, pk)
        if return_value == 'delete':
            return redirect('hr-layout-register-group')
        else:
            return redirect(reverse('hr-layout-update-group', kwargs={'pk': pk}))


# #--------------------------------------------------------------------------------------------------------------------------
# # 그룹 삭제
# #--------------------------------------------------------------------------------------------------------------------------
# @login_required(login_url='/security/login/')
# def hrLayoutDeleteGroupView(request, pk):
#     # pk is q_group.id
#     list_access_level = ['auth_hr_design',]
#     check_authority = check_authority_function(request, list_access_level)
#     if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
#         if request.method == 'POST':
#             q_group = Group.objects.get(id=pk)
#             q_group.delete()
#             messages.warning(request, f"Hi! {request.user}, 선택한 Group를 삭제하였습니다!")
#             return redirect('hr-layout-register-group')
#     else:
#         messages.warning(request, f"Hi! {request.user}, 선택한 Group를 삭제할 권한이 없습니다!")
#         return redirect('hr-layout-register-group')




############################################################################################################################
# Company
############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 회사 관리
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutRegisterCompanyView(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_company_register.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutRegisterCompanyFunction(request)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hrLayoutRegisterCompanyFunction(request)

        return redirect('hr-layout-register-company')


#--------------------------------------------------------------------------------------------------------------------------
# 회사 업데이트
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutUpdateCompanyView(request, pk):
    # pk is q_company.id
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_company_update.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutUpdateCompanyFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hrLayoutUpdateCompanyFunction(request, pk)
        if return_value == 'delete':
            return redirect('hr-layout-register-company')
        else:
            return redirect(reverse('hr-layout-update-company', kwargs={'pk': pk}))


# #--------------------------------------------------------------------------------------------------------------------------
# # 회사 삭제
# #--------------------------------------------------------------------------------------------------------------------------
# @login_required(login_url='/security/login/')
# def hrLayoutDeleteCompanyView(request, pk):
#     # pk is q_company.id
#     list_access_level = ['auth_hr_design',]
#     check_authority = check_authority_function(request, list_access_level)
#     if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
#         if request.method == 'POST':
#             q_company = Company.objects.get(id=pk)
#             q_company.delete()
#             messages.warning(request, f"Hi! {request.user}, 선택한 Company를 삭제하였습니다!")
#             return redirect('hr-layout-register-company')
#     else:
#         messages.warning(request, f"Hi! {request.user}, 선택한 Company 삭제할 권한이 없습니다!")
#         return redirect('hr-layout-register-company')



############################################################################################################################
# Division
############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 부서 관리
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutRegisterDivisionView(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_division_register.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_layout_register_division_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hr_layout_register_division_function(request)

        return redirect('hr-layout-register-division')

#--------------------------------------------------------------------------------------------------------------------------
# 부서 업데이트
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutUpdateDivisionView(request, pk):
    # pk is q_division.id
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_division_update.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutUpdateDivisionFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hrLayoutUpdateDivisionFunction(request, pk)
        if return_value == 'delete':
            return redirect('hr-layout-register-division')
        else:
            return redirect(reverse('hr-layout-update-division', kwargs={'pk': pk}))


# #--------------------------------------------------------------------------------------------------------------------------
# # 부서 삭제
# #--------------------------------------------------------------------------------------------------------------------------
# @login_required(login_url='/security/login/')
# def hrLayoutDeleteDivisionView(request, pk):
#     # pk is q_division.id
#     list_access_level = ['auth_hr_design',]
#     check_authority = check_authority_function(request, list_access_level)
#     if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
#         if request.method == 'POST':
#             q_division = Division.objects.get(id=pk)
#             q_division.delete()
#             messages.warning(request, f"Hi! {request.user}, 선택한 Division을 삭제하였습니다!")
#             return redirect('hr-layout-register-division')
#     else:
#         messages.warning(request, f"Hi! {request.user}, 선택한 Division을 삭제할 권한이 없습니다!")
#         return redirect('hr-layout-register-division')





############################################################################################################################
# Team
############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 팀 관리
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutRegisterTeamView(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_team_register.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutRegisterTeamFunction(request)
        return render(request, template, context)
    if request.method == 'POST':
        pk = hrLayoutRegisterTeamFunction(request)
        return redirect('hr-layout-register-team')

#--------------------------------------------------------------------------------------------------------------------------
# 팀 업데이트
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hrLayoutUpdateTeamView(request, pk):
    # pk is q_team.id
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_team_update.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrLayoutUpdateTeamFunction(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hrLayoutUpdateTeamFunction(request, pk)
        if return_value == 'delete':
            return redirect('hr-layout-register-team')
        else:
            return redirect(reverse('hr-layout-update-team', kwargs={'pk': pk}))


# #--------------------------------------------------------------------------------------------------------------------------
# # 팀 삭제
# #--------------------------------------------------------------------------------------------------------------------------
# @login_required(login_url='/security/login/')
# def hrLayoutDeleteTeamView(request, pk):
#     # pk is q_team.id
#     list_access_level = ['auth_hr_design',]
#     check_authority = check_authority_function(request, list_access_level)
#     if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
#         if request.method == 'POST':
#             q_team = Team.objects.get(id=pk)
#             q_team.delete()
#             messages.warning(request, f"Hi! {request.user}, 선택한 Team을 삭제하였습니다!")
#             return redirect('hr-layout-register-team')
#     else:
#         messages.warning(request, f"Hi! {request.user}, 선택한 Team을 삭제할 권한이 없습니다!")
#         return redirect('hr-layout-register-team')




############################################################################################################################
# Member
############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 멤버 관리
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_layout_register_member_view(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_member_register.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_layout_register_member_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_layout_register_member_function(request)
        if return_value == True:
            return redirect('hr-layout-register-member')
        else:
            return redirect('hr-layout-register-member')


#--------------------------------------------------------------------------------------------------------------------------
# Member 업데이트
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_layout_update_member_view(request, pk):
    # pk is q_member.id
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_member_update.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_layout_update_member_function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_layout_update_member_function(request, pk)
        if return_value == 'delete':
            print('22222222222')
            return redirect('hr-layout-register-member')
        else:
            return redirect(reverse('hr-layout-update-member', kwargs={'pk': pk}))




#--------------------------------------------------------------------------------------------------------------------------
# 멤버 삭제 (퇴사처리)
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_layout_delete_member_view(request, pk):
    # pk is q_team.id
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_member_delete.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_layout_delete_member_function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_layout_delete_member_function(request, pk)
        if return_value == True:
            return redirect(reverse('hr-layout-delete-member', kwargs={'pk': pk}))
        elif return_value == False:
            return redirect(reverse('hr-layout-delete-member', kwargs={'pk': pk}))
        else:
            return redirect(reverse('hr-layout-delete-member', kwargs={'pk': pk}))



############################################################################################################################
# Resign
############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 퇴직자 관리
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_layout_list_resign_view(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_layout_member_resign.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_layout_list_resign_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_layout_list_resign_function(request)
        if return_value == True:
            return redirect('hr-layout-resign-member')
        else:
            return redirect('hr-layout-resign-member')




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
#                                                             권한 설정
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




@login_required(login_url='/security/login/')
def hr_authority_home_view(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_authority_home.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_authority_home_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_authority_home_function(request)
        if return_value == True:
            return redirect('hr-authority-home')
        elif return_value == False:
            return redirect('hr-authority-home')
        else:
            return return_value


@login_required(login_url='/security/login/')
def hrAuthorityRegisterPanelView(request):
    list_access_level = ['auth_hr_design',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True or request.user.profile.check_hr_head == True :
        template = 'hr/hr_authority_register_panel.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hrAuthorityRegisterPanelFunction(request)
        return render(request, template, context)
    if request.method == 'POST':
        hrAuthorityRegisterPanelFunction(request)
        return redirect('hr-authority-register-panel')






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
#                                                             HR Calendar 관리
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
# HR Calendar Control Main View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_calendar_control_view(request):
    list_access_level = ['auth_hr_register',]
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_calendar_control.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_calendar_control_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_calendar_control_function(request)
        if return_value == True:
            return redirect('hr-calendar-control')
        elif return_value == False:
            return redirect('hr-calendar-control')
        elif return_value == 'hr-calendar-delete':
            return redirect('hr-calendar-delete')
        else:
            return redirect('hr-calendar-control')




#--------------------------------------------------------------------------------------------------------------------------
# HR Calendar Delete View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_calendar_delete_view(request, pk):
    list_access_level = ['auth_hr_validation',]  # 삭제 권한은 평가자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_calendar_delete.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_calendar_delete_function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_calendar_delete_function(request, pk)
        if return_value == True:
            return redirect('hr-calendar-control') # 삭제완료시 Control 화면으로 되돌아가기
        elif return_value == False:
            return redirect('hr-calendar-delete')
        elif return_value == 'xxx':
            return redirect('hr-calendar-delete')
        else:
            return redirect('hr-calendar-delete')


    # template = 'hr/hr_admin_deleteholiday.html'
    # # QuerySet
    # holiday_q = HR_Calendar_Event.objects.get(id=pk)

    # ################ 인사팀장 휴일등록 ##################
    # # for update purpose #
    # hddeleteform = HolidayRegisterbyHRLFrom(instance=holiday_q)
    # # Form 승인/거절 데이터 처리
    # if request.method == 'POST':
    #     try:
    #         HR_Calendar_Event.objects.get(id=pk).delete()
    #         messages.success(
    #             request, f"Hi! {req_user.profile.name_korean}, You have deleted {holiday_q.name_holiday} holiday!")
    #     except:
    #         messages.warning(
    #             request, f"Hi! {req_user.profile.name_korean}, You have failed to delete {holiday_q.name_holiday} holiday!")
    #     return redirect('hr-admindashboard')

    # context = {
    #     'hddeleteform': hddeleteform,
    #     'q': holiday_q,
    # }
    # return render(request, template, context)




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
#                                                             HR 문서 관리
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
# HR Document Main View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_document_control_view(request):
    list_access_level = ['auth_hr_register',] # 작성 권한은 등록자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_document_control.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_document_control_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_document_control_function(request)
        if return_value == True:
            return redirect('hr-document-control')
        elif return_value == False:
            return redirect('hr-document-control')
        elif return_value == 'hr-document-delete':
            return redirect('hr-document-delete') # 삭제요청시, 삭제 페이지로 이동하기
        elif return_value == LIST_HR_WORKINGTIME_CONTROL_TYPE[1][0]:
            return redirect('hr-document-control')
        elif return_value == 'hr-document-format-update':
            return redirect('hr-document-format-register-modal-api-get-view-refresh-data') # 삭제요청시, 삭제 페이지로 이동하기
        else:
            return return_value  # 파일 다운로드시






###################################################################################################################################################
#
#                                                             HR Document Format 등록
#
###################################################################################################################################################




#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 refresh로 Data 가져가기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_get_view_refresh_data(request):
    q_profile = request.user.profile
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        q_hrlayout_highest = get_my_highest_q_hrlayout_among_many(q_profile)
        print('q_mysettings_hr', q_mysettings_hr)

        document_format_title = q_mysettings_hr.document_format_title
        if document_format_title is None:
            document_format_title = ''
        document_format_description = q_mysettings_hr.document_format_description
        if document_format_description is None:
            document_format_description = ''
        list_dict_document_referrer = q_mysettings_hr.list_dict_document_referrer
        if list_dict_document_referrer is None:
            list_dict_document_referrer = []
        list_dict_document_referrer_searched = q_mysettings_hr.list_dict_document_referrer_searched
        if list_dict_document_referrer_searched is None:
            list_dict_document_referrer_searched = []
        list_dict_document_receiver = q_mysettings_hr.list_dict_document_receiver
        if list_dict_document_receiver is None:
            list_dict_document_receiver = []
        list_dict_document_receiver_searched = q_mysettings_hr.list_dict_document_receiver_searched
        if list_dict_document_receiver_searched is None:
            list_dict_document_receiver_searched = []

        jsondata = {
            'inputTextTitle': document_format_title,
            'inputTextDescription': document_format_description,
            'list_dict_document_referrer': list_dict_document_referrer,
            'list_dict_document_referrer_searched': list_dict_document_referrer_searched,
            'list_dict_document_receiver': list_dict_document_receiver,
            'list_dict_document_receiver_searched': list_dict_document_receiver_searched,
        }
        print('jsondata////////////////////////////', jsondata)
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 문서제목 입력하기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_get_view_title(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        inputTextTitle = str(request.POST.get('inputTextTitle'))
        if inputTextTitle is None or inputTextTitle == '':
            return None
        data = {
            'document_format_title': inputTextTitle,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        jsondata = {'inputTextTitle':inputTextTitle}
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 문서제목 입력하기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_get_view_description(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        inputTextDescription = str(request.POST.get('inputTextDescription'))
        if inputTextDescription is None or inputTextDescription == '':
            return None
        data = {
            'document_format_description': inputTextDescription,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        jsondata = {'inputTextDescription':inputTextDescription}
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 이름으로 멤버 찾기 (문서 참조자)
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_get_view_search_referrer(request):
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        inputText_str = str(request.GET.get('inputText'))
        if inputText_str is None or inputText_str == '':
            return JsonResponse({}, safe=False)
        list_dict_document_referrer_searched = hr_get_searched_member_hr_information_list_dictionary_format(inputText_str)
        jsondata = {'list_dict_document_referrer_searched': list_dict_document_referrer_searched}
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 멤버 추가하기 (문서 참조자)
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_post_view_select_referrer(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 추가하기
        q_hr_layout_referrer_id = int(request.POST.get('buttonSelectNameReferrer'))
        q_hrlayout_referrer = HR_Layout.objects.get(id=q_hr_layout_referrer_id)
        data = hr_get_selected_member_hr_information_dictionary_format(q_hrlayout_referrer)
        list_dict_document_referrer = q_mysettings_hr.list_dict_document_referrer
        if list_dict_document_referrer is None:
            list_dict_document_referrer = []
        if data not in list_dict_document_referrer:
            list_dict_document_referrer.append(data)
        data = {
            'list_dict_document_referrer': list_dict_document_referrer,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        jsondata = {'list_dict_document_referrer':list_dict_document_referrer}
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 멤버 삭제하기 (문서 참조자)
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_post_view_delete_referrer(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 삭제하기
        q_hr_layout_referrer_id = int(request.POST.get('buttonDeleteNameReferrer'))
        q_hrlayout_referrer = HR_Layout.objects.get(id=q_hr_layout_referrer_id)
        list_dict_document_referrer = q_mysettings_hr.list_dict_document_referrer
        if list_dict_document_referrer is not None or len(list_dict_document_referrer) > 0:
            for dict_document_referrer in list_dict_document_referrer:
                if dict_document_referrer['hrlayout_id'] == q_hr_layout_referrer_id:
                    list_dict_document_referrer.remove(dict_document_referrer)
        data = {
            'list_dict_document_referrer': list_dict_document_referrer,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        jsondata = {'list_dict_document_referrer':list_dict_document_referrer}
        return JsonResponse(jsondata, safe=False)







#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 이름으로 멤버 찾기 (수신처)
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_get_view_search_receiver(request):
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        inputText_str = str(request.GET.get('inputText'))
        if inputText_str is None or inputText_str == '':
            return JsonResponse({}, safe=False)
        list_dict_document_receiver_searched = hr_get_searched_member_hr_information_list_dictionary_format(inputText_str)
        jsondata = {'list_dict_document_receiver_searched': list_dict_document_receiver_searched}
        print('jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 멤버 추가하기 (수신처)
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_post_view_select_receiver(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 추가하기
        q_hr_layout_receiver_id = int(request.POST.get('buttonSelectNameReceiver'))
        q_hrlayout_receiver = HR_Layout.objects.get(id=q_hr_layout_receiver_id)
        print('q_hrlayout_receiver', q_hrlayout_receiver)
        data = hr_get_selected_member_hr_information_dictionary_format(q_hrlayout_receiver)
        list_dict_document_receiver = q_mysettings_hr.list_dict_document_receiver
        if list_dict_document_receiver is None:
            list_dict_document_receiver = []
        if data not in list_dict_document_receiver:
            list_dict_document_receiver.append(data)
        print('list_dict_document_receiver', list_dict_document_receiver)
        data = {
            'list_dict_document_receiver': list_dict_document_receiver,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        jsondata = {'list_dict_document_receiver':list_dict_document_receiver}
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 문서포맷 등록하기 - 모달창에서 멤버 삭제하기 (수신처)
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_document_format_register_modal_api_post_view_delete_receiver(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 삭제하기
        q_hr_layout_receiver_id = int(request.POST.get('buttonDeleteNameReceiver'))
        q_hrlayout_receiver = HR_Layout.objects.get(id=q_hr_layout_receiver_id)
        list_dict_document_receiver = q_mysettings_hr.list_dict_document_receiver
        if list_dict_document_receiver is not None or len(list_dict_document_receiver) > 0:
            for dict_document_receiver in list_dict_document_receiver:
                if dict_document_receiver['hrlayout_id'] == q_hr_layout_receiver_id:
                    list_dict_document_receiver.remove(dict_document_receiver)
        data = {
            'list_dict_document_receiver': list_dict_document_receiver,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        jsondata = {'list_dict_document_receiver':list_dict_document_receiver}
        return JsonResponse(jsondata, safe=False)



#--------------------------------------------------------------------------------------------------------------------------
# 승인한내역 리스트 정보 획득
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_xxx_document_history_readonly_modal_api_refresh_get_view(request):
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

        #--------------------------------------------------------------------------------------------------------------------------
        # 승인한내역 리스트 정보 획득
        list_dict_document_approver_validated = []
        if q_mysettings_hr.document_issued is not None:
            if q_mysettings_hr.document_issued.hrapproval is not None:
                list_dict_document_approver = q_mysettings_hr.document_issued.hrapproval.list_dict_document_approver
                if list_dict_document_approver is not None and len(list_dict_document_approver) > 0:
                    for dict_document_approver in list_dict_document_approver:
                        if 'validation' in dict_document_approver:
                            list_dict_document_approver_validated.append(dict_document_approver)
        #--------------------------------------------------------------------------------------------------------------------------
        data = {}
        MY_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        jsondata = {'list_dict_document_approver_validated': list_dict_document_approver_validated,}
        print('jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)





#############################################################################################################################
# 문서 수정요청 응답하기
#############################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 승인한 문서 수정요청 모달창 Refresh 하기
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_xxx_document_modification_communication_modal_api_refresh_get_view(request):
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

        list_dict_request_talk_for_document_management = []
        q_hr_document_issued = q_mysettings_hr.document_issued
        if q_hr_document_issued is not None:
            q_hrrequest = q_hr_document_issued.hrrequest
            if q_hrrequest is not None:
                list_dict_request_talk_for_document_management = q_hrrequest.list_dict_request_talk_for_document_management
        # print('list_dict_request_talk_for_document_management', list_dict_request_talk_for_document_management)

        # 승인한내역 리스트 정보 획득
        list_dict_document_approver_validated = []
        if q_mysettings_hr.document_issued is not None:
            if q_mysettings_hr.document_issued.hrapproval is not None:
                list_dict_document_approver = q_mysettings_hr.document_issued.hrapproval.list_dict_document_approver
                if list_dict_document_approver is not None and len(list_dict_document_approver) > 0:
                    for dict_document_approver in list_dict_document_approver:
                        if 'validation' in dict_document_approver:
                            list_dict_document_approver_validated.append(dict_document_approver)

        jsondata = {
            'list_dict_request_talk_for_document_management': list_dict_request_talk_for_document_management,
            'list_dict_document_approver_validated': list_dict_document_approver_validated,
            'my_name_korean': request.user.profile.name_korean,
        }
        # print('************************* jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)



#--------------------------------------------------------------------------------------------------------------------------
# 문서 수정요청 Talk 등록하기
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_xxx_document_modification_communication_modal_api_post_talk_register_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        q_user = request.user
        q_profile = q_user.profile
        #--------------------------------------------------------------------------------------------------------------------------
        response_contents_str = request.POST.get('inputTextReason')
        print('response_contents_str', response_contents_str)
        q_hr_document_issued = q_mysettings_hr.document_issued
        if q_hr_document_issued is not None:
            q_hrrequest = q_hr_document_issued.hrrequest
            if q_hrrequest is not None:
                list_dict_request_talk_for_document_management = q_hrrequest.list_dict_request_talk_for_document_management
                if list_dict_request_talk_for_document_management is None:
                    list_dict_request_talk_for_document_management = []
            else:
                list_dict_request_talk_for_document_management = []
        data = {
            'id': len(list_dict_request_talk_for_document_management)+1,
            'name': q_profile.name_korean,
            'position': q_profile.position,
            'talk': response_contents_str,
        }
        list_dict_request_talk_for_document_management.append(data)
        #--------------------------------------------------------------------------------------------------------------------------
        # HR Request 업데이트
        data = {
            'owner': q_user,
            'list_dict_request_talk_for_document_management': list_dict_request_talk_for_document_management,
        }
        if q_hrrequest is not None:
            HR_Document_Request_Management.objects.filter(id=q_hrrequest.id).update(**data)
            q_hrrequest.refresh_from_db()
        else:
            q_hrrequest = HR_Document_Request_Management.objects.create(**data)
        #--------------------------------------------------------------------------------------------------------------------------
        # Document Issued 업데이트
        data = {
            'hrrequest': q_hrrequest,
        }
        HR_Document_Issued.objects.filter(id=q_hr_document_issued.id).update(**data)
        #--------------------------------------------------------------------------------------------------------------------------
        jsondata = {
            'inputTextReason': '',
        }
        return JsonResponse(jsondata, safe=False)



#--------------------------------------------------------------------------------------------------------------------------
# 문서 수정요청 Talk / File 지우기
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_xxx_document_modification_communication_modal_api_post_talk_delete_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        q_user = request.user
        q_profile = q_user.profile
        #--------------------------------------------------------------------------------------------------------------------------
        talkDeleteID = int(request.POST.get('talkDeleteID'))
        print('talkDeleteID', talkDeleteID)
        q_hr_document_issued = q_mysettings_hr.document_issued
        list_dict_request_talk_for_document_management = []
        if q_hr_document_issued is not None:
            print('1')
            q_hrrequest = q_hr_document_issued.hrrequest
            if q_hrrequest is not None:
                print('2')
                list_dict_request_talk_for_document_management = q_hrrequest.list_dict_request_talk_for_document_management
                if list_dict_request_talk_for_document_management is not None:
                    print('3')
                    for dict_request_talk_for_document_management in list_dict_request_talk_for_document_management:
                        if dict_request_talk_for_document_management['id'] == talkDeleteID:
                            print('4')
                            # 첨부파일 있으면 첨부파일부터 먼저 삭제
                            if 'hr_docfile_id' in dict_request_talk_for_document_management:
                                hr_docfile_id = dict_request_talk_for_document_management['hr_docfile_id']
                                data = {
                                    'check_discard': True,
                                }
                                HR_Document_Attached_File_Management.objects.filter(id=hr_docfile_id).update(**data)
                            # Talk 항목 삭제
                            list_dict_request_talk_for_document_management.remove(dict_request_talk_for_document_management)
                            data = {
                                'list_dict_request_talk_for_document_management': list_dict_request_talk_for_document_management,
                            }
                            HR_Document_Request_Management.objects.filter(id=q_hrrequest.id).update(**data)
                            q_hrrequest.refresh_from_db()
                            # 나의 문서 업데이트
                            data = {
                                'hrrequest': q_hrrequest,
                            }
                            HR_Document_Issued.objects.filter(id=q_hr_document_issued.id).update(**data)
    return JsonResponse('jsondata', safe=False)



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
#                                                             HR Workingtime 관리
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
# HR Workingtime Control Main View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_workingtime_control_view(request):
    list_access_level = ['auth_hr_register',] # 작성 권한은 등록자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_workingtime_control.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        print("hr_workingtime_control_view::GET")
        context = hr_workingtime_control_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        first_date = request.POST.get('input-hr-workingtime-control-calendar-select-date-workingtime-control')
        second_date = request.POST.get('input-hr-workingtime-control-calendar-select-date-workingtime-control2')
        print("hr_workingtime_control_view::POST:first_date:", first_date, ", second_date:", second_date)
        return_value = hr_workingtime_control_function(request)
        if return_value == True:
            return redirect(reverse('hr-workingtime-control') + '?' + ('first_date=' + first_date + '&' if first_date != '' and first_date != None else '') + ('second_date=' + second_date if second_date != '' and second_date != None else ''))
        elif return_value == False:
            return redirect(reverse('hr-workingtime-control') + '?' + ('first_date=' + first_date + '&' if first_date != '' and first_date != None else '') + ('second_date=' + second_date if second_date != '' and second_date != None else ''))
            # return redirect('hr-workingtime-control')
        elif return_value == 'hr-workingtime-delete':
            return redirect('hr-workingtime-delete') # 삭제요청시, 삭제 페이지로 이동하기
        elif return_value == LIST_HR_WORKINGTIME_CONTROL_TYPE[1][0]:
            return redirect(reverse('hr-workingtime-control') + '?' + ('first_date=' + first_date + '&' if first_date != '' and first_date != None else '') + ('second_date=' + second_date if second_date != '' and second_date != None else ''))
        else:
            return return_value  # 파일 다운로드시


@login_required(login_url='/security/login/')
def hr_workingtime_control_redirect_request_view(request, pk):
    where_am_i = 'hr'
    q_mysettings_home = get_mysettings_home(request)
    q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
    q_workingtime_plan = Workingtime_Plan.objects.get(id=pk)
    data = {
        'workingtime_plan': q_workingtime_plan,
        'workingtime_control_type': LIST_HR_WORKINGTIME_CONTROL_TYPE[5][0],
        'check_activate_modify_view_for_workingtime_plan': True,
    }
    HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
    return redirect('hr-workingtime-control')



###################################################################################################################################################
# 출퇴근 관리 제외자 설정 모달창
###################################################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 refresh로 Data 가져가기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_issued_unchecked_except_member_modal_api_refresh_view(request):
    q_profile = request.user.profile
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        q_hrlayout_highest = get_my_highest_q_hrlayout_among_many(q_profile)

        q_hr_dms = HR_Document_Minor_Settings.objects.last()
        if q_hr_dms is not None:
            list_dict_excepter = q_hr_dms.list_dict_wkt_issued_check_excepter
        else:
            list_dict_excepter = None
        jsondata = {
            'list_dict_excepter': list_dict_excepter,
            }
        print('************************ jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 이름으로 제외자 찾기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_issued_unchecked_except_member_modal_api_search_member_view(request):
    if request.method == 'GET':
        print('************************ request.post 3', request.GET)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        list_dict_excepter_searched = hr_workingtime_issued_search_member_unchecked_excepter_basic_info(request)
        data = {
            'list_dict_excepter_searched': list_dict_excepter_searched,
        }
        # HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        return JsonResponse(data, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 제외자 추가하기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_issued_unchecked_except_member_modal_api_select_member_view(request):
    if request.method == 'POST':
        print('************************ request.post 1', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 추가하기
        hr_workingtime_issued_register_selected_member_unchecked_excepter(request, q_mysettings_hr)
        return JsonResponse('update successfully', safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 제외자 삭제하기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_issued_unchecked_except_member_modal_api_delete_member_view(request):
    if request.method == 'POST':
        print('************************ request.post 2', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 삭제하기
        hr_workingtime_issued_delete_selected_member_unchecked_excepter(request, q_mysettings_hr)
        return JsonResponse('update successfully', safe=False)





###################################################################################################################################################
# 개인맞춤형 출퇴근 관리자 설정 모달창
###################################################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 refresh로 Data 가져가기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_refresh_view(request):
    q_profile = request.user.profile
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        q_hrlayout_highest = get_my_highest_q_hrlayout_among_many(q_profile)

        q_hr_dms = HR_Document_Minor_Settings.objects.last()
        if q_hr_dms is not None:
            list_dict_wkt_issued_check_personalized = q_hr_dms.list_dict_wkt_issued_check_personalized
        else:
            list_dict_wkt_issued_check_personalized = None
        jsondata = {
            'list_dict_wkt_issued_check_personalized': list_dict_wkt_issued_check_personalized,
            }
        return JsonResponse(jsondata, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 이름으로 멤버 찾기
#--------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_search_member_view(request):
    if request.method == 'GET':
        print('************************ request.post 3', request.GET)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        list_dict_personalized_searched = hr_workingtime_issued_search_member_personalized_basic_info(request)
        data = {
            'list_dict_personalized_searched': list_dict_personalized_searched,
        }
        return JsonResponse(data, safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 멤버 추가하기
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_member_view(request):
    if request.method == 'POST':
        print('************************ request.post 1', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 추가하기
        hr_workingtime_issued_register_selected_member_personalized(request, q_mysettings_hr)
        return JsonResponse('update successfully', safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 멤버 삭제하기
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_delete_member_view(request):
    if request.method == 'POST':
        print('************************ request.post 2', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 선택한 멤버 제외자 리스트에 삭제하기
        hr_workingtime_issued_delete_selected_member_personalized(request, q_mysettings_hr)
        return JsonResponse('update successfully', safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# 모달창에서 선택멤버리스트에서 멤버 선택하기
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_member_from_selected_list_view(request):
    list_access_level = ['auth_hr_register',] # 작성 권한은 등록자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_workingtime_control.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_workingtime_control_function(request)
        return render(request, template, context)

    if request.method == 'POST':
        print('************************ request.post 2', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

        # 모달창에서 선택한 멤버 제외자 리스트에 삭제하기
        selectedMemberEmail = request.POST.get('selectedMemberEmail')
        q_profile = Profile.objects.filter(Q(check_discard=False) & Q(email=selectedMemberEmail)).last()
        email = q_profile.email
        q_user = q_profile.user
        q_workingtime_issued = Workingtime_Issued.objects.filter(Q(check_discard=False) & Q(owner=q_user)).order_by('date_of_work').last()
        data = {
            'workingtime_control_type': 'WORKINGTIME_TODAY', # Submenu 멤버 출퇴근 현황으로 라우팅
            'date_selected_workingtime': q_workingtime_issued.date_of_work,
            'workingtime_issued': q_workingtime_issued, # 선택멤버 최근 출퇴근 이슈 선택
            'check_activate_wkt_personalized_member_list_modal_view': False, #개인맞춤형 모달창 닫기
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        q_mysettings_hr.refresh_from_db()
        # # return JsonResponse('update successfully', safe=False)
        hr_workingtime_issued_personalized_member_list_modal_view_close(request, q_mysettings_hr)

        return redirect('hr-workingtime-control')




#--------------------------------------------------------------------------------------------------------------------------
# 요일별 시간 변경하기
#--------------------------------------------------------------------------------------------------------------------------

# 요일별 30분 다운
def hr_update_wkt_personalized_30_minute_down(request, day_of_week):
    ls_today = datetime.date.today()
    ls_year = ls_today.year
    ls_month = ls_today.month
    selectedMemberEmail = request.POST.get('selectedMemberEmail')
    q_profile = Profile.objects.filter(Q(check_discard=False) & Q(email=selectedMemberEmail)).last()
    email = q_profile.email
    q_user = q_profile.user
    q_workingtime_control = Workingtime_Control.objects.filter(Q(check_discard=False) & Q(owner=q_user) & Q(fiscal_year=ls_year) & Q(fiscal_month=ls_month)).last()
    q_hr_dms = HR_Document_Minor_Settings.objects.filter(Q(check_discard=False)).last()
    if q_profile is not None and q_hr_dms is not None and q_workingtime_control is not None:
        list_dict_wkt_issued_check_personalized = q_hr_dms.list_dict_wkt_issued_check_personalized
        for dict_item in list_dict_wkt_issued_check_personalized:
            if dict_item['email'] == email:
                list_dict_default_wkt_standard_personalized = dict_item['list_dict_default_wkt_standard_personalized']  #  [{'start_hour': 9, 'start_minute': 30, 'end_hour': 18, 'end_minute': 30}], [화요일] [수요일]...}
                if list_dict_default_wkt_standard_personalized is not None and len(list_dict_default_wkt_standard_personalized) > 0:
                    if day_of_week == 'monday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[0]
                    elif day_of_week == 'tuesday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[1]
                    elif day_of_week == 'wednesday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[2]
                    elif day_of_week == 'thursday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[3]
                    elif day_of_week == 'friday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[4]
                    else:
                        return False
                    start_hour = dict_default_wkt['start_hour']
                    start_minute = dict_default_wkt['start_minute']
                    end_hour = dict_default_wkt['end_hour']
                    end_minute = dict_default_wkt['end_minute']
                    if start_minute >= 30:
                        start_hour = start_hour
                        start_minute = start_minute - 30
                    else:
                        start_hour = start_hour - 1
                        start_minute = start_minute + 30
                    if end_minute >= 30:
                        end_hour = end_hour
                        end_minute = end_minute - 30
                    else:
                        end_hour = end_hour - 1
                        end_minute = end_minute + 30
                    if end_hour < 24 and start_hour > 4:
                        dict_default_wkt['start_hour'] = start_hour
                        dict_default_wkt['start_minute'] = start_minute
                        dict_default_wkt['end_hour'] = end_hour
                        dict_default_wkt['end_minute'] = end_minute
        data = {'list_dict_wkt_issued_check_personalized': list_dict_wkt_issued_check_personalized,}
        HR_Document_Minor_Settings.objects.filter(id=q_hr_dms.id).update(**data)
        data = {'list_dict_default_wkt_standard_personalized': list_dict_default_wkt_standard_personalized,}
        Workingtime_Control.objects.filter(id=q_workingtime_control.id).update(**data)
        return True


# 요일별 30분 업
def hr_update_wkt_personalized_30_minute_up(request, day_of_week):
    ls_today = datetime.date.today()
    ls_year = ls_today.year
    ls_month = ls_today.month
    selectedMemberEmail = request.POST.get('selectedMemberEmail')
    q_profile = Profile.objects.filter(Q(check_discard=False) & Q(email=selectedMemberEmail)).last()
    email = q_profile.email
    q_user = q_profile.user
    q_workingtime_control = Workingtime_Control.objects.filter(Q(check_discard=False) & Q(owner=q_user) & Q(fiscal_year=ls_year) & Q(fiscal_month=ls_month)).last()
    q_hr_dms = HR_Document_Minor_Settings.objects.filter(Q(check_discard=False)).last()
    if q_profile is not None and q_hr_dms is not None and q_workingtime_control is not None:
        list_dict_wkt_issued_check_personalized = q_hr_dms.list_dict_wkt_issued_check_personalized
        for dict_item in list_dict_wkt_issued_check_personalized:
            if dict_item['email'] == email:
                list_dict_default_wkt_standard_personalized = dict_item['list_dict_default_wkt_standard_personalized']  #  [{'start_hour': 9, 'start_minute': 30, 'end_hour': 18, 'end_minute': 30}], [화요일] [수요일]...}
                if list_dict_default_wkt_standard_personalized is not None and len(list_dict_default_wkt_standard_personalized) > 0:
                    if day_of_week == 'monday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[0]
                    elif day_of_week == 'tuesday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[1]
                    elif day_of_week == 'wednesday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[2]
                    elif day_of_week == 'thursday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[3]
                    elif day_of_week == 'friday':
                        dict_default_wkt = list_dict_default_wkt_standard_personalized[4]
                    else:
                        return False
                    start_hour = dict_default_wkt['start_hour']
                    start_minute = dict_default_wkt['start_minute']
                    end_hour = dict_default_wkt['end_hour']
                    end_minute = dict_default_wkt['end_minute']
                    if start_minute >= 30:
                        start_hour = start_hour + 1
                        start_minute = start_minute - 30
                    else:
                        start_hour = start_hour
                        start_minute = start_minute + 30
                    if end_minute >= 30:
                        end_hour = end_hour + 1
                        end_minute = end_minute - 30
                    else:
                        end_hour = end_hour
                        end_minute = end_minute + 30
                    if end_hour < 24 and start_hour > 4:
                        dict_default_wkt['start_hour'] = start_hour
                        dict_default_wkt['start_minute'] = start_minute
                        dict_default_wkt['end_hour'] = end_hour
                        dict_default_wkt['end_minute'] = end_minute
        data = {'list_dict_wkt_issued_check_personalized': list_dict_wkt_issued_check_personalized,}
        HR_Document_Minor_Settings.objects.filter(id=q_hr_dms.id).update(**data)
        data = {'list_dict_default_wkt_standard_personalized': list_dict_default_wkt_standard_personalized,}
        Workingtime_Control.objects.filter(id=q_workingtime_control.id).update(**data)
    return True


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_monday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_down(request, 'monday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_monday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_up(request, 'monday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_tuesday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_down(request, 'tuesday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_tuesday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_up(request, 'tuesday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_wednesday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_down(request, 'wednesday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_wednesday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_up(request, 'wednesday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_thursday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_down(request, 'thursday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_thursday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_up(request, 'thursday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_friday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_down(request, 'friday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)


@login_required(login_url='/security/login/')
def hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_friday_view(request):
    if request.method == 'POST':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        hr_update_wkt_personalized_30_minute_up(request, 'friday')
        jsondata = {}
        return JsonResponse(jsondata, safe=False)






###################################################################################################################################################
# 선택멤버 한달치 발행근무쿼리 관리
###################################################################################################################################################

#--------------------------------------------------------------------------------------------------------------------------
# 선택멤버 한달치 발행근무쿼리 테이블 모달창 Refresh Data
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_refresh_get_view(request):
    if request.method == 'GET':
        print('# 선택멤버 한달치 발행근무쿼리 테이블 모달창 Refresh Data ***************************************************** request.get', request.GET)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 선택멤버의 한달치 기간 확정하기
        date_selected_workingtime = q_mysettings_hr.date_selected_workingtime
        days_31 = datetime.timedelta(days=31)
        # print('///////////////////////////////////  date_selected_workingtime ', date_selected_workingtime)
        date_wkt_analytics_start =  q_mysettings_hr.date_wkt_analytics_start
        if date_wkt_analytics_start is not None:
            date_selected_start = date_wkt_analytics_start
        else:
            date_selected_start = date_selected_workingtime - days_31

        date_wkt_analytics_end =  q_mysettings_hr.date_wkt_analytics_end
        if date_wkt_analytics_end is not None:
            date_selected_end = date_wkt_analytics_end
        else:
            date_selected_end = date_selected_workingtime
        #--------------------------------------------------------------------------------------------------------------------------
        # 선택멤버의 한달치 발행출퇴근쿼리 확보하기
        q_workingtime_issued = q_mysettings_hr.workingtime_issued
        q_user = q_workingtime_issued.owner
        q_profile = q_user.profile
        qs_workingtime_issued = Workingtime_Issued.objects.filter(Q(check_discard=False) & Q(owner=q_user) & Q(date_of_work__gte=date_selected_start) & Q(date_of_work__lte=date_selected_end)).order_by('date_of_work')
        print('qs_workingtime_issued', len(qs_workingtime_issued))
        #--------------------------------------------------------------------------------------------------------------------------
        # Workingtime Issued Monthly Analytics
        data = get_dict_data_for_wkt_issued_analytics(qs_workingtime_issued)
        num_workingdays_all_checkin_monthly = data['num_workingdays_all_checkin_monthly']
        num_workingdays_holiday_checkin_all_monthly = data['num_workingdays_holiday_checkin_all_monthly']

        dp_wkt_hour_all_monthly_total = data['dp_wkt_hour_all_monthly_total']
        dp_wkt_minute_all_monthly_total = data['dp_wkt_minute_all_monthly_total']
        total_net_workingtime = f'{dp_wkt_hour_all_monthly_total}시간 {dp_wkt_minute_all_monthly_total}분'

        dp_wkt_hour_business_monthly_total = data['dp_wkt_hour_business_monthly_total']
        dp_wkt_minute_business_monthly_total = data['dp_wkt_minute_business_monthly_total']
        total_net_workingtime_business = f'{dp_wkt_hour_business_monthly_total}시간 {dp_wkt_minute_business_monthly_total}분'

        dp_hour_business_late_checkin_monthly = data['dp_hour_business_late_checkin_monthly']
        dp_minute_business_late_checkin_monthly = data['dp_minute_business_late_checkin_monthly']
        total_net_late_checkin_business = f'{dp_hour_business_late_checkin_monthly}시간 {dp_minute_business_late_checkin_monthly}분'

        dp_hour_business_late_checkout_monthly = data['dp_hour_business_late_checkout_monthly']
        dp_minute_business_late_checkout_monthly = data['dp_minute_business_late_checkout_monthly']
        total_net_late_checkout_business = f'{dp_hour_business_late_checkout_monthly}시간 {dp_minute_business_late_checkout_monthly}분'

        dp_wkt_hour_holiday_monthly_total = data['dp_wkt_hour_holiday_monthly_total']
        dp_wkt_minute_holiday_monthly_total = data['dp_wkt_minute_holiday_monthly_total']
        total_net_workingtime_holiday = f'{dp_wkt_hour_holiday_monthly_total}시간 {dp_wkt_minute_holiday_monthly_total}분'

        time_wkt_business_avg_checkin_monthly = data['time_wkt_business_avg_checkin_monthly']
        time_wkt_business_avg_checkin_monthly_str = f'{time_wkt_business_avg_checkin_monthly.hour}시 {time_wkt_business_avg_checkin_monthly.minute}분'

        time_wkt_business_avg_checkout_monthly = data['time_wkt_business_avg_checkout_monthly']
        time_wkt_business_avg_checkout_monthly_str = f'{time_wkt_business_avg_checkout_monthly.hour}시 {time_wkt_business_avg_checkout_monthly.minute}분'
        #--------------------------------------------------------------------------------------------------------------------------
        # Workingtime Issued Daily Analytics
        list_dict_member_wkt_issued_monthly = []
        datetime_wkt_all_monthly_total = datetime.datetime(1, 1, 1, 0, 0)
        if qs_workingtime_issued is not None and len(qs_workingtime_issued) > 0:
            for q_workingtime_issued in qs_workingtime_issued:
                datetime_start = q_workingtime_issued.datetime_start
                datetime_end = q_workingtime_issued.datetime_end
                if q_workingtime_issued.date_of_work is not None:
                    date_of_work_str = str(q_workingtime_issued.date_of_work), # 근무일
                else:
                    date_of_work_str = None
                if datetime_start is not None:
                    # time_start = f'{str(q_workingtime_issued.datetime_start.hour)}시{str(q_workingtime_issued.datetime_start.minute)}분', # 출근시간
                    time_start_str = str(datetime.time(datetime_start.hour, datetime_start.minute))
                else:
                    time_start_str = None
                if datetime_end is not None:
                    # time_end = f'{str(q_workingtime_issued.datetime_end.hour)}시{str(q_workingtime_issued.datetime_end.minute)}분', # 퇴근시간
                    time_end_str = str(datetime.time(datetime_end.hour, datetime_end.minute))
                else:
                    time_end_str = None
                if q_workingtime_issued.status_working_year is not None:
                    status_working_year = f'{q_workingtime_issued.status_working_year}년차', # 근무년차
                else:
                    status_working_year = None
                status_working_day_str = None
                status_wkt_start_str = None
                status_wkt_end_str = None
                status_working_type_location_str = None
                status_working_day = q_workingtime_issued.status_working_day
                for ITEM in STATUS_WORKING_DAY:
                    if ITEM[0] == status_working_day:
                        status_working_day_str = ITEM[1]
                status_wkt_start = q_workingtime_issued.status_wkt_start
                for ITEM in STATUS_WORKING_TIME_START:
                    if ITEM[0] == status_wkt_start:
                        status_wkt_start_str = ITEM[1]
                status_wkt_end = q_workingtime_issued.status_wkt_end
                for ITEM in STATUS_WORKING_TIME_END:
                    if ITEM[0] == status_wkt_end:
                        status_wkt_end_str = ITEM[1]
                status_working_type_location = q_workingtime_issued.status_working_type_location
                for ITEM in STATUS_WORKING_TYPE_LOCATION:
                    if ITEM[0] == status_working_type_location:
                        status_working_type_location_str = ITEM[1]
                if datetime_start is not None and datetime_end is not None:
                    if datetime_end >= datetime_start:
                        print('1')
                        return_value = hr_workingtime_get_net_working_time(datetime_start, datetime_end)
                        delta_time_net_working = return_value[0]
                        time_net_working = return_value[1]
                        net_workingtime_str = str(time_net_working)
                        if delta_time_net_working is not None:
                            datetime_wkt_all_monthly_total = datetime_wkt_all_monthly_total + delta_time_net_working
                    else:
                        print('2')
                        net_workingtime_str = None
                else:
                    print('3')
                    net_workingtime_str = None

                data = {
                    'id': q_workingtime_issued.id,
                    'name': q_profile.name_korean, # 멤버이름
                    'position': q_profile.position, # 포지션명
                    'date_of_work': date_of_work_str, # 근무일자
                    'status_working_type_location': status_working_type_location_str, # 근무위치상태
                    'status_working_year': status_working_year, # 근무년차
                    'status_working_day': status_working_day_str, # 근무일상태
                    'status_wkt_start': status_wkt_start_str, # 출근상태
                    'time_start': time_start_str, # 근무시작시간
                    'status_wkt_end': status_wkt_end_str, # 퇴근상태
                    'time_end': time_end_str, # 근무종료시간
                    'net_workingtime': net_workingtime_str, # 순근무시간
                }
                print('//////////////////////////////////////////////////////////////////////////////  data',date_of_work_str, data)
                list_dict_member_wkt_issued_monthly.append(data)
            #--------------------------------------------------------------------------------------------------------------------------

        #--------------------------------------------------------------------------------------------------------------------------
        # Data 취합하기
        jsondata = {
            'inputDateStart': date_selected_start,
            'inputDateEnd':date_selected_end,
            'list_dict_member_wkt_issued_monthly': list_dict_member_wkt_issued_monthly,
            'num_workingdays_all_checkin_monthly': num_workingdays_all_checkin_monthly,
            'num_workingdays_holiday_checkin_all_monthly': num_workingdays_holiday_checkin_all_monthly,
            'total_net_workingtime':total_net_workingtime,
            'total_net_workingtime_business': total_net_workingtime_business,
            'total_net_workingtime_holiday': total_net_workingtime_holiday,
            'total_net_late_checkin_business': total_net_late_checkin_business,
            'total_net_late_checkout_business': total_net_late_checkout_business,
            'time_wkt_business_avg_checkin_monthly': time_wkt_business_avg_checkin_monthly_str,
            'time_wkt_business_avg_checkout_monthly': time_wkt_business_avg_checkout_monthly_str,
        }
        # print('jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)



@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_inputdatestart_view(request):
    print('***************************************************** 기간지정 선택멤버 발행출퇴근쿼리 테이블 Input Date Satrt ', request.POST)
    if request.method == 'POST':
        ls_today = datetime.date.today()
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        #--------------------------------------------------------------------------------------------------------------------------
        # 모달창에서 참여율 검색 시작일 Mysettings_hr에 업데이트
        date_wkt_analytics_start = request.POST.get('inputDateStart')
        if date_wkt_analytics_start is not None and date_wkt_analytics_start != '':
            list_date_wkt_analytics_start_str = date_wkt_analytics_start.split('-')
            list_date_wkt_analytics_start_int = list(map(int, list_date_wkt_analytics_start_str))
            date_wkt_analytics_start = datetime.date(list_date_wkt_analytics_start_int[0], list_date_wkt_analytics_start_int[1], list_date_wkt_analytics_start_int[2])
        else:
            date_wkt_analytics_start = None
        date_wkt_analytics_end = q_mysettings_hr.date_wkt_analytics_end
        if date_wkt_analytics_end is not None:
            if date_wkt_analytics_start > date_wkt_analytics_end:
                date_wkt_analytics_start = date_wkt_analytics_end
        data = {
            'date_wkt_analytics_start': date_wkt_analytics_start,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        q_mysettings_hr.refresh_from_db()
        #--------------------------------------------------------------------------------------------------------------------------
        inputDateStart = q_mysettings_hr.date_wkt_analytics_start
        inputDateEnd = q_mysettings_hr.date_wkt_analytics_end
        if inputDateEnd is None:
            inputDateEnd = ls_today
        #--------------------------------------------------------------------------------------------------------------------------
        jsondata = {
            'inputDateStart': inputDateStart,
            'inputDateEnd': inputDateEnd,
        }
        print('jsondata', jsondata)
        #--------------------------------------------------------------------------------------------------------------------------
        return JsonResponse(jsondata, safe=False)



@csrf_exempt
@login_required(login_url='/security/login/')
def hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_inputdateend_view(request):
    print('***************************************************** 기간지정 선택멤버 발행출퇴근쿼리 테이블 Input Date End', request.POST)
    if request.method == 'POST':
        ls_today = datetime.date.today()
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        #--------------------------------------------------------------------------------------------------------------------------
        # 모달창에서 참여율 검색 종료일 업데이트
        date_wkt_analytics_end_str = request.POST.get('inputDateEnd')
        if date_wkt_analytics_end_str is not None and date_wkt_analytics_end_str != '':
            list_date_wkt_analytics_end_str = date_wkt_analytics_end_str.split('-')
            list_date_wkt_analytics_end_int = list(map(int, list_date_wkt_analytics_end_str))
            date_wkt_analytics_end = datetime.date(list_date_wkt_analytics_end_int[0], list_date_wkt_analytics_end_int[1], list_date_wkt_analytics_end_int[2])
        else:
            date_wkt_analytics_end = None
        date_wkt_analytics_start = q_mysettings_hr.date_wkt_analytics_start
        if date_wkt_analytics_start is not None:
            if date_wkt_analytics_start > date_wkt_analytics_end:
                date_wkt_analytics_start = date_wkt_analytics_end
        data = {
            'date_wkt_analytics_end': date_wkt_analytics_end,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        q_mysettings_hr.refresh_from_db()
        #--------------------------------------------------------------------------------------------------------------------------
        inputDateStart = q_mysettings_hr.date_wkt_analytics_start
        if inputDateStart is None:
            inputDateStart = ls_today - datetime.timedelta(days=30)
        inputDateEnd = q_mysettings_hr.date_wkt_analytics_end
        #--------------------------------------------------------------------------------------------------------------------------
        jsondata = {
            'inputDateStart': inputDateStart,
            'inputDateEnd': inputDateEnd,
        }
        print('jsondata', jsondata)
        #--------------------------------------------------------------------------------------------------------------------------
        return JsonResponse(jsondata, safe=False)



@login_required(login_url='/security/login/')
def hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_delete_view(request):
    if request.method == 'POST':
        ls_today = datetime.date.today()
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        #--------------------------------------------------------------------------------------------------------------------------
        # 모달창에서 참여율 검색 종료일 업데이트
        q_wkt_issued_id_int = int(request.POST.get('q_wkt_issued_id'))
        print('q_wkt_issued_id_int', q_wkt_issued_id_int)
        data = {
            'check_discard': True,
        }
        Workingtime_Issued.objects.filter(id=q_wkt_issued_id_int).update(**data)
        return JsonResponse('jsondata', safe=False)





###################################################################################################################################################
# 출퇴근 분석 그래프
###################################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------
# 정규분포 Bellcurve 분석챠트 모달창 Refresh Data
#--------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/security/login/')
def hr_workingtime_control_analytics_graph_chart_modal_refresh_api_view(request):
    if request.method == 'GET':
        print('***************************************************** 44 request.get', request.GET)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 정보 모으기
        list_status_wkt_analytics_chart_target = []
        for ITEM in LIST_WORKING_TIME_ANALYTICS_GRAPH_CHART:
            list_status_wkt_analytics_chart_target.append({'key': ITEM[0], 'value':ITEM[1]})
        # 필터링용 미니 칼랜더 (멤버 출퇴근 분석 탭)
        date_selected_workingtime_control = q_mysettings_hr.date_selected_workingtime_control
        # days_31 = datetime.timedelta(days=31)
        # 월간 출퇴근정보 분석
        hr_workingtime_control_calculate_workingtime_analytics_graph_row(request, q_mysettings_hr)
        list_chart_data_workingtime_analytics = []
        chart_title = 'No Title'
        if q_mysettings_hr.status_activate_wkt_analytics_graph_modal == 'time_wkt_business_avg_monthly_net':
            list_chart_data_workingtime_analytics = q_mysettings_hr.list_net_workingtime_business_all
            chart_title = f'{date_selected_workingtime_control.month}월 평균근무시간 Distribution + Histogram'
        elif q_mysettings_hr.status_activate_wkt_analytics_graph_modal == 'time_wkt_business_avg_checkin_monthly':
            list_chart_data_workingtime_analytics = q_mysettings_hr.list_avg_checkin_business_all
            chart_title = f'{date_selected_workingtime_control.month}월 평균출근시간 Distribution + Histogram'
        elif q_mysettings_hr.status_activate_wkt_analytics_graph_modal == 'time_wkt_business_avg_checkout_monthly':
            list_chart_data_workingtime_analytics = q_mysettings_hr.list_avg_checkout_business_all
            chart_title = f'{date_selected_workingtime_control.month}월 평균퇴근시간 Distribution + Histogram'
        # print('list_chart_data_workingtime_analytics', list_chart_data_workingtime_analytics)
        # print('chart title', chart_title)

        if len(list_chart_data_workingtime_analytics) > 0:
            return_value = get_standard_deviation_and_mean_value_from_list_value(list_chart_data_workingtime_analytics)
            mean = round(return_value[0], 3)
            # print('mean', mean)
            mean_hour = int(str(mean).split('.')[0])
            mean_min = int(float(str(mean).split('.')[1])*0.001*60)
            # print('mean_hour', mean_hour, 'mean_min', mean_min )
            mean_time = f'{mean_hour}시 {mean_min}분'
            # print('mean_time', mean_time)
            sd = round(return_value[1], 2)
            # print('sd', sd)
            number = len(list_chart_data_workingtime_analytics)
        jsondata = {
            'list_status_wkt_analytics_chart_target': list_status_wkt_analytics_chart_target,
            'list_chart_data_workingtime_analytics': list_chart_data_workingtime_analytics,
            'chart_title': chart_title,
            'mean': mean,
            'mean_time': mean_time,
            'sd': sd,
            'number': number,
        }
        return JsonResponse(jsondata, safe=False)



# 정규분포 Bellcurve 분석챠트 모달창 분석모델 선택
@login_required(login_url='/security/login/')
def hr_workingtime_control_analytics_graph_chart_modal_target_api_view(request):
    if request.method == 'POST':
        print('***************************************************** 44 request.post', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

        target_model_key = request.POST.get('target_model_key')
        data = {
            'status_activate_wkt_analytics_graph_modal': target_model_key
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        return JsonResponse('jsondata', safe=False)


# 기간지정, 시작일
@login_required(login_url='/security/login/')
def hr_workingtime_control_analytics_graph_chart_update_inputdatestart_api_view(request):
    if request.method == 'POST':
        print('***************************************************** Input Date Start', request.POST)
        ls_today = datetime.date.today()
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        #--------------------------------------------------------------------------------------------------------------------------
        # 모달창에서 출퇴근 검색 시작일 Mysettings_hr에 업데이트
        date_wkt_analytics_start = request.POST.get('inputDateStart')
        if date_wkt_analytics_start is not None and date_wkt_analytics_start != '':
            list_date_wkt_analytics_start_str = date_wkt_analytics_start.split('-')
            list_date_wkt_analytics_start_int = list(map(int, list_date_wkt_analytics_start_str))
            date_wkt_analytics_start = datetime.date(list_date_wkt_analytics_start_int[0], list_date_wkt_analytics_start_int[1], list_date_wkt_analytics_start_int[2])
        else:
            date_wkt_analytics_start = None
        data = {
            'date_wkt_analytics_start': date_wkt_analytics_start,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        q_mysettings_hr.refresh_from_db()
        #--------------------------------------------------------------------------------------------------------------------------
        inputDateStart = q_mysettings_hr.date_wkt_analytics_start
        inputDateEnd = q_mysettings_hr.date_wkt_analytics_end
        if inputDateEnd is None:
            inputDateEnd = ls_today
        #--------------------------------------------------------------------------------------------------------------------------
        jsondata = {
            'inputDateStart': inputDateStart,
            'inputDateEnd': inputDateEnd,
        }
        print('jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)


# 기간지정, 종료일
@login_required(login_url='/security/login/')
def hr_workingtime_control_analytics_graph_chart_update_inputdateend_api_view(request):
    if request.method == 'POST':
        print('***************************************************** Input Date End', request.POST)
        ls_today = datetime.date.today()
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        #--------------------------------------------------------------------------------------------------------------------------
        # 모달창에서 출퇴근 검색 종료일 업데이트
        date_wkt_analytics_end_str = request.POST.get('inputDateEnd')
        if date_wkt_analytics_end_str is not None and date_wkt_analytics_end_str != '':
            list_date_wkt_analytics_end_str = date_wkt_analytics_end_str.split('-')
            list_date_wkt_analytics_end_int = list(map(int, list_date_wkt_analytics_end_str))
            date_wkt_analytics_end = datetime.date(list_date_wkt_analytics_end_int[0], list_date_wkt_analytics_end_int[1], list_date_wkt_analytics_end_int[2])
        else:
            date_wkt_analytics_end = None
        data = {
            'date_wkt_analytics_end': date_wkt_analytics_end,
        }
        HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
        q_mysettings_hr.refresh_from_db()
        #--------------------------------------------------------------------------------------------------------------------------
        inputDateStart = q_mysettings_hr.date_wkt_analytics_start
        if inputDateStart is None:
            inputDateStart = ls_today - datetime.timedelta(days=30)
        inputDateEnd = q_mysettings_hr.date_wkt_analytics_end
        #--------------------------------------------------------------------------------------------------------------------------
        jsondata = {
            'inputDateStart': inputDateStart,
            'inputDateEnd': inputDateEnd,
        }
        print('jsondata', jsondata)
        #--------------------------------------------------------------------------------------------------------------------------
        return JsonResponse('jsondata', safe=False)



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
#                                                             HR Vacation 관리
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
# HR Vacation Control Main View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_vacation_control_view(request):

    list_access_level = ['auth_hr_register',] # 작성 권한은 등록자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_vacation_control.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_vacation_control_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_vacation_control_function(request)
        if return_value == True:
            return redirect('hr-vacation-control')
        elif return_value == False:
            return redirect('hr-vacation-control')
        elif return_value == 'hr-vacation-delete':
            return redirect('hr-vacation-delete') # 삭제요청시, 삭제 페이지로 이동하기
        elif return_value == LIST_HR_VACATION_CONTROL_TYPE[1][0]:
            return redirect('hr-vacation-control')
        else:
            return return_value




#--------------------------------------------------------------------------------------------------------------------------
# HR Vacation Delete View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_vacation_delete_view(request, pk):
    list_access_level = ['auth_hr_validation',]  # 삭제 권한은 평가자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_vacation_delete.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_vacation_delete_function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_vacation_delete_function(request, pk)
        if return_value == True:
            return redirect('hr-vacation-control') # 삭제완료시 Control 화면으로 되돌아가기
        elif return_value == False:
            return redirect('hr-vacation-delete')
        elif return_value == 'xxx':
            return redirect('hr-vacation-delete')
        else:
            return redirect('hr-vacation-delete')




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
#                                                             HR Task 관리
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
# HR Evaluation Control Main View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_task_control_view(request):

    list_access_level = ['auth_hr_register',] # 작성 권한은 등록자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_task_control.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_task_control_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        print('1')
        return_value = hr_task_control_function(request)
        print('3')
        if return_value == True:
            return redirect('hr-task-control')
        elif return_value == False:
            return redirect('hr-task-control')
        elif return_value == 'hr-task-delete':
            return redirect('hr-task-delete') # 삭제요청시, 삭제 페이지로 이동하기
        elif return_value == LIST_HR_VACATION_CONTROL_TYPE[1][0]:
            return redirect('hr-task-control')
        else:
            print('4')
            print('return value is else!')
            return return_value




#--------------------------------------------------------------------------------------------------------------------------
# HR Evaluation Delete View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_task_delete_view(request, pk):
    list_access_level = ['auth_hr_validation',]  # 삭제 권한은 평가자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_task_delete.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_task_delete_function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_task_delete_function(request, pk)
        if return_value == True:
            return redirect('hr-task-control') # 삭제완료시 Control 화면으로 되돌아가기
        elif return_value == False:
            return redirect('hr-task-delete')
        elif return_value == 'xxx':
            return redirect('hr-task-delete')
        else:
            return redirect('hr-task-delete')



#--------------------------------------------------------------------------------------------------------------------------
# Task Plan Project Analysis Modal View 프로젝트 기준
#--------------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_project_analysis_api_view(request):
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        selected_year = q_mysettings_hr.selected_year
        selected_month = q_mysettings_hr.selected_month
        if q_mysettings_hr.project_simple is not None:
            chart_title = q_mysettings_hr.project_simple.project_name
        else:
            chart_title = None
        qs_project_simple_onprogress = get_project_simple_on_progress_selected_month(request, selected_year, selected_month)
        data_serialsizer_project_simple = Project_Simple_Serializer(qs_project_simple_onprogress, many=True)
        list_project_analysis_pie_chart_selected_project_data = q_mysettings_hr.list_project_analysis_pie_chart_selected_project_data
        list_project_analysis_pie_chart_selected_project_data_by_team = q_mysettings_hr.list_project_analysis_pie_chart_selected_project_data_by_team
        date_project_analysis_start = str(q_mysettings_hr.date_project_analysis_start)
        date_project_analysis_end = str(q_mysettings_hr.date_project_analysis_end)
        list_date_project_analysis = [date_project_analysis_start, date_project_analysis_end]
        jsondata = {'chart_title': chart_title, 'list_date_project_analysis': list_date_project_analysis, 'data_serialsizer_project_simple': data_serialsizer_project_simple.data, 'list_project_analysis_pie_chart_selected_project_data':list_project_analysis_pie_chart_selected_project_data, 'list_project_analysis_pie_chart_selected_project_data_by_team': list_project_analysis_pie_chart_selected_project_data_by_team}
        print('************************* project jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)



@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_project_analysis_update_api_view(request):
    if request.method == 'POST':
        print('************************ request.post 11', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        hr_task_control_selected_project_modal_view_update(request, q_mysettings_hr)
        # 선택한 프로젝트 기준으로 프로젝트별 참여율 리스트 갱신
        get_list_project_analysis_pie_chart_selected_project_selected_period(request, q_mysettings_hr)
        # 선택한 프로젝트/날짜 기준으로 선택기간동안의 팀별 참여율 리스트 dict 구하기
        get_list_project_analysis_pie_chart_selected_project_selected_period_team(request, q_mysettings_hr)
        return JsonResponse('update slot successfully', safe=False)




@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_project_analysis_update_inputdatestart_api_view(request):
    if request.method == 'POST':
        print('************************ request.post 12', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 참여율 검색 시작일 업데이트
        hr_task_control_update_date_project_analysis_start(request, q_mysettings_hr)
        # 선택한 프로젝트 기준으로 프로젝트별 참여율 리스트 갱신
        get_list_project_analysis_pie_chart_selected_project_selected_period(request, q_mysettings_hr)
        # 선택한 프로젝트/날짜 기준으로 선택기간동안의 팀별 참여율 리스트 dict 구하기
        get_list_project_analysis_pie_chart_selected_project_selected_period_team(request, q_mysettings_hr)
        return JsonResponse('update slot successfully', safe=False)



@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_project_analysis_update_inputdateend_api_view(request):
    if request.method == 'POST':
        print('************************ request.post 13', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 참여율 검색 종료일 업데이트
        hr_task_control_update_date_project_analysis_end(request, q_mysettings_hr)
        # 선택한 프로젝트 기준으로 프로젝트별 참여율 리스트 갱신
        get_list_project_analysis_pie_chart_selected_project_selected_period(request, q_mysettings_hr)
        # 선택한 프로젝트/날짜 기준으로 선택기간동안의 팀별 참여율 리스트 dict 구하기
        get_list_project_analysis_pie_chart_selected_project_selected_period_team(request, q_mysettings_hr)
        return JsonResponse('update slot successfully', safe=False)


# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_task_plan_modal_project_analysis_update_closemodalview_api_view(request):
#     if request.method == 'POST':
#         print('************************ request.post 14', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 프로젝트 분석 모달 창 닫기
#         hr_task_control_project_participant_percent_analysis_modal_view_close(request, q_mysettings_hr)
#         return JsonResponse('update slot successfully', safe=False)




#--------------------------------------------------------------------------------------------------------------------------
# Task Plan Project Analysis Modal View # Team 기준
#--------------------------------------------------------------------------------------------------------------------------


@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_team_analysis_api_view(request):
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        if q_mysettings_hr.project_simple is not None:
            chart_title = q_mysettings_hr.project_simple.project_name
        else:
            chart_title = None
        list_project_analysis_pie_chart_selected_team_data = q_mysettings_hr.list_project_analysis_pie_chart_selected_team_data
        #
        selected_team_name = q_mysettings_hr.team.team_name
        list_dict_involved_team_id_name = q_mysettings_hr.list_dict_involved_team_id_name
        list_selected_team_and_list_involved_team = [selected_team_name, list_dict_involved_team_id_name]
        #
        date_project_analysis_start = str(q_mysettings_hr.date_project_analysis_start)
        date_project_analysis_end = str(q_mysettings_hr.date_project_analysis_end)
        list_date_project_analysis = [date_project_analysis_start, date_project_analysis_end]
        print('list_date_project_analysis', list_date_project_analysis)
        #
        jsondata = {'chart_title': chart_title, 'list_date_project_analysis': list_date_project_analysis, 'list_selected_team_and_list_involved_team': list_selected_team_and_list_involved_team, 'list_project_analysis_pie_chart_selected_team_data':list_project_analysis_pie_chart_selected_team_data}
        print('************************* team jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)




@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_team_analysis_update_api_view(request):
    if request.method == 'POST':
        print('************************ request.post 21', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 프로젝트 선택 모델에 업데이트
        hr_task_control_selected_team_modal_view_update(request, q_mysettings_hr)
        # 선택한 프로젝트 기준으로 프로젝트별 참여율 리스트 갱신
        get_list_project_analysis_pie_chart_selected_team_selected_period(request, q_mysettings_hr)
        return JsonResponse('update slot successfully', safe=False)




@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_team_analysis_update_inputdatestart_api_view(request):
    if request.method == 'POST':
        print('************************ request.post 22', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 참여율 검색 시작일 업데이트
        hr_task_control_update_date_project_analysis_start(request, q_mysettings_hr)
        # 선택한 팀 기준으로 프로젝트별 참여율 리스트 갱신
        get_list_project_analysis_pie_chart_selected_team_selected_period(request, q_mysettings_hr)
        return JsonResponse('update slot successfully', safe=False)



@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_team_analysis_update_inputdateend_api_view(request):
    if request.method == 'POST':
        print('************************ request.post 23', request.POST)
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
        # 모달창에서 참여율 검색 종료일 업데이트
        hr_task_control_update_date_project_analysis_end(request, q_mysettings_hr)
        # 선택한 팀 기준으로 프로젝트별 참여율 리스트 갱신
        get_list_project_analysis_pie_chart_selected_team_selected_period(request, q_mysettings_hr)
        return JsonResponse('update slot successfully', safe=False)




# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_task_plan_modal_team_analysis_update_closemodalview_api_view(request):
#     if request.method == 'POST':
#         print('************************ request.post 14', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 팀 분석 모달창 닫기
#         hr_task_control_project_participant_percent_analysis_by_team_modal_view_close(request, q_mysettings_hr)
#         return JsonResponse('update slot successfully', safe=False)


#--------------------------------------------------------------------------------------------------------------------------
# Task Plan Project Analysis Modal View # Member 기준
#--------------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@login_required(login_url='/security/login/')
def hr_task_plan_modal_member_analysis_api_view(request):
    if request.method == 'GET':
        where_am_i = 'hr'
        q_mysettings_home = get_mysettings_home(request)
        q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

        date_project_analysis_start = q_mysettings_hr.date_project_analysis_start
        date_project_analysis_end = q_mysettings_hr.date_project_analysis_end
        #
        q_user = q_mysettings_hr.task_plan.owner
        selected_member_name = q_user.profile.name_korean
        member_chart_title = f'{selected_member_name}님의 {date_project_analysis_start.year}년 {date_project_analysis_start.month}월 부터 ~ {date_project_analysis_end.year}년 {date_project_analysis_end.month}월 까지의 프로젝트 참여비율 분석표'
        #
        get_list_project_analysis_pie_chart_selected_project_selected_period_member(request, q_mysettings_hr, where_am_i, q_user)
        list_project_analysis_pie_chart_selected_member_data = q_mysettings_hr.list_project_analysis_pie_chart_selected_member_data
        # #
        date_project_analysis_start = str(date_project_analysis_start)
        date_project_analysis_end = str(date_project_analysis_end)
        list_date_project_analysis = [date_project_analysis_start, date_project_analysis_end]
        # #
        jsondata = {'member_chart_title': member_chart_title, 'selected_member_name': selected_member_name, 'list_project_analysis_pie_chart_selected_member_data': list_project_analysis_pie_chart_selected_member_data, 'list_date_project_analysis': list_date_project_analysis}

        print('************************* Member jsondata', jsondata)
        return JsonResponse(jsondata, safe=False)





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
#                                                             HR Evaluation 관리
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
# HR Evaluation Control Main View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_evaluation_control_view(request):

    list_access_level = ['auth_hr_register',] # 작성 권한은 등록자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_evaluation_control.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_evaluation_control_function(request)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_evaluation_control_function(request)
        if return_value == True:
            return redirect('hr-evaluation-control')
        elif return_value == False:
            return redirect('hr-evaluation-control')
        elif return_value == 'hr-evaluation-delete':
            return redirect('hr-evaluation-delete') # 삭제요청시, 삭제 페이지로 이동하기
        elif return_value == LIST_HR_VACATION_CONTROL_TYPE[1][0]:
            return redirect('hr-evaluation-control')
        else:
            return return_value




#--------------------------------------------------------------------------------------------------------------------------
# HR Evaluation Delete View
#--------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/security/login/')
def hr_evaluation_delete_view(request, pk):
    list_access_level = ['auth_hr_validation',]  # 삭제 권한은 평가자 이상
    check_authority = check_authority_function(request, list_access_level)
    if check_authority == True or request.user.is_superuser == True or request.user.profile.check_freepass  == True:
        template = 'hr/hr_evaluation_delete.html'
    else:
        template = 'member/unauthorized_member.html'

    if request.method == 'GET':
        context = hr_evaluation_delete_function(request, pk)
        return render(request, template, context)
    if request.method == 'POST':
        return_value = hr_evaluation_delete_function(request, pk)
        if return_value == True:
            return redirect('hr-evaluation-control') # 삭제완료시 Control 화면으로 되돌아가기
        elif return_value == False:
            return redirect('hr-evaluation-delete')
        elif return_value == 'xxx':
            return redirect('hr-evaluation-delete')
        else:
            return redirect('hr-evaluation-delete')









































# ###################################################################################################################################################
# #
# #                                                             HR Document Approval Management
# #
# ###################################################################################################################################################



# ###################################################################################################################################################
# # 공통
# ###################################################################################################################################################

# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 refresh로 Data 가져가기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_get_view(request):
#     q_profile = request.user.profile
#     if request.method == 'GET':
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         q_hrlayout_highest = get_my_highest_q_hrlayout_among_many(q_profile)
#         q_hrapproval = q_mysettings_hr.hrapproval

#         status_dam_modal_view_search_member = q_mysettings_hr.status_dam_modal_view_search_member

#         list_dict_document_approver = q_mysettings_hr.hrapproval.list_dict_document_approver
#         list_dict_document_approver_searched = q_mysettings_hr.list_dict_document_approver_searched
#         list_dict_document_approver_recommended = hr_document_approval_management_get_list_approver_recommended(q_hrlayout_highest)

#         list_dict_document_takeover = q_mysettings_hr.hrapproval.list_dict_document_takeover
#         list_dict_document_takeover_searched = q_mysettings_hr.list_dict_document_takeover_searched
#         list_dict_document_takeover_recommended = hr_document_approval_management_get_list_takeover_recommended(q_hrlayout_highest)

#         list_dict_document_referrer = q_mysettings_hr.hrapproval.list_dict_document_referrer
#         list_dict_document_referrer_searched = q_mysettings_hr.list_dict_document_referrer_searched
#         list_dict_document_referrer_recommended = hr_document_approval_management_get_list_referrer_recommended(q_hrlayout_highest)

#         list_dict_document_receiver = q_mysettings_hr.hrapproval.list_dict_document_receiver
#         list_dict_document_receiver_searched = q_mysettings_hr.list_dict_document_receiver_searched
#         list_dict_document_receiver_recommended = hr_document_approval_management_get_list_receiver_recommended(q_hrlayout_highest)


#         jsondata = {
#             'status_dam_modal_view_search_member': status_dam_modal_view_search_member,

#             'list_dict_document_approver': list_dict_document_approver,
#             'list_dict_document_approver_searched': list_dict_document_approver_searched,
#             'list_dict_document_approver_recommended': list_dict_document_approver_recommended,

#             'list_dict_document_takeover': list_dict_document_takeover,
#             'list_dict_document_takeover_searched': list_dict_document_takeover_searched,
#             'list_dict_document_takeover_recommended': list_dict_document_takeover_recommended,


#             'list_dict_document_referrer': list_dict_document_referrer,
#             'list_dict_document_referrer_searched': list_dict_document_referrer_searched,
#             'list_dict_document_referrer_recommended': list_dict_document_referrer_recommended,

#             'list_dict_document_receiver': list_dict_document_receiver,
#             'list_dict_document_receiver_searched': list_dict_document_receiver_searched,
#             'list_dict_document_receiver_recommended': list_dict_document_receiver_recommended,

#             }
#         print('************************* project jsondata 1', jsondata['list_dict_document_referrer'])
#         return JsonResponse(jsondata, safe=False)



# #--------------------------------------------------------------------------------------------------------------------------
# # 모달 문서승인 프로세스 -
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view(request):
#     if request.method == 'POST':
#         print('************************ request.post 2', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 모달창에서 프로젝트 선택 모델에 업데이트
#         return JsonResponse('update slot successfully', safe=False)



# #--------------------------------------------------------------------------------------------------------------------------
# # 모달 문서승인 프로세스 - 등록 모드 변경
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_get_view_mode_switch(request):
#     if request.method == 'GET':
#         print('************************ request.get 2', request.GET)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 모달창에서 프로젝트 선택 모델에 업데이트
#         hr_document_approval_management_switch_status_dam(request, q_mysettings_hr)
#         return JsonResponse('update slot successfully', safe=False)



# ###################################################################################################################################################
# # 승인권자
# ###################################################################################################################################################

# #--------------------------------------------------------------------------------------------------------------------------
# # 모달 문서승인 프로세스 - 이름으로 승인권자 찾기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_get_view_search_approver(request):
#     if request.method == 'GET':
#         print('************************ request.post 3', request.GET)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 모달창에서 프로젝트 선택 모델에 업데이트
#         list_searched_dict_document_xxx = hr_document_approval_management_search_hrlayout_basic_info(request)
#         # print('list_searched_dict_document_xxx', list_searched_dict_document_xxx)
#         data = {
#             'list_dict_document_approver_searched': list_searched_dict_document_xxx,
#         }
#         HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
#         return JsonResponse(list_searched_dict_document_xxx, safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 승인권자 추가하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_select_approver(request):
#     if request.method == 'POST':
#         print('************************ request.post 4', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 승인권자 추가하기
#         hr_document_approval_management_selected_member_add_to_approver(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 승인권자 아래로
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_down_approver(request):
#     if request.method == 'POST':
#         print('************************ request.post 5', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 승인권자 추가하기
#         hr_document_approval_management_selected_member_down_to_approver(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 승인권자 위로
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_up_approver(request):
#     if request.method == 'POST':
#         print('************************ request.post 6', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 승인권자 추가하기
#         hr_document_approval_management_selected_member_up_to_approver(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 승인권자 삭제하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_delete_approver(request):
#     if request.method == 'POST':
#         print('************************ request.post 7', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 승인권자 추가하기
#         hr_document_approval_management_selected_member_delete_to_approver(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)








# ###################################################################################################################################################
# # 업무인수자
# ###################################################################################################################################################

# #--------------------------------------------------------------------------------------------------------------------------
# # 모달 문서승인 프로세스 - 업무인수자 이름으로 검색결과 찾기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_get_view_search_takeover(request):
#     if request.method == 'GET':
#         print('************************ request.post 3', request.GET)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 모달창에서 프로젝트 선택 모델에 업데이트
#         list_searched_dict_document_xxx = hr_document_approval_management_search_hrlayout_basic_info(request)
#         # print('list_searched_dict_document_xxx', list_searched_dict_document_xxx)
#         data = {
#             'list_dict_document_takeover_searched': list_searched_dict_document_xxx,
#         }
#         HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
#         return JsonResponse(list_searched_dict_document_xxx, safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 업무인수자 추가하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_select_takeover(request):
#     if request.method == 'POST':
#         print('************************ request.post 4', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 업무인수자 추가하기
#         hr_document_approval_management_selected_member_add_to_takeover(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 업무인수자 삭제하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_delete_takeover(request):
#     if request.method == 'POST':
#         print('************************ request.post 7', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 업무인수자 추가하기
#         hr_document_approval_management_selected_member_delete_to_takeover(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)










# ###################################################################################################################################################
# # 문서참조자
# ###################################################################################################################################################

# #--------------------------------------------------------------------------------------------------------------------------
# # 모달 문서승인 프로세스 - 문서참조자 이름으로 검색결과 찾기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_get_view_search_referrer(request):
#     if request.method == 'GET':
#         print('************************ request.post 3', request.GET)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 모달창에서 프로젝트 선택 모델에 업데이트
#         list_searched_dict_document_xxx = hr_document_approval_management_search_hrlayout_basic_info(request)
#         # print('list_searched_dict_document_xxx', list_searched_dict_document_xxx)
#         data = {
#             'list_dict_document_referrer_searched': list_searched_dict_document_xxx,
#         }
#         HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
#         return JsonResponse(list_searched_dict_document_xxx, safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 문서참조자 추가하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_select_referrer(request):
#     if request.method == 'POST':
#         print('************************ request.post 4', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 문서참조자 추가하기
#         hr_document_approval_management_selected_member_add_to_referrer(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 문서참조자 삭제하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_delete_referrer(request):
#     if request.method == 'POST':
#         print('************************ request.post 7', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 문서참조자 추가하기
#         hr_document_approval_management_selected_member_delete_to_referrer(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)









# ###################################################################################################################################################
# # 수신처
# ###################################################################################################################################################

# #--------------------------------------------------------------------------------------------------------------------------
# # 모달 문서승인 프로세스 - 수신처 이름으로 검색결과 찾기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_get_view_search_receiver(request):
#     if request.method == 'GET':
#         print('************************ request.post 3', request.GET)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)
#         # 모달창에서 프로젝트 선택 모델에 업데이트
#         list_searched_dict_document_xxx = hr_document_approval_management_search_hrlayout_basic_info(request)
#         # print('list_searched_dict_document_xxx', list_searched_dict_document_xxx)
#         data = {
#             'list_dict_document_receiver_searched': list_searched_dict_document_xxx,
#         }
#         HR_My_Settings.objects.filter(id=q_mysettings_hr.id).update(**data)
#         return JsonResponse(list_searched_dict_document_xxx, safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 수신처 추가하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_select_receiver(request):
#     if request.method == 'POST':
#         print('************************ request.post 4', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 수신처 추가하기
#         hr_document_approval_management_selected_member_add_to_receiver(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)


# #--------------------------------------------------------------------------------------------------------------------------
# # 모달창에서 선택한 수신처 삭제하기
# #--------------------------------------------------------------------------------------------------------------------------
# @csrf_exempt
# @login_required(login_url='/security/login/')
# def hr_document_approval_management_register_modal_api_post_view_delete_receiver(request):
#     if request.method == 'POST':
#         print('************************ request.post 7', request.POST)
#         where_am_i = 'hr'
#         q_mysettings_home = get_mysettings_home(request)
#         q_mysettings_hr = get_xxx_my_settings(request, q_mysettings_home, where_am_i)

#         # 모달창에서 선택한 수신처 추가하기
#         hr_document_approval_management_selected_member_delete_to_receiver(request, q_mysettings_hr)
#         return JsonResponse('update successfully', safe=False)

