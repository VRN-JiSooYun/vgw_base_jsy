from django.db import models

class ReMember(models.Model) :
    id = models.AutoField(db_column='id', primary_key=True)

    # 회원 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 사용자 아이디
    user_id = models.IntegerField(db_column='user_id', blank=False, null=False, default=0)
    # 사번
    member_company_id = models.CharField(db_column='member_company_id', max_length=5, blank=False, null=False)
    # 성명
    member_name = models.CharField(db_column='member_name', max_length=100, blank=True, null=True)
    # 생년월일
    member_birthday = models.CharField(db_column='member_birthday', max_length=10, blank=True, null=True)
    # 이메일
    member_email = models.CharField(db_column='member_email', max_length=128, blank=True, null=True)
    # 핸드폰번호
    member_hp = models.CharField(db_column='member_hp', max_length=16, blank=True, null=True)
    # 입사일
    join_date = models.DateTimeField(db_column='join_date', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 퇴사일
    leave_date = models.DateTimeField(db_column='leave_date', blank=True, null=True)
    # 회원 사진
    member_image = models.CharField(db_column='member_image', max_length=20, blank=True, null=True)

    # 역활
    member_role = models.CharField(db_column='member_role', max_length=6, blank=True, null=True)
    # 근로구분
    member_type = models.CharField(db_column='member_type', max_length=6, blank=True, null=True)
    # 구분
    working_type = models.CharField(db_column='working_type', max_length=6, blank=True, null=True)
    # 부문 세부
    working_type_detail = models.CharField(db_column='working_type_detail', max_length=6, blank=True, null=True)
    # 연구소
    lab = models.CharField(db_column='lab', max_length=6, blank=True, null=True)
    # 근무지
    working_place = models.CharField(db_column='working_place', max_length=6, blank=True, null=True)

    # 영문명
    member_eng_name = models.CharField(db_column='member_eng_name', max_length=20, null=True, blank=True)
    # 한자
    member_chinese_name = models.CharField(db_column='member_chinese_name', max_length=10, null=True, blank=True)
    # 주민번호
    member_social_id = models.CharField(db_column='member_social_id', max_length=14, blank=True, null=True)
    # 주소
    member_addr = models.CharField(db_column='member_addr', max_length=256, blank=True, null=True)
    # 비상연락처
    member_hp_er = models.CharField(db_column='member_hp_er', max_length=16, blank=True, null=True)
    # 비상연락처명
    member_hp_er_name = models.CharField(db_column='member_hp_er_name', max_length=20, blank=True, null=True)
    # 계죄번호
    member_bank = models.CharField(db_column='member_bank', max_length=20, blank=True, null=True)
    # 계죄번호
    member_bank_num = models.CharField(db_column='member_bank_num', max_length=20, blank=True, null=True)

    # 전역구분
    military_discharge_type = models.CharField(db_column='military_discharge_type', max_length=6, blank=True, null=True)
    # 특례구분
    military_etc_type = models.CharField(db_column='military_etc_type', max_length=6, blank=True, null=True)
    # 군별
    military_type = models.CharField(db_column='military_type', max_length=6, blank=True, null=True)
    # 전역계급
    military_discharge_rank = models.CharField(db_column='military_discharge_rank', max_length=6, blank=True, null=True)
    # 병과
    military_skill = models.CharField(db_column='military_skill', max_length=256, blank=True, null=True)
    # 복무 시작일
    military_start_date = models.CharField(db_column='military_start_date', max_length=10, blank=True, null=True)
    # 복무 종료일
    military_end_date = models.CharField(db_column='military_end_date', max_length=10, blank=True, null=True)
    # 군번
    military_num = models.CharField(db_column='military_num', max_length=16, blank=True, null=True)
    # 미필사유
    military_memo = models.CharField(db_column='military_memo', max_length=16, blank=True, null=True)

    # 국가연구자번호
    researcher_num = models.CharField(db_column='researcher_num', max_length=8, blank=True, null=True)
    # 보훈대상자
    ministry_patriots  = models.CharField(db_column='ministry_patriots', max_length=6, blank=True, null=True)
    # 장애등급
    disabled_level = models.CharField(db_column='disabled_level', max_length=16, blank=True, null=True)
    # 장애종류
    disabled_type = models.CharField(db_column='disabled_type', max_length=16, blank=True, null=True)

    # 비고
    memo = models.CharField(db_column='memo', max_length=256, blank=True, null=True)

    # 연차 누적 일수
    working_off_acc_days = models.FloatField(db_column='working_off_acc_days', blank=False, null=False, default=0.0)
    # 연차 누적 사용일수
    working_off_acc_use_days = models.FloatField(db_column='working_off_acc_use_days', blank=False, null=False, default=0.0)
    # 연차 누적 잔여일수
    working_off_acc_remain_days = models.FloatField(db_column='working_off_acc_remain_days', blank=False, null=False, default=0.0)

    # 연차 일수
    working_off_days = models.FloatField(db_column='working_off_days', blank=False, null=False, default=0.0)
    # 연차 사용일수
    working_off_use_days = models.FloatField(db_column='working_off_use_days', blank=False, null=False, default=0.0)
    # 연차 잔여일수
    working_off_remain_days = models.FloatField(db_column='working_off_remain_days', blank=False, null=False, default=0.0)
    # 연차 시작일
    working_off_start_date = models.CharField(db_column='working_off_start_date', max_length=10, blank=True, null=False)

    # 연차 추가 일수
    working_off_etc_days = models.FloatField(db_column='working_off_etc_days', blank=False, null=False, default=0.0)

    # 대체 휴가 일수
    working_off_add_days = models.FloatField(db_column='working_off_add_days', blank=False, null=False, default=0.0)
    # 대체 휴가 사용일수
    working_off_add_use_days = models.FloatField(db_column='working_off_add_use_days', blank=False, null=False, default=0.0)
    # 대체 휴가 잔여일수
    working_off_add_remain_days = models.FloatField(db_column='working_off_add_remain_days', blank=False, null=False, default=0.0)

    # 근무 check 여부
    check_working = models.BooleanField(db_column='check_working', default=True)

    # 연차 촉진 check 여부
    check_working_off_promote = models.BooleanField(db_column='check_working_off_promote', default=True)

    # 삭제 여부
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_member'

class ReMemberCompany(models.Model) :
    re_member = models.ForeignKey(ReMember, on_delete=models.CASCADE)
    # 회사명
    company_name = models.CharField(db_column='company_name', max_length=20, blank=True, null=True)
    # 근무 시작일
    working_start_date = models.CharField(db_column='working_start_date', max_length=10, blank=True, null=True)
    # 근무 종료일
    working_end_date = models.CharField(db_column='working_end_date', max_length=10, blank=True, null=True)
    # 담당부서
    division = models.CharField(db_column='division', max_length=20, blank=True, null=True)
    # 직급
    position = models.CharField(db_column='position', max_length=20, blank=True, null=True)
    # 담당업무
    job = models.CharField(db_column='job', max_length=20, blank=True, null=True)
    # 연봉
    annual_income = models.CharField(db_column='annual_income', max_length=20, blank=True, null=True)
    # 퇴사 사유
    resign_memo = models.CharField(db_column='resign_memo', max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 're_member_company'

class ReMemberCollege(models.Model) :
    re_member = models.ForeignKey(ReMember, on_delete=models.CASCADE)
    # 학교구분
    college_type = models.CharField(db_column='college_type', max_length=6, blank=True, null=True)
    # 학교명
    college_name = models.CharField(db_column='college_name', max_length=20, blank=True, null=True)
    # 학교 재학 시작일
    college_start_date = models.CharField(db_column='college_start_date', max_length=10, blank=True, null=True)
    # 학교 재학 종료일
    college_end_date = models.CharField(db_column='college_end_date', max_length=10, blank=True, null=True)
    # 학교 재학 상태
    college_status = models.CharField(db_column='college_status', max_length=6, blank=True, null=True)
    # 전공
    college_major = models.CharField(db_column='college_major', max_length=20, blank=True, null=True)
    # 학위번호
    college_degree_num = models.CharField(db_column='college_degree_num', max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 're_member_college'

class ReMemberCertificate(models.Model) :
    re_member = models.ForeignKey(ReMember, on_delete=models.CASCADE)
    # 자격증명
    certificate_name = models.CharField(db_column='certificate_name', max_length=20, blank=True, null=True)
    # 취득일
    certificate_date = models.CharField(db_column='certificate_date', max_length=10, blank=True, null=True)
    # 발행처
    certificate_issuer = models.CharField(db_column='certificate_issuer', max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 're_member_certificate'


class ReMemberForeignLang(models.Model) :
    re_member = models.ForeignKey(ReMember, on_delete=models.CASCADE)
    # 외국어명
    foreign_lang_name = models.CharField(db_column='foreign_lang_name', max_length=20, blank=True, null=True)
    # 외국어시험
    foreign_lang_exam = models.CharField(db_column='foreign_lang_exam', max_length=20, blank=True, null=True)
    # 공인점수
    foreign_lang_exam_level = models.CharField(db_column='foreign_lang_exam_level', max_length=20, blank=True, null=True)
    # 취득일
    foreign_lang_date = models.CharField(db_column='foreign_lang_date', max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 're_member_foreign_lang'

class ReMemberFamily(models.Model) :
    re_member = models.ForeignKey(ReMember, on_delete=models.CASCADE)
    # 관계
    relationship = models.CharField(db_column='relationship', max_length=6, blank=True, null=True)
    # 성명
    name = models.CharField(db_column='name', max_length=20, blank=True, null=True)
    # 생녕월일
    birthday = models.CharField(db_column='birthday', max_length=10, blank=True, null=True)
    # 동거여부
    is_live = models.CharField(db_column='is_live', max_length=1, blank=True, null=True)
    # 거주지
    addr = models.CharField(db_column='addr', max_length=256, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 're_member_family'

