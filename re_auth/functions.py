from re_auth.models import *
from re_group.models import *
from hr.models import *
from re_group.functions import *

def getTargets() :
    return [
        # 공통 #########################################
        { "display": "Member", "name": "member", "isActive": False },
        { "display": "News", "name": "news", "isActive": True },
        { "display": "Myhome", "name": "myhome", "isActive": True },
        { "display": "Todo", "name": "todo", "isActive": True },
        { "display": "Chat GPT", "name": "chatgpt", "isActive": True },
        { "display": "Tracking", "name": "tracking", "isActive": False },
        # 경영 ###############################################
        { "display": "Human R","name": "hr", "isActive": True },
        { "display": "IPS", "name": "ips", "isActive": True },
        { "display": "Business D.", "name": "bd", "isActive": False },
        { "display": "BD QnA", "name": "bdqna", "isActive": False },
        { "display": "Financial M.", "name": "finance", "isActive": False },
        { "display": "Intellectual P.", "name": "ip", "isActive": False },
        { "display": "Material M.", "name": "material", "isActive": False },
        { "display": "Purchasing M.", "name": "purchasing", "isActive": False },
        # Program 관련 ##############################################
        { "display": "Competitor", "name": "competitor", "isActive": False },
        { "display": "Program", "name": "program", "isActive": False },
        { "display": "TPP", "name": "tpp", "isActive": False },
        { "display": "Target", "name": "target", "isActive": False },
        # RnD AI #################################################
        { "display": "AI_ELN", "name": "aieln", "isActive": False },
        { "display": "AI Lab(MMPA)", "name": "aigeneration", "isActive": False },
        { "display": "AI Lab(PDF2Smiles)", "name": "pdf2smiles", "isActive": False },
        { "display": "AI Lab(RxnFinder)", "name": "rxnfinder", "isActive": False },
        # RnD Medichem #################################################
        { "display": "Compound", "name": "compound", "isActive": True },
        { "display": "Project", "name": "project", "isActive": True },
        { "display": "Structure", "name": "structure", "isActive": True },
        { "display": "KP Viewer", "name": "kpviewer", "isActive": True },
        { "display": "Patentability", "name": "patentability", "isActive": False },
        { "display": "SAR", "name": "sar", "isActive": False },
        { "display": "Inventory", "name": "inventory", "isActive": True },
        { "display": "PDB Summary", "name": "pdbsummary", "isActive": True },
        # 현재 사용 안함 #################################################
        { "display": "controlcompound", "name": "controlcompound", "isActive": False },
        { "display": "compoundsynthesis", "name": "compoundsynthesis", "isActive": False },
        { "display": "compoundscreening", "name": "compoundscreening", "isActive": False },
        # RnD Bio #################################################
        { "display": "Bio Study", "name": "biostudy", "isActive": False },
        { "display": "Bio ELN", "name": "bioeln", "isActive": False },
        { "display": "Crystal", "name": "crystal", "isActive": False },
        { "display": "Dashboard", "name": "dashboard", "isActive": True },
        { "display": "Assay", "name": "dashboardpk", "isActive": True },
        { "display": "Excel download", "name": "exceldownload", "isActive": False },
        { "display": "Tumor Manager", "name": "tumormanager", "isActive": True },
        { "display": "IACUC(Animal)", "name": "iacuc", "isActive": False },
        { "display": "Protocol", "name": "protocol", "isActive": False },
        { "display": "Screening in-Vitro", "name": "screeninginvitro", "isActive": False },
        { "display": "Screening in-Vivo", "name": "screeninginvivo", "isActive": False },
    ]

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

def getAuth() :
    return Authority.objects.filter(check_discard=False).last()

def initAuth(memberId) :
    auth = getAuth()

    if memberId not in auth.auth_news : auth.auth_news.append(memberId)
    if memberId not in auth.auth_news_register : auth.auth_news_register.append(memberId)
    if memberId not in auth.auth_news_validation : auth.auth_news_validation.append(memberId)
    if memberId not in auth.auth_news_design : auth.auth_news_design.append(memberId)
    if memberId not in auth.auth_myhome : auth.auth_myhome.append(memberId)
    if memberId not in auth.auth_myhome_register : auth.auth_myhome_register.append(memberId)
    if memberId not in auth.auth_myhome_validation : auth.auth_myhome_validation.append(memberId)
    if memberId not in auth.auth_myhome_design : auth.auth_myhome_design.append(memberId)

    auth.save()

def updateAuth(auths, memberId) :
    authority = Authority.objects.filter(check_discard=False).last()
    authority.member_id = memberId

    targets = getTargets()
    for target in targets :
        targetName = "auth_" + target["name"]
        if targetName in auths : setattr(authority, targetName, auths[targetName])
        targetName = "auth_" + target["name"] + "_register"
        if targetName in auths : setattr(authority, targetName, auths[targetName])
        targetName = "auth_" + target["name"] + "_validation"
        if targetName in auths : setattr(authority, targetName, auths[targetName])
        targetName = "auth_" + target["name"] + "_design"
        if targetName in auths : setattr(authority, targetName, auths[targetName])

    authority.save()
    print("success update authority :", memberId)

    reAuthorityHistory = ReAuthorityHistory()
    reAuthorityHistory.title = authority.title
    reAuthorityHistory.check_discard = authority.check_discard
    reAuthorityHistory.list_member_id_all_part = authority.list_member_id_all_part
    reAuthorityHistory.member_id = memberId

    for target in targets :
        targetName = "auth_" + target["name"]
        setattr(reAuthorityHistory, targetName, getattr(authority, targetName))

        targetName = "auth_" + target["name"] + "_register"
        setattr(reAuthorityHistory, targetName, getattr(authority, targetName))

        targetName = "auth_" + target["name"] + "_validation"
        setattr(reAuthorityHistory, targetName, getattr(authority, targetName))

        targetName = "auth_" + target["name"] + "_design"
        setattr(reAuthorityHistory, targetName, getattr(authority, targetName))

    reAuthorityHistory.save()
    print("success update re authority history :", memberId)

def deleteAuth(memberId) :
    authority = Authority.objects.filter(check_discard=False).last()

    auths = {}
    targets = getTargets()
    for target in targets :
        targetName = "auth_" + target["name"]
        auth_p = getattr(authority, targetName)
        if memberId in auth_p :
            auth_p.remove(memberId)
        auths[targetName] = auth_p
        # print(','.join(str(x) for x in auth_p ))

        targetName = "auth_" + target["name"] + "_register"
        auth_r = getattr(authority, targetName)
        if memberId in auth_r :
            auth_r.remove(memberId)
        auths[targetName] = auth_r
        # print(','.join(str(x) for x in auth_r ))

        targetName = "auth_" + target["name"] + "_validation"
        auth_v = getattr(authority, targetName)
        if memberId in auth_v :
            auth_v.remove(memberId)
        auths[targetName] = auth_v
        # print(','.join(str(x) for x in auth_v ))

        targetName = "auth_" + target["name"] + "_design"
        auth_d = getattr(authority, targetName)
        if memberId in auth_d :
            auth_d.remove(memberId)
        auths[targetName] = auth_d
        # print(','.join(str(x) for x in auth_d ))

    updateAuth(auths, memberId)