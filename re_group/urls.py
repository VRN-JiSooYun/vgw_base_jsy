from django.urls import path, include
from re_group.views import *

urlpatterns = [
    # re_group
    # page
    path('group-view', view_page, name='re-group-home'),

    # api
    path('createGroup', create_group, name='create-group'),

    path('getGroups', get_groups, name='get-groups'),
    path('getMemberGroupInfo', get_member_group_info, name='get-member-group-info'),
    path('getGroupTree', get_group_tree, name='get-group-tree'),

    path('updateDisconnectGroup/<int:groupKey>', update_disconnect_group, name='update-disconnect-group'),
    path('updateGroup/<int:groupKey>', update_group, name='update-group'),
    path('updateGroupDepth', update_group_depth, name='update-group-depth'),

    path('rollbackGroup', rollback_group, name='rollback-group'),

    path('deleteGroup/<int:groupKey>', delete_group, name='delete-group'),

    # re_group_member
    #api
    path('createGroupMember', create_group_member, name='create-group-member'),

    path('getGroupMember/<int:memberId>', get_group_member, name='get-group-member'),
    path('getGroupMemberById/<int:memberId>', get_group_tree_by_member_id, name='get-group-tree-member-id'),
    path('getGroupMemberByGroupId/<int:groupKey>', get_group_tree_by_group_id, name='get-group-tree-group-id'),

    path('updateGroupMemberLeader/<int:memberId>', update_group_member_leader, name='update-group-member-leader'),

    path('deleteGroupMember/<int:memberId>', delete_group_member, name='delete-group-member'),

]

