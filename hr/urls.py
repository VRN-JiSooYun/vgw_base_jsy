from django.urls import path, include
from hr.views import *


# app_name = 'hr'
urlpatterns = [
     #--------------------------------------------------------------------------------------------------------------------------
     path('', hrHomeView, name='hr-home'),

     #--------------------------------------------------------------------------------------------------------------------------
     # 조직구성
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_home', hrLayoutHomeView, name='hr-layout-home'),
     #--------------------------------------------------------------------------------------------------------------------------
     # 조직도 design
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_design_home', hrLayoutDesignHomeView, name='hr-layout-design-home'),
     path('hr_layout_design_m2t_step1', hrLayoutDesignM2TStep1View, name='hr-layout-design-m2t-step1'),
     path('hr_layout_design_m2t_step2/<int:pk>/', hrLayoutDesignM2TStep2View, name='hr-layout-design-m2t-step2'),
     path('hr_layout_design_t2d_step1', hrLayoutDesignT2DStep1View, name='hr-layout-design-t2d-step1'),
     path('hr_layout_design_t2d_step2/<int:pk>/', hrLayoutDesignT2DStep2View, name='hr-layout-design-t2d-step2'),
     path('hr_layout_design_m2d_step1/', hrLayoutDesignM2DStep1View, name='hr-layout-design-m2d-step1'),
     path('hr_layout_design_m2d_step2/<int:pk>/', hrLayoutDesignM2DStep2View, name='hr-layout-design-m2d-step2'),
     path('hr_layout_design_d2c_step1', hrLayoutDesignD2CStep1View, name='hr-layout-design-d2c-step1'),
     path('hr_layout_design_d2c_step2/<int:pk>/', hrLayoutDesignD2CStep2View, name='hr-layout-design-d2c-step2'),
     path('hr_layout_design_m2c_step1/', hrLayoutDesignM2CStep1View, name='hr-layout-design-m2c-step1'),
     path('hr_layout_design_m2c_step2/<int:pk>/', hrLayoutDesignM2CStep2View, name='hr-layout-design-m2c-step2'),
     path('hr_layout_design_c2g_step1/', hrLayoutDesignC2GStep1View, name='hr-layout-design-c2g-step1'),
     path('hr_layout_design_c2g_step2/<int:pk>/', hrLayoutDesignC2GStep2View, name='hr-layout-design-c2g-step2'),
     #--------------------------------------------------------------------------------------------------------------------------
     # 조직도 Register/Update/Delete
     #--------------------------------------------------------------------------------------------------------------------------
     # Group Register/Update/Delete
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_register_group', hrLayoutRegisterGroupView, name='hr-layout-register-group'),
     path('hr_layout_update_group/<int:pk>/', hrLayoutUpdateGroupView, name='hr-layout-update-group'),
     # path('hr_layout_delete_group/<int:pk>/', hrLayoutDeleteGroupView, name='hr-layout-delete-group'),
     #--------------------------------------------------------------------------------------------------------------------------
     # Company Register/Update/Delete
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_register_company', hrLayoutRegisterCompanyView, name='hr-layout-register-company'),
     path('hr_layout_update_company/<int:pk>/', hrLayoutUpdateCompanyView, name='hr-layout-update-company'),
     # path('hr_layout_delete_company/<int:pk>/', hrLayoutDeleteCompanyView, name='hr-layout-delete-company'),
     #--------------------------------------------------------------------------------------------------------------------------
     # Division Register/Update/Delete
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_register_division', hrLayoutRegisterDivisionView, name='hr-layout-register-division'),
     path('hr_layout_update_division/<int:pk>/', hrLayoutUpdateDivisionView, name='hr-layout-update-division'),
     # path('hr_layout_delete_division/<int:pk>/', hrLayoutDeleteDivisionView, name='hr-layout-delete-division'),
     #--------------------------------------------------------------------------------------------------------------------------
     # Team Register/Update/Delete
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_register_team', hrLayoutRegisterTeamView, name='hr-layout-register-team'),
     path('hr_layout_update_team/<int:pk>/', hrLayoutUpdateTeamView, name='hr-layout-update-team'),
     # path('hr_layout_delete_team/<int:pk>/', hrLayoutDeleteTeamView, name='hr-layout-delete-team'),
     #--------------------------------------------------------------------------------------------------------------------------
     # Member Register/Update/Delete
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_register_member', hr_layout_register_member_view, name='hr-layout-register-member'),
     path('hr_layout_update_member/<int:pk>/', hr_layout_update_member_view, name='hr-layout-update-member'),
     path('hr_layout_delete_member/<int:pk>/', hr_layout_delete_member_view, name='hr-layout-delete-member'),  # 퇴사처리
     #--------------------------------------------------------------------------------------------------------------------------
     # Resign Member List/Update
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_layout_list_resign', hr_layout_list_resign_view, name='hr-layout-resign-member'),


     #--------------------------------------------------------------------------------------------------------------------------
     # 권한설정
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_authority_home', hr_authority_home_view, name='hr-authority-home'),
     path('hr_authority_register_panel', hrAuthorityRegisterPanelView, name='hr-authority-register-panel'),


     #--------------------------------------------------------------------------------------------------------------------------
     # 문서관리
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_document_home', hr_document_control_view, name='hr-document-control'),
     # 문서 양식 등록/업데인트
     path('hr_document_format_register_modal_api_get_view_refresh_data/', hr_document_format_register_modal_api_get_view_refresh_data, name='hr-document-format-register-modal-api-get-view-refresh-data'),
     path('hr_document_format_register_modal_api_get_view_title/', hr_document_format_register_modal_api_get_view_title, name='hr-document-format-register-modal-api-get-view-title'),
     path('hr_document_format_register_modal_api_get_view_description/', hr_document_format_register_modal_api_get_view_description, name='hr-document-format-register-modal-api-get-view-description'),
     path('hr_document_format_register_modal_api_get_view_search_referrer/', hr_document_format_register_modal_api_get_view_search_referrer, name='hr-document-format-api-get-view-search-referrer'),
     path('hr_document_format_register_modal_api_post_view_select_referrer/', hr_document_format_register_modal_api_post_view_select_referrer, name='hr-document-format-api-post-view-select-referrer'),
     path('hr_document_format_register_modal_api_post_view_delete_referrer/', hr_document_format_register_modal_api_post_view_delete_referrer, name='hr-document-format-api-post-view-delete-referrer'),
     path('hr_document_format_register_modal_api_get_view_search_receiver/', hr_document_format_register_modal_api_get_view_search_receiver, name='hr-document-format-api-get-view-search-receiver'),
     path('hr_document_format_register_modal_api_post_view_select_receiver/', hr_document_format_register_modal_api_post_view_select_receiver, name='hr-document-format-api-post-view-select-receiver'),
     path('hr_document_format_register_modal_api_post_view_delete_receiver/', hr_document_format_register_modal_api_post_view_delete_receiver, name='hr-document-format-api-post-view-delete-receiver'),

     path('hr_xxx_document_history_readonly_modal_api_refresh_get_view/', hr_xxx_document_history_readonly_modal_api_refresh_get_view, name='hr-xxx-document-history-readonly-modal-api-refresh-get-view'),
     path('hr_xxx_document_modification_communication_modal_api_refresh_get_view/', hr_xxx_document_modification_communication_modal_api_refresh_get_view, name='hr-xxx-document-modification-communication-modal-api-refresh-get-view'),
     path('hr_xxx_document_modification_communication_modal_api_post_talk_register_view/', hr_xxx_document_modification_communication_modal_api_post_talk_register_view, name='hr-xxx-document-modification-communication-modal-api-post-talk-register-view'),
     path('hr_xxx_document_modification_communication_modal_api_post_talk_delete_view/', hr_xxx_document_modification_communication_modal_api_post_talk_delete_view, name='hr-xxx-document-modification-communication-modal-api-post-talk-delete-view'),
     #--------------------------------------------------------------------------------------------------------------------------
     # HR Workingtime Control
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_workingtime_control', hr_workingtime_control_view, name='hr-workingtime-control'),
     path('hr_workingtime_control_redirect_request/<int:pk>/', hr_workingtime_control_redirect_request_view, name='hr-workingtime-control-redirect-request'),
     # modal
     # 출퇴근 관리 제외자 설정 모달창
     path('hr_workingtime_issued_unchecked_except_member_modal_api_refresh_view/', hr_workingtime_issued_unchecked_except_member_modal_api_refresh_view, name='hr-workingtime-issued-unchecked-except-member-modal-api-refresh-view'),
     path('hr_workingtime_issued_unchecked_except_member_modal_api_search_member_view/', hr_workingtime_issued_unchecked_except_member_modal_api_search_member_view, name='hr-workingtime-issued-unchecked-except-member-modal-api-search-member-view'),
     path('hr_workingtime_issued_unchecked_except_member_modal_api_select_member_view/', hr_workingtime_issued_unchecked_except_member_modal_api_select_member_view, name='hr-workingtime-issued-unchecked-except-member-modal-api-select-member-view'),
     path('hr_workingtime_issued_unchecked_except_member_modal_api_delete_member_view/', hr_workingtime_issued_unchecked_except_member_modal_api_delete_member_view, name='hr-workingtime-issued-unchecked-except-member-modal-api-delete-member-view'),
     # 개인맞춤형 출퇴근 관리자 설정 모달창
     path('hr_workingtime_issued_personalized_member_modal_api_refresh_view/', hr_workingtime_issued_personalized_member_modal_api_refresh_view, name='hr-workingtime-issued-personalized-member-modal-api-refresh-view'),
     path('hr_workingtime_issued_personalized_member_modal_api_search_member_view/', hr_workingtime_issued_personalized_member_modal_api_search_member_view, name='hr-workingtime-issued-personalized-member-modal-api-search-member-view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_member_view/', hr_workingtime_issued_personalized_member_modal_api_select_member_view, name='hr-workingtime-issued-personalized-member-modal-api-select-member-view'),
     path('hr_workingtime_issued_personalized_member_modal_api_delete_member_view/', hr_workingtime_issued_personalized_member_modal_api_delete_member_view, name='hr-workingtime-issued-personalized-member-modal-api-delete-member-view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_member_from_selected_list_view/', hr_workingtime_issued_personalized_member_modal_api_select_member_from_selected_list_view, name='hr_workingtime_issued_personalized_member_modal_api_select_member_from_selected_list_view'),
     # 개인맞춤형 출퇴근 날짜별 시간 변경
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_monday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_monday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_monday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_monday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_monday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_monday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_tuesday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_tuesday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_tuesday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_tuesday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_tuesday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_tuesday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_wednesday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_wednesday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_wednesday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_wednesday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_wednesday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_wednesday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_thursday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_thursday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_thursday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_thursday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_thursday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_thursday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_friday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_friday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_down_friday_view'),
     path('hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_friday_view/', hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_friday_view, name='hr_workingtime_issued_personalized_member_modal_api_select_wkt_up_friday_view'),

     # 선택멤버 한달치 발행근무쿼리 관리
     path('hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_refresh_get_view/', hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_refresh_get_view, name='hr-workingtime-control-selected-member-monthly-wkt-issued-modal-api-refresh-get-view'),
     path('hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_inputdatestart_view/', hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_inputdatestart_view, name='hr-workingtime-control-selected-member-monthly-wkt-issued-modal-api-inputdatestart-view'),
     path('hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_inputdateend_view/', hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_inputdateend_view, name='hr-workingtime-control-selected-member-monthly-wkt-issued-modal-api-inputdateend-view'),
     path('hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_delete_view/', hr_workingtime_control_selected_member_monthly_wkt_issued_modal_api_delete_view, name='hr-workingtime-control-selected-member-monthly-wkt-issued-modal-api-delete-view'),
     # 출퇴근 분석 그래프
     path('hr_workingtime_control_analytics_graph_chart_modal_refresh_api_view/', hr_workingtime_control_analytics_graph_chart_modal_refresh_api_view, name='hr-workingtime-control-analytics-graph-chart-modal-refresh-api-view'),
     path('hr_workingtime_control_analytics_graph_chart_modal_target_api_view/', hr_workingtime_control_analytics_graph_chart_modal_target_api_view, name='hr-workingtime-control-analytics-graph-chart-modal-target-api-view'),
     path('hr_workingtime_control_analytics_graph_chart_update_inputdatestart_api_view/', hr_workingtime_control_analytics_graph_chart_update_inputdatestart_api_view, name='hr-workingtime-control-analytics-graph-chart-update-inputdatestart-api-view'),
     path('hr_workingtime_control_analytics_graph_chart_update_inputdateend_api_view/', hr_workingtime_control_analytics_graph_chart_update_inputdateend_api_view, name='hr-workingtime-control-analytics-graph-chart-update-inputdateend-api-view'),

     #--------------------------------------------------------------------------------------------------------------------------
     # HR Vacation Control
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_vacation_control', hr_vacation_control_view, name='hr-vacation-control'),
     path('hr_vacation_delete/<int:pk>/', hr_vacation_delete_view, name='hr-vacation-delete'),

     #--------------------------------------------------------------------------------------------------------------------------
     # HR Task Control
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_task_control', hr_task_control_view, name='hr-task-control'),
     path('hr_task_delete/<int:pk>/', hr_task_delete_view, name='hr-task-delete'),

     # Project 기준 분석
     path('hr_task_plan_modal_project_analysis_api_view/', hr_task_plan_modal_project_analysis_api_view, name="hr-task-plan-modal-project-analysis-api-view"),
     path('hr_task_plan_modal_project_analysis_update_api_view/', hr_task_plan_modal_project_analysis_update_api_view, name='hr-task-plan-modal-project-analysis-update-api-view'),
     path('hr_task_plan_modal_project_analysis_update_inputdatestart_api_view/', hr_task_plan_modal_project_analysis_update_inputdatestart_api_view, name='hr-task-plan-modal-project-analysis-update-inputdatestart-api-view'),
     path('hr_task_plan_modal_project_analysis_update_inputdateend_api_view/', hr_task_plan_modal_project_analysis_update_inputdateend_api_view, name='hr-task-plan-modal-project-analysis-update-inputdateend-api-view'),
     # path('hr_task_plan_modal_project_analysis_update_closemodalview_api_view/', hr_task_plan_modal_project_analysis_update_closemodalview_api_view, name='hr-task-plan-modal-project-analysis-update-closemodalview-api-view'),

     # Team 기준 분석
     path('hr_task_plan_modal_team_analysis_api_view/', hr_task_plan_modal_team_analysis_api_view, name='hr-task-plan-modal-team-analysis-api-view'),
     path('hr_task_plan_modal_team_analysis_update_api_view/', hr_task_plan_modal_team_analysis_update_api_view, name='hr-task-plan-modal-team-analysis-update-api-view'),
     path('hr_task_plan_modal_team_analysis_update_inputdatestart_api_view/', hr_task_plan_modal_team_analysis_update_inputdatestart_api_view, name='hr-task-plan-modal-project-analysis-update-inputdatestart-api-view'),
     path('hr_task_plan_modal_team_analysis_update_inputdateend_api_view/', hr_task_plan_modal_team_analysis_update_inputdateend_api_view, name='hr-task-plan-modal-project-analysis-update-inputdateend-api-view'),
     # path('hr_task_plan_modal_team_analysis_update_closemodalview_api_view/', hr_task_plan_modal_team_analysis_update_closemodalview_api_view, name='hr-task-plan-modal-team-analysis-update-closemodalview-api-view'),

     # Member 기준 분석
     path('hr_task_plan_modal_member_analysis_api_view/', hr_task_plan_modal_member_analysis_api_view, name="hr-task-plan-modal-member-analysis-api-view"),

     #--------------------------------------------------------------------------------------------------------------------------
     # HR Evaluation Control
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_evaluation_control', hr_evaluation_control_view, name='hr-evaluation-control'),
     path('hr_evaluation_delete/<int:pk>/', hr_evaluation_delete_view, name='hr-evaluation-delete'),

     #--------------------------------------------------------------------------------------------------------------------------
     # HR Calendar Control
     #--------------------------------------------------------------------------------------------------------------------------
     path('hr_calendar_control', hr_calendar_control_view, name='hr-calendar-control'),
     path('hr_calendar_delete/<int:pk>/', hr_calendar_delete_view, name='hr-calendar-delete'),

]