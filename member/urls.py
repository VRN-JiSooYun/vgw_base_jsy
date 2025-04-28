from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from member.views import *


# app_name = 'member'
urlpatterns = [
     #--------------------------------------------------------------------------------------------------------------------------
     # Dashboard
     #--------------------------------------------------------------------------------------------------------------------------
     path('member_myprofiledashboard/<int:pk>/', memberMyprofiledashboardView, name='member-myprofiledashboard'),
     path('member_public_dashboard/<int:pk>/', memberPublicDashboardView, name='member-public-dashboard'),

     #--------------------------------------------------------------------------------------------------------------------------
     # Log-In / Log-Out
     #--------------------------------------------------------------------------------------------------------------------------
     path('register/', registerView, name='member-register'),
     path('profile/', profileView, name='member-profile'),
     path('login/', LoginView.as_view(template_name='member/login.html'), name="member-login"),
     path('logout/', LogoutView.as_view(template_name='member/logout.html'), name="member-logout"),

     #--------------------------------------------------------------------------------------------------------------------------
     # MEMBER
     #--------------------------------------------------------------------------------------------------------------------------
     # New
     path('', member_home_view, name='member-home'),
     # path('daily_todo', member_daily_todo_view, name='member-daily-todo'),
     # path('my_workingtime', member_my_workingtime_view, name='member-my-workingtime'),
     # path('my_vacation', member_my_vacation_view, name='member-my-vacation'),

     #--------------------------------------------------------------------------------------------------------------------------
     # Old
     path('worktimeregister/<int:pk>', worktimeStartEndRegisterView, name='member-worktimeregister'),
     path('workingstatus/<int:pk>', workingStatusView, name='member-workingstatus'),

     path('myprofiledashboard/<int:pk>/', myProfileDashboardView, name='member-myprofiledashboard'),
     path('myprofilepersonalinfo/<int:pk>/', myProfilePersonalInfoView, name='member-myprofilepersonalinfo'),
     path('myprofileeducationinfo/<int:pk>/', myProfileEducationInfoView, name='member-myprofileeducationinfo'),
     path('myprofileworkexperienceinfo/<int:pk>/', myProfileWorkExperienceInfoView, name='member-myprofileworkexperienceinfo'),

     path('vacationregister/<int:pk>/', vacationRegisterView, name='member-vacationregister'),
     path('vacationrequestcancel/<int:pk>/', vacationRequestCancelView, name="member-vacationrequestcancel"),

     path('vacationdetail/<int:pk>/', vacationDetailView, name='member-vacationdetail'),
     path('vacationmylist/<int:pk>/', vacationMylistView, name='member-vacationmylist'),
     path('vacationapprovallist/<int:pk>/', vacationApprovallistView, name='member-vacationapprovallist'),
     path('vacationapprovallistsemi/<int:pk>/', vacationApprovallistSemiView, name='member-vacationapprovallistsemi'),
     path('vacationapprovallistsemifinal/<int:pk>/', vacationApprovallistSemifinalView, name='member-vacationapprovallistsemifinal'),
     path('vacationapprovallistfinal/<int:pk>/', vacationApprovallistFinalView, name='member-vacationapprovallistfinal'),

     path('vacationapproval/approvalformsemi/<int:pk>/', vacationApprovalFormSemiView, name='member-vacationapprovalformsemi'),
     path('vacationapproval/approvalformsemifinal/<int:pk>/', vacationApprovalFormSemifinalView, name='member-vacationapprovalformsemifinal'),
     path('vacationapproval/approvalformfinal/<int:pk>/', vacationApprovalFormFinalView, name='member-vacationapprovalformfinal'),

     ############## Authority ###############################
     path('member_authority_home', authorityHomeView, name='member-authority-home'),



]
