from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q, Count, F, Value

# models
# from ai.models import AI_My_Settings
# from aieln.models import AI_ELN_My_Settings
from home.models import *
# from compound.models import My_Favorite_Compound, CompoundSAR_My_Settings
# from compoundbank.models import Compoundbank_My_Settings
# from compounddesign.models import Compounddesign_My_Settings
# from compoundmaterial.models import Compoundmaterial_My_Settings
# from compoundpatentability.models import Compoundpatentability_My_Settings
# from compoundsynthesis.models import Compoundsynthesis_My_Settings
# from compoundscreening.models import Compoundscreening_My_Settings
# from crystal.models import Crystal_My_Settings
# from hr.models import *
# from kpviewer.models import KPViewer_My_Settings
# from member.models import Member_My_Settings
# from my.models import MY_My_Settings
# from project.models import Project_My_Settings
# from screeningoutsourcing.models import Screeningoutsourcing_My_Settings
# from target.models import Target_My_Settings
# from todo.models import Todo_My_Settings, Todo_Control






############################################################################################################################
# hrlayout active 한 녀석을 하나 찾거나 지정하고 Home_Mysettings에 업데이트 한다.
############################################################################################################################
def update_active_hrlayout_to_home_mysettings_and_list_up_my_hrlayout_to_member(request):
    q_mysettings_home = get_mysettings_home(request)
    qs_hrlayout = HR_Layout.objects.filter(Q(check_discard=False) & Q(member=request.user.member))
    if qs_hrlayout is None or len(qs_hrlayout) == 0:
        messages.warning(request, f'멤버의 조직도 권한정보 쿼리가 없습니다. 관리자에게 문의하세요.')
        return None
    else:
        list_hr_layout_id = []
        for q_hrlayout in qs_hrlayout:
            if q_hrlayout.id not in list_hr_layout_id:
                list_hr_layout_id.append(q_hrlayout.id)
        data = {
            'list_hr_layout_id': list_hr_layout_id,
        }
        Member.objects.filter(id=request.user.member.id).update(**data)

    if q_mysettings_home.hrlayout is None:
        # q_hrlayout = HR_Layout.objects.filter(Q(check_discard=False) & Q(member=request.user.member) & Q(check_active=True)).last()
        q_hrlayout = HR_Layout.objects.filter(Q(check_discard=False) & Q(member=request.user.member) & Q(check_active=True)).last()
        if q_hrlayout is not None:
            data = {
                'hrlayout': q_hrlayout,
            }
            Home_My_Settings.objects.filter(id=q_mysettings_home.id).update(**data)
        else:
            i = 0
            for q_hrlayout in qs_hrlayout:
                if i == 0:
                    data = {
                        'check_active': True,
                    }
                    HR_Layout.objects.filter(id=q_hrlayout.id).update(**data)
                    q_hrlayout.refresh_from_db()
                    data = {
                        'hrlayout': q_hrlayout,
                    }
                    Home_My_Settings.objects.filter(id=q_mysettings_home.id).update(**data)
                else:
                    data = {
                        'check_active': False,
                    }
                    HR_Layout.objects.filter(id=q_hrlayout.id).update(**data)
                i = i + 1
            q_hrlayout = HR_Layout.objects.filter(Q(check_discard=False) & Q(member=request.user.member) & Q(check_active=True)).last()
        q_mysettings_home.refresh_from_db()
    return q_hrlayout




############################################################################################################################
# 신규 Authority 생성하기
############################################################################################################################
def initiate_superuser_authority_table():
    qs_user = User.objects.all()
    q_authority = Authority.objects.create()
    for AUTH_FIELD in LIST_AUTH_FIELD:
        for q_user in qs_user:
            if q_user.is_superuser:
                data = {
                    f'{AUTH_FIELD}':[q_user.id],
                }
                Authority.objects.filter(id=q_authority.id).update(**data)
    return q_authority

# Superuser Member, Profile 쿼리 생성/업데이트
def create_or_update_superuser_member_and_profile(request):
    q_user = request.user
    if q_user.is_superuser:
        q_member = Member.objects.filter(user=q_user).last()
        data = {
            'user': q_user,
            'member_name': f'Admin({q_user.id})'
        }
        if q_member is None:
            q_member = Member.objects.create(**data)
        else:
            pass
            # Member.objects.filter(id=q_member.id).update(**data)
        q_profile = Profile.objects.filter(user=q_user).last()
        data = {
            'user': q_user,
            'member': q_member,
            'name_korean': f'Admin({q_user.id})',
        }
        if q_profile is None:
            q_profile = Profile.objects.create(**data)
        else:
            pass
            # Profile.objects.filter(id=q_profile.id).update(**data)

############################################################################################################################
# 신규 User XXX My Settings 쿼리 모두 생성하기
############################################################################################################################

def create_or_update_default_mysettings(q_user):
    # print('444444')
    # My Favorites
    #########################################################################################
    # q_myfavorite_compound = My_Favorite_Compound.objects.filter(owner=q_user).last()
    q_myfavorite_compound = None
    if q_myfavorite_compound is None:
        data = {
            'owner':q_user,
        }
        # q_myfavorite_compound = My_Favorite_Compound.objects.create(**data)
        q_myfavorite_compound = None
        # print('Create New mysettings_home')

    # My Settings
    #########################################################################################
    # A
    # q_mysettings_ai = AI_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_ai = None
    if q_mysettings_ai is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_ai = AI_My_Settings.objects.create(**data)
        q_mysettings_ai = None
        # print('Create New mysettings_ai')

    # q_mysettings_aieln = AI_ELN_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_aieln = None
    if q_mysettings_aieln is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_aieln = AI_ELN_My_Settings.objects.create(**data)
        q_mysettings_aieln = None
        # print('Create New mysettings_aieln')
    # C
    # q_mysettings_compound = Compound_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compound = None
    if q_mysettings_compound is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_compound = Compound_My_Settings.objects.create(**data)
        Compound_My_Settings = None
        # print('Create New mysettings_compound')

    # q_mysettings_compoundbank = Compoundbank_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compoundbank = None
    if q_mysettings_compoundbank is None:
        data = {
            'owner':q_user,
            'myfavorite_compound': q_myfavorite_compound,
        }
        # q_mysettings_compoundbank = Compoundbank_My_Settings.objects.create(**data)
        q_mysettings_compoundbank = None
        # print('Create New mysettings_compoundbank')

    # q_mysettings_compounddesign = Compounddesign_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compounddesign = None
    if q_mysettings_compounddesign is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_compounddesign = Compounddesign_My_Settings.objects.create(**data)
        q_mysettings_compounddesign = None
        # print('Create New mysettings_compounddesign')

    # q_mysettings_compoundmaterial = Compoundmaterial_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compoundmaterial = None
    if q_mysettings_compoundmaterial is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_compoundmaterial = Compoundmaterial_My_Settings.objects.create(**data)
        q_mysettings_compoundmaterial = None
        # print('Create New mysettings_compoundmaterial')

    # q_mysettings_compoundsynthesis = Compoundsynthesis_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compoundsynthesis = None
    if q_mysettings_compoundsynthesis is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_compoundsynthesis = Compoundsynthesis_My_Settings.objects.create(**data)
        q_mysettings_compoundsynthesis = None
        # print('Create New mysettings_compoundsynthesis')

    # q_mysettings_compoundscreening = Compoundscreening_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compoundscreening = None
    if q_mysettings_compoundscreening is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_compoundscreening = Compoundscreening_My_Settings.objects.create(**data)
        q_mysettings_compoundscreening = None
        # print('Create New mysettings_compoundscreening')

    # q_mysettings_compoundsar = CompoundSAR_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compoundsar = None
    if q_mysettings_compoundsar is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_compoundsar = CompoundSAR_My_Settings.objects.create(**data)
        q_mysettings_compoundsar = None
        # print('Create New mysettings_compoundsar')

    # q_mysettings_compoundpatentabiltity = Compoundpatentability_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_compoundpatentabiltity = None
    if q_mysettings_compoundpatentabiltity is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_compoundpatentabiltity = Compoundpatentability_My_Settings.objects.create(**data)
        q_mysettings_compoundpatentabiltity = None
        # print('Create New mysettings_compoundsar')
    # q_mysettings_crystal = Crystal_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_crystal = None
    if q_mysettings_crystal is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_crystal = Crystal_My_Settings.objects.create(**data)
        q_mysettings_crystal = None
        # print('Create New mysettings_crystal')
    # H
    q_mysettings_hr = HR_My_Settings.objects.filter(owner=q_user).last()
    if q_mysettings_hr is None:
        data = {
            'owner':q_user,
        }
        if q_user.is_superuser == True:
            q_authority = initiate_superuser_authority_table()
            data['authority'] = q_authority
        q_mysettings_hr = HR_My_Settings.objects.create(**data)
        # print('Create New HR_My_Settings')
    # K
    # q_mysettings_kpviewer = KPViewer_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_kpviewer = None
    if q_mysettings_kpviewer is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_kpviewer = KPViewer_My_Settings.objects.create(**data)
        q_mysettings_kpviewer = None
        # print('Create New mysettings_crystal')
    # M
    q_mysettings_member = Member_My_Settings.objects.filter(owner=q_user).last()
    if q_mysettings_member is None:
        data = {
            'owner':q_user,
        }
        q_mysettings_member = Member_My_Settings.objects.create(**data)
        # print('Create New mysettings_crystal')
    # q_mysettings_my = MY_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_my = None
    if q_mysettings_my is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_my = MY_My_Settings.objects.create(**data)
        q_mysettings_my = None
    # P
    # q_mysettings_program = Program_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_program = None
    if q_mysettings_program is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_program = Program_My_Settings.objects.create(**data)
        q_mysettings_program = None
        # print('Create New mysettings_program')

    # q_mysettings_project = Project_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_project = None
    if q_mysettings_project is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_project = Project_My_Settings.objects.create(**data)
        q_mysettings_project = None
        # print('Create New mysettings_project')
    # S
    # q_mysettings_screeningoutsourcing = Screeningoutsourcing_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_screeningoutsourcing = None
    if q_mysettings_screeningoutsourcing is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_screeningoutsourcing = Screeningoutsourcing_My_Settings.objects.create(**data)
        q_mysettings_screeningoutsourcing = None
        # print('Create New mysettings_screeningoutsourcing')
    # T
    # q_mysettings_target = Target_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_target = None
    if q_mysettings_target is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_target = Target_My_Settings.objects.create(**data)
        q_mysettings_target = None
        # print('Create New mysettings_target')
    # q_mysettings_todo = Todo_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_todo = None

    if q_mysettings_todo is None:
        data = {
            'owner':q_user,
        }
        # q_mysettings_todo = Todo_My_Settings.objects.create(**data)
        q_mysettings_todo = None
        # print('Create New mysettings_todo')
    # if Todo_Control.objects.last() == None:
    #     data = {}
    #     Todo_Control.objects.create(**data)

    # Where Am I
    #########################################################################################
    # q_whereami = Where_Am_I.objects.filter(owner=q_user).last()
    q_whereami = None
    if q_whereami is None:
        data = {
            'owner':q_user,
        }
        # q_whereami = Where_Am_I.objects.create(**data)
        q_whereami = None
        # print('Create New whereami')

    # Home
    #########################################################################################
    # q_mysettings_home = Home_My_Settings.objects.filter(owner=q_user).last()
    q_mysettings_home = None
    data = {
        'owner':q_user,
        'whereami': q_whereami,
        'mysettings_ai': q_mysettings_ai,
        'mysettings_aieln': q_mysettings_aieln,
        # 'mysettings_compound': q_mysettings_compound,
        'mysettings_compound': None,
        'mysettings_compoundbank': q_mysettings_compoundbank,
        'mysettings_compounddesign': q_mysettings_compounddesign,
        'mysettings_compoundmaterial': q_mysettings_compoundmaterial,
        'mysettings_compoundpatentability': q_mysettings_compoundpatentabiltity,
        'mysettings_compoundsynthesis': q_mysettings_compoundsynthesis,
        'mysettings_compoundscreening': q_mysettings_compoundscreening,
        'mysettings_compoundsar': q_mysettings_compoundsar,
        'mysettings_crystal': q_mysettings_crystal,
        'mysettings_hr': q_mysettings_hr,
        'mysettings_kpviewer': q_mysettings_kpviewer,
        'mysettings_member': q_mysettings_member,
        'mysettings_my': q_mysettings_my,
        'mysettings_project': q_mysettings_project,
        'mysettings_program': q_mysettings_program,
        'mysettings_screeningoutsourcing': q_mysettings_screeningoutsourcing,
        'mysettings_target': q_mysettings_target,
        'mysettings_todo': q_mysettings_todo,
    }
    if q_mysettings_home is None:
        # q_mysettings_home = Home_My_Settings.objects.create(**data)
        q_mysettings_home = None
        # print('Create New mysettings_home')
    else:
        # Home_My_Settings.objects.filter(id=q_mysettings_home.id).update(**data)
        q_mysettings_home.refresh_from_db()
        # print('Update New mysettings_home')
    return True


# My Settings 생성
def get_mysettings_home(request):
    # create_or_update_default_mysettings(request.user)
    # q_mysettings_home = Home_My_Settings.objects.filter(owner=request.user).last()
    q_mysettings_home = None
    return q_mysettings_home


############################################################################################################################
# 앱별 XXX My Settings 쿼리 찾기/생성하기
############################################################################################################################

# XXX My Settings 쿼리 찾기/생성하기
def check_xxx_my_settings(request, q_mysettings_home, where_am_i):
    if where_am_i == 'ai':
        q_mysettings_xxx = q_mysettings_home.mysettings_ai
    if where_am_i == 'aieln':
        q_mysettings_xxx = q_mysettings_home.mysettings_aieln
    if where_am_i == 'compound':
        q_mysettings_xxx = q_mysettings_home.mysettings_compound
    if where_am_i == 'compoundbank':
        q_mysettings_xxx = q_mysettings_home.mysettings_compoundbank
    if where_am_i == 'compounddesign':
        q_mysettings_xxx = q_mysettings_home.mysettings_compounddesign
    if where_am_i == 'compoundmaterial':
        q_mysettings_xxx = q_mysettings_home.mysettings_compoundmaterial
    if where_am_i == 'compoundpatentability':
        q_mysettings_xxx = q_mysettings_home.mysettings_compoundpatentability
    if where_am_i == 'compoundsynthesis':
        q_mysettings_xxx = q_mysettings_home.mysettings_compoundsynthesis
    if where_am_i == 'compoundscreening':
        q_mysettings_xxx = q_mysettings_home.mysettings_compoundscreening
    if where_am_i == 'compoundsar':
        q_mysettings_xxx = q_mysettings_home.mysettings_compoundsar
    if where_am_i == 'crystal':
        q_mysettings_xxx = q_mysettings_home.mysettings_crystal
    if where_am_i == 'member':
        q_mysettings_xxx = q_mysettings_home.mysettings_member
    if where_am_i == 'my':
        q_mysettings_xxx = q_mysettings_home.mysettings_my
    if where_am_i == 'hr':
        q_mysettings_xxx = q_mysettings_home.mysettings_hr
    if where_am_i == 'kpviewer':
        q_mysettings_xxx = q_mysettings_home.mysettings_kpviewer
    if where_am_i == 'project':
        q_mysettings_xxx = q_mysettings_home.mysettings_project
    if where_am_i == 'program':
        q_mysettings_xxx = q_mysettings_home.mysettings_program
    if where_am_i == 'program':
        q_mysettings_xxx = q_mysettings_home.mysettings_screeningoutsourcing
    if where_am_i == 'target':
        q_mysettings_xxx = q_mysettings_home.mysettings_target
    if where_am_i == 'todo':
        q_mysettings_xxx = q_mysettings_home.mysettings_todo
    return q_mysettings_xxx



def get_xxx_my_settings(request, q_mysettings_home, where_am_i):
    q_mysettings_xxx = check_xxx_my_settings(request, q_mysettings_home, where_am_i)
    if q_mysettings_xxx is None:
        # create_or_update_default_mysettings(request.user)
        q_mysettings_xxx = check_xxx_my_settings(request, q_mysettings_home, where_am_i)
    return q_mysettings_xxx





############################################################################################################################
# User 위치 파악하기
############################################################################################################################

def reset_where_am_i(request, q_mysettings_home):
    return
    for site in LIST_SITE_MAP_FIELD:
        if site == 'level':
            data = {
                f'{site}': 0,
            }
        else:
            data = {
                f'{site}': None,
            }
        if q_mysettings_home.whereami is not None:
            Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
        else:
            data = {
                'owner': request.user,
            }
            Where_Am_I.objects.create(**data)
    # print('reset done!')


def save_where_am_i(request, whereami, q_mysettings_home):
    return
    # print('where am i?', whereami)
    reset_where_am_i(request, q_mysettings_home)
    if whereami in SITE_MAP_BASE:
        data = {
            'base': whereami,
            'level': 0,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_MEMBER:
        data = {
            'base': 'member',
            'member': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_TARGET:
        data = {
            'base': 'target',
            'target': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_TARGET_GENE:
        data = {
            'base': 'target',
            'target': 'target_gene',
            'target_gene': whereami,
            'level': 2,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_TARGET_PROTEIN:
        data = {
            'base': 'target',
            'target': 'target_protein',
            'target_protein': whereami,
            'level': 2,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_PROGRAM:
        data = {
            'base': 'program',
            'program': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_PROTOCOL:
        data = {
            'base': 'protocol',
            'protocol': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_COMPOUND:
        data = {
            'base': 'compound',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_COMPOUND_SEARCH:
        data = {
            'base': 'compound',
            'compound': 'compound_search',
            'compound_search': whereami,
            'level': 2,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_COMPOUND_REGISTER:
        data = {
            'base': 'compound',
            'compound': 'compound_register',
            'compound_register': whereami,
            'level': 2,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_COMPOUND_SAR:
        data = {
            'base': 'compound',
            'compound': 'compound_sar',
            'compound_sar': whereami,
            'level': 2,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_CRYSTAL:
        data = {
            'base': 'crystal',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_SCREENING:
        data = {
            'base': 'screening',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_PRECLINICAL:
        data = {
            'base': 'preclinical',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_ELN:
        data = {
            'base': 'eln',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_STUDY:
        data = {
            'base': 'study',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_WAREHOUSE:
        data = {
            'base': 'warehouse',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_BD:
        data = {
            'base': 'bd',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)
    if whereami in SITE_MAP_HR:
        data = {
            'base': 'hr',
            'compound': whereami,
            'level': 1,
        }
        Where_Am_I.objects.filter(id=q_mysettings_home.whereami.id).update(**data)


def home_function(request):
    return {
        'SITE_MAP_BASE': None,
        'q_mysettings_home': None,
        'whereami': None,
    }
    # print('#-------------------- My Settings home function ')
    q_mysettings_home = get_mysettings_home(request)
    whereami = SITE_MAP_BASE[0]
    save_where_am_i(request, whereami, q_mysettings_home)
    # Superuser Member, Profile 쿼리 생성/업데이트
    create_or_update_superuser_member_and_profile(request)

    ####################################################
    if request.method == 'GET':
        context = {
            'SITE_MAP_BASE': SITE_MAP_BASE,
            'q_mysettings_home': q_mysettings_home,
            'whereami': whereami,
        }
        return context
    pass


