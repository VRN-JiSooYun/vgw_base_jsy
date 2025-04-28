from django.urls import path, include
from re_member.views import *

urlpatterns = [
    # page
    path('member-list-view', member_list_page, name='re-member-list-home'),
    path('member-view/<int:memberId>', member_page, name='re-member-home'),
    path('member-card-view', member_card_page, name='re-member-card-home'),

    # api
    path('createMember', create_member, name='create-member'),

    path('getMembers', get_members, name='get-members'),
    path('getMe', get_me, name='get-me'),
    path('getMember/<int:memberId>', get_member, name='get-member'),
    path('getMemberColleges/<int:memberId>', get_member_colleges, name='get-member-colleges'),
    path('getMemberCertificates/<int:memberId>', get_member_certificates, name='get-member-certificates'),
    path('getMemberForeignLangs/<int:memberId>', get_member_foregin_langs, name='get-member-foregin-langs'),
    path('getMemberCompanys/<int:memberId>', get_member_companys, name='get-member-companys'),
    path('getMemberFamilys/<int:memberId>', get_member_familys, name='get-member-s'),
    path('getSearch', get_search, name='get-search'),

    path('updateMemberInfoDefault', update_member_info_default, name='update-member-info-default'),
    path('updateMemberInfo', update_member_info, name='update-member-info'),
    path('updateMemberInfoCard/<int:memberId>', update_member_info_card, name='update-member-info-card'),
    path('updateMemberImage/<int:memberId>', update_member_image, name='update-member-image'),

    path('reJoinMember/<int:memberId>', re_join_member, name='re-join-member'),
    path('leaveMember/<int:memberId>', leave_member, name='leave-member'),
    path('deleteMember/<int:memberId>', delete_member, name='delete-member'),

    # excel
    path('uploadMemberImage/<int:memberId>', upload_member_image, name='upload-member-image'),
]