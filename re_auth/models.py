from django.db import models
import json


class ReAuthorityHistory(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False)

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
    # Crystal
    auth_crystal = models.JSONField(null=True, blank=True)
    auth_crystal_register = models.JSONField(null=True, blank=True)
    auth_crystal_validation = models.JSONField(null=True, blank=True)
    auth_crystal_design = models.JSONField(null=True, blank=True)
    # Dashboard PK
    auth_dashboardpk = models.JSONField(null=True, blank=True)
    auth_dashboardpk_register = models.JSONField(null=True, blank=True)
    auth_dashboardpk_validation = models.JSONField(null=True, blank=True)
    auth_dashboardpk_design = models.JSONField(null=True, blank=True)

    # Dashboard
    auth_dashboard = models.JSONField(null=True, blank=True)
    auth_dashboard_register = models.JSONField(null=True, blank=True)
    auth_dashboard_validation = models.JSONField(null=True, blank=True)
    auth_dashboard_design = models.JSONField(null=True, blank=True)

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

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)

    class Meta:
        managed = True
        db_table = 're_authority_history'
