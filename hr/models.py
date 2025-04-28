from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from member.models import *
# from project.models import *
import datetime

#################################################################################
#
#   Model Table 작성 및 수정 방법
#
#
#  1. Field 추가시 Table 제일 아랫줄에 작성하여 migration 한다.
#  2. Git Push 한다.
#  3. 필요시 원하는 위치로 이동한 뒤 migration 한다.
#  4. Git Push 한다.
#
#  !. null=True, blank=True는 기본적으로 기입 가능한 모든 field에 추가한다.
#
#################################################################################



#--------------------------------------------------------------------------------------------------------------------------
# HR 기본 시간값 세팅
#--------------------------------------------------------------------------------------------------------------------------
class HR_Default_Settings(models.Model):
    default_user_password = models.CharField(max_length=100, null=True, blank=True)
    default_datebaseline_time = models.TimeField(null=True, blank=True, default=datetime.time(4, 0)) # 날짜 기준선

    default_time_start_standard = models.TimeField(null=True, blank=True, default=datetime.time(9, 0)) # 정상출근시간
    default_time_start_early = models.TimeField(null=True, blank=True, default=datetime.time(7, 0)) # 조기출근간주시간
    default_time_end_standard = models.TimeField(null=True, blank=True, default=datetime.time(18, 0)) # 정상퇴근시간
    default_time_end_lately = models.TimeField(null=True, blank=True, default=datetime.time(20, 0)) # 야근시작시간

    default_lunchtime_start = models.TimeField(null=True, blank=True, default=datetime.time(12, 30)) # 점심식사 시작시간
    default_lunchtime_end = models.TimeField(null=True, blank=True, default=datetime.time(13, 30)) # 점심식사 종료시간
    default_dinnertime_start = models.TimeField(null=True, blank=True, default=datetime.time(18, 30)) # 저녁식사 시작시간
    default_dinnertime_end = models.TimeField(null=True, blank=True, default=datetime.time(19, 30)) # 저녁식사 종료시간

    # 점심식사 저녁식사 시간 빼기 기준
    check_default_baseline_lunchtime_start = models.BooleanField(default=False) # True: 점심식사 한것으로 간주하는 근무시작시간 기준선 활성화
    check_default_baseline_lunchtime_end = models.BooleanField(default=False) # True: 점심식사 한것으로 간주하는 근무종료시간 기준선 활성화
    check_default_baseline_dinnertime_start = models.BooleanField(default=False) # True: 저녁식사 한것으로 간주하는 근무시작시간 기준선 활성화
    check_default_baseline_dinnertime_end = models.BooleanField(default=False) # True: 저녁식사 한것으로 간주하는 근무종료시간 기준선 활성화

    default_margin_lunchtime_involved = models.TimeField(null=True, blank=True, default=datetime.time(1, 0)) # 점심식사시간 기준 점심식사 한것으로 간주하는 마진
    default_margin_dinnertime_involved = models.TimeField(null=True, blank=True, default=datetime.time(1, 0)) # 저녁식사시간 기준 저녁식사 한것으로 간주하는 마진

    default_baseline_lunchtime_start = models.TimeField(null=True, blank=True, default=datetime.time(11, 0)) # 점심식사 한것으로 간주하는 근무시작시간 기준선
    default_baseline_lunchtime_end = models.TimeField(null=True, blank=True, default=datetime.time(14, 0)) # 점심식사 한것으로 간주하는 근무종료시간 기준선
    default_baseline_dinnertime_start = models.TimeField(null=True, blank=True, default=datetime.time(17, 0)) # 저녁식사 한것으로 간주하는 근무시작시간 기준선
    default_baseline_dinnertime_end = models.TimeField(null=True, blank=True, default=datetime.time(20, 0)) # 저녁식사 한것으로 간주하는 근무종료시간 기준선




#--------------------------------------------------------------------------------------------------------------------------
# HR 기타 세팅 관리
#--------------------------------------------------------------------------------------------------------------------------
class HR_Document_Minor_Settings(models.Model):
    # data = {
    #     'name': q_hrlayout.member.user.profile.name_korean,
    #     'position': position_str,
    #     'email': email_str,
    #     'phone_mobile': phone_mobile_str,
    #     'hrlayout_id': q_hrlayout.id,
    #     'profile_id': q_profile.id,
    #     'list_dict_default_wkt_standard_personalized': list_dict_default_wkt_standard_personalized,  # 개인맞춤형 멤버만 해당
    # }

    # 출퇴근관리 제외자 정보
    list_dict_wkt_issued_check_excepter = models.JSONField(verbose_name="출근 체크 리스트에서 제외하는 멤버 Dict 정보 리스트", null=True, blank=True)  #
    list_profile_id_wkt_issued_check_excepter = models.JSONField(verbose_name="출근 체크 리스트에서 제외하는 멤버 리스트 프로필 ID", null=True, blank=True)  #
    # 출퇴근 개인맞춤형 관리자 정보
    list_dict_wkt_issued_check_personalized = models.JSONField(verbose_name="개인 맞춤형 출퇴근 멤버 Dict 정보 리스트", null=True, blank=True)  #
    list_profile_id_wkt_issued_check_personalized = models.JSONField(verbose_name="개인 맞춤형 출퇴근 멤버 리스트 프로필 ID", null=True, blank=True)  #
    # System
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)




#--------------------------------------------------------------------------------------------------------------------------
# 멤버별 인사조직도상의 포지션 정보
#--------------------------------------------------------------------------------------------------------------------------
class HR_Layout(models.Model):
    position = models.CharField(max_length=250, null=True, blank=True) # Position 이름
    # 조직도
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    # 해당포지션의 리더들
    company_leader = models.ForeignKey(Member, related_name="회사리더", on_delete=models.SET_NULL, null=True, blank=True)
    division_leader = models.ForeignKey(Member, related_name="부서리더", on_delete=models.SET_NULL, null=True, blank=True)
    team_leader = models.ForeignKey(Member, related_name="팀리더", on_delete=models.SET_NULL, null=True, blank=True)
    # 담당자 / 후임자
    member = models.ForeignKey(Member, related_name="담당자", on_delete=models.CASCADE, null=True, blank=True) # 해당 포지션 담당자
    list_member_taken_this_position_id = models.JSONField(null=True, blank=True)  # 현재 포지션을 거쳐간 멤버 id 리스트
    #--------------------------------------------------------------------------------------------------------------------------
    # check leader
    check_team_leader = models.BooleanField(default=False)
    check_division_leader = models.BooleanField(default=False)
    check_company_leader = models.BooleanField(default=False)
    # check status
    check_active = models.BooleanField(default=False) # True : 복수의 포지션을 가지고 있는 멤버의 현재 선택된 포지션. 및 단수의 포지션을 가지고 있는 모든 멤버
    check_backup = models.BooleanField(default=False) # Backup용 데이터, 바로직전 1번만
    check_discard = models.BooleanField(default=False)
    #--------------------------------------------------------------------------------------------------------------------------
    # version
    version = models.IntegerField(default=1)

    def __str__(self):
        if self.member is not None:
            return self.member.member_name
        else:
            return str(self.id)


#--------------------------------------------------------------------------------------------------------------------------
# 보직변경 처리 관련
#--------------------------------------------------------------------------------------------------------------------------
MEMBER_SHIFT_TYPE = (
    ('RESIGN', '퇴사에 따른 변경'),
    ('PROMOTION', '승진에 따른 변경'),
    ('OPEN', '신규 보직 생성에 따른 변경'),
    ('CLOSED', '기존 보직 삭제에 따른 변경'),
)

class HR_Layout_Member_Management(models.Model):
    hrlayout = models.ForeignKey(HR_Layout, related_name="predecessor_to_successor", on_delete=models.CASCADE, null=True, blank=True) # 전임자 권한 => 후임자 권한으로 승계
    #--------------------------------------------------------------------------------------------------------------------------
    # 전임자 정보 (백업하여 저장, 후임자에게 기존 정보를 물려줘야 하기에.== 권한 및 포지션의 member 정보를 바꿔치기 함), 백업에는 바꿔치기 전의 정보
    #--------------------------------------------------------------------------------------------------------------------------
    # 전임자 멤버정보 백업
    member_predecessor = models.ForeignKey(Member, related_name="전임자", on_delete=models.SET_NULL, null=True, blank=True) # 해당 보직을 넘겨주는 자
    # 전임자 권한 백업
    hrlayout_predecessor_backup = models.ForeignKey(HR_Layout, related_name="for_predecessor_backup", on_delete=models.SET_NULL, null=True, blank=True) # 백업된 전임자 권한
    # 전임자 포지션 백업 리스트
    list_m2t_id = models.JSONField(null=True, blank=True)
    list_m2d_id = models.JSONField(null=True, blank=True)
    list_m2c_id = models.JSONField(null=True, blank=True)
    list_t2d_id = models.JSONField(null=True, blank=True)
    list_d2c_id = models.JSONField(null=True, blank=True)
    list_c2g_id = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    check_member_successor_exist = models.BooleanField(default=False)  # True: 보직 넘겨받는 사람이 있는 경우
    #--------------------------------------------------------------------------------------------------------------------------
    # 후임자 정보
    #--------------------------------------------------------------------------------------------------------------------------
    member_successor = models.ForeignKey(Member, related_name="후임자", on_delete=models.SET_NULL, null=True, blank=True) # 해당 보작을 넘겨받는 자
    #--------------------------------------------------------------------------------------------------------------------------
    shift_type = models.CharField(max_length=250, choices=MEMBER_SHIFT_TYPE, null=True, blank=True) # 보직 변경 타입
    date_shift = models.DateField(null=True, blank=True)
    comment = models.CharField(max_length=250, null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # check flag
    check_completed = models.BooleanField(default=False)  # 변경처리 완료시
    check_discard = models.BooleanField(default=False)
    #--------------------------------------------------------------------------------------------------------------------------
    # system
    date_created = models.DateField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        if self.hrlayout is not None:
            return self.hrlayout.member.member_name
        else:
            return str(self.id)








################################################################################################
################################################################################################
################################################################################################
#
#                                       Authority
#
################################################################################################
################################################################################################
################################################################################################


LIST_AUTH_FIELD = [
    # 공통 #########################################
    # member
    'auth_member',
    'auth_member_register',
    'auth_member_validation',
    'auth_member_design',
    # todo
    'auth_todo',
    'auth_todo_register',
    'auth_todo_validation',
    'auth_todo_design',
    # chatGPT
    'auth_chatgpt',
    'auth_chatgpt_register',
    'auth_chatgpt_validation',
    'auth_chatgpt_design',
    # tracking
    'auth_tracking',
    'auth_tracking_register',
    'auth_tracking_validation',
    'auth_tracking_design',

    # Program ##############################################
    # competitor
    'auth_competitor',
    'auth_competitor_register',
    'auth_competitor_validation',
    'auth_competitor_design',
    # program
    'auth_program',
    'auth_program_register',
    'auth_program_validation',
    'auth_program_design',
    # TPP
    'auth_tpp',
    'auth_tpp_register',
    'auth_tpp_validation',
    'auth_tpp_design',
    # Target
    'auth_target',
    'auth_target_register',
    'auth_target_validation',
    'auth_target_design',


    # RnD AI #################################################
    # AI ELN
    'auth_aieln',
    'auth_aieln_register',
    'auth_aieln_validation',
    'auth_aieln_design',
    # AI Generation
    'auth_aigeneration',
    'auth_aigeneration_register',
    'auth_aigeneration_validation',
    'auth_aigeneration_design',
    # PDF2Smiles
    'auth_pdf2smiles',
    'auth_pdf2smiles_register',
    'auth_pdf2smiles_validation',
    'auth_pdf2smiles_design',
    # RxnFinder
    'auth_rxnfinder',
    'auth_rxnfinder_register',
    'auth_rxnfinder_validation',
    'auth_rxnfinder_design',


    # RnD Medichem #################################################
    # compound
    'auth_compound',
    'auth_compound_register',
    'auth_compound_validation',
    'auth_compound_design',
    # project
    'auth_project',
    'auth_project_register',
    'auth_project_validation',
    'auth_project_design',
    # structure
    'auth_structure',
    'auth_structure_register',
    'auth_structure_validation',
    'auth_structure_design',
    # kpviewer
    'auth_kpviewer',
    'auth_kpviewer_register',
    'auth_kpviewer_validation',
    'auth_kpviewer_design',
    # patentability
    'auth_patentability',
    'auth_patentability_register',
    'auth_patentability_validation',
    'auth_patentability_design',
    # sar
    'auth_sar',
    'auth_sar_register',
    'auth_sar_validation',
    'auth_sar_design',
    # inventory
    'auth_inventory',
    'auth_inventory_register',
    'auth_inventory_validation',
    'auth_inventory_design',
    # control compound
    'auth_controlcompound',
    'auth_controlcompound_register',
    'auth_controlcompound_validation',
    'auth_controlcompound_design',
    # compoundsynthesis
    'auth_compoundsynthesis',
    'auth_compoundsynthesis_register',
    'auth_compoundsynthesis_validation',
    'auth_compoundsynthesis_design',
    # compoundscreening
    'auth_compoundscreening',
    'auth_compoundscreening_register',
    'auth_compoundscreening_validation',
    'auth_compoundscreening_design',


    # RnD Bio #################################################
    # Bio Study
    'auth_biostudy',
    'auth_biostudy_register',
    'auth_biostudy_validation',
    'auth_biostudy_design',
    # Bio ELN
    'auth_bioeln',
    'auth_bioeln_register',
    'auth_bioeln_validation',
    'auth_bioeln_design',
    # crystal
    'auth_crystal',
    'auth_crystal_register',
    'auth_crystal_validation',
    'auth_crystal_design',
    # dashboard
    'auth_dashboard',
    'auth_dashboard_register',
    'auth_dashboard_validation',
    'auth_dashboard_design',
    # dashboard pk
    # ==> assay로 메뉴명만 변경
    'auth_dashboardpk',
    'auth_dashboardpk_register',
    'auth_dashboardpk_validation',
    'auth_dashboardpk_design',
    # excel_download
    'auth_exceldownload',
    'auth_exceldownload_register',
    'auth_exceldownload_validation',
    'auth_exceldownload_design',
    # tumormanager
    'auth_tumormanager',
    'auth_tumormanager_register',
    'auth_tumormanager_validation',
    'auth_tumormanager_design',
    # iacuc
    'auth_iacuc',
    'auth_iacuc_register',
    'auth_iacuc_validation',
    'auth_iacuc_design',
    # Protocol
    'auth_protocol',
    'auth_protocol_register',
    'auth_protocol_validation',
    'auth_protocol_design',
    # screening invitro
    'auth_screeninginvitro',
    'auth_screeninginvitro_register',
    'auth_screeninginvitro_validation',
    'auth_screeninginvitro_design',
    # screening invivo (animal)
    'auth_screeninginvivo',
    'auth_screeninginvivo_register',
    'auth_screeninginvivo_validation',
    'auth_screeninginvivo_design',


    # 경영 ###############################################
    # bd
    'auth_bd',
    'auth_bd_register',
    'auth_bd_validation',
    'auth_bd_design',
    # bdqna
    'auth_bdqna',
    'auth_bdqna_register',
    'auth_bdqna_validation',
    'auth_bdqna_design',
    # finance
    'auth_finance',
    'auth_finance_register',
    'auth_finance_validation',
    'auth_finance_design',
    # human resources
    'auth_hr',
    'auth_hr_register',
    'auth_hr_validation',
    'auth_hr_design',
    # ip
    'auth_ip',
    'auth_ip_register',
    'auth_ip_validation',
    'auth_ip_design',
    # material and resources
    'auth_material',
    'auth_material_register',
    'auth_material_validation',
    'auth_material_design',
    # purchasing
    'auth_purchasing',
    'auth_purchasing_register',
    'auth_purchasing_validation',
    'auth_purchasing_design',
]


# 각 필드에는 권한을 가진 멤버 ID값이 들어있다.
class Authority(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)

    ##################################################################################
    # check_list
    ##################################################################################
    check_discard = models.BooleanField(default=False)
    list_member_id_all_part = models.JSONField(null=True, blank=True)
    # 공통 #########################################
    # member
    auth_member = models.JSONField(null=True, blank=True)
    auth_member_register = models.JSONField(null=True, blank=True)
    auth_member_validation = models.JSONField(null=True, blank=True)
    auth_member_design = models.JSONField(null=True, blank=True)
    # news
    auth_news = models.JSONField(null=True, blank=True)
    auth_news_register = models.JSONField(null=True, blank=True)
    auth_news_validation = models.JSONField(null=True, blank=True)
    auth_news_design = models.JSONField(null=True, blank=True)
    # myhome
    auth_myhome = models.JSONField(null=True, blank=True)
    auth_myhome_register = models.JSONField(null=True, blank=True)
    auth_myhome_validation = models.JSONField(null=True, blank=True)
    auth_myhome_design = models.JSONField(null=True, blank=True)
    # todo
    auth_todo = models.JSONField(null=True, blank=True)
    auth_todo_register = models.JSONField(null=True, blank=True)
    auth_todo_validation = models.JSONField(null=True, blank=True)
    auth_todo_design = models.JSONField(null=True, blank=True)
    # chatGPT
    auth_chatgpt = models.JSONField(null=True, blank=True)
    auth_chatgpt_register = models.JSONField(null=True, blank=True)
    auth_chatgpt_validation = models.JSONField(null=True, blank=True)
    auth_chatgpt_design = models.JSONField(null=True, blank=True)
    # tracking
    auth_tracking = models.JSONField(null=True, blank=True)
    auth_tracking_register = models.JSONField(null=True, blank=True)
    auth_tracking_validation = models.JSONField(null=True, blank=True)
    auth_tracking_design = models.JSONField(null=True, blank=True)

    # Program 관련 ##############################################
    # Competitor
    auth_competitor = models.JSONField(null=True, blank=True)
    auth_competitor_register = models.JSONField(null=True, blank=True)
    auth_competitor_validation = models.JSONField(null=True, blank=True)
    auth_competitor_design = models.JSONField(null=True, blank=True)
    # Program
    auth_program = models.JSONField(null=True, blank=True)
    auth_program_register = models.JSONField(null=True, blank=True)
    auth_program_validation = models.JSONField(null=True, blank=True)
    auth_program_design = models.JSONField(null=True, blank=True)
    # TPP
    auth_tpp = models.JSONField(null=True, blank=True)
    auth_tpp_register = models.JSONField(null=True, blank=True)
    auth_tpp_validation = models.JSONField(null=True, blank=True)
    auth_tpp_design = models.JSONField(null=True, blank=True)
    # Target
    auth_target = models.JSONField(null=True, blank=True)
    auth_target_register = models.JSONField(null=True, blank=True)
    auth_target_validation = models.JSONField(null=True, blank=True)
    auth_target_design = models.JSONField(null=True, blank=True)

    # RnD AI #################################################
    # AI Generation
    auth_aieln = models.JSONField(null=True, blank=True)
    auth_aieln_register = models.JSONField(null=True, blank=True)
    auth_aieln_validation = models.JSONField(null=True, blank=True)
    auth_aieln_design = models.JSONField(null=True, blank=True)
    # AI Generation
    auth_aigeneration = models.JSONField(null=True, blank=True)
    auth_aigeneration_register = models.JSONField(null=True, blank=True)
    auth_aigeneration_validation = models.JSONField(null=True, blank=True)
    auth_aigeneration_design = models.JSONField(null=True, blank=True)
    # PDF2Smiles
    auth_pdf2smiles = models.JSONField(null=True, blank=True)
    auth_pdf2smiles_register = models.JSONField(null=True, blank=True)
    auth_pdf2smiles_validation = models.JSONField(null=True, blank=True)
    auth_pdf2smiles_design = models.JSONField(null=True, blank=True)
    # RxnFinder
    auth_rxnfinder = models.JSONField(null=True, blank=True)
    auth_rxnfinder_register = models.JSONField(null=True, blank=True)
    auth_rxnfinder_validation = models.JSONField(null=True, blank=True)
    auth_rxnfinder_design = models.JSONField(null=True, blank=True)

    # RnD Medichem #################################################
    # Compound overall
    auth_compound = models.JSONField(null=True, blank=True)
    auth_compound_register = models.JSONField(null=True, blank=True)
    auth_compound_validation = models.JSONField(null=True, blank=True)
    auth_compound_design = models.JSONField(null=True, blank=True)

    # Project
    auth_project = models.JSONField(null=True, blank=True)
    auth_project_register = models.JSONField(null=True, blank=True)
    auth_project_validation = models.JSONField(null=True, blank=True)
    auth_project_design = models.JSONField(null=True, blank=True)

    # Structure
    auth_structure = models.JSONField(null=True, blank=True)
    auth_structure_register = models.JSONField(null=True, blank=True)
    auth_structure_validation = models.JSONField(null=True, blank=True)
    auth_structure_design = models.JSONField(null=True, blank=True)

    # KP viewer
    auth_kpviewer = models.JSONField(null=True, blank=True)
    auth_kpviewer_register = models.JSONField(null=True, blank=True)
    auth_kpviewer_validation = models.JSONField(null=True, blank=True)
    auth_kpviewer_design = models.JSONField(null=True, blank=True)
    # Patentability
    auth_patentability = models.JSONField(null=True, blank=True)
    auth_patentability_register = models.JSONField(null=True, blank=True)
    auth_patentability_validation = models.JSONField(null=True, blank=True)
    auth_patentability_design = models.JSONField(null=True, blank=True)
    # SAR compound
    auth_sar = models.JSONField(null=True, blank=True)
    auth_sar_register = models.JSONField(null=True, blank=True)
    auth_sar_validation = models.JSONField(null=True, blank=True)
    auth_sar_design = models.JSONField(null=True, blank=True)
    # Inventory
    auth_inventory = models.JSONField(null=True, blank=True)
    auth_inventory_register = models.JSONField(null=True, blank=True)
    auth_inventory_validation = models.JSONField(null=True, blank=True)
    auth_inventory_design = models.JSONField(null=True, blank=True)
    # PDB Summary
    auth_pdbsummary = models.JSONField(null=True, blank=True)
    auth_pdbsummary_register = models.JSONField(null=True, blank=True)
    auth_pdbsummary_validation = models.JSONField(null=True, blank=True)
    auth_pdbsummary_design = models.JSONField(null=True, blank=True)

    # 현재 사용 안함 #################################################
    # control compound
    auth_controlcompound = models.JSONField(null=True, blank=True)
    auth_controlcompound_register = models.JSONField(null=True, blank=True)
    auth_controlcompound_validation = models.JSONField(null=True, blank=True)
    auth_controlcompound_design = models.JSONField(null=True, blank=True)
    # compound Synthesis
    auth_compoundsynthesis = models.JSONField(null=True, blank=True)
    auth_compoundsynthesis_register = models.JSONField(null=True, blank=True)
    auth_compoundsynthesis_validation = models.JSONField(null=True, blank=True)
    auth_compoundsynthesis_design = models.JSONField(null=True, blank=True)
    # compound Screening
    auth_compoundscreening = models.JSONField(null=True, blank=True)
    auth_compoundscreening_register = models.JSONField(null=True, blank=True)
    auth_compoundscreening_validation = models.JSONField(null=True, blank=True)
    auth_compoundscreening_design = models.JSONField(null=True, blank=True)

    # RnD Bio #################################################
    # Bio Study
    auth_biostudy = models.JSONField(null=True, blank=True)
    auth_biostudy_register = models.JSONField(null=True, blank=True)
    auth_biostudy_validation = models.JSONField(null=True, blank=True)
    auth_biostudy_design = models.JSONField(null=True, blank=True)
    # Bio ELN
    auth_bioeln = models.JSONField(null=True, blank=True)
    auth_bioeln_register = models.JSONField(null=True, blank=True)
    auth_bioeln_validation = models.JSONField(null=True, blank=True)
    auth_bioeln_design = models.JSONField(null=True, blank=True)
    # Crystal
    auth_crystal = models.JSONField(null=True, blank=True)
    auth_crystal_register = models.JSONField(null=True, blank=True)
    auth_crystal_validation = models.JSONField(null=True, blank=True)
    auth_crystal_design = models.JSONField(null=True, blank=True)
    # Dashboard
    auth_dashboard = models.JSONField(null=True, blank=True)
    auth_dashboard_register = models.JSONField(null=True, blank=True)
    auth_dashboard_validation = models.JSONField(null=True, blank=True)
    auth_dashboard_design = models.JSONField(null=True, blank=True)
    # Dashboard PK
    # ==> assay로 메뉴명만 변경
    auth_dashboardpk = models.JSONField(null=True, blank=True)
    auth_dashboardpk_register = models.JSONField(null=True, blank=True)
    auth_dashboardpk_validation = models.JSONField(null=True, blank=True)
    auth_dashboardpk_design = models.JSONField(null=True, blank=True)
    # Excel Download
    auth_exceldownload = models.JSONField(null=True, blank=True)
    auth_exceldownload_register = models.JSONField(null=True, blank=True)
    auth_exceldownload_validation = models.JSONField(null=True, blank=True)
    auth_exceldownload_design = models.JSONField(null=True, blank=True)
    # tumormanager
    auth_tumormanager = models.JSONField(null=True, blank=True)
    auth_tumormanager_register = models.JSONField(null=True, blank=True)
    auth_tumormanager_validation = models.JSONField(null=True, blank=True)
    auth_tumormanager_design = models.JSONField(null=True, blank=True)
    # IACUC
    auth_iacuc = models.JSONField(null=True, blank=True)
    auth_iacuc_register = models.JSONField(null=True, blank=True)
    auth_iacuc_validation = models.JSONField(null=True, blank=True)
    auth_iacuc_design = models.JSONField(null=True, blank=True)
    # Protocol
    auth_protocol = models.JSONField(null=True, blank=True)
    auth_protocol_register = models.JSONField(null=True, blank=True)
    auth_protocol_validation = models.JSONField(null=True, blank=True)
    auth_protocol_design = models.JSONField(null=True, blank=True)
    # Screening invitro
    auth_screeninginvitro =  models.JSONField(null=True, blank=True)
    auth_screeninginvitro_register =  models.JSONField(null=True, blank=True)
    auth_screeninginvitro_validation =  models.JSONField(null=True, blank=True)
    auth_screeninginvitro_design =  models.JSONField(null=True, blank=True)
    # Screening invivo (animal)
    auth_screeninginvivo = models.JSONField(null=True, blank=True)
    auth_screeninginvivo_register = models.JSONField(null=True, blank=True)
    auth_screeninginvivo_validation = models.JSONField(null=True, blank=True)
    auth_screeninginvivo_design = models.JSONField(null=True, blank=True)

    # 경영 ###############################################
    # BD
    auth_bd = models.JSONField(null=True, blank=True)
    auth_bd_register = models.JSONField(null=True, blank=True)
    auth_bd_validation = models.JSONField(null=True, blank=True)
    auth_bd_design = models.JSONField(null=True, blank=True)
    # BD Q&A
    auth_bdqna = models.JSONField(null=True, blank=True)
    auth_bdqna_register = models.JSONField(null=True, blank=True)
    auth_bdqna_validation = models.JSONField(null=True, blank=True)
    auth_bdqna_design = models.JSONField(null=True, blank=True)
    # Finance
    auth_finance = models.JSONField(null=True, blank=True)
    auth_finance_register = models.JSONField(null=True, blank=True)
    auth_finance_validation = models.JSONField(null=True, blank=True)
    auth_finance_design = models.JSONField(null=True, blank=True)
    # Human Resources
    auth_hr = models.JSONField(null=True, blank=True)
    auth_hr_register = models.JSONField(null=True, blank=True)
    auth_hr_validation = models.JSONField(null=True, blank=True)
    auth_hr_design = models.JSONField(null=True, blank=True)
    # IP
    auth_ip = models.JSONField(null=True, blank=True)
    auth_ip_register = models.JSONField(null=True, blank=True)
    auth_ip_validation = models.JSONField(null=True, blank=True)
    auth_ip_design = models.JSONField(null=True, blank=True)
    # Material and resources
    auth_material = models.JSONField(null=True, blank=True)
    auth_material_register = models.JSONField(null=True, blank=True)
    auth_material_validation = models.JSONField(null=True, blank=True)
    auth_material_design = models.JSONField(null=True, blank=True)
    # Purchasing
    auth_purchasing = models.JSONField(null=True, blank=True)
    auth_purchasing_register = models.JSONField(null=True, blank=True)
    auth_purchasing_validation = models.JSONField(null=True, blank=True)
    auth_purchasing_design = models.JSONField(null=True, blank=True)
    # IPS
    auth_ips = models.JSONField(null=True, blank=True)
    auth_ips_register = models.JSONField(null=True, blank=True)
    auth_ips_validation = models.JSONField(null=True, blank=True)
    auth_ips_design = models.JSONField(null=True, blank=True)
    
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)

class Authority_Field(models.Model):
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True, blank=True)






###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#
#                                                            HR 문서 관리
#
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


LIST_HR_DOCUMENT_FORMAT_TYPE = (
    # my
    ('vacation_plan', '휴가계획서'), # 0
    ('workingtime_plan', '근무계획서'),  # 1 자택근무/출장/휴일근무 신청서 모두 여기서
    ('workingtime_plan_comeback', '복직신청서'), # 2
    # 구매
    ('purchase_plan_general', '구매요청서(일반)'), # 3
    ('purchase_plan_asset', '구매요청서(자산)'), # 4
    # 지급
    ('payment_plan_cash', '현금지출결의서'), # 5
    ('payment_plan_card', '카드지출결의서'), # 6
    ('payment_plan_payback', '실비요청서'), # 7
    # 팀운영
    ('supplement_personnel_plan', '인원충원요청서'), # 8
    ('research_plan_education', '교육계획서'), # 9
    ('research_report_education', '교육결과보고서'), # 10
    ('research_plan_paper', '논문계획서'), # 11
    ('research_plan_poster', '포스터 발표 계획서'), # 12
)


#--------------------------------------------------------------------------------------------------------------------------
# 문서 포맷 관리
#
# 기본 획득정보
    # 'id': 순번,
    # 'name': 참자조 이름,
    # 'position': 참조자 직책,
    # 'email': 참조자 email,
    # 'hrlayout_id': 참조자 hrlayout_id,
    # 'profile_id': 참조자 profile_id,
#
#--------------------------------------------------------------------------------------------------------------------------
class HR_Document_Format(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    type_format = models.CharField(max_length=100, choices=LIST_HR_DOCUMENT_FORMAT_TYPE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file_format = models.FileField(upload_to='hr/document/file_format/', null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # 문서 참조자
    list_dict_document_referrer = models.JSONField(null=True, blank=True) # 문서내용 참조자
    #--------------------------------------------------------------------------------------------------------------------------
    # 문서 수신처
    list_dict_document_receiver = models.JSONField(null=True, blank=True) # 문서내용 수신처

    #--------------------------------------------------------------------------------------------------------------------------
    # 추후 추가될 자동양식 레이아웃 저장용
    #--------------------------------------------------------------------------------------------------------------------------
    # 텍스트 입력창 소제목 리스트
    list_title_input_text_column = models.JSONField(null=True, blank=True) # 문서에 추가될 Text 입력항목의 제목
    #--------------------------------------------------------------------------------------------------------------------------
    # 날짜 정보 입력창 소제목 리스트
    list_title_input_date_column = models.JSONField(null=True, blank=True) # 문서에 추가될 Text 입력항목의 제목

    #--------------------------------------------------------------------------------------------------------------------------
    # System
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    check_activate = models.BooleanField(default=False)
    check_discard = models.BooleanField(default=False)

    def __str__(self):
        if self.title is not None:
            return self.title
        else:
            return self.id



#--------------------------------------------------------------------------------------------------------------------------
# 문서 첨부파일 관리
#--------------------------------------------------------------------------------------------------------------------------
def get_upload_document_request_management(instance, dummy):
    return instance.file_path + "/" + instance.file_name

class HR_Document_Attached_File_Management(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    file_path = models.CharField(max_length=250, null=True, blank=True)
    file_name = models.CharField(max_length=250, null=True, blank=True)
    file = models.FileField(upload_to=get_upload_document_request_management, null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # System
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    check_temp = models.BooleanField(default=False) # 임시저장
    check_discard = models.BooleanField(default=False)





#--------------------------------------------------------------------------------------------------------------------------
# # 추후 hrapproval_process 완성시 삭제
# STATUS_MY_VACATION_PLAN = (
#     ('WRITING', '작성중'), # 0 light
#     ('UNDER_APPROVAL', '승인요청중'), # 1 info
#     ('REQ_MODIFICATION', '수정요청'),  # 2 warning
#     ('DONE_MODIFICATION', '수정완료'),  # 3 primary
#     ('APPROVED', '승인완료'),  # 4 success
#     ('REJECTED', '승인거절'),  # 5 danger
#     ('CANCEL', '등록취소'),  # 6 secondary
# )


#--------------------------------------------------------------------------------------------------------------------------
# 문서 승인 관리
#
# * 문서승인프로세스가 필요한 모든 앱에서 key를 삽입하면 사용가능하도록 개발
# * 개인별 쿼리(mysettings 처럼)
# * 승인과정에서 일어나는 모든내용 사용자정보/시간 기록

# 기본 정보
# 'id': 순번,
# 'name': 해당자 이름,
# 'position': 해당자 직책,
# 'email': 해당자 email,
# 'hrlayout_id': 해당자 hrlayout_id,
# 'profile_id': 해당자 profile_id,

# 승인권자 추가정보
# 'validation': '평가(승인/거절)여부 (예: STATUS_HR_DOCUMENT_APPROVER_VALIDATION[0][0])',
# 'datetime': '평가(승인/거절)시간 (예: 2023-01-10 16:22)',
# 'comment': '코멘트',
#--------------------------------------------------------------------------------------------------------------------------

# 승인 진행단계
STATUS_HR_DOCUMENT_APPROVAL_PROCESS = (
    ('WRITING', '작성중'), # 0 light
    ('UNDER_APPROVAL', '승인요청중'), # 1 info
    ('REQ_MODIFICATION', '수정요청'),  # 2 warning
    ('DONE_MODIFICATION', '수정완료'),  # 3 primary
    ('APPROVED', '승인완료'),  # 4 success
    ('REJECTED', '승인거절'),  # 5 danger
    ('CANCEL', '등록취소'),  # 6 secondary , 작성자가 승인절차 중 등록을 스스로 취소함 (승인절차 개시 이후)
)

# 각 승인권자가 결정한 내용
STATUS_HR_DOCUMENT_APPROVER_VALIDATION = (
    ('APPROVAL', '승인'),  # 0 success
    ('REQ_MODIFICATION', '수정요청'),  # 1 warning
    ('REJECTION', '거절'),  # 2 danger
)


class HR_Document_Approval_Management(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # title = models.CharField(max_length=250, null=True, blank=True)
    document_format = models.ForeignKey(HR_Document_Format, null=True, blank=True, on_delete=models.SET_NULL)
    #--------------------------------------------------------------------------------------------------------------------------
    # 진행상태
    status_document_approval_process = models.CharField(max_length=100, choices=STATUS_HR_DOCUMENT_APPROVAL_PROCESS, default=STATUS_HR_DOCUMENT_APPROVAL_PROCESS[0][0], blank=True)
    check_process_activated = models.BooleanField(default=False) # True: 승인과정 개시
    check_process_completed = models.BooleanField(default=False) # True: 승인완료/승인거절/등록취소 해당하여 승인과정이 종료되는 경우 경우
    reason_drop = models.CharField(max_length=250, null=True, blank=True) # 작성자에 의해 승인과정 개시 후 승인요청을 취소하는 경우 이유 명시
    #--------------------------------------------------------------------------------------------------------------------------
    # 문서 상신자
    hrlayout_applicant = models.ForeignKey(HR_Layout, related_name="DAM_상신자", null=True, blank=True, on_delete=models.SET_NULL) # 문서 상신자(신청자) 조직도 정보
    # # 문서 상신자의 직속상사
    # hrlayout_approver_teamleader = models.ForeignKey(HR_Layout, related_name="document_approver_teamleader", null=True, blank=True, on_delete=models.SET_NULL) # 승인권자 팀장 조직도 정보
    # hrlayout_approver_divisionleader = models.ForeignKey(HR_Layout, related_name="document_approver_divisionleader", null=True, blank=True, on_delete=models.SET_NULL) # 승인권자 부서장 조직도 정보
    # hrlayout_approver_companyleader = models.ForeignKey(HR_Layout, related_name="document_approver_companyleader", null=True, blank=True, on_delete=models.SET_NULL) # 승인권자 회사장 조직도 정보
    #--------------------------------------------------------------------------------------------------------------------------
    # 문서 승인권자
    list_dict_document_approver = models.JSONField(null=True, blank=True)
    list_profile_id_approver = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # 문서 인수자
    list_dict_document_takeover = models.JSONField(null=True, blank=True)
    list_profile_id_takeover = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # 문서 참조자
    list_dict_document_referrer = models.JSONField(null=True, blank=True) # 문서내용 알람 대상자
    list_profile_id_referrer = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # 문서 수신처
    list_dict_document_receiver = models.JSONField(null=True, blank=True) # 문서내용 수신처
    list_profile_id_receiver = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # 진행시간
    datetime_process_start = models.DateTimeField(null=True, blank=True) # 문서 승인 과정 시작시점 저장
    datetime_process_end = models.DateTimeField(null=True, blank=True) # 문서 승인 과정 종료시점 저장
    #--------------------------------------------------------------------------------------------------------------------------
    # System
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    check_discard = models.BooleanField(default=False)
    #--------------------------------------------------------------------------------------------------------------------------
    # 아래는 체크 후 삭제
    check_process_validated_first = models.BooleanField(default=False) # True : 최초 승인 하였음 == 승인과정 세부내용 표시 ((2번째 부터는 승인과정을 표시해야 함)


#--------------------------------------------------------------------------------------------------------------------------
# 문서 수정요청 관리
#
# list_dict_request_talk_for_document_management 내용
# 기본 정보
# 'id': 순번,
# 'name': 해당자 이름,
# 'position': 해당자 직책,
# 'talk': 등록한 대화내용,
# 'file_name': 임시 등록한 파일 이름,
# 'file_path': 임시 등록한 파일 경로,
# 'hr_docfile_id': 임시 등록한 파일 쿼리 ID,
#--------------------------------------------------------------------------------------------------------------------------

STATUS_MY_XXX_DOCUMENT_PLAN_REQUEST_TO = (
    ('NORMAL', '정상상태'), # 0
    ('REQUESTED_TO_HR', '문서담당팀에 정정 요청'), # 1
    ('REQUESTED_TO_ME', '작성자에게 정정 요청'), # 2
    ('MODIFIED_BY_HR', '문서담당팀이 정정 완료'), # 3
    ('MODIFIED_BY_ME', '작성자가 정정 완료'), # 4
    ('RESPONSED_TO_ME', '정정내용 작성자에게 발송'),  # 5
    ('RESPONSED_TO_HR', '정정내용 문서담당팀에 발송'),  # 6
    ('ACCEPTED_BY_ME', '정정내용 작성자 동의 및 완료'),  # 7
    ('ACCEPTED_BY_HR', '정정내용 문서담당팀 동의 및 완료'),  # 8
)

LIST_HR_DOCUMENT_MY_INVOLVED_ROLE = (
    ('approver', '승인권자'),
    ('takeover', '업무인수자'),
    ('referrer', '참조자'),
    ('receiver', '수신처'),
)

class HR_Document_Request_Management(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status_document_request_to = models.CharField(max_length=100, choices=STATUS_MY_XXX_DOCUMENT_PLAN_REQUEST_TO, default=STATUS_MY_XXX_DOCUMENT_PLAN_REQUEST_TO[0][0], blank=True)
    check_hr_document_request_to_xxx_activated = models.BooleanField(default=False) # True: 내가 문서담당팀에 문서 정정/취소 관련 요청함
    list_dict_request_talk_for_document_management = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # System
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    check_discard = models.BooleanField(default=False)





# 추후 삭제
STATUS_MY_VACATION_PLAN_REQUEST_FROM_HR = (
    ('NORMAL', '정상상태'),  # 0
    ('REQUESTED', '인사팀이 정정 요청'), # 1
    ('MODIFIED', '사용자가 정정 내용 기입 완료, 내용확인'), # 2
    ('RESPONSED', '정정 내용 인사팀에게 발송'),  # 3
    ('ACCEPTED', '정정 내용 인사팀 동의 및 완료'),  # 4
)



###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                           HR Calendar 관리
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


class HR_Calendar_Control(models.Model):
    year_calendar = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    check_discard = models.BooleanField(default=False)



NATIONAL_EVENT_TYPES = (
    ('NATIONAL_HOLIDAY', '국경일'),
    ('NATIONAL_ANNIVERSARY_DAY', '기념일'),
    ('SEASONAL_DIVISIONS', '24절기'),
    ('OTHER_DIVISIONS', '잡절'),
)

VORONOI_EVENT_TYPES = (
    ('NOTIFICATION', '공지'),
    ('LECTURE', '강의'),
    ('MEETING', '미팅'),
    ('ANNIVERSARY', '기념'),
    ('VISITING', '손님방문'),
    ('ETC', '기타'),
)


class HR_Calendar_Event(models.Model):
    calendar_control = models.ForeignKey(HR_Calendar_Control, null=True, blank=True, on_delete=models.CASCADE)
    # Event
    date_event = models.DateField(verbose_name="Event 날짜", null=True, blank=True)
    name_event = models.CharField(verbose_name="Event 이름", max_length=200, null=True, blank=True)
    type_event_national = models.CharField(verbose_name="National Event 종류", choices=NATIONAL_EVENT_TYPES, max_length=200, null=True, blank=True)
    type_event_voronoi = models.CharField(verbose_name="Voronoi Event 종류", choices=VORONOI_EVENT_TYPES, max_length=200, null=True, blank=True)
    # Check list
    check_voronoi_event = models.BooleanField(default=False)  # True : 보로노이 Event인 경우
    check_holiday = models.BooleanField(default=False)  # True: 휴일인 경우 (법정공휴일 또는 보로노이 지정 휴일)
    # 추가정보
    comment = models.CharField(verbose_name="Event 내용", max_length=200, null=True, blank=True)
    list_applied_company = models.JSONField(null=True, blank=True) # all: 보로노이 그룹 전체, voronoi: 보로노이, voronoibio : 보로노이바이오, b2sbio: 비투에스바이오
    check_discard = models.BooleanField(default=False)

    def __str__(self):
        if self.name_event is not None:
            return self.name_event
        else:
            return self.date_event



class HR_Calendar_Vacation(models.Model):
    # Event
    date_vacation = models.DateField(null=True, blank=True)
    list_attendee = models.JSONField(null=True, blank=True) # 해당 날짜 휴가자 [vacation_plan_id]
    # 추가정보
    check_discard = models.BooleanField(default=False)


class HR_Calendar_Document(models.Model):
    date_document = models.DateField(null=True, blank=True)
    list_document_id = models.JSONField(null=True, blank=True) # 해당 날짜 휴가자 [hr_document_issued_id]
    document_format = models.ForeignKey(HR_Document_Format, null=True, blank=True, on_delete=models.SET_NULL)
    # 추가정보
    check_discard = models.BooleanField(default=False)







###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                        HR Vacation 관리
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################




LIST_VACATION_TYPES = (
    ('VC_REGULAR', '연차'),  # success
    ('VC_OFFICIAL', '공가'),  # 1  primary
    ('VC_SICK', '병가'),  # 2 # warning
    ('VC_BIRTH', '출산휴가'),  # 3 # secondary
    ('VC_EVENT', '경조휴가'),  # 4 # dark
    ('VC_MILITARY', '병무휴가'),  # 5 # info
    ('VC_SPECIAL', '보건휴가'),  # 6 # danger
    ('VC_ETC', '기타휴가'),  # 7 # secondary
    ('VC_NOPAY', '무급휴가'),  # 8 # light
)

LIST_VACATION_REGULAR_TYPES = (
    ('VC_WHOLEDAY', '하루'), # dark
    ('VC_HALFDAY', '반차'), # secondary
    ('VC_QUARTERDAY', '반반차'), # normal
)

LIST_VACATION_TIME_HOUR = (
    ('9', '9'),  # 0
    ('10', '10'),  # 1
    ('11', '11'),  # 2
    ('12', '12'),  # 3
    ('13', '13'),  # 4
    ('14', '14'),  # 5
    ('15', '15'),  # 6
    ('16', '16'),  # 7
    ('17', '17'),  # 8
    ('18', '18'),  # 9
)

LIST_VACATION_TIME_MINUTE = (
    ('0', '00'),  # 0
    ('10', '10'),  # 1
    ('15', '15'),  # 2
    ('20', '20'),  # 3
    ('30', '30'),  # 4
    ('40', '40'),  # 5
    ('45', '45'),  # 6
    ('50', '50'),  # 7
)


LIST_VACATION_TIME_HALF = (
    ('morning', '오전'),
    ('afternoon', '오후'),
)

LIST_VACATION_TIME_QUATER = (
    ('q1', '9시 ~ 11시'),
    ('q2', '10시 ~ 12시'),
    ('q3', '11시 ~ 14시'),
    ('q4', '12시 ~ 15시'),
    ('q5', '12시 30분 ~ 15시 30분'),
    ('q6', '14시 ~ 16시'),
    ('q7', '15시 ~ 17시'),
    ('q8', '16시 ~ 18시'),
)

#--------------------------------------------------------------------------------------------------------------------------
# HR 부서의 양식 관리
#--------------------------------------------------------------------------------------------------------------------------

class HR_Vacation_Document_Format_Management(models.Model):
    file_vc_plan_autoupload = models.FileField(upload_to='hr/vacation/document/format/planautoupload', null=True, blank=True)
    dict_error_type_and_name_upload_vc_plan_file = models.JSONField(null=True, blank=True)
    file_member_profile_autoupload = models.FileField(upload_to='hr/vacation/document/format/memberprofile', null=True, blank=True)
    check_discard = models.BooleanField(default=False)



#--------------------------------------------------------------------------------------------------------------------------
# HR 부서의 연차촉진 관리
# 1년차(신입)은 2차(60일), 3차(30일) 발송
# 2년차 이상은 1차(180일), 2차(60일) 발송
#--------------------------------------------------------------------------------------------------------------------------
class HR_Vacation_Promotion_Settings(models.Model):
    delta_days_warning_y1_l1 = models.IntegerField(default=60) # 신입 1차 연차촉진을 위한 1차 알람발송을 연차 만료일 몇일 전으로 할지 결정
    delta_days_warning_y1_l2 = models.IntegerField(default=30) # 신입 2차 연차촉진을 위한 2차 알람발송을 연차 만료일 몇일 전으로 할지 결정
    delta_days_warning_y2_l1 = models.IntegerField(default=180) # 다년차 연차촉진을 위한 1차 알람발송을 연차 만료일 몇일 전으로 할지 결정
    delta_days_warning_y2_l2 = models.IntegerField(default=60) # 다년차 연차촉진을 위한 2차 알람발송을 연차 만료일 몇일 전으로 할지 결정
    file_vc_promotion_report = models.FileField(upload_to='hr/vacation/promotion/file/format/', null=True, blank=True)
    text_promotion_additional_information = models.CharField(max_length=250, null=True, blank=True) # 추가적인 연차촉진을 위한 알람발송 인사팀 멘트
    check_activate_additional_information = models.BooleanField(default=False) # True : 추가 정보 표시
    check_activate_additional_information_only_manual = models.BooleanField(default=False) # True : 추가 정보 표시를 추가로 수동으로 발송한 알람에만 표시
    check_discard = models.BooleanField(default=False)
    date_refreshed = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)




#--------------------------------------------------------------------------------------------------------------------------
# 멤버별 년차별 Vacation 관리 쿼리
#--------------------------------------------------------------------------------------------------------------------------

STATUS_MY_VACATION_CONTROL = (
    ('NORMAL', '정상 상태'), # 0
    ('USED', '해당년차 만료 전 모든 휴가 사용완료'), # 1
    ('EXPIRED', '해당년차 기한 만료'),  # 2
    ('WARNING_Y1_L1_INFORMED', '신입 1차알람 발송'),  # 3
    ('WARNING_Y1_L1_RESPONSED', '신입 1차알람 사용자 확인'),  # 4
    ('WARNING_Y1_L2_INFORMED', '신입 2차알람 발송'),  # 5
    ('WARNING_Y1_L2_RESPONSED', '신입 2차알람 사용자 확인'),  # 6
    ('WARNING_Y2_L1_INFORMED', '다년차 1차알람 발송'),  # 7
    ('WARNING_Y2_L1_RESPONSED', '다년차 1차알람 사용자 확인'),  # 8
    ('WARNING_Y2_L2_INFORMED', '다년차 2차알람 발송'),  # 9
    ('WARNING_Y2_L2_RESPONSED', '다년차 2차알람 사용자 확인'),  # 10
    ('WARNING_Y1_L1_NOT_RESPONSED', '신입 1차 미확인 및 2차고지 대상'),  # 11
    ('WARNING_Y2_L1_NOT_RESPONSED', '다년차 1차 미확인 및 2차고지 대상'),  # 12
)


def get_upload_vacation_promotion_plan(instance, dummy):
    print('path', instance.path)
    print('instance', instance.filename)
    return instance.path + "/" + instance.filename

class Vacation_Control(models.Model):
    # 매 근무년차별 사용자별 발행
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    status_working_year = models.IntegerField(null=True, blank=True) # 근무 년차
    status_working_month_first_year = models.IntegerField(null=True, blank=True) # 근무 월차 (근무 첫해의, 예: 1월차 == 1 ~ 30일 근무)
    date_workingyear_start = models.DateField(null=True, blank=True) # 휴가컨트롤 발행된 근무년차의 근무시작일
    date_workingyear_end = models.DateField(null=True, blank=True) # 휴가컨트롤 발행된 근무년차의 근무종료일
    #--------------------------------------------------------------------------------------------------------------------------
    # 휴가 선발행 컨트롤
    # 현재 근무년차 혹은 과거 근무년차일 경우 상관없음. 미래의 근무년차일 경우에 해당
    #--------------------------------------------------------------------------------------------------------------------------
    limit_number_issue_vc_future = models.IntegerField(default=0) # 미래의 휴가를 미리 사용 가능하도록 허용하는 개수, 0 == 허용안함

    #--------------------------------------------------------------------------------------------------------------------------
    # 휴가 컨트롤 연차촉진 상태
    #--------------------------------------------------------------------------------------------------------------------------
    status_vacation_control = models.CharField(max_length=100, choices=STATUS_MY_VACATION_CONTROL, default=STATUS_MY_VACATION_CONTROL[0][0], blank=True)
    date_confirm_promotion_l1 = models.DateField(null=True, blank=True) # 연차촉진알람 1차 사용자 확인날짜
    date_confirm_promotion_l2 = models.DateField(null=True, blank=True) # 연차촉진알람 2차 사용자 확인날짜
    percent_consumption = models.FloatField(default=0) # 연차소진율 값 저장 (Sorting용)
    percent_deadline = models.FloatField(default=0) # 연차마감까지 도달율 값 저장 (Sorting용)
    days_remained = models.IntegerField(default=0) # 연차마감일까지 남은 날수
    check_promotion_inform_manually = models.BooleanField(default=False)   # True: 수동으로 강제 1번 연차촉진 알람 띄움
    list_date_confirm_promotion_irregular = models.JSONField(null=True, blank=True) # 비정기 수동 연차촉진 알림 확인 날짜 리스트
    #--------------------------------------------------------------------------------------------------------------------------
    # 휴가 사용시기 지정통보서 파일 업로드
    #--------------------------------------------------------------------------------------------------------------------------
    check_need_to_upload_promotion_plan = models.BooleanField(default=False)   # True: 연차 유급휴가 지정통보서 등록이 필요한 경우
    check_uploaded_promotion_plan = models.BooleanField(default=False)   # True: 연차 유급휴가 지정통보서 등록한 경우
    path = models.CharField(max_length=250, null=True, blank=True)
    filename = models.CharField(max_length=250, null=True, blank=True)
    promotion_plan_file = models.FileField(upload_to=get_upload_vacation_promotion_plan, null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # Vacation Status
    #--------------------------------------------------------------------------------------------------------------------------
    vc_count_revived_prev_unused_expired_total = models.FloatField(verbose_name="직전년차 미사용 기한만료 소생시킨 휴가 개수", null=True, blank=True) # 이번년차에서 사용을 위해
    vc_count_issued_total = models.FloatField(verbose_name="연차받은개수", null=True, blank=True)
    vc_count_underapproval_total = models.FloatField(verbose_name="연차신청중인개수", null=True, blank=True)
    vc_count_used_total = models.FloatField(verbose_name="연차사용한개수", null=True, blank=True)
    vc_count_unused_expired_total = models.FloatField(verbose_name="이번년차 미사용 기한만료개수", null=True, blank=True)
    vc_count_revived_unused_expired_total = models.FloatField(verbose_name="이번년차 미사용 기한만료 소생시킨 휴가 개수", null=True, blank=True) # 다음년차에서 사용을 위해
    vc_count_available_total = models.FloatField(verbose_name="연차사용가능개수", null=True, blank=True)
    list_vc_issued_additionally = models.JSONField(verbose_name="추가로받은 휴가 리스트", null=True, blank=True) # 연차 이외에 받은 휴가(Vacation_Issued) 쿼리 id 리스트
    #--------------------------------------------------------------------------------------------------------------------------
    # Trouble 핸들링
    #--------------------------------------------------------------------------------------------------------------------------
    # 사용자 발행휴가 수정요청
    check_hr_vc_issued_request_to_hr_activated = models.BooleanField(default=False) # True: 발행휴가 Trouble 해결요청
    check_hr_vc_issued_request_to_hr_responsed = models.BooleanField(default=False) # True: 발행휴가 Trouble 해결요청에 대한 응답 완료
    # 인사팀 휴가계획서 수정요청
    check_hr_vc_plan_request_from_hr_activated = models.BooleanField(default=False) # True: 인사팀 휴가계획서 관련 요청 발동
    # System
    check_last = models.BooleanField(default=False) # True: 마자믹에 생성된 근무년차
    check_selected = models.BooleanField(default=False) # True: 현재 선택된 근무년차
    check_discard = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)



    #---------------
    year_vacation = models.IntegerField(verbose_name="연차발행년도", null=True, blank=True) # 추후 삭제

    # @property
    # def __str__(self):
    #     if self.owner.profile is not None:
    #         name_str = self.owner.profile.name_korean
    #         if name_str is not None:
    #             if self.status_working_year is not None:
    #                 return name_str + "(" + str(self.status_working_year) + "년차)"
    #             else:
    #                 return name_str
    #         else:
    #             return self.owner.email
    #     else:
    #         return self.owner.email


#--------------------------------------------------------------------------------------------------------------------------
# 멤버별 발행된 Vacation 쿼리
#--------------------------------------------------------------------------------------------------------------------------

VACATION_ISSUED_REVIVAL_EXTENDED_DAYS = (
    ('1', '+ 1개월'),
    ('3', '+ 3개월'),
    ('6', '+ 6개월'),
    ('12', '+ 12개월'),
    ('TYPE', '직접입력'),
)


STATUS_MY_VACATION_ISSUED_REQUEST_TO_HR = (
    ('NORMAL', '정상상태'),  # 0
    ('REQUESTED', '인사팀에 정정 요청'), # 1
    ('MODIFIED', '인사팀이 정정 내용 기입 완료, 내용확인'), # 2
    ('RESPONSED', '정정 내용 사용자에게 발송'),  # 3
    ('ACCEPTED', '정정 내용 사용자 동의 및 완료'),  # 4
)

STATUS_VACATION_ISSUED = (
    ('VALID', '사용가능'),
    ('REVIVED', '이월됨'),
    ('UNDERAPPROVAL', '승인요청중'),
    ('USED', '모두사용됨'),
    ('REFUNDED', '돈으로지불됨'),
    ('EXPIRED', '기간만료됨'),
    ('INVALID', '사용중지'),
)


class Vacation_Issued(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    vacation_control = models.ForeignKey(Vacation_Control, null=True, on_delete=models.CASCADE)
    vacation_type = models.CharField(verbose_name="휴가종류", choices=LIST_VACATION_TYPES, default=LIST_VACATION_TYPES[0][0], max_length=200, null=True, blank=True) # 휴가 타입에 맞게 휴가 계획을 사용해야 함. 다른 휴가 타입으로 휴가계획을 작성 못함.
    status = models.CharField(verbose_name="발행휴가상태", choices=STATUS_VACATION_ISSUED, default=STATUS_VACATION_ISSUED[0][0], max_length=200, null=True, blank=True) # 발행휴가 상태
    # Credit
    # Credit + Credit_used + Credit_refunded == 1
    credit = models.FloatField(default=1) # 하루 = 1 차감, 반차 = 0.5 차감, 반반차 = 0.25 차감 , 포인트가 0이 되면 expired 된다. 더 이상 사용 불가, 크레딧 차감은 휴가계획서 승인 확정될 때 수행
    credit_scheduled_to_use = models.FloatField(default=0) # 휴가계획서 승인 전까지 사용계획된 크레딧 작성. 휴가계획서 승인시 Credit을 차감사키고 0으로 바꾼다.
    credit_used = models.FloatField(default=0) # 사용된 Credit
    credit_refunded = models.FloatField(default=0) # 남은 휴가 Credit을 돈으로 환산지급하고 소진시킨 Credit 값
    # 발행된 휴가 날짜
    date_issued = models.DateField(verbose_name="휴가발행날짜", null=True, blank=True) # 1년차는 근무 한 달 채우면 1개 발행(11개). 2년차부터는 본인 입사일 기준으로 연차(15개~) 발행
    date_expired = models.DateField(verbose_name="휴가만료날짜", null=True, blank=True) # 1년차 발행 연차는 만 1년 채우는 날까지 유효, 2년차 부터는 만 1년간 사용가능
    date_extended = models.DateField(verbose_name="미사용연차의 연장된 만료날짜", null=True, blank=True) # 미사용 만료되어 기준 인사팀에서 연장해준 연장된 만료일
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # 연결된 휴가 계획서
    list_linked_vacation_plan = models.JSONField(null=True, blank=True) # 발행된 휴가와 연결된 휴가계획서 ID 리스트
    # check list
    check_modified_manually = models.BooleanField(default=False) # True: 수동 수정
    check_issued_regularly = models.BooleanField(default=False) # True: 정기발행 연차인 경우(일반적인 모든 연차가 해당됨)
    check_discard = models.BooleanField(default=False) # True: 휴가 파기되었음


    # Trouble 핸들링 -> document request 만들면 아래 삭제
    status_vacation_issued_requested_to_hr = models.CharField(max_length=100, choices=STATUS_MY_VACATION_ISSUED_REQUEST_TO_HR, default=STATUS_MY_VACATION_ISSUED_REQUEST_TO_HR[0][0], blank=True)
    check_hr_vc_issued_request_to_hr_activated = models.BooleanField(default=False) # True: 인사팀에게 발행휴가 정정/취소 관련 요청함
    dict_request_for_my_issued_vc_trouble = models.JSONField(null=True, blank=True) # 발행된 휴가 관련 인사팀 요청하기 대화내용 저장

    # status 적용 이후 아래 두 항목 삭제
    check_report_trouble_submitted = models.BooleanField(default=False) # True: 발행휴가 Trouble 해결요청 중
    check_hr_vc_issued_request_to_hr_responsed = models.BooleanField(default=False) # True: 발행휴가 Trouble 해결요청에 대한 응답 완료
    # check_underapproval = models.BooleanField(default=False) # True: 휴가 사용 요청중
    # check_expired = models.BooleanField(default=False) # True: 휴가 사용기간 만료되었음
    # check_revived = models.BooleanField(default=False) # True: 직전년차에서 휴가 사용기간 만료되었으나 사용가능하도록 이번년차에 되살림
    # check_valid = models.BooleanField(default=True) # False: 휴가 사용 불가 ,

    def __str__(self):
        return f'{self.id}-{self.owner.profile.name_korean}'



def get_upload_vacation_reference(instance, dummy):
    print('path', instance.path)
    print('instance', instance.filename)
    return instance.path + "/" + instance.filename

def get_upload_vacation_reference_cancel(instance, dummy):
    print('path', instance.path_cancel)
    print('instance', instance.filename_cancel)
    return instance.path_cancel + "/" + instance.filename_cancel


# 휴가계획서
class Vacation_Plan(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    vacation_control = models.ForeignKey(Vacation_Control, null=True, on_delete=models.CASCADE)
    hrapproval = models.ForeignKey(HR_Document_Approval_Management, null=True, on_delete=models.CASCADE)
    #--------------------------------------------------------------------------------------------------------------------------
    # 휴가계획서 관련
    #--------------------------------------------------------------------------------------------------------------------------
    # Type
    vacation_type = models.CharField(verbose_name="휴가종류", choices=LIST_VACATION_TYPES, max_length=200, null=True, blank=True)
    vacation_regular_type_start = models.CharField(verbose_name="개시일 연차사용타입", choices=LIST_VACATION_REGULAR_TYPES, max_length=200, null=True, blank=True)
    vacation_regular_type_end = models.CharField(verbose_name="종료일 연차사용타입", choices=LIST_VACATION_REGULAR_TYPES, max_length=200, null=True, blank=True)
    # 휴가계획서 연계된 발행된 휴가 정보
    list_date_vacation = models.JSONField(null=True, blank=True) # 휴가계획서에 사용되는 날짜 리스트
    list_used_vacation_issued_id = models.JSONField(null=True, blank=True) # 휴가계획에 사용된 발행된 휴가 ID 리스트
    dict_used_vacation_issued_id_credit = models.JSONField(null=True, blank=True) # 휴가계획에 사용된 발행된 휴가 ID 및 사용된 credit Dictionary
    credit_used_total = models.FloatField(null=True, blank=True)  # 휴가에 사용한 총 크레딧, 예) 연차 하루: 1, 반차: 0.5, 반반차: 0.25, 연차 3일: 3
    # 휴가계획서 작성시점 기준 휴가 상황 저장
    vc_count_issued_and_revied = models.FloatField(verbose_name="직전년차 미사용 기한만료 소생시킨 휴가 개수 + 연차받은개수", null=True, blank=True)  # 이번년차 총 사용가능 개수 (사용한다고 변하지 않음)
    vc_count_used = models.FloatField(verbose_name="기 사용한 연차 개수", null=True, blank=True) # 사용한 연차
    vc_count_plan = models.FloatField(verbose_name="이번 휴가계획에 사용한 개수", null=True, blank=True) # 이번에 사용하는 연차
    vc_count_remained = models.FloatField(verbose_name="사용가능한 남은 연차 개수", null=True, blank=True) # 앞으로 사용 가능한 연차  = vc_count_issued_and_revied - (vc_count_used + vc_count_plan)
    #--------------------------------------------------------------------------------------------------------------------------
    # 공통필드
    #--------------------------------------------------------------------------------------------------------------------------
    # Date Time
    datetime_start = models.DateTimeField(null=True, blank=True)
    datetime_end = models.DateTimeField(null=True, blank=True)
    # Destination and Reason
    reason = models.TextField(verbose_name="휴가사유", null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # Comment
    dict_comment = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # system
    #--------------------------------------------------------------------------------------------------------------------------
    check_valid = models.BooleanField(verbose_name="휴가계획서 유효성 여부", default=True) # False : 휴가 종료일이 지날경우, 승인 후 작성자가 취소할 경우
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    check_discard = models.BooleanField(default=False) # 승인 전 작성자가 취소한 경우



    # 아래내용 hr doc file 완성뒤 삭제
    # Reference File
    path = models.CharField(max_length=250, null=True, blank=True)
    filename = models.CharField(max_length=250, null=True, blank=True)
    reference_file = models.FileField(upload_to=get_upload_vacation_reference, null=True, blank=True)

    #--------------------------------------------------------------------------------------------------------------------------
    # >>>  인사팀과 수정요청관련  <<< 추후 인사팀 수정요청관리 테이블로 빼고나면 아래내용 삭제
    #--------------------------------------------------------------------------------------------------------------------------
    # 인사팀으로 부터 휴가 계획 자료 요청
    status_vacation_plan_requested_from_hr = models.CharField(max_length=100, choices=STATUS_MY_VACATION_PLAN_REQUEST_FROM_HR, default=STATUS_MY_VACATION_PLAN_REQUEST_FROM_HR[0][0], blank=True)
    check_hr_vc_plan_request_from_hr_activated = models.BooleanField(default=False) # True: 인사팀으로부터 휴가계획서 자료 요청이 들어옴
    check_hr_vc_plan_request_from_hr_response_to_hr_activated = models.BooleanField(default=False) # True: 인사팀의 휴가계획서 자료 요청에 응답함
    # 인사팀에게 개시된 휴가 계획서 정정/취소 요청
    status_xxx_document_plan_requested_to = models.CharField(max_length=100, choices=STATUS_MY_XXX_DOCUMENT_PLAN_REQUEST_TO, default=STATUS_MY_XXX_DOCUMENT_PLAN_REQUEST_TO[0][0], blank=True)
    check_hr_xxx_document_plan_request_to_hr_activated = models.BooleanField(default=False) # True: 인사팀에게 휴가계획서 정정/취소 관련 요청함
    check_vacation_plan_edit_mode = models.BooleanField(default=False)  # True: 휴가계획서 취소 , False: 휴가계획서 정정
    dict_modified_issued_vc_id_and_restored_credit = models.JSONField(null=True, blank=True)  # 요청에 의한 {수정후 발행휴가 ID: 복구후의 Credit ... }
    # Talk
    dict_request_talk_for_reference = models.JSONField(null=True, blank=True) # 자료 요청 내용에 관한 대화내용 저장
    dict_communication_with_hr_for_my_xxx_document_plan = models.JSONField(null=True, blank=True) # 취소 요청 내용에 관한 대화내용 저장
    # 수정용 Cache
    edit_vacation_type = models.CharField(verbose_name="수정될휴가종류", choices=LIST_VACATION_TYPES, max_length=200, null=True, blank=True)
    edit_vacation_regular_type = models.CharField(verbose_name="수정될연차사용타입", choices=LIST_VACATION_REGULAR_TYPES, max_length=200, null=True, blank=True)
    credit_planned_to_use = models.FloatField(default=0) # 사용 예정인 Credit 수
    credit_planned_to_restore = models.FloatField(default=0) # 복구 예정인 Credit 수
    edit_datetime_vacation_start = models.DateTimeField(null=True, blank=True)
    edit_datetime_vacation_end = models.DateTimeField(null=True, blank=True)
    # 수정 파일첨부
    path_cancel = models.CharField(max_length=250, null=True, blank=True)
    filename_cancel = models.CharField(max_length=250, null=True, blank=True)
    reference_file_cancel = models.FileField(upload_to=get_upload_vacation_reference_cancel, null=True, blank=True)








###################################################################################################################################################
# Calendar Vacation
####
class Member_Vacation_Calendar(models.Model):
    # Project Intro
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Host
    vacation_plan = models.ForeignKey(Vacation_Plan, null=True, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField(null=True, blank=True)
    datetime_end = models.DateTimeField(null=True, blank=True)
    check_discard = models.BooleanField(default=False)
    status = models.CharField(verbose_name="발행휴가상태", choices=STATUS_VACATION_ISSUED, default=STATUS_VACATION_ISSUED[0][0], max_length=200, null=True, blank=True) # 발행휴가 상태




###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                        HR Working Time 관리
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


class Workingtime_Control(models.Model):
    # 월간 근무시간 컨트롤
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    hrlayout = models.ForeignKey(HR_Layout, null=True, on_delete=models.CASCADE)
    fiscal_year = models.IntegerField(null=True, blank=True) # 회계년도
    fiscal_month = models.IntegerField(null=True, blank=True) # 회계
    #--------------------------------------------------------------------------------------------------------------------------
    # 출퇴근시간 기간별분석정보
    #--------------------------------------------------------------------------------------------------------------------------
    # 근무 횟수 관리


    # 휴일+평일
    num_workingdays_all_checkin_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일+평일 근무 횟수
    # 평일 출퇴근 정보
    num_workingdays_business_valid_checkin_checkout_onsite_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 출퇴근 정보 있는 횟수
    # 평일 출근 장소
    num_workingdays_business_checkin_all_monthly = models.IntegerField(null=True, blank=True) # 0 월간 평일 출근 횟수(외근후 출근, 반차/반반차후 출근, 외근, 재택 포함,  휴가 불포함)    0 = 1 + 2 + 3
    num_workingdays_business_checkin_onsite_monthly = models.IntegerField(null=True, blank=True) # 1 월간 평일 회사 바로출근 횟수(외근후 출근, 반차/반반차후 출근 불포함)
    num_workingdays_business_checkin_outside_monthly = models.IntegerField(null=True, blank=True) # 2 월간 평일 출장/외근 횟수
    num_workingdays_business_checkin_home_monthly = models.IntegerField(null=True, blank=True) # 3 월간 평일 자택근무 횟수
    # 평일 출근 상태
    num_workingdays_business_checkin_standard_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 정상 출근 횟수
    num_workingdays_business_checkin_late_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 지각 횟수
    # num_workingdays_business_checkin_unknown_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 출근 누락 횟수
    # 평일 퇴근 상태
    num_workingdays_business_checkout_standard_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 정상 퇴근 횟수
    num_workingdays_business_checkout_late_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 연장근로 횟수
    # num_workingdays_business_checkout_unknown_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 퇴근 누락 횟수
    num_workingdays_business_checkin_checkout_unknown_monthly = models.IntegerField(null=True, blank=True) # 월간 평일 출퇴근 누락 횟수
    # 휴일 (휴일 출퇴근은 누락이 아니면 모두 정상근무시간으로 적용(지각/연장근로 없음))
    num_workingdays_holiday_checkin_all_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일 출근 횟수
    num_workingdays_holiday_checkin_checkout_unknown_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일 출퇴근 누락 횟수
    # num_workingdays_holiday_valid_checkin_checkout_onsite_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일 출퇴근 정보 있는 횟수
    # num_workingdays_holiday_checkin_standard_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일 정상출근 횟수
    # num_workingdays_holiday_checkin_unknown_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일 누락출근 횟수
    # num_workingdays_holiday_checkout_standard_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일 정상퇴근 횟수
    # num_workingdays_holiday_checkout_unknown_monthly = models.IntegerField(null=True, blank=True) # 월간 휴일 누락퇴근 횟수
    #--------------------------------------------------------------------------------------------------------------------------
    # 총 시간
    # 총 근무시간(식사시간 차감안함) # 넷 근무시간(식사시간 차감))
    #--------------------------------------------------------------------------------------------------------------------------
    # 평일 + 휴일 근무시간
    datetime_wkt_all_monthly_total = models.DateTimeField(null=True, blank=True) # 월간 휴일+평일 총 근무시간(외근/자택근무 포함)
    datetime_wkt_all_monthly_net = models.DateTimeField(null=True, blank=True) # 월간 휴일+평일 넷 근무시간(외근/자택근무 포함)
    datetime_wkt_all_monthly_total_on_site = models.DateTimeField(null=True, blank=True) # 월간 휴일+평일 총 근무시간(외근/자택근무 제외)
    datetime_wkt_all_monthly_net_on_site = models.DateTimeField(null=True, blank=True) # 월간 휴일+평일 넷 근무시간(외근/자택근무 제외)
    # 평일 근무시간 관련
    datetime_wkt_business_monthly_total = models.DateTimeField(null=True, blank=True) # 월간 평일 총 근무시간(외근/자택근무 포함)
    datetime_wkt_business_monthly_net = models.DateTimeField(null=True, blank=True) # 월간 평일 넷 근무시간(외근/자택근무 포함)
    datetime_wkt_business_monthly_total_on_site = models.DateTimeField(null=True, blank=True) # 월간 평일 회사출근 총 근무시간(조기출근/정상출근/지각, 조기퇴근/정상퇴근/야근)
    datetime_wkt_business_monthly_net_on_site = models.DateTimeField(null=True, blank=True) # 월간 평일 회사출근 넷 근무시간(조기출근/정상출근/지각, 조기퇴근/정상퇴근/야근)
    # 휴일 근무시간 관련
    datetime_wkt_holiday_monthly_total = models.DateTimeField(null=True, blank=True) # 월간 휴일 총 근무시간
    datetime_wkt_holiday_monthly_net = models.DateTimeField(null=True, blank=True) # 월간 휴일 넷 근무시간
    # 평일 총 지각/야근
    datetime_wkt_business_total_late_checkin_monthly = models.DateTimeField(null=True, blank=True) # 월간 평일 총 지각시간
    datetime_wkt_business_total_late_checkout_monthly = models.DateTimeField(null=True, blank=True) # 월간 평일 총 야근시간
    #--------------------------------------------------------------------------------------------------------------------------
    # 평균 시간
    #--------------------------------------------------------------------------------------------------------------------------
    # 평일 평균 출근시간 / 퇴근시간 / 근무시간
    time_wkt_business_avg_monthly_total = models.TimeField(null=True, blank=True) # 월간 평일 평균 총 근무시간
    time_wkt_business_avg_monthly_net = models.TimeField(null=True, blank=True) # 월간 평일 평균 넷 근무시간
    time_wkt_business_avg_checkin_monthly = models.TimeField(null=True, blank=True) # 월간 평일 평균 회사 출근시간
    time_wkt_business_avg_checkout_monthly = models.TimeField(null=True, blank=True) # 월간 평일 평균 회사 퇴근시간
    time_wkt_holiday_avg_monthly_total = models.TimeField(null=True, blank=True) # 월간 휴일 평균 총 근무시간
    time_wkt_holiday_avg_monthly_net = models.TimeField(null=True, blank=True) # 월간 휴일 평균 넷 근무시간
    #--------------------------------------------------------------------------------------------------------------------------
    # Display용 정보
    #--------------------------------------------------------------------------------------------------------------------------
    # Display용 총 근무시간(식사시간 차감안함)
    # Display용 총 근무시간(식사시간 차감)
    dp_wkt_hour_all_monthly_total = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 총 근무시간(외근/자택근무 포함) (시)
    dp_wkt_minute_all_monthly_total = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 총 근무시간(외근/자택근무 포함) (분)
    dp_wkt_hour_all_monthly_net = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 순 근무시간 (외근/자택근무 포함) (시)
    dp_wkt_minute_all_monthly_net = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 순 근무시간 (외근/자택근무 포함) (분)

    dp_wkt_hour_all_monthly_total_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 총 근무시간(외근/자택근무 제외) (시)
    dp_wkt_minute_all_monthly_total_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 총 근무시간(외근/자택근무 제외) (분)
    dp_wkt_hour_all_monthly_net_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 순 근무시간(외근/자택근무 제외) (시)
    dp_wkt_minute_all_monthly_net_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일+평일 순 근무시간(외근/자택근무 제외) (분)

    dp_wkt_hour_business_monthly_total = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (시)
    dp_wkt_minute_business_monthly_total = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (분)
    dp_wkt_hour_business_monthly_net = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (시)
    dp_wkt_minute_business_monthly_net = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (분)

    dp_wkt_hour_business_monthly_total_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (외근/자택근무 제외) (시)
    dp_wkt_minute_business_monthly_total_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (외근/자택근무 제외) (분)
    dp_wkt_hour_business_monthly_net_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (외근/자택근무 제외) (시)
    dp_wkt_minute_business_monthly_net_on_site = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 근무시간 (외근/자택근무 제외) (분)

    dp_wkt_hour_holiday_monthly_total = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일 총 근무시간 (시)
    dp_wkt_minute_holiday_monthly_total = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일 총 근무시간 (분)
    dp_wkt_hour_holiday_monthly_net = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일 총 근무시간 (시)
    dp_wkt_minute_holiday_monthly_net = models.IntegerField(null=True, blank=True)   # 표시용 월간 휴일 총 근무시간 (분)

    #--------------------------------------------------------------------------------------------------------------------------
    # Display용 지각 시간
    dp_hour_business_late_checkin_monthly = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 지각시간 (시)
    dp_minute_business_late_checkin_monthly = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 지각시간 (분)
    # Display용 야근 시간
    dp_hour_business_late_checkout_monthly = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 야근시간 (시)
    dp_minute_business_late_checkout_monthly = models.IntegerField(null=True, blank=True)   # 표시용 월간 평일 총 야근시간 (분)


    #--------------------------------------------------------------------------------------------------------------------------
    # # Analytics Graph
    # distribution_rate_avg_wkt_business = models.FloatField(null=True, blank=True)  #
    #--------------------------------------------------------------------------------------------------------------------------
    # 휴일 출근 상태 지정
    check_status_holiday_mandatory = models.BooleanField(default=False)  # True: 휴일 근무일 경우 정상 출퇴근시간 적용받음
    #--------------------------------------------------------------------------------------------------------------------------
    # 출퇴근시간 개인맞춤 세팅
    #--------------------------------------------------------------------------------------------------------------------------
    # 요일별 개인맞춤 출퇴근시간 적용
    check_default_datetime_personalization_activated = models.BooleanField(default=False) # True : 요일별 개인맞춤형 출퇴근시간 활성화
    list_dict_default_wkt_standard_personalized = models.JSONField(null=True, blank=True)  # [{'start_hour': 9, 'start_minute': 30, 'end_hour': 18, 'end_minute': 30}], [화요일] [수요일]...}
    # 활성화될 경우 HR 기본 출퇴근시간 적용이 아닌 개인 기본 출퇴근 시간 적용됨
    check_default_datetime_start_activated = models.BooleanField(default=False) # True : 출근시간 개인 기본설정시간 활성화
    check_default_datetime_end_activated = models.BooleanField(default=False) # True : 퇴근시간 개인 기본설정시간 활성화
    default_time_start_standard = models.TimeField(blank=True, null=True) # 개인 기본설정 출근시간
    default_time_end_standard = models.TimeField(blank=True, null=True) # 개인 기본설정 퇴근시간
    #--------------------------------------------------------------------------------------------------------------------------
    # Trouble 핸들링
    check_report_trouble_submitted = models.BooleanField(default=False)
    #--------------------------------------------------------------------------------------------------------------------------
    # System
    check_discard = models.BooleanField(default=False)






LIST_TYPE_WORKINGTIME = (
    ('WORK_AT_FIELD', '출장(외부근무)'), # 0 출장
    ('WORK_AT_HOME', '재택근무'),  # 1 재택
    ('WORK_ON_HOLIDAY', '휴일근무'),  # 2 휴일
    ('WORKING_TIME_PERSONALIZE', '맞춤형근무시간'),  # 3
)

LIST_TYPE_WORKINGTIME_FIELD = (
    ('DOMESTIC', '국내출장'),
    ('OVERSEA', '해외출장'),
)

LIST_TYPE_WORKINGTIME_HOME = (
    ('SPECIFIC', '기간설정'),
    ('PERIODIC', '매주반복'),
)

LIST_TYPE_WORKINGTIME_HOME_PERIODIC = (
    ('ON-SITE', '정상출근'),
    ('WHOLE_DAY', '하루재택'),
    ('HALF_AM', '오전재택'),
    ('HALF_PM', '오후재택'),
)




def get_upload_path(instance, dummy):
    return instance.path + "/" + instance.filename


# 근무계획서
class Workingtime_Plan(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    hrapproval = models.ForeignKey(HR_Document_Approval_Management, null=True, on_delete=models.CASCADE)
    # 아래 status는 modal창을 통한 등록/업데이트가 완성되면 삭제
    #--------------------------------------------------------------------------------------------------------------------------
    # 근무계획서 관련
    #--------------------------------------------------------------------------------------------------------------------------
    # Type
    type_workingtime = models.CharField(verbose_name="근무형태", max_length=100, choices=LIST_TYPE_WORKINGTIME, blank=True, null=True)
    type_workingtime_field = models.CharField(verbose_name="외근(출장)형태", max_length=100, choices=LIST_TYPE_WORKINGTIME_FIELD, blank=True, null=True)
    type_workingtime_home = models.CharField(verbose_name="재택근무 형태", max_length=100, choices=LIST_TYPE_WORKINGTIME_HOME, blank=True, null=True)
    type_workingtime_home_periodic = models.CharField(verbose_name="재택근무 반복근무 재택시간", max_length=100, choices=LIST_TYPE_WORKINGTIME_HOME_PERIODIC, blank=True, null=True)
    # 요일별 재택근무 시간
    dict_type_workingtime_home_periodic_weekdays_time = models.JSONField(null=True, blank=True)  # {'monday': 'ON-SITE', 'tuesday': 'WHOLE_DAY', 'wednesday': 'HALF-AM', 'thursday': 'HALF-PM', 'friday': 'ON-SITE'}
    # 개인맞춤형 출퇴근 시간
    list_dict_default_wkt_standard_personalized = models.JSONField(null=True, blank=True) #  [{'start_hour': 9, 'start_minute': 30, 'end_hour': 18, 'end_minute': 30}], [화요일] [수요일]...}
    #--------------------------------------------------------------------------------------------------------------------------
    # 공통필드
    #--------------------------------------------------------------------------------------------------------------------------
    # Date Time
    datetime_start = models.DateTimeField(blank=True, null=True)
    datetime_end = models.DateTimeField(blank=True, null=True)
    # Destination and Reason
    destination = models.CharField(max_length=250, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # system
    #--------------------------------------------------------------------------------------------------------------------------
    check_valid = models.BooleanField(verbose_name="문서 유효성 여부", default=True) # False : 근무계획 종료일이 지날경우, 승인 후 작성자가 취소할 경우
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    check_discard = models.BooleanField(default=False) # 1명 이상 승인 전에 취소하면 discard 시킨다.
    # 추후 삭제
    #--------------------------------------------------------------------------------------------------------------------------
    # 인사팀과 수정요청관련
    status_xxx_document_plan_requested_to = models.CharField(max_length=100, choices=STATUS_MY_XXX_DOCUMENT_PLAN_REQUEST_TO, default=STATUS_MY_XXX_DOCUMENT_PLAN_REQUEST_TO[0][0], blank=True)
    check_hr_xxx_document_plan_request_to_hr_activated = models.BooleanField(default=False) # True: 인사팀에게 근무계획서 정정/취소 관련 요청함, False: 요청내용수정완료시/취소시
    dict_communication_with_hr_for_my_xxx_document_plan = models.JSONField(null=True, blank=True) # 발행된 근무계획서 관련 인사팀 요청하기 대화내용 저장
    dict_modified_draft_for_xxx_document_plan_from_hr = models.JSONField(null=True, blank=True) # 인사팀이 수정한 임시 근무계획서 관련 내용 저장
    #--------------------------------------------------------------------------------------------------------------------------
    # 아래내용 hr doc file 완성뒤 삭제
    # Reference File
    # Reference File
    path = models.CharField(max_length=250, null=True, blank=True)
    filename = models.CharField(max_length=250, null=True, blank=True)
    reference_file = models.FileField(upload_to=get_upload_path, null=True, blank=True)



STATUS_WORKING_DAY = (
    ('WK_DAY_NORMAL', '정상근무일'),  # 0
    ('WK_DAY_HOLYDAY', '주말/국공휴일/회사휴일'),  # 1
)

STATUS_WORKING_TIME_START = (
    ('WKD_TIME_EARLY', '조기출근'),  # 0
    ('WKD_TIME_NORMAL', '정상출근'),  # 1
    ('WKD_TIME_LATE', '지각'),  # 2
    ('WKD_TIME_UNKNOWN', '출근미상'),  # 3
    ('WKD_TIME_EXTRA', '근무일 외 출근'),  # 4
    ('WKD_TIME_VACATION_AND_WORK', '반차/반반차 후 출근'),  # 5
    ('WKD_TIME_ON_VACATION', '휴가중'),  # 6
    ('WKD_TIME_OFF_SITE_AND_ON_SITE', '외근 후 출근'),  # 7
    ('WKD_TIME_OFF_SITE', '외부근무'),  # 7
    ('WKD_TIME_HOME', '자택근무'),  # 8
)
STATUS_WORKING_TIME_END = (
    ('WKD_TIME_EARLY', '조기퇴근'),  # 0
    ('WKD_TIME_NORMAL', '정상퇴근'),  # 1
    ('WKD_TIME_LATE', '연장근로'),  # 2
    ('WKD_TIME_UNKNOWN', '퇴근미상'),  # 3
    ('WKD_TIME_EXTRA', '근무일 외 퇴근'),  # 4
    ('WKD_TIME_VACATION_AND_WORK', '반차/반반차 퇴근'),  # 5
    ('WKD_TIME_ON_VACATION', '휴가중'),  # 6
    ('WKD_TIME_OFF_SITE_AND_ON_SITE', '외근 후 퇴근'),  # 7
    ('WKD_TIME_OFF_SITE', '외부근무'),  # 7
    ('WKD_TIME_HOME', '자택근무'),  # 8
)

STATUS_WORKING_TYPE_LOCATION = (
    ('ON-SITE', '회사출근'), # 0 부분 휴가/출장/자택근무 모두 회사출근으로 간주
    ('OUTSIDE', '외근/출장'),  # 1  whole day 출장/자택근무인 경우만
    ('HOME', '재택근무'),  # 2 whole day 자택근무인 경우만
    ('VACATION', '휴가'),  # 3 whole day 휴가인 경우만
    ('UNKNOWN', '미상'),  # 4
)


STATUS_MY_WORKINGTIME_ISSUED_REQUEST_TO_HR = (
    ('NORMAL', '정상상태'),  # 0
    ('REQUESTED', '인사팀에 정정 요청'), # 1
    ('MODIFIED', '인사팀이 정정 내용 기입 완료, 내용확인'), # 2
    ('RESPONSED', '정정 내용 사용자에게 발송'),  # 3
    ('ACCEPTED', '정정 내용 사용자 동의 및 완료'),  # 4
)


class Workingtime_Issued(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    workingtime_control = models.ForeignKey(Workingtime_Control, on_delete=models.CASCADE, null=True, blank=True)
    workingtime_plan = models.ForeignKey(Workingtime_Plan, on_delete=models.SET_NULL, null=True, blank=True)
    vacation_plan = models.ForeignKey(Vacation_Plan, on_delete=models.SET_NULL, null=True, blank=True)
    # Date
    date_of_work = models.DateField(blank=True, null=True)  # 출퇴근 날짜
    # Date Time
    datetime_start = models.DateTimeField(blank=True, null=True) # 출근 날짜/시간
    datetime_end = models.DateTimeField(blank=True, null=True) # 퇴근 날짜/시간
    datetime_end_manual = models.DateTimeField(blank=True, null=True) # 전일 퇴근시간 미등록에 따른 익일 수동등록시 퇴근 날짜/시간
    time_net_working = models.TimeField(blank=True, null=True) # 오늘 실제 근무시간
    time_total_working = models.TimeField(blank=True, null=True) # 오늘 총 근무시간
    # Status
    status_working_year = models.IntegerField(verbose_name="근무년차", null=True, blank=True) # 근무 년차 (예 : 1년차 == 1일 ~ 365일 근무)
    status_working_day = models.CharField(verbose_name="근무일상태", max_length=100, choices=STATUS_WORKING_DAY, blank=True, null=True)
    status_wkt_start = models.CharField(verbose_name="출근상태", max_length=100, choices=STATUS_WORKING_TIME_START, blank=True, null=True)
    status_wkt_end = models.CharField(verbose_name="퇴근상태", max_length=100, choices=STATUS_WORKING_TIME_END, blank=True, null=True)
    # 근무형태(회사출근/외부근무/재택근무)
    status_working_type_location = models.CharField(max_length=100, choices=STATUS_WORKING_TYPE_LOCATION, blank=True, null=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # 인사팀과 수정요청관련
    #--------------------------------------------------------------------------------------------------------------------------
    # Status
    status_workingtime_issued_requested_to_hr = models.CharField(max_length=100, choices=STATUS_MY_WORKINGTIME_ISSUED_REQUEST_TO_HR, default=STATUS_MY_WORKINGTIME_ISSUED_REQUEST_TO_HR[0][0], blank=True)
    check_hr_wkt_issued_request_to_hr_activated = models.BooleanField(default=False) # True:  본인이 미기입된 출퇴근 정보 기입 완료시(인사팀에게 출퇴근쿼리 정정/취소 관련 요청), False: 요청내용수정완료시/취소시
    # Talk
    dict_request_for_my_issued_wkt_trouble = models.JSONField(null=True, blank=True) # 발행된 출퇴근쿼리 관련 인사팀 요청하기 대화내용 저장
    # Cache Data
    dict_modified_draft_for_workingtime_issued_from_hr = models.JSONField(null=True, blank=True) # 인사팀이 수정한 임시 출퇴근쿼리 관련 내용
    dict_modified_draft_for_workingtime_issued_by_me = models.JSONField(null=True, blank=True) # 본인이 작성한 임시 출퇴근쿼리 관련 내용
    # check list
    check_confirmed = models.BooleanField(default=False) # 확정
    check_discard = models.BooleanField(default=False) # 삭제

    def __str__(self):
        return f'{self.owner.profile.name_korean}-({self.date_of_work})_({self.id})'



###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                               HR Document
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################




class HR_Document_Issued(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hrlayout = models.ForeignKey(HR_Layout, null=True, on_delete=models.CASCADE)
    document_format = models.ForeignKey(HR_Document_Format, on_delete=models.SET_NULL, null=True, blank=True) # 문서 포맷
    hrapproval = models.ForeignKey(HR_Document_Approval_Management, on_delete=models.SET_NULL, null=True, blank=True) # 문서승인절차관리
    hrrequest = models.ForeignKey(HR_Document_Request_Management, on_delete=models.SET_NULL, null=True, blank=True) # 인사팀수정요청관리
    hrdocfile = models.ForeignKey(HR_Document_Attached_File_Management, on_delete=models.SET_NULL, null=True, blank=True) # 첨부파일관리
    list_hrdocfile_id = models.JSONField(null=True, blank=True) # 첨부파일이 2개 이상인 경우 ID 관리
    code = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # Plans
    vacation_plan = models.ForeignKey(Vacation_Plan, on_delete=models.SET_NULL, null=True, blank=True) # 본인의 현재 선택된 q_hr_layout 정보
    workingtime_plan = models.ForeignKey(Workingtime_Plan, on_delete=models.SET_NULL, null=True, blank=True) # 본인의 현재 선택된 q_hr_layout 정보
    #--------------------------------------------------------------------------------------------------------------------------
    # Check
    #--------------------------------------------------------------------------------------------------------------------------
    # System
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    check_discard = models.BooleanField(default=False)




###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                        HR Task 관리
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


class Task_Plan(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    hrlayout = models.ForeignKey(HR_Layout, null=True, on_delete=models.CASCADE)
    list_hrlayout_id = models.JSONField(null=True, blank=True) # 복수의 포지션을 가진 멤버의 경우
    list_dict_project_id_project_percent = models.JSONField(null=True, blank=True) # 프로젝트별 업무 분담율
    # [{"id": 0, "project_name": "C797S", "participant_percent": 50}, {"id": 1, "project_name": "EGFR", "participant_percent": 30}, {"id": 2, "project_name": "KRAS", "participant_percent": 20}]
    contribution_current_total = models.IntegerField(default=0)  # 입력한 기여도 % 현재 합한 값. 최종 100이 되야 한다.
    num_of_involved_project = models.IntegerField(default=1)  # 참여한 프로젝트 개수
    accomplishment = models.CharField(max_length=250, null=True, blank=True) # 업무관련 성취한 특이사항
    dict_comment = models.JSONField(null=True, blank=True)
    date_start_task_submission = models.DateField(null=True, blank=True) # 해당 근무월의 입력받기 시작일, 자동으로 기입
    date_deadline_task_submission = models.DateField(null=True, blank=True) # 해당 근무월의 입력받기 마감일, 자동으로 기입
    date_remind_me_later = models.DateField(null=True, blank=True) # 오늘 날짜와 일치하면 모달창을 더 이상 띄우지 않는다.
    date_created = models.DateTimeField(auto_now_add=True, null=True) # 작성일

    check_activate_submission_form = models.BooleanField(default=False)  # True: 기한이 되면 사용자가 월별 근무내용을 입력할 수 있도록 입력양식을 활성화시켜줌
    check_activate_submission_form_enforced = models.BooleanField(default=False)  # True: 인사팀이 강제로 활성화시킴
    check_alert_submission_late = models.BooleanField(default=False)  # True: 제출마감일 몇일 전까지 미제출상태. 알람 띄워주기
    check_submitted = models.BooleanField(default=False)  # True: 제출함
    check_hr_confirmed = models.BooleanField(default=False)  # True: 인사팀 확인함(확인하면 수정 불가)
    check_discard = models.BooleanField(default=False)

    # 관리자 세팅값 :
    # 0. Project_Simple 모델의 프로젝트 이름 입력해야 사용자가 검색으로 선택 가능.
    # 1. 월말일 몇 일 전에 입력양식을 활성화 시켜줄 것인가?
    # 2. 월말일 몇 일 전에 미입력시 경고창을 띄워줄 것인가?
    # 3. 경고창 내용은 어떤 내용을 보낼 것인가?

    def __str__(self):
        return_value = f'{self.owner.profile.name_korean}({self.date_deadline_task_submission})'
        return return_value




class Task_Analysis_by_Project(models.Model):
    participant_percent_among_all = models.FloatField(default=0)  # 모든 프로젝트들 중 해당 프로젝트에 참여한 비중 % (모든 프로젝트의 합은 100%)
    list_dict_participant_percent_by_project = models.JSONField(null=True, blank=True)
    list_dict_participant_percent_by_team = models.JSONField(null=True, blank=True)
    list_dict_participant_percent_by_member = models.JSONField(null=True, blank=True)
    dict_comment = models.JSONField(null=True, blank=True)
    # date_analysis_project_simple = models.DateField(null=True, blank=True) # 프로젝트 분석에 해당하는 달의 첫째날 기입
    date_created = models.DateTimeField(auto_now_add=True, null=True) # 작성일
    check_discard = models.BooleanField(default=False)

    def __str__(self):
        return_value = f'{self.date_analysis_project_simple}'
        return return_value





###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                             HR News
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


def get_upload_member_news_user(instance, dummy):
    return instance.path + "/" + instance.filename

LIST_NEWS_ARTICLE_TYPE = (
    ('VORONOI', '보로노이 소식'),  # 0
    ('DIVISION', '부서 소식'),  # 1
    ('TEAM', '팀 소식'),  # 2
    ('MY', '나의 메모'),  # 3
    ('SYSTEM', '시스템 알림'),  # 4
)

LIST_NEWS_INFORM_TYPE = (
    ('NEWS', '새소식'),  # 0
    ('NOTICE', '공지사항'),  # 1
    ('ALERT', '긴급사항'),  # 2
)


class HR_News_Article(models.Model):
    # Keys
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hrlayout = models.ForeignKey(HR_Layout, on_delete=models.SET_NULL, null=True, blank=True)
    list_selected_team_id = models.JSONField(null=True, blank=True)
    # News
    news_type = models.CharField(max_length=50, choices=LIST_NEWS_ARTICLE_TYPE, default=LIST_NEWS_ARTICLE_TYPE[0][0], blank=True)
    news_inform_type = models.CharField(max_length=50, choices=LIST_NEWS_INFORM_TYPE, default=LIST_NEWS_INFORM_TYPE[0][0], blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True) # News 내용
    # reference file 저장
    path = models.CharField(max_length=250, null=True, blank=True)
    filename = models.CharField(max_length=250, null=True, blank=True)
    reference_file = models.FileField(upload_to=get_upload_member_news_user, null=True, blank=True)
    # system
    datetime_created = models.DateTimeField(auto_now_add=True, null=True)
    check_discard = models.BooleanField(default=False)



###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
#
#                                                               Mysettings
#
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################




# Member 등록화면 리스트 테이블 Column Index
MEMBER_REGISTER_FIELD=(
    ('id', '순번'),
    ('name_korean', '한글 이름'),
    ('first_name', '영문 이름'),
    ('date_joined', '입사일'),
    ('date_left', '퇴사일'),
    ('delta_day_joined', '총근무일'),
    ('email', '이메일 주소'),
    ('phone_office', '회사 전화번호'),
    ('phone_mobile', '핸드폰 번호'),
    ('date_of_birth', '생일'),
)


LIST_HR_DOCUMENT_CONTROL_TYPE = (
    ('DOCUMENT_FORMAT', '문서형식관리'),
    ('DOCUMENT_APPROVED', '승인문서관리'),
    ('DOCUMENT_REQUESTED', '수정요청문서관리'),
)

LIST_DOCUMENT_CONTROL_TABLE_COLUMN_INDEX = (
    ('DOCUMENT_FORMAT_CODE', '문서양식 코드'),
    ('DOCUMENT_FORMAT_TITLE', '문서양식 제목'),
    ('DOCUMENT_FORMAT_DESCRIPTION', '문서양식 설명'),
    ('DOCUMENT_FORMAT_REFERRER', '문서양식 참조자'),
    ('DOCUMENT_FORMAT_RECEIVER', '문서양식 수신처'),
    ('DOCUMENT_FORMAT_DATE', '문서양식 등록일'),
)

STATUS_HR_DAM_MODAL_VIEW_SEARCH_MEMBER = (
    ('APPROVAL', '승인권자찾기'),  # 0
    ('TAKEOVER', '업무인수자찾기'),  # 1
    ('REFERRER', '참조자찾기'),  # 2
    ('RECEIVER', '수신처찾기'),  # 3
    ('COMPLETED', '작성완료'),  # 4
)

# Workingtime Submenu
LIST_HR_WORKINGTIME_CONTROL_TYPE = (
    ('WORKINGTIME_TODAY', '멤버 출퇴근 현황'), # 0
    ('WORKINGTIME_ANALYTICS', '멤버 출퇴근 분석'), # 1
    ('WORKINGTIME_REQUEST', '멤버 출퇴근 요청대응'), # 2
    ('WORKINGTIME_SETTINGS', '멤버 근무시간 설정'), # 3
    ('WORKINGTIME_PLAN', '멤버 근무계획서 현황'), # 4
    ('WORKINGTIME_PLNA_REQUEST', '멤버 근무계획서 요청대응'), # 5
)

LIST_HR_VACATION_CONTROL_TYPE = (
    ('VACATION_CALENDAR', '휴가 Calendar'), # 0
    ('VACATION_ISSUED_CONTROL', '휴가 발행 및 관리'), # 1
    ('VACATION_PLAN_CONTROL', '휴가 계획서 관리'), # 2
    ('VACATION_PROMOTION_CONTROL', '연차 소모 관리'), # 3
)

LIST_HR_VACATION_CONTROL_PLAN_DISPLY_TYPE = (
    ('VACATION_PLAN_ORDER_BY_DATE_APPROVAL', '최근 등록일순 표시'),  # 0
    ('VACATION_PLAN_ORDER_BY_MEMBER_NAME_ASC', '멤버이름별 오름차순 표시'),  # 1
    ('VACATION_PLAN_ORDER_BY_MEMBER_NAME_DESC', '멤버이름별 내림차순 표시'),  # 2
    ('VACATION_PLAN_ORDER_BY_DATE_START_ASC', '휴가시작일 과거일 먼저표시'),  # 3
    ('VACATION_PLAN_ORDER_BY_DATE_START_DESC', '휴가시작일 최근일 먼저표시'),  # 4
    ('VACATION_PLAN_BY_SELECTED_MEMBER', '선택멤버만 표시'),  # 5
)

LIST_HR_VACATION_CONTROL_ISSUED_SUBMENU_TYPE = (
    ('VACATION_CONTROL_AUTOREGISTER', '연차 자동등록'),
    ('VACATION_CONTROL_MANUALREGISTER', '휴가 수동등록'),
    ('VACATION_CONTROL_HISTROY', '휴가관리 히스토리'),
)

LIST_HR_VACATION_CONTROL_PLAN_SUBMENU_TYPE = (
    ('VACATION_PLAN_AUTOREGISTER', '휴가계획서 자동등록'),
    ('VACATION_PLAN_MANUALREGISTER', '휴가계획서 수동등록'),
    ('VACATION_PLAN_DOWNLOAD', '휴가계획서 파일받기'),
)


LIST_HR_CALENDAR_CONTROL_TYPE = (
    ('HOLYDAY_CALENDAR', 'Calendar'),
    ('NATIONAL_EVENT_REGISTER', '국가 Event 등록'),
    ('VORONOI_EVENT_REGISTER', 'Voronoi Event 등록'),
)

STATUS_HR_VACATION_PLAN_REGISTER_MANUALLY = (
    ('STEP1_APPLICANT', '신청자 정보 입력'),  # 0
    ('STEP2_APPROVER', '결재자 정보 입력'),  # 1
    ('STEP3_VACATION_PLAN', '휴가계획서 정보 입력'),  # 2
    ('STEP4_FINAL_CHECK', '휴가계획서 최종 확인'),  # 3
)



LIST_VACATION_PROMOTION_SUBMENU = (
    ('INFORM_MANUALLY', '연차사용 촉진 수동 공지'),
    ('PROMOTION_SETTINGS', '연차 소모 관리자 세팅'),
)

LIST_VACATION_PROMOTION_ORDERING_TYPES = (
    ('MEMBER_NAME_ASC', '멤버이름 오름차순'),  # 0
    ('MEMBER_NAME_DESC', '멤버이름 내림차순'),  # 1
    ('USED_PROGRESS_ASC', '연차사용 오름차순'),  # 2
    ('USED_PROGRESS_DESC', '연차사용 내림차순'),  # 3
    ('DEADLINE_REMAINED_ASC', '연차만료 오름차순'),  # 4
    ('DEADLINE_REMAINED_DESC', '연차만료 내림차순'),  # 5
)


LIST_HR_TASK_CONTROL_TYPE = (
    ('TASK_PROJECT', '프로젝트 관리'), # 0
    ('TASK_CONTROL', '업무 관리'), # 1
)

LIST_HR_MEMBER_REGISTER_TYPE = (
    ('REGISTER_MANUAL', '수동으로 등록하기'), # 0
    ('REGISTER_FILE', 'File로 등록하기'), # 1
    ('REGISTER_SETTINGS', '기본값 세팅'), # 2
)

LIST_TASK_PROJECT_CONTROL_SUBMENU = (
    ('CREATE_PROJECT', '프로젝트 생성'),
    ('UPDATE_PROJECT', '프로젝트 업데이트'),
    ('DELETE_PROJECT', '프로젝트 삭제'),
)

LIST_TASK_PROJECT_PARTICIPANT_SUBMENU = (
    ('STATISTICS_PROJECT', '프로젝트별 파일 다운'),
    ('STATISTICS_TEAM', '팀별 파일 다운'),
    ('STATISTICS_MEMBER', '개인별 파일 다운'),
)



LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_TODAY = (
    ('owner__profile__name_korean', '이름'), # 0
    ('workingtime_control__hrlayout__division', '소속 부서'), # 1
    ('workingtime_control__hrlayout__team', '소속 팀'), # 2
    ('date_of_work', '근무일'), # 3
    ('datetime_start', '출근 시간'), # 4
    ('status_wkt_start', '출근 상태'), # 5
    ('datetime_end', '퇴근 시간'), # 6
    ('status_wkt_end', '퇴근 상태'), # 7
    ('time_net_working', '실근무시간'), # 8
    ('status_working_type_location', '근무지역'), # 9
    ('workingtime_plan', '근무계획서'), # 10
    ('vacation_plan', '휴가계획서'), # 11
    ('workingtime_control__check_default_datetime_end_activated', '자동등록여부'), # 12
)

LIST_HR_WORKING_TIME_TABLE_COLUMN_INDEX_TYPE = (
    ('ALLDAY', '평일+휴일'), # 0
    ('BUSINESSDAY', '평일'), # 1
    ('HOLIDAY', '휴일'), # 2
)

LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_ANALYTICS = (
    ('owner__profile__name_korean', '이름'), # 0
    ('hrlayout__division', '소속 부서'), # 1
    ('hrlayout__team', '소속 팀'), # 2
    # 평일 + 휴일
    ('num_workingdays_all_checkin_monthly', '월간 평일+휴일 근무 횟수'), # 3 : 연차 제외
    ('datetime_wkt_all_monthly_total', '월간 평일+휴일 총 근무시간'),  # 4
    ('datetime_wkt_all_monthly_total_on_site', '월간 평일+휴일 총 근무시간 (외근/자택 제외)'),  # 4
    # 평일 근무
    ('num_workingdays_business_valid_checkin_checkout_onsite_monthly', '월간 평일 출퇴근 근무횟수'), # 5 평일 출퇴근 정보 있는 근무 횟수
    ('datetime_wkt_business_monthly_total', '월간 평일 총 근무시간'),  # 6
    ('datetime_wkt_business_monthly_total_on_site', '월간 평일 총 근무시간 (외근/자택 제외)'),
    ('time_wkt_business_avg_monthly_total', '월간 평일 평균 근무시간'),  # 7 : 누락, 연차(반차, 반반차) 제외, 연차 결합시 자동으로 휴가 제외하기 기능 추가해야 함.
    # 평일 출근 상태
    ('time_wkt_business_avg_checkin_monthly', '월간 평일 평균 출근시간'), # 8
    ('datetime_wkt_business_total_late_checkin_monthly', '월간 평일 총 지각시간'), # 9
    ('num_workingdays_business_checkin_standard_monthly', '월간 평일 정상 출근 횟수'), # 10
    ('num_workingdays_business_checkin_late_monthly', '월간 평일 지각 횟수'), # 11
    # ('num_workingdays_business_checkin_unknown_monthly', '월간 평일 출근누락 횟수'), # 12
    # 평일 퇴근 상태
    ('time_wkt_business_avg_checkout_monthly', '월간 평일 평균 퇴근시간'), # 13
    ('datetime_wkt_business_total_late_checkout_monthly', '월간 평일 총 야근시간'), # 14
    ('num_workingdays_business_checkout_standard_monthly', '월간 평일 정상 퇴근 횟수'), # 15
    ('num_workingdays_business_checkout_late_monthly', '월간 평일 연장근로 횟수'), # 16
    # ('num_workingdays_business_checkout_unknown_monthly', '월간 평일 퇴근누락 횟수'), # 17
    ('num_workingdays_business_checkin_checkout_unknown_monthly', '월간 평일 출퇴근 누락 횟수'), # 17
    # 평일 근무 위치
    ('num_workingdays_business_checkin_onsite_monthly', '월간 평일 회사출근 횟수'), # 18
    ('num_workingdays_business_checkin_outside_monthly', '월간 평일 출장/외근 횟수'), # 19
    ('num_workingdays_business_checkin_home_monthly', '월간 평일 재택근무 횟수'), # 20
    # 휴일 근무
    ('num_workingdays_holiday_valid_checkin_checkout_onsite_monthly', '월간 휴일 출퇴근 횟수'), # 21
    ('datetime_wkt_holiday_monthly_total', '월간 휴일 총 근무시간'), # 22
    ('time_wkt_holiday_avg_monthly_total', '월간 휴일 평균 근무시간'), # 23
    # ('num_workingdays_holiday_checkin_standard_monthly', '월간 휴일 정상출근 횟수'), # 23
    # ('num_workingdays_holiday_checkin_unknown_monthly', '월간 휴일 출근누락 횟수'), # 24
    # ('num_workingdays_holiday_checkout_standard_monthly', '월간 휴일 정상퇴근 횟수'), # 25
    # ('num_workingdays_holiday_checkout_unknown_monthly', '월간 휴일 퇴근누락 횟수'), # 26
    ('num_workingdays_holiday_checkin_checkout_unknown_monthly', '월간 휴일 출퇴근 누락 횟수'), # 17
)

LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_PLAN = (
    ('owner__profile__name_korean', '이름'), # 0
    ('hrapproval__hrlayout_applicant__division', '소속 부서'), # 1
    ('hrapproval__hrlayout_applicant__team', '소속 팀'), # 2
    # 평일 + 휴일
    ('type_workingtime', '근무계획서 종류'), # 3
    ('datetime_process_start', '출장(자택)근무 시작일'), # 4
    ('datetime_process_end', '출장(자택)근무 종료일'), # 5
    ('type_workingtime_field', '출장 종류'), # 6
    ('destination', '출장지'), # 7
    ('reason', '내용(이유)'), # 8
    ('filename', '첨부파일'), # 9
    ('hrapproval', '문서승인'), # 10
)

LIST_TASK_PLAN_TABLE_COLUMN_INDEX = (
    ('owner__profile__name_korean', '이름'), # 0
    ('hrlayout__division', '소속 부서'), # 1
    ('hrlayout__team', '소속 팀'), # 2
)

LIST_WORKING_TIME_ANALYTICS_GRAPH_CHART = (
    ('time_wkt_business_avg_monthly_net', '월간 평일 평균 근무시간'),
    ('time_wkt_business_avg_checkin_monthly', '월간 평일 평균 출근시간'),
    ('time_wkt_business_avg_checkout_monthly', '월간 평일 평균 퇴근시간'),
)



class HR_My_Settings(models.Model):
    owner = models.ForeignKey(User, related_name='Owner_User', on_delete=models.CASCADE, null=True, blank=True)
    authority = models.ForeignKey(Authority, on_delete=models.SET_NULL, null=True, blank=True)
    date_reset = models.DateField(null=True, blank=True) # 하루 한 번씩 리셋
    # Created or Selected F.Key
    user = models.ForeignKey(User, related_name='Member_User', on_delete=models.SET_NULL, null=True, blank=True) # 선택된/생성된 유저
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True) # 선택된/생성된 멤버
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True) # 선택된/생성된 멤버
    profile_resign = models.ForeignKey(Profile, related_name="Resign_Member_Profile", on_delete=models.SET_NULL, null=True, blank=True) # 은퇴한 멤버 프로필
    hrlayout = models.ForeignKey(HR_Layout, on_delete=models.SET_NULL, null=True, blank=True)
    hrlayout_management = models.ForeignKey(HR_Layout_Member_Management, on_delete=models.SET_NULL, null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # Search
    #--------------------------------------------------------------------------------------------------------------------------
    list_member_hr_id_searched = models.JSONField(null=True, blank=True) # 검색된 멤버 id
    list_input_keyword = models.JSONField(null=True, blank=True)
    list_member_id_discard = models.JSONField(null=True, blank=True) # 퇴사처리된 멤버 id
    list_member_id_searched = models.JSONField(null=True, blank=True) # 검색된 멤버 id
    list_member_id_all_part = models.JSONField(null=True, blank=True)
    list_profile_id_searched = models.JSONField(null=True, blank=True) # 멤버 프로필 검색 결과
    list_resign_profile_id_searched = models.JSONField(null=True, blank=True) # 퇴사한 멤버 프로필 검색 결과
    check_subsearch = models.BooleanField(default=False)
    #--------------------------------------------------------------------------------------------------------------------------
    # update check
    #--------------------------------------------------------------------------------------------------------------------------
    list_member_hr_id_added = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # display settings
    #--------------------------------------------------------------------------------------------------------------------------
    page_number_auth_panel = models.IntegerField(default=1)
    selected_field_ordering = models.CharField(max_length=200, choices=MEMBER_REGISTER_FIELD, default=MEMBER_REGISTER_FIELD[1][0], blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # Resign
    #--------------------------------------------------------------------------------------------------------------------------
    resign_step = models.IntegerField(default=1)
    list_resign_successor_searched_member_id = models.JSONField(null=True, blank=True)  # 검색된 퇴작지 후임자 멤버 id 리스트
    #--------------------------------------------------------------------------------------------------------------------------
    # Alert Modal
    #--------------------------------------------------------------------------------------------------------------------------
    activate_modal_warning_delete_member_permanently = models.BooleanField(default=False) # True: 멤버 정보 영구 삭제 경고창 활성화
    #--------------------------------------------------------------------------------------------------------------------------
    # check_list
    #--------------------------------------------------------------------------------------------------------------------------\community\adultpic\84701\
    check_display_order_field_ascending = models.BooleanField(default=False)
    check_searched = models.BooleanField(default=False)
    check_member_searched_selected = models.BooleanField(default=False)

    ###################################################################################################################################################
    # Calendar
    ###################################################################################################################################################
    #--------------------------------------------------------------------------------------------------------------------------
    # Calendar Control
    #--------------------------------------------------------------------------------------------------------------------------
    # Calendar Display
    calendar_control_type = models.CharField(max_length=50, choices=LIST_HR_CALENDAR_CONTROL_TYPE, default=LIST_HR_CALENDAR_CONTROL_TYPE[0][0], blank=True)
    # Calendar 이동하기 선택된 년/월/일
    selected_year = models.IntegerField(null=True, blank=True)
    selected_month = models.IntegerField(null=True, blank=True)
    selected_day = models.IntegerField(null=True, blank=True)
    # Calendar Event 등록
    calendar_control = models.ForeignKey(HR_Calendar_Control, null=True, blank=True, on_delete=models.SET_NULL)
    selected_year_register_event = models.IntegerField(null=True, blank=True)

    #--------------------------------------------------------------------------------------------------------------------------
    # 필터링용 미니 칼랜더 날짜
    date_selected_workingtime = models.DateField(null=True)  # 미니칼렌다에서 선택된 검색하려는 출퇴근 날짜
    date_selected_workingtime_control = models.DateField(null=True)  # 검색하려는 Workingtime Control 회계년도/회계년월, day == 1

    ###################################################################################################################################################
    # Document 관리
    ###################################################################################################################################################
    document_issued = models.ForeignKey(HR_Document_Issued, on_delete=models.SET_NULL, null=True, blank=True)
    document_format = models.ForeignKey(HR_Document_Format, related_name="HR_Document_Format", null=True, blank=True, on_delete=models.SET_NULL)
    document_control_type = models.CharField(max_length=50, choices=LIST_HR_DOCUMENT_CONTROL_TYPE, default=LIST_HR_DOCUMENT_CONTROL_TYPE[0][0], blank=True)
    check_display_size_document_format_table_fullwidth = models.BooleanField(default=False) # 문서포맷 관리페이지 Full width 보기
    check_activate_document_format_register_modal_view = models.BooleanField(default=False) # 문서포맷 등록 모달창으로 띄우기
    # 문서승인 모달창 키값
    hrapproval = models.ForeignKey(HR_Document_Approval_Management, related_name="HR_Document_Approval", null=True, blank=True, on_delete=models.SET_NULL)
    hrapproval_ref = models.ForeignKey(HR_Document_Approval_Management, related_name="HR_Document_Approval_for_Reference", null=True, blank=True, on_delete=models.SET_NULL)
    #--------------------------------------------------------------------------------------------------------------------------
    # Modal창 임시정보 캐쉬역할
    #--------------------------------------------------------------------------------------------------------------------------
    document_format_title = models.CharField(max_length=250, null=True, blank=True) # 문서 정보 타이틀 임시저장
    document_format_description = models.TextField(null=True, blank=True) # 문서 정보 타이틀 임시저장
    #--------------------------------------------------------------------------------------------------------------------------
    status_dam_modal_view_search_member = models.CharField(max_length=50, choices=STATUS_HR_DAM_MODAL_VIEW_SEARCH_MEMBER, default=STATUS_HR_DAM_MODAL_VIEW_SEARCH_MEMBER[0][0], blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    list_dict_document_approver = models.JSONField(null=True, blank=True)  # 추가한 승인권자 [ {name, position, email, hrlayout_id}, ... ] 임시저장
    list_dict_document_takeover = models.JSONField(null=True, blank=True)  # 추가한 업무인수자 임시저장
    list_dict_document_referrer = models.JSONField(null=True, blank=True)  # 추가한 참조자 임시저장
    list_dict_document_receiver = models.JSONField(null=True, blank=True)  # 추가한 수신처 임시저장
    list_dict_document_approver_searched = models.JSONField(null=True, blank=True)  # 검색된 승인권자 [ {name, position, email, hrlayout_id}, ... ] 임시저장
    list_dict_document_takeover_searched = models.JSONField(null=True, blank=True)  # 검색된 업무인수자 임시저장
    list_dict_document_referrer_searched = models.JSONField(null=True, blank=True)  # 검색된 참조자 임시저장
    list_dict_document_receiver_searched = models.JSONField(null=True, blank=True)  # 검색된 수신처 임시저장
    list_dict_document_approver_recommended = models.JSONField(null=True, blank=True)  # 추천된 승인권자 [ {name, position, email, hrlayout_id}, ... ] 임시저장
    list_dict_document_takeover_recommended = models.JSONField(null=True, blank=True)  # 추천된 업무인수자 임시저장
    list_dict_document_referrer_recommended = models.JSONField(null=True, blank=True)  # 추천된 참조자 임시저장
    list_dict_document_receiver_recommended = models.JSONField(null=True, blank=True)  # 추천된 수신처 임시저장
    #--------------------------------------------------------------------------------------------------------------------------
    # 승인문서 관리
    #--------------------------------------------------------------------------------------------------------------------------
    list_document_issued_id_searched = models.JSONField(null=True, blank=True)  # 검색된 승인된문서 ID 리스트
    list_document_issued_id_selected = models.JSONField(null=True, blank=True)  # 선택된 승인된문서 ID 리스트
    #--------------------------------------------------------------------------------------------------------------------------
    # 모달 관리
    #--------------------------------------------------------------------------------------------------------------------------
    check_activate_xxx_document_plan_readonly_info_modal_view = models.BooleanField(default=False) # True: 모달 발행 문서 읽기전용 띄우기
    check_activate_xxx_document_communication_modal_view = models.BooleanField(default=False) # True: 모달 문서 수정요청 대응 모달창 띄우기

    ###################################################################################################################################################
    # Workingtime
    ###################################################################################################################################################
    # F.Keys
    workingtime_control = models.ForeignKey(Workingtime_Control, on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 workingtime Control 쿼리
    workingtime_issued = models.ForeignKey(Workingtime_Issued, on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 workingtime Issued 쿼리
    workingtime_plan = models.ForeignKey(Workingtime_Plan, on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 workingtime Plan 쿼리
    vacation_plan_wkt = models.ForeignKey(Vacation_Plan, related_name="HR_Vacation_Plan_selected_at_WKT", on_delete=models.SET_NULL, null=True, blank=True)  # WorkingTime(출퇴근항목)에서 선택된 Vacation Plan 쿼리
    # Display Conditions
    workingtime_control_type = models.CharField(max_length=50, choices=LIST_HR_WORKINGTIME_CONTROL_TYPE, default=LIST_HR_WORKINGTIME_CONTROL_TYPE[0][0], blank=True)
    check_display_size_workingtime_today_table_fullwidth = models.BooleanField(default=False)
    check_display_size_workingtime_analytics_table_fullwidth = models.BooleanField(default=False)
    check_display_size_workingtime_plan_table_fullwidth = models.BooleanField(default=False)
    #--------------------------------------------------------------------------------------------------------------------------
    # Modal창 관련 (Workingtime Issued)
    #--------------------------------------------------------------------------------------------------------------------------
    # Workingtime Modal창 열기/닫기
    check_activate_modal_view_for_member_wkt_issued_monthly = models.BooleanField(default=False)  # True: 선택멤버의 한달치 발행출퇴근쿼리 정보 모달창 열기
    check_activate_wkt_issued_unchecked_member_list_modal_view = models.BooleanField(default=False) # 미출근자 리스트 모달창으로 띄우기
    check_activate_wkt_issued_unchecked_member_except_modal_view = models.BooleanField(default=False) # 미출근 체크 리스트 제외자 리스트 모달창으로 띄우기
    check_activate_modal_view_for_vacation_plan = models.BooleanField(default=False)  # True: 모달창으로 선택한 Vacation Plan 내용 표시
    check_activate_wkt_personalized_member_list_modal_view = models.BooleanField(default=False)  # True: 모달창으로 개인별 맞춤형 출퇴근 시간 관리
    #--------------------------------------------------------------------------------------------------------------------------
    # Searching & Filtering & Sorting
    #--------------------------------------------------------------------------------------------------------------------------
    list_wkt_control_id_searched = models.JSONField(null=True, blank=True)  # 검색된 Workingtime Profile ID 리스트
    list_wkt_control_id_selected = models.JSONField(null=True, blank=True)  # 선택된 Workingtime Profile ID 리스트
    list_workingtime_issued_id_searched = models.JSONField(null=True, blank=True)  # 검색된 Workingtime Profile ID 리스트
    list_workingtime_issued_id_selected = models.JSONField(null=True, blank=True)  # 선택된 Workingtime Profile ID 리스트
    list_workingtime_issued_id_activated_modification = models.JSONField(null=True, blank=True)  # 수정창 활성화
    list_dict_excepter_searched = models.JSONField(null=True, blank=True)  # 검색된 미출근 체크 리스트 제외자 리스트
    # 조건값으로 필터링하기
    status_working_day_workingtime = models.CharField(verbose_name="근무일상태", max_length=100, choices=STATUS_WORKING_DAY, blank=True, null=True)
    status_wkt_start_workingtime = models.CharField(verbose_name="출근상태", max_length=100, choices=STATUS_WORKING_TIME_START, blank=True, null=True)
    status_wkt_end_workingtime = models.CharField(verbose_name="퇴근상태", max_length=100, choices=STATUS_WORKING_TIME_END, blank=True, null=True)
    # 정렬하기
    selected_field_name_for_wkt_today_sorting = models.CharField(max_length=200, choices=LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_TODAY, default=LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_TODAY[0][0], blank=True, null=True)
    check_selected_field_descend_for_wkt_today_sorting = models.BooleanField(default=False) # True: 내림차순
    #--------------------------------------------------------------------------------------------------------------------------
    # Workingtime Analytics
    #--------------------------------------------------------------------------------------------------------------------------
    # Modal창 관련
    check_activate_workingtime_control_analytics_graph_modal_view = models.BooleanField(default=False)
    status_activate_wkt_analytics_graph_modal = models.CharField(max_length=100, choices=LIST_WORKING_TIME_ANALYTICS_GRAPH_CHART, default=LIST_WORKING_TIME_ANALYTICS_GRAPH_CHART[0][0])
    # 입력날짜
    date_wkt_analytics_start = models.DateField(null=True, blank=True)
    date_wkt_analytics_end = models.DateField(null=True, blank=True)
    # Analytics
    selected_field_name_for_wkt_analytics_type = models.CharField(max_length=200, choices=LIST_HR_WORKING_TIME_TABLE_COLUMN_INDEX_TYPE, default=LIST_HR_WORKING_TIME_TABLE_COLUMN_INDEX_TYPE[0][0], blank=True, null=True)
    list_selected_field_name_for_wkt_analytics_type = models.JSONField(null=True, blank=True)
    selected_field_name_for_wkt_analytics_sorting = models.CharField(max_length=200, choices=LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_ANALYTICS, default=LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_ANALYTICS[0][0], blank=True, null=True)
    check_selected_field_name_for_wkt_analytics_sorting_descend = models.BooleanField(default=False) # True: 내림차순
    selected_company_name_for_wkt = models.CharField(max_length=200, blank=True, null=True)
    selected_division_name_for_wkt = models.CharField(max_length=200, blank=True, null=True)
    selected_team_name_for_wkt = models.CharField(max_length=200, blank=True, null=True)

    check_activate_analytics_table_graph = models.BooleanField(default=False) # True: 그래프표시 활성화(화면전환)
    list_dict_wkt_control_analytics_graph = models.JSONField(null=True, blank=True) # 월별 멤버 출퇴근 분석 그래프 표시 List Dictionary
    list_net_workingtime_business_all = models.JSONField(null=True, blank=True) # 월별 멤버 출퇴근 평일순근무시간 리스트
    list_avg_checkin_business_all = models.JSONField(null=True, blank=True) # 월별 멤버 출퇴근 평일출근시간 리스트
    list_avg_checkout_business_all = models.JSONField(null=True, blank=True) # 월별 멤버 출퇴근 평일퇴근시간 리스트
    #--------------------------------------------------------------------------------------------------------------------------
    # Workingtime Plan
    #--------------------------------------------------------------------------------------------------------------------------
    # 조건값으로 필터링하기
    type_workingtime = models.CharField(verbose_name="근무계획서종류", max_length=100, choices=LIST_TYPE_WORKINGTIME, blank=True, null=True)
    type_workingtime_field = models.CharField(verbose_name="출장형태", max_length=100, choices=LIST_TYPE_WORKINGTIME_FIELD, blank=True, null=True)
    # Workingtime Plan Control
    selected_field_name_for_wkt_plan_sorting = models.CharField(max_length=200, choices=LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_PLAN, default=LIST_WORKING_TIME_TABLE_COLUMN_INDEX_FOR_PLAN[0][0], blank=True, null=True)
    list_workingtime_plan_id_searched = models.JSONField(null=True, blank=True)  # 검색된 Workingtime Plan ID 리스트
    list_workingtime_plan_id_selected = models.JSONField(null=True, blank=True)  # 선택된 Workingtime Plan ID 리스트
    # Wkt Plan Communication w/ HR
    check_activate_modify_view_for_workingtime_plan = models.BooleanField(default=False)  # True: 근무계획서 수정하기 위한 창 표시

    ###################################################################################################################################################
    # Vacation
    ###################################################################################################################################################
    #--------------------------------------------------------------------------------------------------------------------------
    # Vacation Control
    #--------------------------------------------------------------------------------------------------------------------------
    year_vc_issued_selected = models.IntegerField(null=True, blank=True) # 휴가관리를 위해 선택한 휴가 발행 년도
    vacation_control = models.ForeignKey(Vacation_Control, related_name="selected_by_member", on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 Vacation Control 쿼리
    vacation_control_type = models.CharField(max_length=50, choices=LIST_HR_VACATION_CONTROL_TYPE, default=LIST_HR_VACATION_CONTROL_TYPE[0][0], blank=True)
    vacation_issued = models.ForeignKey(Vacation_Issued, on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 Vacation Control 쿼리
    vacation_control_issued_submenu_type = models.CharField(max_length=50, choices=LIST_HR_VACATION_CONTROL_ISSUED_SUBMENU_TYPE, default=LIST_HR_VACATION_CONTROL_ISSUED_SUBMENU_TYPE[0][0], blank=True)
    check_activate_detail_vacation_control_view = models.BooleanField(default=False)  # 멤버별 디테일 휴가관리창 활성화
    check_activate_detail_vacation_issued_modification_view = models.BooleanField(default=False)  # 멤버별 디테일 휴가발행 수정하기 창 활성화
    check_activate_detail_vacation_issued_revival_view = models.BooleanField(default=False)  # 멤버별 디테일 휴가발행 되살리기 창 활성화
    check_activate_detail_vacation_plan_view = models.BooleanField(default=False)  # 멤버별 디테일 휴가계획창 활성화
    check_activate_form_date_joined = models.BooleanField(default=False)  # 입사일 입력 폼 활성화
    check_plan_detail_display_activated = models.BooleanField(default=False) # True: 휴가계획서 자세한 내용 표시 Fold / Unfold
    list_vacation_control_id_searched = models.JSONField(null=True, blank=True)  # 검색된 Vacation Control 쿼리 ID 리스트
    list_vacation_control_id_selected = models.JSONField(null=True, blank=True)  # 선택된 Vacation Control 쿼리 ID 리스트
    # 멤버 검색 결과 관리
    list_searched_vc_receiver_hrlayout_id = models.JSONField(null=True, blank=True) # 휴가 수신처 추가를 위한 검색된 hrlayout id 리스트
    #--------------------------------------------------------------------------------------------------------------------------
    # Vacation Plan (발행된 휴가계획서 관리)
    #--------------------------------------------------------------------------------------------------------------------------
    vacation_plan = models.ForeignKey(Vacation_Plan, related_name="HR_Vacation_Plan", on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 Vacation Plan 쿼리
    list_vacation_plan_id_searched = models.JSONField(null=True, blank=True)  # 검색된 Vacation Plan 쿼리 ID 리스트
    list_vacation_plan_id_membername = models.JSONField(null=True, blank=True)  # 멤버_이름으로 선택된 멤버의 모든 Vacation Plan 쿼리 ID 리스트
    list_vacation_plan_id_selected = models.JSONField(null=True, blank=True)  # 선택된 Vacation Plan 쿼리 ID 리스트
    list_document_issued_id_searched_for_vacation = models.JSONField(null=True, blank=True)  # 검색된 My Document Issued ID 리스트
    list_document_issued_id_selected_for_vacation = models.JSONField(null=True, blank=True)  # 선택된 My Document Issued ID 리스트
    vacation_control_plan_submenu_type = models.CharField(max_length=50, choices=LIST_HR_VACATION_CONTROL_PLAN_SUBMENU_TYPE, default=LIST_HR_VACATION_CONTROL_PLAN_SUBMENU_TYPE[0][0], blank=True)
    vacation_control_plan_display_type = models.CharField(max_length=50, choices=LIST_HR_VACATION_CONTROL_PLAN_DISPLY_TYPE, default=LIST_HR_VACATION_CONTROL_PLAN_SUBMENU_TYPE[0][0], blank=True)
    check_search_only_last_workingyear = models.BooleanField(default=True)  # True: 휴가계획서 검색시 현재년차만 결과에 포함시킴
    check_vacation_type = models.CharField(verbose_name="휴가종류", choices=LIST_VACATION_TYPES, max_length=200, null=True, blank=True)
    check_vacation_regular_type = models.CharField(verbose_name="연차사용타입", choices=LIST_VACATION_REGULAR_TYPES, max_length=200, null=True, blank=True)
    check_vc_plan_request_from_hr_communication_panel_show = models.BooleanField(default=False) # True: 인사팀요청에 의한 커뮤니케이션 정정/취소 요청내용 펼치기
    check_vc_plan_request_to_hr_communication_panel_show = models.BooleanField(default=False) # True: 종료된 정정/취소 요청내용 펼치기
    #--------------------------------------------------------------------------------------------------------------------------
    # Vacation Plan Register Manually
    #--------------------------------------------------------------------------------------------------------------------------
    # 휴가계획서 수동등록
    vacation_control_register = models.ForeignKey(Vacation_Control, related_name="HR_Vacation_Control_for_register", on_delete=models.SET_NULL, null=True, blank=True)  # 수동 저장을 위해 임시저정한 Vacation Control 쿼리
    vacation_plan_register = models.ForeignKey(Vacation_Plan, related_name="HR_Vacation_Plan_for_register", on_delete=models.SET_NULL, null=True, blank=True)  # 수동 저장을 위해 임시저정한 Vacation Plan 쿼리
    status_hr_vacation_plan_register_manually = models.CharField(max_length=100, choices=STATUS_HR_VACATION_PLAN_REGISTER_MANUALLY, default=STATUS_HR_VACATION_PLAN_REGISTER_MANUALLY[0][0], blank=True)
    # Step 1 작성자 정보 임시저장
    hrlayout_applicant = models.ForeignKey(HR_Layout, related_name="vacation_plan_register_applicant", null=True, blank=True, on_delete=models.SET_NULL) # 휴가 신청자 조직도정보
    list_searched_vc_plan_owner_hrlayout_id = models.JSONField(null=True, blank=True)
    # Step 2 결재자 정보 임시저장
    hrlayout_approver_1 = models.ForeignKey(HR_Layout, related_name="vacation_plan_register_approver_1", null=True, blank=True, on_delete=models.SET_NULL) # 휴가 결재자 정보 1
    hrlayout_approver_2 = models.ForeignKey(HR_Layout, related_name="vacation_plan_register_approver_2", null=True, blank=True, on_delete=models.SET_NULL) # 휴가 결재자 정보 2
    hrlayout_approver_3 = models.ForeignKey(HR_Layout, related_name="vacation_plan_register_approver_3", null=True, blank=True, on_delete=models.SET_NULL) # 휴가 결재자 정보 3

    list_searched_vc_plan_approver_1_hrlayout_id = models.JSONField(null=True, blank=True)
    list_searched_vc_plan_approver_2_hrlayout_id = models.JSONField(null=True, blank=True)
    list_searched_vc_plan_approver_3_hrlayout_id = models.JSONField(null=True, blank=True)
    # Step 3 업무인수자 정보 임시저장
    check_hrlayout_takeover = models.BooleanField(default=False) # True == 업무인수자 선택 혹은 건너뛰기 선택한 경우, 업무인수자 선택한 경우 hrlayout 정보는 vacation_plan에 저장
    list_searched_vc_plan_takeover_hrlayout_id = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    # Vacation Plan Register Manually
    #--------------------------------------------------------------------------------------------------------------------------
    # 휴가계획서 자동등록
    check_vc_plan_file_upload_error_report_view_activate = models.BooleanField(default=False) # True: 자동등록 휴가 에러 표시창 표시
    #--------------------------------------------------------------------------------------------------------------------------
    # 연차사용촉진 관련
    #--------------------------------------------------------------------------------------------------------------------------
    check_display_size_vc_promotion_fullwidth = models.BooleanField(default=False)  # True: 화면 테이블 Full width
    # Sorting Conditions
    status_vacation_promotion_submenu = models.CharField(max_length=100, choices=LIST_VACATION_PROMOTION_SUBMENU, default=LIST_VACATION_PROMOTION_SUBMENU[0][0], blank=True)
    status_vacation_control = models.CharField(max_length=100, choices=STATUS_MY_VACATION_CONTROL, null=True, blank=True)
    status_vc_promotion_ordering_type = models.CharField(max_length=200, choices=LIST_VACATION_PROMOTION_ORDERING_TYPES, null=True, blank=True)
    list_searched_vc_control_id_for_promotion = models.JSONField(null=True, blank=True)  # 검색된 휴가컨트롤 ID
    list_selected_vc_control_id_for_promotion = models.JSONField(null=True, blank=True)  # 선택된 휴가컨트롤 ID
    # 선택된 휴가컨트롤 연차촉진
    vacation_control_promotion = models.ForeignKey(Vacation_Control, related_name="HR_Vacation_Control_for_promotion", on_delete=models.SET_NULL, null=True, blank=True)  # 연차 촉친을 위해 임시저정한 Vacation Control 쿼리
    #--------------------------------------------------------------------------------------------------------------------------
    # Vacation Issued 수정 요청
    #--------------------------------------------------------------------------------------------------------------------------
    check_vc_issued_request_to_hr_communication_panel_show = models.BooleanField(default=False) # True: 발행된 휴가 정정 요청내용 펼치기


    ###################################################################################################################################################
    # Task
    ###################################################################################################################################################
    #--------------------------------------------------------------------------------------------------------------------------
    # Task Control
    #--------------------------------------------------------------------------------------------------------------------------
    task_plan = models.ForeignKey(Task_Plan, related_name="selected_task_plan", on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 Vacation Control 쿼리
    task_analysis_project = models.ForeignKey(Task_Analysis_by_Project, related_name="selected_task_analysis_project", on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 Vacation Control 쿼리
    task_control_type = models.CharField(max_length=50, choices=LIST_HR_TASK_CONTROL_TYPE, default=LIST_HR_TASK_CONTROL_TYPE[0][0], blank=True)
    # project_simple = models.ForeignKey(Project_Simple, related_name="selected_project_simple", on_delete=models.SET_NULL, null=True, blank=True)
    status_task_project_control_submenu = models.CharField(max_length=100, choices=LIST_TASK_PROJECT_CONTROL_SUBMENU, default=LIST_TASK_PROJECT_CONTROL_SUBMENU[0][0], blank=True)
    status_task_project_participant_submenu = models.CharField(max_length=50, choices=LIST_TASK_PROJECT_PARTICIPANT_SUBMENU, default=LIST_TASK_PROJECT_PARTICIPANT_SUBMENU[0][0], blank=True)
    # Table 정렬
    selected_field_name_for_task_plan_sorting = models.CharField(max_length=200, choices=LIST_TASK_PLAN_TABLE_COLUMN_INDEX, default=LIST_TASK_PLAN_TABLE_COLUMN_INDEX[0][0], blank=True, null=True)
    check_selected_field_name_for_task_plan_sorting_inverse = models.BooleanField(default=False)  # 역순으로 정렬
    list_searched_task_plan_id = models.JSONField(null=True, blank=True)  # 검색된 업무관리 쿼리 id
    list_selected_task_plan_id = models.JSONField(null=True, blank=True)  # 선택된 업무관리 쿼리 id
    check_display_size_task_table_fullwidth = models.BooleanField(default=False)  # True: 화면 Full width
    check_activate_task_plan_modify_view = models.BooleanField(default=False)  # True: 선택된 task_plan 쿼리 수정을 위한 화면 활성화
    check_activate_task_plan_analytics_view = models.BooleanField(default=False) # True : 선택된 Task Plan 분석화면 표시
    check_activate_task_plan_delete_view = models.BooleanField(default=False)  # True: 선택된 task_plan 쿼리 삭제를 위한 화면 활성화
    # Project 분석 기간
    date_project_analysis_start = models.DateField(null=True)
    date_project_analysis_end = models.DateField(null=True)
    # Project 기준 분석
    check_activate_task_plan_analysis_modal_view = models.BooleanField(default=False)  # True: 프로젝트 참여비율 분석모달창 활성화
    list_project_analysis_pie_chart_selected_project_data = models.JSONField(null=True, blank=True)
    list_project_analysis_pie_chart_selected_project_data_by_team = models.JSONField(null=True, blank=True)
    # 팀 기준 분석
    team = models.ForeignKey(Team, related_name="selected_team", on_delete=models.SET_NULL, null=True, blank=True)  # 선택된 Team 쿼리
    list_dict_involved_team_id_name = models.JSONField(null=True, blank=True) # 선택된 기한 내에 프로젝트에 참여한 팀 ID 이름 리스트 [{'id': 1, 'name': '수리응용팀'}, {'id': 2, 'name': '플랫폼개발팀'}, ...]
    list_selected_team_member_id = models.JSONField(null=True, blank=True) # 선택된 팀에 소속된 Member ID
    check_activate_task_plan_analysis_by_team_modal_view = models.BooleanField(default=False)  # True: 프로젝트 팀별 참여비율 분석모달창 활성화
    list_project_analysis_pie_chart_selected_team_data = models.JSONField(null=True, blank=True)
    # 멤버 기준 분석
    list_project_analysis_pie_chart_selected_member_data = models.JSONField(null=True, blank=True)
    #--------------------------------------------------------------------------------------------------------------------------
    ###################################################################################################################################################
    # HR Layout
    ###################################################################################################################################################
    status_member_register_type = models.CharField(max_length=50, choices=LIST_HR_MEMBER_REGISTER_TYPE, default=LIST_HR_MEMBER_REGISTER_TYPE[0][0], blank=True)
    check_display_size_member_control_table_fullwidth = models.BooleanField(default=False) # True : 멤버관리 창 Full width
    #--------------------------------------------------------------------------------------------------------------------------

    def __str__(self):
        if self.owner is not None:
            if self.owner.member is not None:
                if self.owner.member.member_name is not None:
                    return str(self.owner.member.member_name)
                else:
                    return str(self.id)
            else:
                return str(self.id)
        else:
            return str(self.id)






