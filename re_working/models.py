from django.db import models

# 근무
class ReWorking(models.Model) :
    # 근무 아이디
    working_id = models.AutoField(db_column='working_id', primary_key=True)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 근무일
    working_date = models.CharField(db_column='working_date', max_length=10, blank=False, null=False)
    # 근무 시작 시간
    working_start_datetime = models.DateTimeField(db_column='working_start_datetime', blank=False, null=False)
    # 근무 종료 시간
    working_end_datetime = models.DateTimeField(db_column='working_end_datetime', blank=False, null=False)
    # 근무 시작 체크 시간
    working_start_check_datetime = models.DateTimeField(db_column='working_start_check_datetime', blank=True, null=True)
    # 근무 종료 체크 시간
    working_end_check_datetime = models.DateTimeField(db_column='working_end_check_datetime', blank=True, null=True)
    # 근무 시작 변경 시간
    working_start_change_datetime = models.DateTimeField(db_column='working_start_change_datetime', blank=True, null=True)
    # 근무 종료 변경 시간
    working_end_change_datetime = models.DateTimeField(db_column='working_end_change_datetime', blank=True, null=True)
    # 사유
    working_time_change_reason = models.CharField(db_column='working_time_change_reason', max_length=1000, blank=True, null=False)
    # 근무 시간 변경 여부
    is_working_time_change = models.CharField(db_column='is_working_time_change', max_length=1, blank=True, null=False, default="N")
    # 실 근무 시작 시간
    working_start_check_ori_datetime = models.DateTimeField(db_column='working_start_check_ori_datetime', blank=True, null=True)
    # 실 근무 종료 시간
    working_end_check_ori_datetime = models.DateTimeField(db_column='working_end_check_ori_datetime', blank=True, null=True)


    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working'


# 외부 근무
class ReWorkingOut(models.Model) :
    # 외부 근무 아이디
    working_out_id = models.AutoField(db_column='working_out_id', primary_key=True)
    # 외부 근무 양식 아이디
    working_out_form_id = models.IntegerField(db_column='working_out_form_id', blank=False, null=False, default=0)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 외부 근무 타입
    working_out_type = models.CharField(db_column='working_out_type', max_length=6, blank=False, null=False)
    # 외부 근무일
    working_out_date = models.CharField(db_column='working_out_date', max_length=10, blank=True, null=False)

    # 삭제 여부
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_out'

# 외부 근무 양식
class ReWorkingOutForm(models.Model) :
    # 외부 근무 아이디
    working_out_form_id = models.AutoField(db_column='working_out_form_id', primary_key=True)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 외부 근무 타입
    working_out_form_type = models.CharField(db_column='working_out_form_type', max_length=6, blank=False, null=False)
    # 외부 근무 시작일
    working_out_form_start_date = models.CharField(db_column='working_out_form_start_date', max_length=10, blank=True, null=False)
    # 외부 근무 종료일
    working_out_form_end_date = models.CharField(db_column='working_out_form_end_date', max_length=10, blank=True, null=False)

    # 삭제 여부
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_out_form'

# 휴가
class ReWorkingOff(models.Model) :
    # 휴가 아이디
    working_off_id = models.AutoField(db_column='working_off_id', primary_key=True)
    # 휴가 양식 아이디
    working_off_form_id = models.IntegerField(db_column='working_off_form_id', blank=False, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 휴가 타입
    working_off_type = models.CharField(db_column='working_off_type', max_length=6, blank=False, null=False)
    # 휴가 시간
    working_off_time = models.CharField(db_column='working_off_time', max_length=6, blank=False, null=False)
    # 휴가 상태
    working_off_state = models.CharField(db_column='working_off_state', max_length=6, blank=False, null=False)
    # 휴가일
    working_off_date = models.CharField(db_column='working_off_date', max_length=10, blank=True, null=True)
    # 휴가 시작 시간
    working_off_start_datetime = models.DateTimeField(db_column='working_off_start_datetime', blank=True, null=True)
    # 휴가 종료 시간
    working_off_end_datetime = models.DateTimeField(db_column='working_off_end_datetime', blank=True, null=True)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_off'

# 휴가 양식
class ReWorkingOffForm(models.Model) :
    # 휴가 아이디
    working_off_form_id = models.AutoField(db_column='working_off_form_id', primary_key=True)
    # 양식 제목
    working_off_form_title = models.CharField(db_column='working_off_form_title', max_length=100, blank=True, null=False)
    # 결재 아이디
    approval_id =  models.CharField(db_column='approval_id', max_length=17, blank=False, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 휴가 양식 타입
    working_off_form_type = models.CharField(db_column='working_off_form_type', max_length=6, blank=False, null=False)
    # 휴가 양식 상태
    working_off_form_state = models.CharField(db_column='working_off_form_state', max_length=6, blank=False, null=False)
    # 휴가 양식 작성일
    working_off_form_datetime = models.DateTimeField(db_column='working_off_form_datetime', blank=True, null=True, auto_now_add=True)
    # 휴가 시작일
    working_off_form_start_date = models.CharField(db_column='working_off_form_start_date', max_length=10, blank=True, null=False)
    # 휴가 종료일
    working_off_form_end_date = models.CharField(db_column='working_off_form_end_date', max_length=10, blank=True, null=False)
    # 휴가 사용 수
    working_off_form_use_num = models.FloatField(db_column='working_off_form_use_num', blank=False, null=False, default=0.0)
    # 사유
    reason = models.CharField(db_column='reason', max_length=1000, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_off_form'

# 휴일 근무
class ReWorkingWeekendForm(models.Model) :
    # 휴일근무 아이디
    working_weekend_form_id = models.AutoField(db_column='working_weekend_form_id', primary_key=True)
    # 양식 제목
    working_weekend_form_title = models.CharField(db_column='working_weekend_form_title', max_length=100, blank=True, null=False)
    # 결재 아이디
    approval_id =  models.CharField(db_column='approval_id', max_length=17, blank=False, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 휴일 근무 상태
    working_weekend_form_state = models.CharField(db_column='working_weekend_form_state', max_length=6, blank=False, null=False)
    # 휴일 양식 작성일
    working_weekend_form_datetime = models.DateTimeField(db_column='working_weekend_form_datetime', blank=True, null=True, auto_now_add=True)
    # 휴일 근무 일
    working_weekend_date = models.CharField(db_column='working_weekend_date', max_length=10, blank=True, null=False)
    # 휴일 근무 시작 시간
    working_weekend_start_datetime = models.DateTimeField(db_column='working_weekend_start_datetime', blank=True, null=True)
    # 휴일 근무 종료 시간
    working_weekend_end_datetime = models.DateTimeField(db_column='working_weekend_end_datetime', blank=True, null=True)
    # 휴일 근무 시간
    working_weekend_time = models.CharField(db_column='working_weekend_time', max_length=5, blank=True, null=False)
    # 사유
    reason = models.CharField(db_column='reason', max_length=1000, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_weekend_form'

# 휴일 근무 노트
class ReWorkingWeekendNoteForm(models.Model) :
    # 휴일 근무 노트 아이디
    working_weekend_note_form_id = models.AutoField(db_column='working_weekend_note_form_id', primary_key=True)
    # 양식 제목
    working_weekend_note_form_title = models.CharField(db_column='working_weekend_note_form_title', max_length=100, blank=True, null=False)
    # 결재 아이디
    approval_id =  models.CharField(db_column='approval_id', max_length=17, blank=False, null=False)
    # 휴일근무 참조 결재 아이디
    ref_approval_id = models.CharField(db_column='ref_approval_id', max_length=17, blank=False, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 휴일근무 노트 상태
    working_weekend_note_form_state = models.CharField(db_column='working_weekend_note_form_state', max_length=6, blank=False, null=False)
    # 휴일근무 노트 양식 작성일
    working_weekend_note_form_datetime = models.DateTimeField(db_column='working_weekend_note_form_datetime', blank=True, null=True, auto_now_add=True)
    # 실 휴일 근무일
    working_weekend_date = models.CharField(db_column='working_weekend_date', max_length=10, blank=True, null=False)
    # 실 휴일 근무 시작 시간
    working_weekend_start_datetime = models.DateTimeField(db_column='working_weekend_start_datetime', blank=True, null=True)
    # 실 휴일 근무 종료 시간
    working_weekend_end_datetime = models.DateTimeField(db_column='working_weekend_end_datetime', blank=True, null=True)
    # 휴일 근무 휴게시간
    working_weekend_free_time = models.CharField(db_column='working_weekend_free_time', max_length=5, blank=True, null=False)
    # 프로젝트명
    working_project_name = models.CharField(db_column='working_project_name', max_length=200, blank=True, null=False)
    # 휴일근무 업무내용
    working_note = models.CharField(db_column='working_note', max_length=3000, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_weekend_note_form'


# 결재
class ReApproval(models.Model) :
    # 결재번호
    approval_id = models.CharField(db_column='approval_id', primary_key=True, max_length=17, blank=False, null=False)
    # 결재 타입
    approval_type = models.CharField(db_column='approval_type', max_length=6, blank=True, null=False)
    # 요청자
    req_member_id = models.IntegerField(db_column='req_member_id', blank=False, null=False, default=0)
    # 응답자
    res_member_id = models.IntegerField(db_column='res_member_id', blank=False, null=False, default=0)
    # 순서
    step = models.IntegerField(db_column='step', blank=False, null=False, default=1)
    # 결재 상태
    approval_state = models.CharField(db_column='approval_state', max_length=6, blank=False, null=False)
    # 처리일
    approval_date = models.DateTimeField(db_column='approval_date', blank=True, null=True, auto_now=True, auto_now_add=False)
    # comment
    comment = models.CharField(db_column='comment', max_length=1000, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_approval'

# 결재 히스토리
class ReApprovalHistory(models.Model) :
    # 결재 히스토리 아이디
    approval_history_id = models.AutoField(db_column='approval_history_id', primary_key=True)
    # 결재번호
    approval_id = models.CharField(db_column='approval_id', max_length=17, blank=False, null=False)
    # 결재 타입
    approval_type = models.CharField(db_column='approval_type', max_length=6, blank=True, null=False)
    # 요청자
    req_member_id = models.IntegerField(db_column='req_member_id', blank=False, null=False, default=0)
    # 응답자
    res_member_id = models.IntegerField(db_column='res_member_id', blank=False, null=False, default=0)
    # 순서
    step = models.IntegerField(db_column='step', blank=False, null=False, default=1)
    # 결재 상태
    approval_state = models.CharField(db_column='approval_state', max_length=6, blank=False, null=False)
    # 처리일
    approval_date = models.DateTimeField(db_column='approval_date', blank=True, null=True, auto_now=True, auto_now_add=False)
    # comment
    comment = models.CharField(db_column='comment', max_length=1000, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_approval_history'


# 결재자
class ReApprovalMember(models.Model) :
    # 결재자 아이디
    approval_member_id = models.AutoField(db_column='approval_member_id', primary_key=True)
    # 결재번호
    approval_id =  models.CharField(db_column='approval_id', max_length=17, blank=False, null=False)
    # 결재 타입
    approval_type = models.CharField(db_column='approval_type', max_length=6, blank=True, null=False)
    # 결재자
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 순서
    step = models.IntegerField(db_column='step', blank=False, null=False, default=1)

    class Meta:
        managed = True
        db_table = 're_approval_member'


# 참조/수신자
class ReApprovalEtcMember(models.Model) :
    #  아이디
    approval_etc_member_id = models.AutoField(db_column='approval_etc_member_id', primary_key=True)
    # 참조/수신자 타입
    approval_etc_member_type = models.CharField(db_column='approval_etc_member_type', max_length=6, blank=True, null=False)
    # 결재번호
    approval_id =  models.CharField(db_column='approval_id', max_length=17, blank=False, null=False)
    # 참조/수신자
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)

    class Meta:
        managed = True
        db_table = 're_approval_etc_member'

# 결제 승인 첨부 파일
class ReApprovalUploadFile(models.Model) :
    # 업로드 아이디
    upload_file_id = models.CharField(db_column='upload_file_id', max_length=13, primary_key=True)
    # 결재번호
    approval_id =  models.CharField(db_column='approval_id', max_length=17, blank=False, null=False)
    # 업로드 파일 확장자
    upload_file_ext = models.CharField(db_column='upload_file_ext', max_length=10, blank=False, null=False)
    # 업로드 파일명
    upload_file_name = models.CharField(db_column='upload_file_name',  max_length=100, blank=False, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_approval_upload_file'

# 공휴일
class ReHoliday(models.Model) :
    # 공휴일 아이디
    holiday_id = models.AutoField(db_column='holiday_id', primary_key=True)
    # 공휴일명
    holiday_name = models.CharField(db_column='holiday_name', max_length=100, blank=False, null=False)
    # 공휴일
    holiday_date = models.CharField(db_column='holiday_date', max_length=10, blank=False, null=False)
    # 공휴일 시작 시간
    holiday_start_datetime = models.DateTimeField(db_column='holiday_start_datetime', blank=True, null=True, auto_now=False, auto_now_add=False)
    # 공휴일 종료 시간
    holiday_end_datetime = models.DateTimeField(db_column='holiday_end_datetime', blank=True, null=True, auto_now=False, auto_now_add=False)
    # 공휴일 생성 타입
    holiday_create_type = models.CharField(db_column='holiday_create_type', max_length=6, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_holiday'

# 근무(출퇴근) 시간
class ReWorkingTime(models.Model) :
    # 근무 시간 아이디
    working_time_id = models.AutoField(db_column='working_time_id', primary_key=True)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 월 출퇴근 시간
    working_time_start_time_1 = models.CharField(db_column='working_time_start_time_1', max_length=5, blank=True, null=False)
    working_time_end_time_1 = models.CharField(db_column='working_time_end_time_1', max_length=5, blank=True, null=False)
    # 화 출퇴근 시간
    working_time_start_time_2 = models.CharField(db_column='working_time_start_time_2', max_length=5, blank=True, null=False)
    working_time_end_time_2 = models.CharField(db_column='working_time_end_time_2', max_length=5, blank=True, null=False)
    # 수 출퇴근 시간
    working_time_start_time_3 = models.CharField(db_column='working_time_start_time_3', max_length=5, blank=True, null=False)
    working_time_end_time_3 = models.CharField(db_column='working_time_end_time_3', max_length=5, blank=True, null=False)
    # 목 출퇴근 시간
    working_time_start_time_4 = models.CharField(db_column='working_time_start_time_4', max_length=5, blank=True, null=False)
    working_time_end_time_4 = models.CharField(db_column='working_time_end_time_4', max_length=5, blank=True, null=False)
    # 금 출퇴근 시간
    working_time_start_time_5 = models.CharField(db_column='working_time_start_time_5', max_length=5, blank=True, null=False)
    working_time_end_time_5 = models.CharField(db_column='working_time_end_time_5', max_length=5, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_time'

# 근무 참여율
class ReWorkingPart(models.Model) :
    # 근무 참여 아이디
    working_part_id = models.AutoField(db_column='working_part_id', primary_key=True)
    # 근무 참여 월
    working_part_date = models.CharField(db_column='working_part_date', max_length=7, blank=True, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 프로젝트 별 근무 참여
    working_part_projects = models.CharField(db_column='working_part_projects', max_length=500, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_part'

# 연차 촉진
class ReWorkingOffPromote(models.Model) :
    # 연차촉진 아이디python manage.py showmigrations re_working
    working_off_promote_id = models.AutoField(db_column='working_off_promote_id', primary_key=True)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 연차 사용 시작일
    working_off_start_date = models.CharField(db_column='working_off_start_date', max_length=10, blank=True, null=False)
    # 1차 촉진일
    first_promote_date = models.CharField(db_column='first_promote_date', max_length=10, blank=True, null=False)
    # 1차 촉진 상태
    first_promote_status = models.CharField(db_column='first_promote_status', max_length=6, blank=True, null=False)
    # 1차 촉진 제출일
    first_promote_submit_datetime = models.DateTimeField(db_column='first_promote_submit_datetime', blank=False, null=True)
    # 1차 연차 일수
    first_working_off_days = models.FloatField(db_column='first_working_off_days', blank=False, null=False, default=0.0)
    # 1차 연차 사용일수
    first_working_off_use_days = models.FloatField(db_column='first_working_off_use_days', blank=False, null=False, default=0.0)
    # 1차 연차 잔여일수
    first_working_off_remain_days = models.FloatField(db_column='first_working_off_remain_days', blank=False, null=False, default=0.0)
    # 2차 촉진일
    second_promote_date = models.CharField(db_column='second_promote_date', max_length=10, blank=True, null=False)
    # 2차 촉진 상태
    second_promote_status = models.CharField(db_column='second_promote_status', max_length=6, blank=True, null=False)
    # 2차 촉진 제출일
    second_promote_submit_datetime = models.DateTimeField(db_column='second_promote_submit_datetime', blank=False, null=True)
    # 2차 연차 일수
    second_working_off_days = models.FloatField(db_column='second_working_off_days', blank=False, null=False, default=0.0)
    # 2차 연차 사용일수
    second_working_off_use_days = models.FloatField(db_column='second_working_off_use_days', blank=False, null=False, default=0.0)
    # 2차 연차 잔여일수
    second_working_off_remain_days = models.FloatField(db_column='second_working_off_remain_days', blank=False, null=False, default=0.0)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_off_promote'

# 연차 촉진 사용계획서
class ReWorkingOffPromotePlan(models.Model) :
    # 연차촉진 사용계획서 아이디
    working_off_promote_plan_id = models.AutoField(db_column='working_off_promote_plan_id', primary_key=True)
    # 연차촉진 아이디
    working_off_promote_id = models.IntegerField(db_column='working_off_promote_id', blank=False, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 연차 촉진 횟차
    working_off_promote_num = models.IntegerField(db_column='working_off_promote_num', blank=False, null=False)
    # 연차 시작일
    working_off_start_date = models.CharField(db_column='working_off_start_date', max_length=10, blank=True, null=False)
    # 연차 종료일
    working_off_end_date = models.CharField(db_column='working_off_end_date', max_length=10, blank=True, null=False)
    # 연차 사용 수
    working_off_use_num = models.FloatField(db_column='working_off_use_num', blank=False, null=False, default=0.0)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_off_promote_plan'

# 근무 증명서
class ReWorkingCertificate(models.Model) :
    # 증명서 아이디
    working_certificate_id = models.AutoField(db_column='working_certificate_id', primary_key=True)
    # 문서 ID
    doc_id = models.CharField(db_column='doc_id', max_length=17, blank=True, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 증명서 신청 상태
    working_certificate_status = models.CharField(db_column='working_certificate_status', max_length=6, blank=True, null=False)
    # 공개여부
    is_blind = models.CharField(db_column='is_blind', max_length=1, blank=True, null=False, default='Y')
    # 증명서 종류
    working_certificate_type = models.CharField(db_column='working_certificate_type', max_length=6, blank=True, null=False)
    # 요청 기간
    working_certificate_date = models.CharField(db_column='working_certificate_date', max_length=7, blank=True, null=False)
    # 증명서 용도
    working_certificate_purpose = models.CharField(db_column='working_certificate_purpose', max_length=6, blank=True, null=False)
    # 제출처
    working_certificate_destination = models.CharField(db_column='working_certificate_destination', max_length=200, blank=True, null=False)
    # 수령희망일자
    receive_date = models.CharField(db_column='receive_date', max_length=10, blank=True, null=False)
    # 수령 방법
    receive_type = models.CharField(db_column='receive_type', max_length=6, blank=True, null=False)
    # 수령 방법
    receive_email = models.CharField(db_column='receive_email', max_length=100, blank=True, null=False)
    # 증명서 발급요청일
    working_certificate_req_date = models.CharField(db_column='working_certificate_req_date', max_length=10, blank=True, null=False)
    # 증명서 발급완료일
    working_certificate_done_date = models.CharField(db_column='working_certificate_done_date', max_length=10, blank=True, null=False)
    # 입사일
    join_date = models.CharField(db_column='join_date', max_length=10, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_certificate'

class ReWorkingOffYearly(models.Model) :
    # 휴가 연차 아이디
    working_off_yearly_id = models.AutoField(db_column='working_off_yearly_id', primary_key=True)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 연차 년수
    since_years = models.IntegerField(db_column='since_years', blank=False, null=False, default=0)
    # 연차 총일수
    working_off_total_days = models.FloatField(db_column='working_off_total_days', blank=False, null=False, default=0.0)
    # 연차 일수
    working_off_days = models.FloatField(db_column='working_off_days', blank=False, null=False, default=0.0)
    # 연차 사용일수
    working_off_use_days = models.FloatField(db_column='working_off_use_days', blank=False, null=False, default=0.0)
    # 연차 잔여일수
    working_off_remain_days = models.FloatField(db_column='working_off_remain_days', blank=False, null=False, default=0.0)
    # 연차 추가 일수
    working_off_etc_days = models.FloatField(db_column='working_off_etc_days', blank=False, null=False, default=0.0)
    # 연차 시작일
    working_off_start_date = models.CharField(db_column='working_off_start_date', max_length=10, blank=True, null=False)
    # 연차 종료일
    working_off_end_date = models.CharField(db_column='working_off_end_date', max_length=10, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_off_yearly'