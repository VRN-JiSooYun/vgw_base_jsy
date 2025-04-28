from django.shortcuts import render
from re_group.models import *
from re_member.models import *
from dateutil.parser import parse
from datetime import datetime
from django.db import connection, transaction
from django.forms.models import model_to_dict
from django.conf import settings
from django.db.models import Q
import json
import random
import time
from home.code_singleton import Code

# re-group
def createGroup(request) :
    try :
        for i in range(5):
            groupCode = "VN_G_" + str(random.randrange(1, 9)) + str(random.randrange(1, 9)) + str(random.randrange(1, 9)) + str(random.randrange(1, 9)) + str(random.randrange(1, 9))
            if len(ReGroup.objects.filter(group_code = groupCode)) == 0 :
                break
            else :
                groupCode = ""

        if groupCode != "" :
            reGroup = ReGroup.objects.create(
                group_name = request.POST.get("group_name"),
                group_type = request.POST.get("group_type"),
                group_code = groupCode,
            )
            print("success create group")
    except Exception as e :
        print("Exception::", e)

    return reGroup

def getGroups() :
    return ReGroup.objects.order_by('date_updated', 'group_key').all()


def getMemberIdsInGroup(memberId) :
    if isGroupLeader(memberId) :
        return getMemberIdsInReaderGroup(memberId)
    else :
        return getMemberIdsInMyGroup(memberId)

def getMemberIdsInReaderGroup(memberId) :
    groupKeys = []
    groups = getGroups()

    groupMembers = getGroupMember(memberId)
    for groupMember in groupMembers :
        groupKeys.append(groupMember.group_key)
        for group in groups :
            if groupMember.group_key == group.parent_group_key :
                groupKeys.append(groupMember.group_key)
                getParentGroupKeyInGroup(groupMember.group_key, groups, groupKeys)

    groupMembers = ReGroupMember.objects.filter(Q(group_key__in = groupKeys))

    memberIds = []
    for groupMember in groupMembers :
        memberIds.append(str(groupMember.member_id))

    return memberIds

def getMemberIdsInMyGroup(memberId) :
    groupKeys = []

    groupMembers = getGroupMember(memberId)
    for groupMember in groupMembers :
        groupKeys.append(groupMember.group_key)

    groupMembers = ReGroupMember.objects.filter(Q(group_key__in = groupKeys))

    memberIds = []
    for groupMember in groupMembers :
        memberIds.append(str(groupMember.member_id))

    return memberIds

def getParentGroupLeader(memberId) :
    reGroupMembers = ReGroupMember.objects.filter(Q(member_id = memberId))

    groupKeys = []
    for reGroupMember in reGroupMembers :
        groupKeys.append(reGroupMember.group_key)

    reGroups = ReGroup.objects.filter(group_key__in = groupKeys)

    parentGroupKeys = []
    for reGroup in reGroups :
        parentGroupKeys.append(reGroup.parent_group_key)

    reGroupLeaders = ReGroupMember.objects.filter(Q(group_key__in = parentGroupKeys) & Q(is_leader = "Y"))

    memberIds = []
    for reGroupLeader in reGroupLeaders :
        memberIds.append(reGroupLeader.member_id)

    return memberIds

def getGroupLeader(groupKey) :
    memberId = 0
    reGroupMembers = ReGroupMember.objects.filter(Q(group_key = groupKey) & Q(is_leader = 'Y'))
    for reGroupMember in reGroupMembers :
        if ReMember.objects.filter(Q(member_id = reGroupMember.member_id) & Q(leave_date = None)).count() > 0 :
            memberId = reGroupMember.member_id
            break

    return memberId

def getGroupLeaderInMyGroup(memberId) :
    reGroupMembers = ReGroupMember.objects.filter(Q(member_id = memberId))

    groupKeys = []
    for reGroupMember in reGroupMembers :
        groupKeys.append(reGroupMember.group_key)

    reGroupLeaders = ReGroupMember.objects.filter(Q(group_key__in = groupKeys) & Q(is_leader = "Y"))

    memberIds = []
    for reGroupLeader in reGroupLeaders :
        memberIds.append(reGroupLeader.member_id)

    return memberIds

def getGroupLeadersInMyParentGroup(memberId) :
    reGroupMembers = ReGroupMember.objects.filter(Q(member_id = memberId))

    groupKeys = []
    for reGroupMember in reGroupMembers :
        groupKeys.append(reGroupMember.group_key)

    reGroups = ReGroup.objects.filter(group_key__in = groupKeys)

    parentGroupKeys = []
    for reGroup in reGroups :
        parentGroupKeys.append(reGroup.parent_group_key)
    reGroups = ReGroup.objects.filter(parent_group_key__in = parentGroupKeys)

    groupKeys = []
    for reGroup in reGroups :
        groupKeys.append(reGroup.group_key)

    reGroupLeaders = ReGroupMember.objects.filter(Q(group_key__in = groupKeys) & Q(is_leader = "Y"))

    memberIds = []
    for reGroupLeader in reGroupLeaders :
        if reGroupLeader.member_id == memberId : continue
        memberIds.append(reGroupLeader.member_id)

    return memberIds

def getParentGroupKeyInGroup(groupKey, groups, groupKeys) :
    for group in groups :
        if groupKey == group.parent_group_key :
            groupKeys.append(getParentGroupKeyInGroup(group.group_key, groups, groupKeys))

    return groupKey


def getParentGroupKey(groupKey, groups, groupKeys) :
    for group in groups :
        if groupKey == group.group_key :
            groupKeys.append(getParentGroupKey(group.parent_group_key, groups, groupKeys))

    return groupKey

def getMemberGroupNames(memberId) :
    groupKeys = []
    groups = getGroups()

    groupMembers = getGroupMember(memberId)
    for groupMember in groupMembers :
        for group in groups :
            if groupMember.group_key == group.group_key :
                groupKeys.append(getParentGroupKey(group.parent_group_key, groups, groupKeys))

        groupKeys.append(groupMember.group_key)

    groupNames = []
    for groupKey in groupKeys :
        for group in groups :
            if group.group_key == groupKey :
                groupNames.append(group.group_name)

    return groupNames


def updateDisconnectGroup(request, groupKey) :
    data = json.loads(request.body)["data"]
    try :
        reGroup = ReGroup.objects.get(group_key = groupKey)
        reGroup.parent_group_key = data["parent_group_key"]
        reGroup.group_depth = data["group_depth"]
        ReGroup.save(reGroup)
        print("success update group")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateGroup(request, groupKey) :
    data = json.loads(request.body)

    try :
        reGroup = ReGroup.objects.get(group_key = groupKey)
        reGroup.group_name = data["group_name"]
        reGroup.group_type = data["group_type"]
        reGroup.save()

        print("success update group name")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateGroupDepth(request) :
    try :
        groupHistoryKey = str(round(time.time() * 1000))
        reGroups = ReGroup.objects.all()
        for reGroup in reGroups :
            reGroupHistory = ReGroupHistory(
                group_history_key = groupHistoryKey,
                group_key = reGroup.group_key,
                group_name = reGroup.group_name,
                parent_group_key = reGroup.parent_group_key,
                group_depth = reGroup.group_depth,
                group_type = reGroup.group_type,
                group_code = reGroup.group_code,
            )
            reGroupHistory.save()

        groups = json.loads(request.body)["groups"]

        for group in groups :
            reGroup = ReGroup.objects.get(group_key = group["group_key"])
            reGroup.parent_group_key = group["parent_group_key"]
            reGroup.group_depth = group["group_depth"]
            ReGroup.save(reGroup)

        print("success update group depth")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def rollbackGroup() :
    try :
        reGroupHistory = ReGroupHistory.objects.order_by('group_history_key').distinct().last()
        reGroupHistorys = ReGroupHistory.objects.filter(Q(group_history_key = reGroupHistory.group_history_key))

        ReGroup.objects.all().delete()

        for reGroupHistory in reGroupHistorys :
            reGroup = ReGroup(
                group_key = reGroupHistory.group_key,
                group_name = reGroupHistory.group_name,
                parent_group_key = reGroupHistory.parent_group_key,
                group_depth = reGroupHistory.group_depth,
                group_type = reGroupHistory.group_type,
                group_code = reGroupHistory.group_code,
            )
            reGroup.save()
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def deleteGroup(request, groupKey) :
    try :
        groupKeys = json.loads(request.body)["group_keys"]

        ReGroup.objects.get(group_key = groupKey).delete()
        ReGroupMember.objects.filter(group_key = groupKey).delete()

        reGoups = ReGroup.objects.filter(group_key__in = groupKeys)
        reGoups.update(parent_group_key = -1, group_depth = -1)
        reGoups = ReGroup.objects.filter(group_key__in = groupKeys)

        print("success delete group")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

# re-group=member
def createGroupMember(request) :
    data = json.loads(request.body)["group_member"]
    try :
        ReGroupMember.objects.create(
            group_key = data["group_key"],
            member_id = data["member_id"],
            is_leader = data["is_leader"]
        )
        print("success create group member")
    except Exception as e :
        print("Exception::", e)

def getGroupMember(memberId) :
    return ReGroupMember.objects.filter(member_id = memberId)

def getGroupTreeByMemberId(memberId) :
    reMember = ReMember.objects.get(member_id = memberId)
    reGroupMembers = ReGroupMember.objects.filter(member_id = memberId)

    reGroupMember = reGroupMembers.last()
    reGroup = ReGroup.objects.filter(group_key = reGroupMember.group_key).get()
    list = []
    data = {
        "group_key": reGroup.group_key,
        "group_name": reGroup.group_name,
        "group_type": Code().getCodeDtlNm(reGroup.group_type),
        "is_leader": reGroupMember.is_leader,
        "member_name": reMember.member_name,
    }
    list.append(data)

    parentGroupKey = reGroup.parent_group_key
    while(parentGroupKey != 0) :
        reGroup = ReGroup.objects.filter(group_key = parentGroupKey).get()
        data = {
            "group_key": reGroup.group_key,
            "group_name": reGroup.group_name,
            "group_type": Code().getCodeDtlNm(reGroup.group_type),
            "is_leader": "N",
        }
        list.append(data)
        parentGroupKey = reGroup.parent_group_key

    return list

def getGroupTreeByGroupId(groupKey) :
    groups = []

    reGroup = ReGroup.objects.filter(group_key = groupKey).get()
    groupKey = reGroup.group_key
    groupName = reGroup.group_name
    groupType = Code().getCodeDtlNm(reGroup.group_type)

    members = []
    reGroupMembers = ReGroupMember.objects.filter(Q(group_key = groupKey)).order_by("-is_leader")
    if len(reGroupMembers) > 0 :
        for reGroupMember in reGroupMembers :
            reMember = ReMember.objects.get(member_id = reGroupMember.member_id)
            member = {
                "group_key": groupKey,
                "group_name": groupName,
                "group_type": groupType,
                "is_leader": reGroupMember.is_leader,
                "member_id": reMember.member_id,
                "member_name": reMember.member_name,
            }
            members.append(member)

    groups.append({
        "group_key": groupKey,
        "group_name": groupName,
        "group_type": groupType,
        "members": members,
        "groups": getGroupsToJson(groupKey)
    })

    return groups


def getGroupsToJson(groupKey) :
    groups = []
    reGroups = ReGroup.objects.filter(parent_group_key = groupKey)
    for reGroup in reGroups :
        groupKey = reGroup.group_key
        groupName = reGroup.group_name
        groupType = Code().getCodeDtlNm(reGroup.group_type)

        members = []
        reGroupMembers = ReGroupMember.objects.filter(Q(group_key = groupKey)).order_by("-is_leader")
        if len(reGroupMembers) > 0 :
            for reGroupMember in reGroupMembers :
                reMember = ReMember.objects.get(member_id = reGroupMember.member_id)
                member = {
                    "group_key": groupKey,
                    "group_name": groupName,
                    "group_type": groupType,
                    "is_leader": reGroupMember.is_leader,
                    "member_id": reMember.member_id,
                    "member_name": reMember.member_name,
                }
                members.append(member)

        group = {
            "group_key": groupKey,
            "group_name": groupName,
            "group_type": groupType,
            "members": members,
            "groups": getGroupsToJson(groupKey)
        }
        groups.append(group)

    return groups

def getGroupTree() :
    groups = getGroups()
    groupMembers = getGroupMembers()

    groupMembersDic = {}
    for groupMember in groupMembers :
        groupKey = groupMember["group_key"]
        isLeader = groupMember["is_leader"]
        teamLeader = ""
        if  isLeader == "Y" :
            teamLeader = "(팀리더)"

        for inx in range(len(groupMember["member_id"])) :

            if groupKey in groupMembersDic :
                groupMembersDic[groupKey].append({
                    "member_id": groupMember["member_id"][inx],
                    "member_name": groupMember["member_name"][inx] + teamLeader
                })
            else :
                groupMembersDic[groupKey] = [{
                    "member_id": groupMember["member_id"][inx],
                    "member_name": groupMember["member_name"][inx] + teamLeader
                }]

    node_map = {}
    for group in groups :
        node_map[group.group_key] = TreeNode(group.group_key, group.group_name)

    for group in groups :
        if group.parent_group_key != 0 :
            node = node_map.get(group.group_key)
            parent_node = node_map.get(group.parent_group_key)

            if parent_node is None : continue

            parent_node.addChildren(node)

            if group.group_key in groupMembersDic :
                childrens = groupMembersDic[group.group_key]
                for children in childrens :
                    node.addChildren(TreeNode(str(group.group_key) + "_" + str(children["member_id"]), children["member_name"]))

    return node_map.get(1)

def getGroupByMemberId(request) :
    memberId = request.user.id

    groups = getGroups()
    groupMembers = getGroupMembers()

    node_map = {}
    if isGroupLeader(memberId) :
        node_map = {}
        todoGroupKey = 0
        groupMembersDic = {}
        for groupMember in groupMembers :
            groupKey = groupMember["group_key"]

            for inx in range(len(groupMember["member_id"])) :
                if groupMember["member_id"][inx] == memberId :
                    todoGroupKey = groupKey

                if groupKey in groupMembersDic :
                    groupMembersDic[groupKey].append({
                        "member_id": groupMember["member_id"][inx],
                        "member_name": groupMember["member_name"][inx]
                    })
                else :
                    groupMembersDic[groupKey] = [{
                        "member_id": groupMember["member_id"][inx],
                        "member_name": groupMember["member_name"][inx]
                    }]

        for group in groups :
            node_map[group.group_key] = TreeNode(group.group_key, group.group_name)

        for group in groups :
            if group.parent_group_key != 0 :
                node = node_map.get(group.group_key)
                parent_node = node_map.get(group.parent_group_key)

                if parent_node is None : continue

                parent_node.addChildren(node)

                if group.group_key in groupMembersDic :
                    childrens = groupMembersDic[group.group_key]
                    for children in childrens :
                        node.addChildren(TreeNode(str(group.group_key) + "_" + str(children["member_id"]), children["member_name"]))

        # 홍경순 팀장님인 경우 전체 보기(최상위 그룹키)
        if (memberId == 22 or memberId == 225) :
            todoGroupKey = 1

        for key in node_map :
            if key == todoGroupKey :
                node_map = node_map[key]

    return node_map

def getGroupMembers() :
    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_group_member.get_group_members)
    cur.execute(query)

    groupMembers = dictfetchall(cur)
    if cur != None :
        cur.close()

    return groupMembers

def getGroupKeyByDepth(memberId, depth) :
    reGroups = ReGroup.objects.all()
    reGroupMember = ReGroupMember.objects.filter(member_id = memberId).first()
    return findGroupKey(reGroups, reGroupMember.group_key, depth)
    
def findGroupKey(reGroups, groupKey, depth) :
    for reGroup in reGroups :
        if groupKey == reGroup.group_key :
            if reGroup.group_depth == depth :
                break
            else :
                groupKey = findGroupKey(reGroups, reGroup.parent_group_key, depth)
            
    return groupKey

def isGroupLeader(memberId) :
    reGroupMembers = ReGroupMember.objects.filter(member_id = memberId)

    for reGroupMember in reGroupMembers :
        if reGroupMember.is_leader == "Y" :
            return True

    return False

def updateGroupMemberLeader(request, memberId) :
    try :
        groupKey = json.loads(request.body)["group_key"]
        reGroupMember = ReGroupMember.objects.get(group_key = groupKey, member_id = memberId)
        reGroupMember.is_leader = "Y"
        reGroupMember.save()
        print("success update group member leader")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def deleteGroupMember(request, memberId) :
    try :
        groupKey = json.loads(request.body)["group_key"]
        ReGroupMember.objects.get(group_key = groupKey, member_id = memberId).delete()
        print("success delete group member")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def queryConv(queryArr) :
    listQuery = ''
    for queryStr in queryArr :
        listQuery += queryStr
    return listQuery

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]
