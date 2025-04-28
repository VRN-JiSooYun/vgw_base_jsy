from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q, Count, F, Value
from django.conf import settings
from django.db import connection, transaction
# models
from home.models import *
# from compound.models import *
# from compoundbank.models import *
from hr.models import *
# from project.models import *



#####################################################################################################
############################################ Common #################################################
#####################################################################################################
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

def queryConv(queryArr) :
    listQuery = ''
    for queryStr in queryArr :
        listQuery += queryStr
    return listQuery


#####################################################################################################
###################################### Structure Authority ##########################################
#####################################################################################################
def checkStructureAuthority(request, compound_code) :
    if request == None :
        raise Exception('An error occurred with request is not defined.')
    if compound_code == None or compound_code == '' :
        raise Exception('An error occurred with compound_code is not defined.')

    owner_id = request.user.id
    visible = False
    modify = False

    compound = Design_Compound_V2.objects.filter(Q(check_discard=False) & Q(compound_code=compound_code)).last()
    q_authority = Authority.objects.filter(check_discard=False).last()
    auth_d = -1
    auth_r = -1
    auth_v = -1
    try :
        auth_d = q_authority.auth_compound_design.index(request.user.member.id)
    except :
        pass
    try :
        auth_r = q_authority.auth_compound_register.index(request.user.member.id)
    except :
        pass
    try :
        auth_v = q_authority.auth_compound_validation.index(request.user.member.id)
    except :
        pass

    if compound == None :
        raise Exception('An error occurred with compound is not exist.')
    user_id = compound.owner_id

    # 특수 화합물 체크
    if compound.check_struct_invisible :
        # 무조건 못 봄.
        visible = False
        # compound D 권한이 있을 경우 수정 가능
        if auth_d >= 0 :
            modify = True

    else :
        if compound.check_reference :
            visible = True

        # 특정 화합물로 visible 권한이 있을 경우
        compound_auth = Design_Compound_Authority.objects.filter(Q(check_discard=False) & Q(compound_code=compound_code) & Q(auth_id=owner_id)).last()
        if compound_auth != None :
            visible = True

        if owner_id == user_id :
            # 본인이 등록한 화합물.
            visible = True
            # compound R 권한이 있을 경우 수정 가능
            if auth_r >= 0 :
                modify = True
        else :
            # 본인이 올리지 않은 화합물.

            # project - structure 권한이 있는지 여부
            project_compounds = Design_Project_Compound.objects.filter(Q(compound_code=compound_code)).all()
            project_struct = Project_Project_Struct.objects.filter(Q(owner_id=owner_id)).all()
            for p_compound in project_compounds :
                for s_project in project_struct :
                    if p_compound.project_code == s_project.project_code :
                        visible = True
                        if auth_v >= 0 :
                            modify = True
                        break

            # 팀원이 올린 건지 체크
            cur = connection.cursor()
            searchQueryArr = settings.QUERY_INFO.authority.get_members
            searchQueryArr = queryConv(searchQueryArr)

            cur.execute(searchQueryArr, (owner_id,owner_id,))
            team_data = dictfetchall(cur)
            if len(team_data) > 0 :
                if team_data[0].get('user_id') != None and user_id in team_data[0].get('user_id') :
                    visible = True
                    # compound V 권한이 있을 경우 수정 가능
                    if auth_v >= 0 :
                        modify = True



    return {"visible":visible, "modify":modify}


def getTeamMember(request) :
    cur = connection.cursor()
    listQueryArr = settings.QUERY_INFO.common.get_team_member
    listQuery = queryConv(listQueryArr)
    cur.execute( listQuery, (request.user.id,) )
    team_data = dictfetchall(cur)

    return team_data[0].get('members')