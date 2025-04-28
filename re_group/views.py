from django.shortcuts import render
from re_group.functions import *
from re_member.functions import *
# from project.views import authority
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from home.code_singleton import Code

# re-group
@login_required(login_url='/security/login/')
def view_page(request) :
    print("view_page :", request.user.id)
    # auth = authority("hr", request)
    auth = False
    if auth["D"] == True :
        context = {
            "codes": Code().getCodes(),
            "codeDtls": Code().getCodeDtls(),
        }
        return render(request, "group_view.html", context)
    else :
        return render(request, "group_access_auth.html")

@csrf_exempt
def create_group(request) :
    print("create_group :", request.user.id)
    if request.method == "POST":
        return JsonResponse(model_to_dict(createGroup(request)), safe=False)

@csrf_exempt
def get_groups(request) :
    print("get_groups :", request.user.id)
    return JsonResponse(list(getGroups().values()), safe=False)

@csrf_exempt
def get_member_group_info(request) :
    print("get_member_group_info :", request.user.id)
    memberId = request.GET.get('member_id')
    groupNames = getMemberGroupNames(memberId)
    member = getMember(memberId)
    context = {
        "memberName": member["member_name"],
        "groupName": '->'.join(groupNames)
    }
    return JsonResponse(context, json_dumps_params={'ensure_ascii': False}, safe=False)

@csrf_exempt
def get_group_tree(request) :
    print("get_group_tree :", request.user.id)

    # 순환참조 (Circular Import)로 인하여 여기서 import
    from re_group.functions import getGroupTree
    return JsonResponse(json.loads(getGroupTree().toJSON()), safe=False)

@csrf_exempt
def update_disconnect_group(request, groupKey) :
    print("update_disconnect_group :", request.user.id, groupKey)
    if request.method == "POST":
        process = updateDisconnectGroup(request, groupKey)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_group(request, groupKey) :
    print("update_group :", request.user.id, groupKey)
    if request.method == "POST":
        process = updateGroup(request, groupKey)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_group_depth(request) :
    print("update_group_depth :", request.user.id)
    if request.method == "POST":
        process = updateGroupDepth(request)
        return JsonResponse(process, safe=False)
@csrf_exempt
def rollback_group(request) :
    process = rollbackGroup()
    return JsonResponse(process, safe=False)

@csrf_exempt
def delete_group(request, groupKey) :
    print("delete_group :", request.user.id, groupKey)
    if request.method == "POST":
        process = deleteGroup(request, groupKey)
        return JsonResponse(process, safe=False)

# re-group-member
@csrf_exempt
def create_group_member(request) :
    print("create_group_member :", request.user.id)
    if request.method == "POST":
        return JsonResponse(createGroupMember(request), safe=False)

@csrf_exempt
def get_group_member(request, memberId) :
    print("get_group_member :", request.user.id, memberId)
    return JsonResponse(list(getGroupMember(memberId).values()), safe=False)

@csrf_exempt
def get_group_tree_by_member_id(request, memberId) :
    print("get_group_tree_by_member_id :", request.user.id, memberId)
    return JsonResponse(getGroupTreeByMemberId(memberId), json_dumps_params={'ensure_ascii': False}, safe=False)

@csrf_exempt
def get_group_tree_by_group_id(request, groupKey) :
    print("get_group_tree_by_group_id :", request.user.id, groupKey)
    return JsonResponse(getGroupTreeByGroupId(groupKey), json_dumps_params={'ensure_ascii': False}, safe=False)

@csrf_exempt
def update_group_member_leader(request, memberId) :
    print("update_group_member_leader :", request.user.id, memberId)
    if request.method == "POST":
        process = updateGroupMemberLeader(request, memberId)
        return JsonResponse(process, safe=False)

@csrf_exempt
def delete_group_member(request, memberId) :
    print("delete_group_member :", request.user.id, memberId)
    if request.method == "POST":
        process = deleteGroupMember(request, memberId)
        return JsonResponse(process, safe=False)