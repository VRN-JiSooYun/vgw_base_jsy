from django.urls import path, include
from re_working_admin.views import *

urlpatterns = [
    # page
    path('working-month-admin-view', working_month_admin_page, name='re-working-month-admin-home'),
    path('working-week-admin-view', working_week_admin_page, name='re-working-week-admin-home'),
    path('working-off-admin-view', working_off_admin_page, name='re-working-off-admin-home'),
    path('working-off-yearly-admin-view', working_off_yearly_admin_page, name='re-working-off-yearly-admin-home'),
    path('working-off-promote-admin-view', working_off_promote_admin_page, name='re-working-off-promote-admin-home'),
    path('working-admin-view', working_admin_page, name='re-working-admin-home'),
    path('working-time-admin-view', working_time_admin_page, name='re-working-time-admin-home'),
    path('working-time-change-admin-view', working_time_change_admin_page, name='re-working-time-change-admin-home'),
    path('working-stat-admin-view', working_stat_admin_page, name='re-working-stat-admin-home'),
    path('working-part-admin-view', working_part_admin_page, name='re-working-part-admin-home'),
    path('working-approval-admin-view', working_approval_admin_page, name='re-working-approval-admin-home'),
    path('working-weekend-stat-admin-view', working_weekend_stat_admin_page, name='re-working-weekend-stat-admin-home'),
    path('working-certificate-admin-view', working_certificate_admin_page, name='re-working-certificate-admin-home'),
    path('holiday-view', holiday_page, name='re-holiday-home'),

    # api
    path('createHoliday', create_holiday, name='re-create-holiday'),
    path('createWorkingTime', create_working_time, name='re-create-working-time'),

    path('getWorkingMonthData', get_working_month_data, name='re-get-working-month-data'),
    path('getWorkingWeekData', get_working_week_data, name='re-get-working-week-data'),
    path('getWorkingOffHistorys', get_working_off_historys, name='re-get-working-off-historys'),
    path('getWorkings', get_workings, name='re-get-workings'),
    path('getWorkingHistorys', get_working_historys, name='re-get-working-history'),
    path('getChangeWorkingTimes', get_change_working_times, name='re-get-change-working-times'),
    path('getHolidays', get_holidays, name='re-get-holidays'),
    path('getHoliday', get_holiday, name='re-get-holiday'),
    path('getWorkingTimes', get_working_times, name='re-get-working-times'),
    path('getWorkingStats', get_working_stats, name='re-get-working-stats'),
    path('getWorkingParts', get_working_parts, name='re-get-working-parts'),
    path('getProjects', get_projects, name='re-get-projects'),
    path('getWorkingTimeGroupTree', get_working_time_group_tree, name='re-get-working-time-group-tree'),
    path('getWorkingApprovals/<int:limit>/<int:offset>', get_working_approvals, name='re-get-working-approvals'),
    path('getWorkingWeekendStats', get_working_weekend_stats, name='re-get-working-weekend_stats'),
    path('getWorkingWeekendStatsDaily/<int:memberId>', get_working_weekend_stats_daily, name='re-get-working-weekend_stats_daily'),
    path('getWorkingOffPromotes', get_working_off_promotes, name='re-get-working-off-promotes'),
    path('getWorkingOffPromotePlans/<int:workingOffPromoteId>', get_working_off_promote_plans, name='re-get-working-off-promote-plans'),
    path('getWorkingCertificates', get_working_certificates, name='re-get-working-certificates'),
    path('getWorkingOffYearlys', get_working_off_yearlys, name='re-get-working-off-yearlys'),

    path('updateWorkingOffCancel/<int:workingOffFormId>', update_working_off_cancel, name='re-update-working-off-cancel'),
    path('updatePrevWorkingOffCancel/<int:workingOffFormId>', update_prev_working_off_cancel, name='re-update-prev-working-off-cancel'),
    path('updateWorkingOffDays/<int:memberId>', update_working_off_days, name='re-update-working-off-days'),
    path('updateWorkingOffAddDays', update_working_off_add_days, name='re-update-working-off-add-days'),
    path('updateWorkingTime', update_working_time, name='re-update-working-time'),
    path('updateWorkingChangeTime', update_working_change_time, name='re-update-working-change-time'),
    path('updateWorkingTimeChange', update_working_time_change, name='re-update-working-time-change'),
    path('updateWorkingOffPromote/<int:workingOffPromoteId>', update_working_off_promote, name='re-update-working-off-promote'),
    path('resendWorkingOffPromote', resend_working_off_promote, name='re-resend-working-off-promote'),
    path('updateWorkingCertificateStatusDone/<int:workingCertificateId>', update_working_certificate_status_done, name='re-update-working-certificate-status-done'),
    path('updateWorkingCertificateStatusReject/<int:workingCertificateId>', update_working_certificate_status_reject, name='re-update-working-certificate-status-reject'),
    path('updateWorkingCertificateJoinDate/<int:workingCertificateId>', update_working_certificate_join_date, name='re-update-working-certificate-join-date'),
    path('updateWorkingOffYearlyDays/<int:workingOffYearlyId>', update_working_off_yearly_days, name='re-update-working-off-yearly-days'),

    path('updateHoliday', update_holiday, name='re-update-holiday'),

    path('deleteWorkingChangeTime/<int:workingId>', delete_working_change_time, name='re-delete-working-change-time'),
    path('deleteWorkingTime/<int:workingTimeId>', delete_working_time, name='re-delete-working-time'),
    path('deleteHoliday/<int:holidayId>', delete_holiday, name='re-delete-holiday'),

    # download
    path('workingDownload', working_download, name='re-working-download'),
    path('workingOffPromoteDownload', working_off_promote_download, name='re-working-off-promote-download'),

    # etc api
    path('loadHoliday/<str:year>', load_holiday, name='re-load-holiday'),

    path('makeWokringStat', make_wokring_stat, name='re-make-wokring-stat'),

    path('runSchedule', run_schedule, name='re-schedule'),

]



