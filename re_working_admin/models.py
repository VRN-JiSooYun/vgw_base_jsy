from django.db import models

# Create your models here.
from django.db import models

class ReWorkingStat(models.Model) :
    # 근무 시간 아이디
    working_stat_date = models.CharField(db_column='working_stat_date', max_length=10, blank=True, null=False)
    # 사용자 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # 평일 근무
    working_weekday = models.IntegerField(db_column='working_weekday', blank=False, null=False, default=0)
    # 외부 근무
    working_out = models.IntegerField(db_column='working_out', blank=False, null=False, default=0)
    # 휴가
    working_off = models.IntegerField(db_column='working_off', blank=False, null=False, default=0)
    # 휴일 근무
    working_weekend = models.IntegerField(db_column='working_weekend', blank=False, null=False, default=0)
    # 평일 근무 누락
    working_weekday_omit = models.IntegerField(db_column='working_weekday_omit', blank=False, null=False, default=0)
    # 평일 근무 시간
    working_weekday_time = models.IntegerField(db_column='working_weekday_time', blank=False, null=False, default=0)
    # 휴일 근무 시간
    working_weekend_time = models.IntegerField(db_column='working_weekend_time', blank=False, null=False, default=0)
    # 평일 근무 + (휴가, 외부근무 포함) 시간
    working_all_time = models.IntegerField(db_column='working_all_time', blank=False, null=False, default=0)
    # 평일 출근 시간
    working_start_time = models.IntegerField(db_column='working_start_time', blank=False, null=False, default=0)
    # 평일 퇴근 시간
    working_end_time = models.IntegerField(db_column='working_end_time', blank=False, null=False, default=0)
    # 지각
    working_late = models.IntegerField(db_column='working_late', blank=False, null=False, default=0)
    # 지각 시간
    working_late_time = models.IntegerField(db_column='working_late_time', blank=False, null=False, default=0)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_working_stat'