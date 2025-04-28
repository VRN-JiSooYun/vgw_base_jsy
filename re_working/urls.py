from django.urls import path, include
from re_working.views import *

urlpatterns = [
    # page
    path('', working_month_page, name='re-home'),
    path('working-month-view', working_month_page, name='re-working-month-home'),
    path('working-share-month-view', working_share_month_page, name='re-working-share-month-home'),
    path('working-share-week-view', working_share_week_page, name='re-working-share-week-home'),
    path('working-off-view', working_off_page, name='re-working-off-home'),
    path('working-weekend-view', working_weekend_page, name='re-working-weekend-home'),
    path('working-approval-view', working_approval_page, name='re-working-approval-home'),
    path('working-approval-etc-view', working_approval_etc_page, name='re-working-approval-etc-home'),
    path('working-certificate-view', working_certificate_page, name='re-working-certificate-home'),

    # api
    path('createWorkingOut', create_working_out, name='re-create-working-out'),
    path('createWorkingOff', create_working_off, name='re-create-working-off'),
    path('createWorkingWeekend', create_working_weekend, name='re-create-working-weekend'),
    path('createWorkingWeekendNote', create_working_weekend_note, name='re-create-working-weekend-note'),
    path('createWorkingPart', create_working_part, name='re-create-working-part'),
    path('createWorkingCertificate', create_working_certificate, name='re-create-working-certificate'),

    # page data
    path('getWorkingMonthData', get_working_month_data, name='re-get-working-month-data'),
    path('getWorkingShareMonthData', get_working_share_month_data, name='re-get-working-share-month-data'),
    path('getWorkingShareWeekData', get_working_share_week_data, name='re-get-working-share-week-data'),
    path('getWorkingApprovalRequest', get_working_approval_request, name='re-get-working-approval_request'),
    path('getWorkingApprovals', get_working_approvals, name='re-get-working-approvals'),
    path('getWorkingApprovalEtcRefs', get_working_approval_etc_refs, name='re-get-working-approval-etc-refs'),
    path('getWorkingApprovalEtcRecvs', get_working_approval_etc_recvs, name='re-get-working-approval-etc-recvs'),

    # get working
    path('getWorking/<str:workingDate>', get_working, name='re-get-working'),

    # get working out
    path('getWorkingOutForm/<int:workingOutFormId>', get_working_out_form, name='re-get-working-out-form'),

    # get working off
    path('getWorkingOffForm/<int:workingOffFormId>', get_working_off_form, name='re-get-working-off-form'),
    path('getWorkingOffForms', get_working_off_forms, name='re-get-working-off-forms'),
    path('getWorkingOffView/<int:workingOffFormId>', get_working_off_view, name='re-get-working-off-view'),

    # get working weekend
    path('getWorkingWeekendForm/<int:workingWeekendFormId>', get_working_weekend_form, name='re-get-working-weekend-form'),
    path('getWorkingWeekendForms', get_working_weekend_forms, name='re-get-working-weekend-forms'),
    path('getWorkingWeekendView/<int:workingWeekendFormId>', get_working_weekend_view, name='re-get-working-weekend-view'),
    path('getPrevWorkingWeekendForms', get_prev_working_weekend_forms, name='re-get-prev-working-weekend-forms'),

    # get working weekend note
    path('getWorkingWeekendNoteForm/<int:workingWeekendNoteFormId>', get_working_weekend_note_form, name='re-get-working-weekend-note-form'),
    path('getWorkingWeekendNoteForms', get_working_weekend_note_forms, name='re-get-working-weekend-note-forms'),
    path('getWorkingWeekendNoteView/<int:workingWeekendNoteFormId>', get_working_weekend_note_view, name='re-get-working-weekend-note-view'),

    # get approval
    path('getApprovalHistory/<str:approvalId>', get_approval_historys, name='re-get-approval-historys'),
    path('getApprovalMembers/<str:approvalId>', get_approval_members, name='re-get-approval-members'),
    path('getApprovalEtcMembers/<str:approvalId>', get_approval_etc_members, name='re-get-approval-etc-members'),
    path('getPrevApprovalMembers', get_prev_approval_members, name='re-get-prev-approval-members'),
    path('getRecommendApprovalMembers', get_recommend_approval_members, name='re-get-recommend-approval-members'),
    path('getRecommendApprovalRefMembers', get_recommend_approval_ref_members, name='re-get-recommend-approval-ref-members'),
    path('getApprovalUploadFiles/<str:approvalId>', get_approval_upload_files, name='re-get-approval-upload-files'),
    path('getApprovalRequestCount', get_approval_request_count, name='re-get-approval-request-count'),

    # get working time
    path('getWorkingTime', get_working_time, name='re-get-working-time'),

    # get working off promote
    path('getWorkingOffPromoteNum', get_working_off_promote_num, name='re-get-working-off-promote-num'),
    path('getWorkingOffPromote', get_working_off_promote, name='re-get-working-off-promote'),
    path('getWorkingOffPromotePlans/<int:workingOffPromoteId>', get_working_off_promote_plans, name='re-get-working-off-promote-plans'),

    # get working part
    path('getWorkingPart', get_working_part, name='re-get-working-part'),
    path('getProjects', get_projects, name='re-get-projects'),

    # get working certificate
    path('getWorkingCertificates', get_working_certificates, name='re-get-working-certificates'),

    # get working off yearly
    path('getWorkingOffYearlys', get_working_off_yearlys, name='re-get-working-off-yearlys'),

    # get working off yearly
    path('getWorkingOffTeams', get_working_off_teams, name='re-get-working-off-teams'),

    # get chart data
    path('getChartData', get_chart_data, name='re-get-chart-data'),

    # update working out
    path('updateWorkingOut/<int:workingOutFormId>', update_working_out, name='re-update-working-out'), # type: ignore

    # update working off
    path('updateWorkingOffOk/<int:workingOffFormId>', update_working_off_ok, name='re-update-working-off-ok'),
    path('updateWorkingOffReject/<int:workingOffFormId>', update_working_off_reject, name='re-update-working-off-reject'),
    path('updateWorkingOffCancel/<int:workingOffFormId>', update_working_off_cancel, name='re-update-working-off-cancel'),

    # update working weekend
    path('updateWorkingWeekendOk/<int:workingWeekendFormId>', update_working_weekend_ok, name='re-update-working-weekend-ok'),
    path('updateWorkingWeekendReject/<int:workingWeekendFormId>', update_working_weekend_reject, name='re-update-working-weekend-reject'),
    path('updateWorkingWeekendCancel/<int:workingWeekendFormId>', update_working_weekend_cancel, name='re-update-working-weekend-cancel'),

    # update working weekend note
    path('updateWorkingWeekendNoteOk/<int:workingWeekendNoteFormId>', update_working_weekend_note_ok, name='re-update-working-weekend-note-ok'),
    path('updateWorkingWeekendNoteReject/<int:workingWeekendNoteFormId>', update_working_weekend_note_reject, name='re-update-working-weekend-note-reject'),
    path('updateWorkingWeekendNoteCancel/<int:workingWeekendNoteFormId>', update_working_weekend_note_cancel, name='re-update-working-weekend-note-cancel'),

    # send mail
    path('sendMailWorkingOff/<str:approvalId>', send_mail_working_off, name='re-send-mail-working-off'),
    path('sendMailWorkingWeekend/<str:approvalId>', send_mail_working_weekend, name='re-send-mail-working-weekend'),
    path('sendMailWorkingWeekendNote/<str:approvalId>', send_mail_working_weekend_note, name='re-send-mail-working-weekend-note'),

    # send mail update working off
    path('sendMailWorkingOk/<str:formType>/<str:approvalId>', send_mail_working_ok, name='re-send-mail-working-ok'),
    path('sendMailWorkingReject/<str:formType>/<str:approvalId>', send_mail_working_reject, name='re-send-mail-working-reject'),
    path('sendMailWorkingCancel/<str:formType>/<str:approvalId>', send_mail_working_cancel, name='re-send-mail-working-cancel'),

    # update working off promote
    path('updateWorkingOffPromoteDone/<int:workingOffPromoteId>', update_working_off_promote_done, name='re-update-working-off-promote-done'),

    # update working part
    path('updateWorkingPart/<int:workingPartId>', update_working_part, name='re-update-working-part'),

    # update working
    path('workingStart', working_start, name='re-working-start'),
    path('workingEnd/<int:memberId>', working_end, name='re-working-end'),
    path('changeWorkingTime', change_working_time, name='re-change-working-time'),

    # check
    path('checkWorkingStart', check_working_start, name='re-check-working-start'),
    path('checkWorkingYesterday', check_working_yesterday, name='re-check-working-yesterday'),
    path('checkWorkingPart', check_working_part, name='re-check-working-part'),

    # upload & download
    path('uploadFile/<str:approvalId>', upload_file, name='re-upload-file'),
    path('downloadFile/<int:uploadFileId>', download_file, name='re-download-file'),

    # delete
    path('deleteWorkingOut/<int:workingOutFormId>', delete_working_out, name='re-delete-working-out'),
]